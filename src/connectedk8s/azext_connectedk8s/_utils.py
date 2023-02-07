# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import shutil
import subprocess
from subprocess import Popen, PIPE
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

from knack.util import CLIError
from knack.log import get_logger
from knack.prompting import NoTTYException, prompt_y_n
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import send_raw_request
from azure.cli.core import telemetry
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
from msrest.exceptions import AuthenticationError, HttpOperationError, TokenExpiredError
from msrest.exceptions import ValidationError as MSRestValidationError
from kubernetes.client.rest import ApiException
from azext_connectedk8s._client_factory import resource_providers_client, cf_resource_groups
import azext_connectedk8s._constants as consts
import azext_connectedk8s._precheckutils as precheckutils
import azext_connectedk8s._troubleshootutils as troubleshootutils
from kubernetes import client as kube_client
from azure.cli.core import get_default_cli
from azure.cli.core.azclierror import CLIInternalError, ClientRequestError, ArgumentUsageError, ManualInterrupt, AzureResponseError, AzureInternalError, ValidationError

logger = get_logger(__name__)

# pylint: disable=line-too-long
# pylint: disable=bare-except


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = consts.DEFAULT_REQUEST_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def validate_location(cmd, location):
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID') if os.getenv('AZURE_ACCESS_TOKEN') else get_subscription_id(cmd.cli_ctx)
    rp_locations = []
    resourceClient = resource_providers_client(cmd.cli_ctx, subscription_id=subscription_id)
    try:
        providerDetails = resourceClient.get('Microsoft.Kubernetes')
    except Exception as e:  # pylint: disable=broad-except
        arm_exception_handler(e, consts.Get_ResourceProvider_Fault_Type, 'Failed to fetch resource provider details')
    for resourceTypes in providerDetails.resource_types:
        if resourceTypes.resource_type == 'connectedClusters':
            rp_locations = [location.replace(" ", "").lower() for location in resourceTypes.locations]
            if location.lower() not in rp_locations:
                telemetry.set_exception(exception='Location not supported', fault_type=consts.Invalid_Location_Fault_Type,
                                        summary='Provided location is not supported for creating connected clusters')
                raise ArgumentUsageError("Connected cluster resource creation is supported only in the following locations: " +
                                         ', '.join(map(str, rp_locations)), recommendation="Use the --location flag to specify one of these locations.")
            break


def validate_custom_token(cmd, resource_group_name, location):
    if os.getenv('AZURE_ACCESS_TOKEN'):
        if os.getenv('AZURE_SUBSCRIPTION_ID') is None:
            telemetry.set_exception(exception='Required environment variables and parameters are not set', fault_type=consts.Custom_Token_Environments_Fault_Type,
                                    summary='Required environment variables and parameters are not set')
            raise ValidationError("Environment variable 'AZURE_SUBSCRIPTION_ID' should be set when custom access token is enabled.")
        if os.getenv('AZURE_TENANT_ID') is None:
            telemetry.set_exception(exception='Required environment variables and parameters are not set', fault_type=consts.Custom_Token_Environments_Fault_Type,
                                    summary='Required environment variables and parameters are not set')
            raise ValidationError("Environment variable 'AZURE_TENANT_ID' should be set when custom access token is enabled.")
        if location is None:
            try:
                resource_client = cf_resource_groups(cmd.cli_ctx, os.getenv('AZURE_SUBSCRIPTION_ID'))
                rg = resource_client.get(resource_group_name)
                location = rg.location
            except Exception as ex:
                telemetry.set_exception(exception=ex, fault_type=consts.Location_Fetch_Fault_Type,
                                        summary='Unable to fetch location from resource group')
                raise ValidationError("Unable to fetch location from resource group: ".format(str(ex)))
        return True, location
    return False, location


def get_chart_path(registry_path, kube_config, kube_context, helm_client_location, chart_folder_name='AzureArcCharts', chart_name='azure-arc-k8sagents'):
    # Pulling helm chart from registry
    os.environ['HELM_EXPERIMENTAL_OCI'] = '1'
    pull_helm_chart(registry_path, kube_config, kube_context, helm_client_location, chart_name)

    # Exporting helm chart after cleanup
    chart_export_path = os.path.join(os.path.expanduser('~'), '.azure', chart_folder_name)
    try:
        if os.path.isdir(chart_export_path):
            shutil.rmtree(chart_export_path)
    except:
        logger.warning("Unable to cleanup the {} already present on the machine. In case of failure, please cleanup the directory '{}' and try again.".format(chart_folder_name, chart_export_path))

    export_helm_chart(registry_path, chart_export_path, kube_config, kube_context, helm_client_location, chart_name)

    # Returning helm chart path
    helm_chart_path = os.path.join(chart_export_path, chart_name)
    if chart_folder_name == consts.Pre_Onboarding_Helm_Charts_Folder_Name:
        chart_path = helm_chart_path
    else:
        chart_path = os.getenv('HELMCHART') if os.getenv('HELMCHART') else helm_chart_path

    return chart_path


def pull_helm_chart(registry_path, kube_config, kube_context, helm_client_location, chart_name='azure-arc-k8sagents'):
    cmd_helm_chart_pull = [helm_client_location, "chart", "pull", registry_path]
    if kube_config:
        cmd_helm_chart_pull.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_chart_pull.extend(["--kube-context", kube_context])
    response_helm_chart_pull = subprocess.Popen(cmd_helm_chart_pull, stdout=PIPE, stderr=PIPE)
    _, error_helm_chart_pull = response_helm_chart_pull.communicate()
    if response_helm_chart_pull.returncode != 0:
        telemetry.set_exception(exception=error_helm_chart_pull.decode("ascii"), fault_type=consts.Pull_HelmChart_Fault_Type,
                                summary="Unable to pull {} helm charts from the registry".format(chart_name))
        raise CLIInternalError("Unable to pull {} helm chart from the registry '{}': ".format(chart_name, registry_path) + error_helm_chart_pull.decode("ascii"))


def export_helm_chart(registry_path, chart_export_path, kube_config, kube_context, helm_client_location, chart_name='azure-arc-k8sagents'):
    cmd_helm_chart_export = [helm_client_location, "chart", "export", registry_path, "--destination", chart_export_path]
    if kube_config:
        cmd_helm_chart_export.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_chart_export.extend(["--kube-context", kube_context])
    response_helm_chart_export = subprocess.Popen(cmd_helm_chart_export, stdout=PIPE, stderr=PIPE)
    _, error_helm_chart_export = response_helm_chart_export.communicate()
    if response_helm_chart_export.returncode != 0:
        telemetry.set_exception(exception=error_helm_chart_export.decode("ascii"), fault_type=consts.Export_HelmChart_Fault_Type,
                                summary='Unable to export {} helm chart from the registry'.format(chart_name))
        raise CLIInternalError("Unable to export {} helm chart from the registry '{}': ".format(chart_name, registry_path) + error_helm_chart_export.decode("ascii"))


def check_cluster_DNS(dns_check_log, filepath_with_timestamp, storage_space_available, diagnoser_output):

    try:
        if consts.DNS_Check_Result_String not in dns_check_log:
            return consts.Diagnostic_Check_Incomplete, storage_space_available
        formatted_dns_log = dns_check_log.replace('\t', '')
        # Validating if DNS is working or not and displaying proper result
        if("NXDOMAIN" in formatted_dns_log or "connection timed out" in formatted_dns_log):
            logger.warning("Error: We found an issue with the DNS resolution on your cluster. For details about debugging DNS issues visit 'https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/'.\n")
            diagnoser_output.append("Error: We found an issue with the DNS resolution on your cluster. For details about debugging DNS issues visit 'https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/'.\n")
            if storage_space_available:
                dns_check_path = os.path.join(filepath_with_timestamp, consts.DNS_Check)
                with open(dns_check_path, 'w+') as dns:
                    dns.write(formatted_dns_log + "\nWe found an issue with the DNS resolution on your cluster.")
            telemetry.set_exception(exception='DNS resolution check failed in the cluster', fault_type=consts.DNS_Check_Failed, summary="DNS check failed in the cluster")
            return consts.Diagnostic_Check_Failed, storage_space_available
        else:
            if storage_space_available:
                dns_check_path = os.path.join(filepath_with_timestamp, consts.DNS_Check)
                with open(dns_check_path, 'w+') as dns:
                    dns.write(formatted_dns_log + "\nCluster DNS check passed successfully.")
            return consts.Diagnostic_Check_Passed, storage_space_available

    # For handling storage or OS exception that may occur during the execution
    except OSError as e:
        if "[Errno 28]" in str(e):
            storage_space_available = False
            telemetry.set_exception(exception=e, fault_type=consts.No_Storage_Space_Available_Fault_Type, summary="No space left on device")
            shutil.rmtree(filepath_with_timestamp, ignore_errors=False, onerror=None)
        else:
            logger.warning("An exception has occured while performing the DNS check on the cluster. Exception: {}".format(str(e)) + "\n")
            telemetry.set_exception(exception=e, fault_type=consts.Cluster_DNS_Check_Fault_Type, summary="Error occured while performing cluster DNS check")
            diagnoser_output.append("An exception has occured while performing the DNS check on the cluster. Exception: {}".format(str(e)) + "\n")

    # To handle any exception that may occur during the execution
    except Exception as e:
        logger.warning("An exception has occured while performing the DNS check on the cluster. Exception: {}".format(str(e)) + "\n")
        telemetry.set_exception(exception=e, fault_type=consts.Cluster_DNS_Check_Fault_Type, summary="Error occured while performing cluster DNS check")
        diagnoser_output.append("An exception has occured while performing the DNS check on the cluster. Exception: {}".format(str(e)) + "\n")

    return consts.Diagnostic_Check_Incomplete, storage_space_available


def check_cluster_outbound_connectivity(outbound_connectivity_check_log, filepath_with_timestamp, storage_space_available, diagnoser_output):

    try:
        outbound_connectivity_response = outbound_connectivity_check_log[-1:-4:-1]
        outbound_connectivity_response = outbound_connectivity_response[::-1]
        if consts.Outbound_Connectivity_Check_Result_String not in outbound_connectivity_check_log:
            return consts.Diagnostic_Check_Incomplete, storage_space_available
        # Validating if outbound connectiivty is working or not and displaying proper result
        if(outbound_connectivity_response != "000"):
            if storage_space_available:
                outbound_connectivity_check_path = os.path.join(filepath_with_timestamp, consts.Outbound_Network_Connectivity_Check)
                with open(outbound_connectivity_check_path, 'w+') as outbound:
                    outbound.write("Response code " + outbound_connectivity_response + "\nOutbound network connectivity check passed successfully.")
            return consts.Diagnostic_Check_Passed, storage_space_available
        else:
            logger.warning("Error: We found an issue with outbound network connectivity from the cluster.\nIf your cluster is behind an outbound proxy server, please ensure that you have passed proxy parameters during the onboarding of your cluster.\nFor more details visit 'https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#connect-using-an-outbound-proxy-server'.\nPlease ensure to meet the following network requirements 'https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#meet-network-requirements' \n")
            diagnoser_output.append("Error: We found an issue with outbound network connectivity from the cluster.\nIf your cluster is behind an outbound proxy server, please ensure that you have passed proxy parameters during the onboarding of your cluster.\nFor more details visit 'https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#connect-using-an-outbound-proxy-server'.\nPlease ensure to meet the following network requirements 'https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#meet-network-requirements' \n")
            if storage_space_available:
                outbound_connectivity_check_path = os.path.join(filepath_with_timestamp, consts.Outbound_Network_Connectivity_Check)
                with open(outbound_connectivity_check_path, 'w+') as outbound:
                    outbound.write("Response code " + outbound_connectivity_response + "\nWe found an issue with Outbound network connectivity from the cluster.")
            telemetry.set_exception(exception='Outbound network connectivity check failed', fault_type=consts.Outbound_Connectivity_Check_Failed, summary="Outbound network connectivity check failed in the cluster")
            return consts.Diagnostic_Check_Failed, storage_space_available

    # For handling storage or OS exception that may occur during the execution
    except OSError as e:
        if "[Errno 28]" in str(e):
            storage_space_available = False
            telemetry.set_exception(exception=e, fault_type=consts.No_Storage_Space_Available_Fault_Type, summary="No space left on device")
            shutil.rmtree(filepath_with_timestamp, ignore_errors=False, onerror=None)
        else:
            logger.warning("An exception has occured while performing the outbound connectivity check on the cluster. Exception: {}".format(str(e)) + "\n")
            telemetry.set_exception(exception=e, fault_type=consts.Outbound_Connectivity_Check_Fault_Type, summary="Error occured while performing outbound connectivity check in the cluster")
            diagnoser_output.append("An exception has occured while performing the outbound connectivity check on the cluster. Exception: {}".format(str(e)) + "\n")

    # To handle any exception that may occur during the execution
    except Exception as e:
        logger.warning("An exception has occured while performing the outbound connectivity check on the cluster. Exception: {}".format(str(e)) + "\n")
        telemetry.set_exception(exception=e, fault_type=consts.Outbound_Connectivity_Check_Fault_Type, summary="Error occured while performing outbound connectivity check in the cluster")
        diagnoser_output.append("An exception has occured while performing the outbound connectivity check on the cluster. Exception: {}".format(str(e)) + "\n")

    return consts.Diagnostic_Check_Incomplete, storage_space_available


def fetching_cli_output_logs(filepath_with_timestamp, storage_space_available, flag, for_preonboarding_checks=False):

    # This function is used to store the output that is obtained throughout the Diagnoser process
    if for_preonboarding_checks:
        diagnoser_output = precheckutils.diagnoser_output
    else:
        diagnoser_output = troubleshootutils.diagnoser_output

    try:
        # If storage space is available then only we store the output
        if storage_space_available:
            # Path to store the diagnoser results
            cli_output_logger_path = os.path.join(filepath_with_timestamp, consts.Diagnoser_Results)
            # If any results are obtained during the process than we will add it to the text file.
            if len(diagnoser_output) > 0:
                with open(cli_output_logger_path, 'w+') as cli_output_writer:
                    for output in diagnoser_output:
                        cli_output_writer.write(output + "\n")
                    # If flag is 0 that means that process was terminated using the Keyboard Interrupt so adding that also to the text file
                    if flag == 0:
                        cli_output_writer.write("Process terminated externally.\n")

            # If no issues was found during the whole troubleshoot execution
            elif flag:
                with open(cli_output_logger_path, 'w+') as cli_output_writer:
                    cli_output_writer.write("The diagnoser didn't find any issues on the cluster.\n")
            # If process was terminated by user
            else:
                with open(cli_output_logger_path, 'w+') as cli_output_writer:
                    cli_output_writer.write("Process terminated externally.\n")

        return consts.Diagnostic_Check_Passed

    # For handling storage or OS exception that may occur during the execution
    except OSError as e:
        if "[Errno 28]" in str(e):
            storage_space_available = False
            telemetry.set_exception(exception=e, fault_type=consts.No_Storage_Space_Available_Fault_Type, summary="No space left on device")
            shutil.rmtree(filepath_with_timestamp, ignore_errors=False, onerror=None)

    # To handle any exception that may occur during the execution
    except Exception as e:
        logger.warning("An exception has occured while trying to store the diagnoser results. Exception: {}".format(str(e)) + "\n")
        telemetry.set_exception(exception=e, fault_type=consts.Diagnoser_Result_Fault_Type, summary="Error while storing the diagnoser results")

    return consts.Diagnostic_Check_Failed


def create_folder_diagnosticlogs(time_stamp, folder_name):

    try:
        # Fetching path to user directory to create the arc diagnostic folder
        home_dir = os.path.expanduser('~')
        filepath = os.path.join(home_dir, '.azure', folder_name)
        # Creating Diagnostic folder and its subfolder with the given timestamp and cluster name to store all the logs
        try:
            os.mkdir(filepath)
        except FileExistsError:
            pass
        filepath_with_timestamp = os.path.join(filepath, time_stamp)
        try:
            os.mkdir(filepath_with_timestamp)
        except FileExistsError:
            # Deleting the folder if present with the same timestamp to prevent overriding in the same folder and then creating it again
            shutil.rmtree(filepath_with_timestamp, ignore_errors=True)
            os.mkdir(filepath_with_timestamp)
            pass

        return filepath_with_timestamp, True

    # For handling storage or OS exception that may occur during the execution
    except OSError as e:
        if "[Errno 28]" in str(e):
            shutil.rmtree(filepath_with_timestamp, ignore_errors=False, onerror=None)
            telemetry.set_exception(exception=e, fault_type=consts.No_Storage_Space_Available_Fault_Type, summary="No space left on device")
            return "", False
        else:
            logger.warning("An exception has occured while creating the diagnostic logs folder in your local machine. Exception: {}".format(str(e)) + "\n")
            telemetry.set_exception(exception=e, fault_type=consts.Diagnostics_Folder_Creation_Failed_Fault_Type, summary="Error while trying to create diagnostic logs folder")
            return "", False

    # To handle any exception that may occur during the execution
    except Exception as e:
        logger.warning("An exception has occured while creating the diagnostic logs folder in your local machine. Exception: {}".format(str(e)) + "\n")
        telemetry.set_exception(exception=e, fault_type=consts.Diagnostics_Folder_Creation_Failed_Fault_Type, summary="Error while trying to create diagnostic logs folder")
        return "", False


def add_helm_repo(kube_config, kube_context, helm_client_location):
    repo_name = os.getenv('HELMREPONAME')
    repo_url = os.getenv('HELMREPOURL')
    cmd_helm_repo = [helm_client_location, "repo", "add", repo_name, repo_url]
    if kube_config:
        cmd_helm_repo.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_repo.extend(["--kube-context", kube_context])
    response_helm_repo = Popen(cmd_helm_repo, stdout=PIPE, stderr=PIPE)
    _, error_helm_repo = response_helm_repo.communicate()
    if response_helm_repo.returncode != 0:
        telemetry.set_exception(exception=error_helm_repo.decode("ascii"), fault_type=consts.Add_HelmRepo_Fault_Type,
                                summary='Failed to add helm repository')
        raise CLIInternalError("Unable to add repository {} to helm: ".format(repo_url) + error_helm_repo.decode("ascii"))


def get_helm_registry(cmd, config_dp_endpoint, dp_endpoint_dogfood=None, release_train_dogfood=None):
    # Setting uri
    get_chart_location_url = "{}/{}/GetLatestHelmPackagePath?api-version=2019-11-01-preview".format(config_dp_endpoint, 'azure-arc-k8sagents')
    release_train = os.getenv('RELEASETRAIN') if os.getenv('RELEASETRAIN') else 'stable'
    if dp_endpoint_dogfood:
        get_chart_location_url = "{}/azure-arc-k8sagents/GetLatestHelmPackagePath?api-version=2019-11-01-preview".format(dp_endpoint_dogfood)
        if release_train_dogfood:
            release_train = release_train_dogfood
    uri_parameters = ["releaseTrain={}".format(release_train)]
    resource = cmd.cli_ctx.cloud.endpoints.active_directory_resource_id
    headers = None
    if os.getenv('AZURE_ACCESS_TOKEN'):
        headers = ["Authorization=Bearer {}".format(os.getenv('AZURE_ACCESS_TOKEN'))]
    # Sending request
    try:
        r = send_raw_request(cmd.cli_ctx, 'post', get_chart_location_url, headers=headers, uri_parameters=uri_parameters, resource=resource)
    except Exception as e:
        telemetry.set_exception(exception=e, fault_type=consts.Get_HelmRegistery_Path_Fault_Type,
                                summary='Error while fetching helm chart registry path')
        raise CLIInternalError("Error while fetching helm chart registry path: " + str(e))
    if r.content:
        try:
            return r.json().get('repositoryPath')
        except Exception as e:
            telemetry.set_exception(exception=e, fault_type=consts.Get_HelmRegistery_Path_Fault_Type,
                                    summary='Error while fetching helm chart registry path')
            raise CLIInternalError("Error while fetching helm chart registry path from JSON response: " + str(e))
    else:
        telemetry.set_exception(exception='No content in response', fault_type=consts.Get_HelmRegistery_Path_Fault_Type,
                                summary='No content in acr path response')
        raise CLIInternalError("No content was found in helm registry path response.")


def arm_exception_handler(ex, fault_type, summary, return_if_not_found=False):
    if isinstance(ex, AuthenticationError):
        telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
        raise AzureResponseError("Authentication error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))

    if isinstance(ex, TokenExpiredError):
        telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
        raise AzureResponseError("Token expiration error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))

    if isinstance(ex, HttpOperationError):
        status_code = ex.response.status_code
        if status_code == 404 and return_if_not_found:
            return
        if status_code // 100 == 4:
            telemetry.set_user_fault()
        telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
        if status_code // 100 == 5:
            raise AzureInternalError("Http operation error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))
        raise AzureResponseError("Http operation error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))

    if isinstance(ex, MSRestValidationError):
        telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
        raise AzureResponseError("Validation error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))

    if isinstance(ex, HttpResponseError):
        status_code = ex.status_code
        if status_code == 404 and return_if_not_found:
            return
        if status_code // 100 == 4:
            telemetry.set_user_fault()
        telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
        if status_code // 100 == 5:
            raise AzureInternalError("Http response error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))
        raise AzureResponseError("Http response error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))

    if isinstance(ex, ResourceNotFoundError) and return_if_not_found:
        return

    telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
    raise ClientRequestError("Error occured while making ARM request: " + str(ex) + "\nSummary: {}".format(summary))


def kubernetes_exception_handler(ex, fault_type, summary, error_message='Error occured while connecting to the kubernetes cluster: ',
                                 message_for_unauthorized_request='The user does not have required privileges on the kubernetes cluster to deploy Azure Arc enabled Kubernetes agents. Please ensure you have cluster admin privileges on the cluster to onboard.',
                                 message_for_not_found='The requested kubernetes resource was not found.', raise_error=True):
    telemetry.set_user_fault()
    if isinstance(ex, ApiException):
        status_code = ex.status
        if status_code == 403:
            logger.warning(message_for_unauthorized_request)
        elif status_code == 404:
            logger.warning(message_for_not_found)
        else:
            logger.debug("Kubernetes Exception: " + str(ex))
        if raise_error:
            telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
            raise ValidationError(error_message + "\nError Response: " + str(ex.body))
    else:
        if raise_error:
            telemetry.set_exception(exception=ex, fault_type=fault_type, summary=summary)
            raise ValidationError(error_message + "\nError: " + str(ex))
        else:
            logger.debug("Kubernetes Exception: " + str(ex))


def validate_infrastructure_type(infra):
    for s in consts.Infrastructure_Enum_Values[1:]:  # First value is "auto"
        if s.lower() == infra.lower():
            return s
    return None


def get_values_file():
    values_file_provided = False
    values_file = os.getenv('HELMVALUESPATH')
    if (values_file is not None) and (os.path.isfile(values_file)):
        values_file_provided = True
        logger.warning("Values files detected. Reading additional helm parameters from same.")
        # trimming required for windows os
        if (values_file.startswith("'") or values_file.startswith('"')):
            values_file = values_file[1:]
        if (values_file.endswith("'") or values_file.endswith('"')):
            values_file = values_file[:-1]

    return values_file_provided, values_file


def ensure_namespace_cleanup():
    api_instance = kube_client.CoreV1Api()
    timeout = time.time() + 180
    while True:
        if time.time() > timeout:
            telemetry.set_user_fault()
            logger.warning("Namespace 'azure-arc' still in terminating state. Please ensure that you delete the 'azure-arc' namespace before onboarding the cluster again.")
            return
        try:
            api_response = api_instance.list_namespace(field_selector='metadata.name=azure-arc')
            if not api_response.items:
                return
            time.sleep(5)
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Error while retrieving namespace information: " + str(e))
            kubernetes_exception_handler(e, consts.Get_Kubernetes_Namespace_Fault_Type, 'Unable to fetch kubernetes namespace',
                                         raise_error=False)


def delete_arc_agents(release_namespace, kube_config, kube_context, helm_client_location, is_arm64_cluster=False, no_hooks=False):
    if(no_hooks):
        cmd_helm_delete = [helm_client_location, "delete", "azure-arc", "--namespace", release_namespace, "--no-hooks"]
    else:
        cmd_helm_delete = [helm_client_location, "delete", "azure-arc", "--namespace", release_namespace]
    if is_arm64_cluster:
        cmd_helm_delete.extend(["--timeout", "15m"])
    if kube_config:
        cmd_helm_delete.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_delete.extend(["--kube-context", kube_context])
    response_helm_delete = Popen(cmd_helm_delete, stdout=PIPE, stderr=PIPE)
    _, error_helm_delete = response_helm_delete.communicate()
    if response_helm_delete.returncode != 0:
        if 'forbidden' in error_helm_delete.decode("ascii") or 'Error: warning: Hook pre-delete' in error_helm_delete.decode("ascii") or 'Error: timed out waiting for the condition' in error_helm_delete.decode("ascii"):
            telemetry.set_user_fault()
        telemetry.set_exception(exception=error_helm_delete.decode("ascii"), fault_type=consts.Delete_HelmRelease_Fault_Type,
                                summary='Unable to delete helm release')
        raise CLIInternalError("Error occured while cleaning up arc agents. " +
                               "Helm release deletion failed: " + error_helm_delete.decode("ascii") +
                               " Please run 'helm delete azure-arc' to ensure that the release is deleted.")
    ensure_namespace_cleanup()
    # Cleanup azure-arc-release NS if present (created during helm installation)
    cleanup_release_install_namespace_if_exists()


def cleanup_release_install_namespace_if_exists():
    api_instance = kube_client.CoreV1Api()
    try:
        api_instance.read_namespace(consts.Release_Install_Namespace)
    except Exception as ex:
        if ex.status == 404:
            # Nothing to delete, exiting here
            return
        else:
            kubernetes_exception_handler(ex, consts.Get_Kubernetes_Helm_Release_Namespace_Fault_Type, error_message='Unable to fetch details about existense of kubernetes namespace: {}'.format(consts.Release_Install_Namespace), summary='Unable to fetch kubernetes namespace: {}'.format(consts.Release_Install_Namespace))

    # If namespace exists, delete it
    try:
        api_instance.delete_namespace(consts.Release_Install_Namespace)
    except Exception as ex:
        kubernetes_exception_handler(ex, consts.Delete_Kubernetes_Helm_Release_Namespace_Fault_Type, error_message='Unable to clean-up kubernetes namespace: {}'.format(consts.Release_Install_Namespace), summary='Unable to delete kubernetes namespace: {}'.format(consts.Release_Install_Namespace))


# DO NOT use this method for re-put scenarios. This method involves new NS creation for helm release. For re-put scenarios, brownfield scenario needs to be handled where helm release still stays in default NS
def helm_install_release(chart_path, subscription_id, kubernetes_distro, kubernetes_infra, resource_group_name, cluster_name,
                         location, onboarding_tenant_id, http_proxy, https_proxy, no_proxy, proxy_cert, private_key_pem,
                         kube_config, kube_context, no_wait, values_file_provided, values_file, cloud_name, disable_auto_upgrade,
                         enable_custom_locations, custom_locations_oid, helm_client_location, enable_private_link, onboarding_timeout="600",
                         container_log_path=None):
    cmd_helm_install = [helm_client_location, "upgrade", "--install", "azure-arc", chart_path,
                        "--set", "global.subscriptionId={}".format(subscription_id),
                        "--set", "global.kubernetesDistro={}".format(kubernetes_distro),
                        "--set", "global.kubernetesInfra={}".format(kubernetes_infra),
                        "--set", "global.resourceGroupName={}".format(resource_group_name),
                        "--set", "global.resourceName={}".format(cluster_name),
                        "--set", "global.location={}".format(location),
                        "--set", "global.tenantId={}".format(onboarding_tenant_id),
                        "--set", "global.onboardingPrivateKey={}".format(private_key_pem),
                        "--set", "systemDefaultValues.spnOnboarding=false",
                        "--set", "global.azureEnvironment={}".format(cloud_name),
                        "--set", "systemDefaultValues.clusterconnect-agent.enabled=true",
                        "--namespace", "{}".format(consts.Release_Install_Namespace),
                        "--create-namespace",
                        "--output", "json"]
    # Add custom-locations related params
    if enable_custom_locations and not enable_private_link:
        cmd_helm_install.extend(["--set", "systemDefaultValues.customLocations.enabled=true"])
        cmd_helm_install.extend(["--set", "systemDefaultValues.customLocations.oid={}".format(custom_locations_oid)])
    # Disable cluster connect if private link is enabled
    if enable_private_link is True:
        cmd_helm_install.extend(["--set", "systemDefaultValues.clusterconnect-agent.enabled=false"])
    # To set some other helm parameters through file
    if values_file_provided:
        cmd_helm_install.extend(["-f", values_file])
    if disable_auto_upgrade:
        cmd_helm_install.extend(["--set", "systemDefaultValues.azureArcAgents.autoUpdate={}".format("false")])
    if https_proxy:
        cmd_helm_install.extend(["--set", "global.httpsProxy={}".format(https_proxy)])
    if http_proxy:
        cmd_helm_install.extend(["--set", "global.httpProxy={}".format(http_proxy)])
    if no_proxy:
        cmd_helm_install.extend(["--set", "global.noProxy={}".format(no_proxy)])
    if proxy_cert:
        cmd_helm_install.extend(["--set-file", "global.proxyCert={}".format(proxy_cert)])
        cmd_helm_install.extend(["--set", "global.isCustomCert={}".format(True)])
    if https_proxy or http_proxy or no_proxy:
        cmd_helm_install.extend(["--set", "global.isProxyEnabled={}".format(True)])
    if container_log_path is not None:
        cmd_helm_install.extend(["--set", "systemDefaultValues.fluent-bit.containerLogPath={}".format(container_log_path)])
    if kube_config:
        cmd_helm_install.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_install.extend(["--kube-context", kube_context])
    if not no_wait:
        # Change --timeout format for helm client to understand
        onboarding_timeout = onboarding_timeout + "s"
        cmd_helm_install.extend(["--wait", "--timeout", "{}".format(onboarding_timeout)])
    response_helm_install = Popen(cmd_helm_install, stdout=PIPE, stderr=PIPE)
    _, error_helm_install = response_helm_install.communicate()
    if response_helm_install.returncode != 0:
        if ('forbidden' in error_helm_install.decode("ascii") or 'timed out waiting for the condition' in error_helm_install.decode("ascii")):
            telemetry.set_user_fault()
        telemetry.set_exception(exception=error_helm_install.decode("ascii"), fault_type=consts.Install_HelmRelease_Fault_Type,
                                summary='Unable to install helm release')
        logger.warning("Please check if the azure-arc namespace was deployed and run 'kubectl get pods -n azure-arc' to check if all the pods are in running state. A possible cause for pods stuck in pending state could be insufficient resources on the kubernetes cluster to onboard to arc.")
        raise CLIInternalError("Unable to install helm release: " + error_helm_install.decode("ascii"))


def get_release_namespace(kube_config, kube_context, helm_client_location, release_name='azure-arc'):
    cmd_helm_release = [helm_client_location, "list", "-a", "--all-namespaces", "--output", "json"]
    if kube_config:
        cmd_helm_release.extend(["--kubeconfig", kube_config])
    if kube_context:
        cmd_helm_release.extend(["--kube-context", kube_context])
    response_helm_release = Popen(cmd_helm_release, stdout=PIPE, stderr=PIPE)
    output_helm_release, error_helm_release = response_helm_release.communicate()
    if response_helm_release.returncode != 0:
        if 'forbidden' in error_helm_release.decode("ascii"):
            telemetry.set_user_fault()
        telemetry.set_exception(exception=error_helm_release.decode("ascii"), fault_type=consts.List_HelmRelease_Fault_Type,
                                summary='Unable to list helm release')
        raise CLIInternalError("Helm list release failed: " + error_helm_release.decode("ascii"))
    output_helm_release = output_helm_release.decode("ascii")
    try:
        output_helm_release = json.loads(output_helm_release)
    except json.decoder.JSONDecodeError:
        return None
    for release in output_helm_release:
        if release['name'] == release_name:
            return release['namespace']
    return None


def flatten(dd, separator='.', prefix=''):
    try:
        if isinstance(dd, dict):
            return {prefix + separator + k if prefix else k: v for kk, vv in dd.items() for k, v in flatten(vv, separator, kk).items()}
        else:
            return {prefix: dd}
    except Exception as e:
        telemetry.set_exception(exception=e, fault_type=consts.Error_Flattening_User_Supplied_Value_Dict,
                                summary='Error while flattening the user supplied helm values dict')
        raise CLIInternalError("Error while flattening the user supplied helm values dict")


def check_features_to_update(features_to_update):
    update_cluster_connect, update_azure_rbac, update_cl = False, False, False
    for feature in features_to_update:
        if feature == "cluster-connect":
            update_cluster_connect = True
        elif feature == "azure-rbac":
            update_azure_rbac = True
        elif feature == "custom-locations":
            update_cl = True
    return update_cluster_connect, update_azure_rbac, update_cl


def user_confirmation(message, yes=False):
    if yes:
        return
    try:
        if not prompt_y_n(message):
            raise ManualInterrupt('Operation cancelled.')
    except NoTTYException:
        raise CLIInternalError('Unable to prompt for confirmation as no tty available. Use --yes.')


def is_guid(guid):
    import uuid
    try:
        uuid.UUID(guid)
        return True
    except ValueError:
        return False


def try_list_node_fix():
    try:
        from kubernetes.client.models.v1_container_image import V1ContainerImage

        def names(self, names):
            self._names = names

        V1ContainerImage.names = V1ContainerImage.names.setter(names)
    except Exception as ex:
        logger.debug("Error while trying to monkey patch the fix for list_node(): {}".format(str(ex)))


def check_provider_registrations(cli_ctx, subscription_id):
    try:
        rp_client = resource_providers_client(cli_ctx, subscription_id)
        cc_registration_state = rp_client.get(consts.Connected_Cluster_Provider_Namespace).registration_state
        if cc_registration_state != "Registered":
            telemetry.set_exception(exception="{} provider is not registered".format(consts.Connected_Cluster_Provider_Namespace), fault_type=consts.CC_Provider_Namespace_Not_Registered_Fault_Type,
                                    summary="{} provider is not registered".format(consts.Connected_Cluster_Provider_Namespace))
            raise ValidationError("{} provider is not registered. Please register it using 'az provider register -n 'Microsoft.Kubernetes' before running the connect command.".format(consts.Connected_Cluster_Provider_Namespace))
        kc_registration_state = rp_client.get(consts.Kubernetes_Configuration_Provider_Namespace).registration_state
        if kc_registration_state != "Registered":
            telemetry.set_user_fault()
            logger.warning("{} provider is not registered".format(consts.Kubernetes_Configuration_Provider_Namespace))
    except ValidationError as e:
        raise e
    except Exception as ex:
        logger.warning("Couldn't check the required provider's registration status. Error: {}".format(str(ex)))


def can_create_clusterrolebindings():
    try:
        api_instance = kube_client.AuthorizationV1Api()
        access_review = kube_client.V1SelfSubjectAccessReview(spec={
            "resourceAttributes": {
                "verb": "create",
                "resource": "clusterrolebindings",
                "group": "rbac.authorization.k8s.io"
            }
        })
        response = api_instance.create_self_subject_access_review(access_review)
        return response.status.allowed
    except Exception as ex:
        logger.warning("Couldn't check for the permission to create clusterrolebindings on this k8s cluster. Error: {}".format(str(ex)))
        return "Unknown"


def validate_node_api_response(api_instance, node_api_response):
    if node_api_response is None:
        try:
            node_api_response = api_instance.list_node()
            return node_api_response
        except Exception as ex:
            logger.debug("Error occcured while listing nodes on this kubernetes cluster: {}".format(str(ex)))
            return None
    else:
        return node_api_response


def az_cli(args_str):
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args, out_file=open(os.devnull, 'w'))
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise Exception(cli.result.error)
    return True


# def is_cli_using_msal_auth():
#     response_cli_version = az_cli("version --output json")
#     try:
#         cli_version = response_cli_version['azure-cli']
#     except Exception as ex:
#         raise CLIInternalError("Unable to decode the az cli version installed: {}".format(str(ex)))
#     if version.parse(cli_version) >= version.parse(consts.AZ_CLI_ADAL_TO_MSAL_MIGRATE_VERSION):
#         return True
#     else:
#         return False

def is_cli_using_msal_auth():
    response_cli_version = az_cli("version --output json")
    try:
        cli_version = response_cli_version['azure-cli']
    except Exception as ex:
        raise CLIInternalError("Unable to decode the az cli version installed: {}".format(str(ex)))
    v1 = cli_version
    v2 = consts.AZ_CLI_ADAL_TO_MSAL_MIGRATE_VERSION
    for i, j in zip(map(int, v1.split(".")), map(int, v2.split("."))):
        if i == j:
            continue
        return i > j
    return len(v1.split(".")) == len(v2.split("."))
