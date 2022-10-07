# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


# pylint: disable=line-too-long

Distribution_Enum_Values = ["auto", "generic", "openshift", "rancher_rke", "kind", "k3s", "minikube", "gke", "eks", "aks", "aks_management", "aks_workload", "capz", "aks_engine", "tkg"]
Infrastructure_Enum_Values = ["auto", "generic", "azure", "aws", "gcp", "azure_stack_hci", "azure_stack_hub", "azure_stack_edge", "vsphere", "windows_server"]
Feature_Values = ["cluster-connect", "azure-rbac", "custom-locations"]
CRD_FOR_FORCE_DELETE = ["arccertificates.clusterconfig.azure.com", "azureclusteridentityrequests.clusterconfig.azure.com", "azureextensionidentities.clusterconfig.azure.com", "connectedclusters.arc.azure.com", "customlocationsettings.clusterconfig.azure.com", "extensionconfigs.clusterconfig.azure.com", "gitconfigs.clusterconfig.azure.com"]
Custom_Locations_Provider_Namespace = 'Microsoft.ExtendedLocation'
Connected_Cluster_Provider_Namespace = 'Microsoft.Kubernetes'
Kubernetes_Configuration_Provider_Namespace = 'Microsoft.KubernetesConfiguration'
Arc_Namespace = 'azure-arc'
Azure_PublicCloudName = 'AZUREPUBLICCLOUD'
Azure_USGovCloudName = 'AZUREUSGOVERNMENTCLOUD'
Azure_ChinaCloudName = 'AZURECHINACLOUD'
Azure_DogfoodCloudName = 'AZUREDOGFOOD'
PublicCloud_OriginalName = 'AZURECLOUD'
MSI_Certificate_Secret_Name = 'azure-identity-certificate'
KAP_Certificate_Secret_Name = 'kube-aad-proxy-certificate'
USGovCloud_OriginalName = 'AZUREUSGOVERNMENT'
Dogfood_RMEndpoint = 'https://api-dogfood.resources.windows-int.net/'
Client_Request_Id_Header = 'x-ms-client-request-id'
Default_Onboarding_Source_Tracking_Guid = "77ade16b-0f55-403b-b7d2-739554a897f2"
Helm_Environment_File_Fault_Type = 'helm-environment-file-error'
Invalid_Location_Fault_Type = 'location-validation-error'
Pls_Location_Mismatch_Fault_Type = 'pls-location-mismatch-error'
Invalid_Argument_Fault_Type = 'argument-validation-error'
Load_Kubeconfig_Fault_Type = 'kubeconfig-load-error'
Read_ConfigMap_Fault_Type = 'configmap-read-error'
Get_ResourceProvider_Fault_Type = 'resource-provider-fetch-error'
Get_ConnectedCluster_Fault_Type = 'connected-cluster-fetch-error'
Create_ConnectedCluster_Fault_Type = 'connected-cluster-create-error'
Update_ConnectedCluster_Fault_Type = 'connected-cluster-update-error'
Delete_ConnectedCluster_Fault_Type = 'connected-cluster-delete-error'
Bad_DeleteRequest_Fault_Type = 'bad-delete-request-error'
Cluster_Already_Onboarded_Fault_Type = 'cluster-already-onboarded-error'
Resource_Already_Exists_Fault_Type = 'resource-already-exists-error'
Resource_Does_Not_Exist_Fault_Type = 'resource-does-not-exist-error'
Create_ResourceGroup_Fault_Type = 'resource-group-creation-error'
Add_HelmRepo_Fault_Type = 'helm-repo-add-error'
List_HelmRelease_Fault_Type = 'helm-list-release-error'
KeyPair_Generate_Fault_Type = 'keypair-generation-error'
PublicKey_Export_Fault_Type = 'publickey-export-error'
PrivateKey_Export_Fault_Type = 'privatekey-export-error'
Install_HelmRelease_Fault_Type = 'helm-release-install-error'
Delete_HelmRelease_Fault_Type = 'helm-release-delete-error'
Check_PodStatus_Fault_Type = 'check-pod-status-error'
Kubernetes_Connectivity_FaultType = 'kubernetes-cluster-connection-error'
Helm_Version_Fault_Type = 'helm-not-updated-error'
Check_HelmVersion_Fault_Type = 'helm-version-check-error'
Helm_Installation_Fault_Type = 'helm-not-installed-error'
Check_HelmInstallation_Fault_Type = 'check-helm-installed-error'
Get_HelmRegistery_Path_Fault_Type = 'helm-registry-path-fetch-error'
Pull_HelmChart_Fault_Type = 'helm-chart-pull-error'
Export_HelmChart_Fault_Type = 'helm-chart-export-error'
Get_Kubernetes_Version_Fault_Type = 'kubernetes-get-version-error'
Get_Kubernetes_Distro_Fault_Type = 'kubernetes-get-distribution-error'
Get_Kubernetes_Namespace_Fault_Type = 'kubernetes-get-namespace-error'
Update_Agent_Success = 'Agents for Connected Cluster {} have been updated successfully'
Update_Agent_Failure = 'Error while updating agents. Please run \"kubectl get pods -n azure-arc\" to check the pods in case of timeout error. Error: {}'
Get_Credentials_Failed_Fault_Type = 'failed-to-get-list-cluster-user-credentials'
Failed_To_Merge_Credentials_Fault_Type = "failed-to-merge-credentials"
Kubeconfig_Failed_To_Load_Fault_Type = "failed-to-load-kubeconfig-file"
Failed_To_Load_K8s_Configuration_Fault_Type = "failed-to-load-kubernetes-configuration"
Failed_To_Merge_Kubeconfig_File = "failed-to-merge-kubeconfig-file"
Download_Helm_Fault_Type = "helm-client-download-error"
Create_HelmExe_Fault_Type = "helm-client-create-error"
Extract_HelmExe_Fault_Type = "helm-client-extract-error"
Different_Object_With_Same_Name_Fault_Type = "Kubeconfig has an object with same name"
Download_Exe_Fault_Type = "Error while downloading client proxy executable from storage account"
Create_Directory_Fault_Type = "Error while creating directory for placing the executable"
Run_Clientproxy_Fault_Type = "Error while starting client proxy process."
Post_Hybridconn_Fault_Type = "Error while posting hybrid connection details to proxy process"
Post_RefreshToken_Fault_Type = "Error while posting refresh token details to proxy process"
Merge_Kubeconfig_Fault_Type = "Error while merging kubeconfig."
Create_CSPExe_Fault_Type = "Error while creating csp executable"
Remove_Config_Fault_Type = "Error while removing old csp config"
Load_Creds_Fault_Type = "Error while loading accessToken.json"
Creds_NotFound_Fault_Type = "Credentials of user not found"
Create_Config_Fault_Type = "Error while creating config file for proxy"
Run_RefreshThread_Fault_Type = "Error while starting refresh thread"
Load_Kubeconfig_Fault_Type = "Error while loading kubeconfig"
Run_Check_CSP_Thread_Fault_Type = "Error while starting 'check csp thread'."
Proxy_Closed_Externally_Fault_Type = "Proxy closed externally."
Client_Proxy_Port_Fault_Type = "Client proxy port was in use."
Unsupported_Fault_Type = "Error while checking operating system.Unsupported OS detected."
Unsupported_Architecture_Fault_Type = "Unsupported architecture detected."
Helm_Unsupported_OS_Fault_Type = "helm-client-unsupported-os-error."
Port_Check_Fault_Type = "Error while checking if port is in use."
Kubeconfig_Failed_To_Load_Fault_Type = "failed-to-load-kubeconfig-file"
Proxy_Cert_Path_Does_Not_Exist_Fault_Type = 'proxy-cert-path-does-not-exist-error'
Proxy_Cert_Path_Does_Not_Exist_Error = 'Proxy cert path {} does not exist. Please check the path provided'
Get_Kubernetes_Infra_Fault_Type = 'kubernetes-get-infrastructure-error'
No_Param_Error = 'No parmeters were specified with update command. Please run az connectedk8s update --help to check parameters available for update'
EnableProxy_Conflict_Error = 'Conflict detected: --disable-proxy can not be set with --https-proxy, --http-proxy, --proxy-skip-range and --proxy-cert at the same time. Please run az connectedk8s update --help for more information about the parameters'
Manual_Upgrade_Called_In_Auto_Update_Enabled = 'Manual Upgrade was called while in auto_Update enabled mode'
Upgrade_Agent_Success = 'Agents for Connected Cluster {} have been upgraded successfully'
Upgrade_Agent_Failure = 'Error while upgrading agents. Please run \"kubectl get pods -n azure-arc\" to check the pods in case of timeout error. Error: {}'
Release_Namespace_Not_Found = 'Error while getting azure-arc releasenamespace'
Get_Helm_Values_Failed = 'Error while doing helm get values azure-arc'
Helm_Existing_User_Supplied_Value_Get_Fault = 'Error while loading the user supplied helm values'
Error_Flattening_User_Supplied_Value_Dict = 'Error while flattening the user supplied helm values dict'
Upgrade_RG_Cluster_Name_Conflict = 'The provided cluster name and rg correspond to different cluster'
Corresponding_CC_Resource_Deleted_Fault = 'CC resource corresponding to this cluster has been deleted by the customer'
Kubernetes_Node_Type_Fetch_Fault = 'Error while trying to find a linux/amd64 node for scheduling pods'
Linux_Amd64_Node_Not_Exists = 'Kubernetes cluster doesnt have amd64/linux node'
Operate_RG_Cluster_Name_Conflict = 'The provided cluster name and rg correspond to different cluster being operated on'
Custom_Locations_Registration_Check_Fault_Type = "Error while checking resource provider registration of custom locations."
Custom_Locations_OID_Fetch_Fault_Type = "Error while fetching oid for custom locations."
Application_Details_Not_Provided_For_Azure_RBAC_Fault = 'Application ID or secret not provided for Azure RBAC'
Successfully_Enabled_Features = 'Successsfully enabled features: {} for the Connected Cluster {}'
Successfully_Disabled_Features = 'Successsfully disabled features: {} for the Connected Cluster {}'
Error_enabling_Features = 'Error while updating agents for enabling features. Please run \"kubectl get pods -n azure-arc\" to check the pods in case of timeout error. Error: {}'
Error_disabling_Features = 'Error while updating agents for disabling features. Please run \"kubectl get pods -n azure-arc\" to check the pods in case of timeout error. Error: {}'
Proxy_Kubeconfig_During_Deletion_Fault_Type = 'Encountered proxy kubeconfig during deletion.'
Cannot_Create_ClusterRoleBindings_Fault_Type = 'Cannot create cluster role bindings on this Kubernets cluster'
CC_Provider_Namespace_Not_Registered_Fault_Type = "Connected Cluster Provider MS.K8 namespace not registered"
Default_Namespace_Does_Not_Exist_Fault_Type = "The default namespace defined in the kubeconfig doesn't exist on the kubernetes cluster."
ClusterConnect_Not_Present_Fault_Type = "cluster-connect-feature-unavailable"
KAP_1P_Server_App_Scope = "6256c85f-0aad-4d50-b960-e6e9b21efe35/.default"
KAP_1P_Server_AppId = "6256c85f-0aad-4d50-b960-e6e9b21efe35"
Get_PublicKey_Info_Fault_Type = 'Error while fetching the PoP publickey information from client proxy'
PoP_Public_Key_Expried_Fault_Type = 'The PoP public key used to generate the at has expired'
Post_AT_To_ClientProxy_Failed_Fault_Type = 'Failed to post access token to client proxy'
Kubectl_Get_Events_Failed_Fault_Type = "Error while doing kubectl get events"
Fetch_Arc_Agent_Logs_Failed_Fault_Type = "Error occured in arc agents logger"
Fetch_Arc_Agents_Events_Logs_Failed_Fault_Type = "Error occured in arc agents events logger"
Fetch_Arc_Deployment_Logs_Failed_Fault_Type = "Error occured in deployments logger"
Agent_State_Check_Fault_Type = "Error occured while performing the agent state check"
Agent_Version_Check_Fault_Type = "Error occured while performing the agent version check"
Diagnoser_Job_Failed_Fault_Type = "Error while executing Diagnoser Job"
Diagnoser_Container_Check_Failed_Fault_Type = "Error occured while performing the diagnoser container checks"
Cluster_DNS_Check_Fault_Type = "Error occured while performing cluster DNS check"
Outbound_Connectivity_Check_Fault_Type = "Error occured while performing outbound connectivity check in the cluster"
MSI_Cert_Check_Fault_Type = "Error occurred while trying to perform MSI ceritificate presence check"
Cluster_Security_Policy_Check_Fault_Type = "Error occured while performing cluster security policy check"
KAP_Cert_Check_Fault_Type = "Error occurred while trying to perform KAP ceritificate presence check"
MSI_Cert_Expiry_Check_Fault_Type = "Error occured while trying to perform the MSI cert expiry check"
Diagnostics_Folder_Creation_Failed_Fault_Type = "Error while trying to create diagnostic logs folder"
Describe_Stuck_Agents_Fault_Type = "Error occured while storing the description of non running agents"
No_Storage_Space_Available_Fault_Type = "No space left on device"
Connected_Cluster_Resource_Fetch_Fault_Type = "Error occured while fetching the Get output of connected cluster"
Diagnoser_Result_Fault_Type = "Error while storing the diagnoser results"
Kubectl_Cluster_Info_Failed_Fault_Type = "Error while doing kubectl cluster-info"
Fetch_Kubectl_Cluster_Info_Fault_Type = "Error occured while fetching cluster-info"
Fetch_Kubectl_Cluster_Info = "kubectl_cluster_info"
Diagnostic_Check_Passed = "Passed"
Diagnostic_Check_Failed = "Failed"
Diagnostic_Check_Incomplete = "Incomplete"
# Name of the checks and operations
Retrieve_Arc_Agents_Event_Logs = "retrieved_arc_agents_event_logs"
Retrieve_Arc_Agents_Logs = "retrieved_arc_agents_logs"
Retrieve_Deployments_Logs = "retrieved_deployments_logs"
Fetch_Connected_Cluster_Resource = "fetch_connected_cluster_resource"
Storing_Diagnoser_Results_Logs = "storing_diagnoser_results_logs"
MSI_Cert_Expiry_Check = "msi_cert_expiry_check"
KAP_Security_Policy_Check = "kap_security_policy_check"
KAP_Cert_Check = "kap_cert_check"
Diagnoser_Check = "diagnoser_check"
MSI_Cert_Check = "msi_cert_check"
Agent_Version_Check = "agent_version_check"
Arc_Agent_State_Check = "arc_agent_state_check"
# Diagnoser files name
Arc_Agents_Logs = "arc_agents_logs"
Arc_Deployment_Logs = "arc_deployment_logs"
Arc_Diagnostic_Logs = "arc_diagnostic_logs"
Describe_Non_Ready_Arc_Agents = "describe_non_ready_arc_agents"
Agent_State = "agent_state.txt"
Arc_Agents_Events = "arc_agent_events.txt"
Diagnoser_Results = "diagnoser_output.txt"
Connected_Cluster_Resource = "connected_cluster_resource_snapshot.txt"
DNS_Check = "dns_check.txt"
K8s_Cluster_Info = "k8s_cluster_info.txt"
Outbound_Network_Connectivity_Check = "outbound_network_connectivity_check.txt"
Events_of_Incomplete_Diagnoser_Job = "diagnoser_failure_events.txt"

# Diagnostic Results Name
Outbound_Connectivity_Check_Result_String = "Outbound Network Connectivity Result:"
DNS_Check_Result_String = "DNS Result:"
AZ_CLI_ADAL_TO_MSAL_MIGRATE_VERSION = '2.30.0'
CLIENT_PROXY_VERSION = '1.3.019103'
API_SERVER_PORT = 47011
CLIENT_PROXY_PORT = 47010
CLIENTPROXY_CLIENT_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
API_CALL_RETRIES = 12
DEFAULT_REQUEST_TIMEOUT = 10  # seconds
RELEASE_DATE_WINDOWS = 'release31-03-22'
RELEASE_DATE_LINUX = 'release31-03-22'
CSP_REFRESH_TIME = 300
# URL constants
CSP_Storage_Url = "https://k8sconnectcsp.azureedge.net"
CSP_Storage_Url_Mooncake = "https://k8sconnectcsp.blob.core.chinacloudapi.cn"
HELM_STORAGE_URL = "https://k8connecthelm.azureedge.net"
HELM_VERSION = 'v3.6.3'
Download_And_Install_Kubectl_Fault_Type = "Failed to download and install kubectl"
