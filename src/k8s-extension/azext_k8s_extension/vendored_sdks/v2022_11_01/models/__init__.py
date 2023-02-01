# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._models_py3 import AzureBlobDefinition
from ._models_py3 import AzureBlobPatchDefinition
from ._models_py3 import BucketDefinition
from ._models_py3 import BucketPatchDefinition
from ._models_py3 import ComplianceStatus
from ._models_py3 import ErrorAdditionalInfo
from ._models_py3 import ErrorDetail
from ._models_py3 import ErrorResponse
from ._models_py3 import Extension
from ._models_py3 import ExtensionPropertiesAksAssignedIdentity
from ._models_py3 import ExtensionStatus
from ._models_py3 import ExtensionsList
from ._models_py3 import FluxConfiguration
from ._models_py3 import FluxConfigurationPatch
from ._models_py3 import FluxConfigurationsList
from ._models_py3 import GitRepositoryDefinition
from ._models_py3 import GitRepositoryPatchDefinition
from ._models_py3 import HelmOperatorProperties
from ._models_py3 import HelmReleasePropertiesDefinition
from ._models_py3 import Identity
from ._models_py3 import KustomizationDefinition
from ._models_py3 import KustomizationPatchDefinition
from ._models_py3 import ManagedIdentityDefinition
from ._models_py3 import ManagedIdentityPatchDefinition
from ._models_py3 import ObjectReferenceDefinition
from ._models_py3 import ObjectStatusConditionDefinition
from ._models_py3 import ObjectStatusDefinition
from ._models_py3 import OperationStatusList
from ._models_py3 import OperationStatusResult
from ._models_py3 import PatchExtension
from ._models_py3 import Plan
from ._models_py3 import ProxyResource
from ._models_py3 import RepositoryRefDefinition
from ._models_py3 import Resource
from ._models_py3 import ResourceProviderOperation
from ._models_py3 import ResourceProviderOperationDisplay
from ._models_py3 import ResourceProviderOperationList
from ._models_py3 import Scope
from ._models_py3 import ScopeCluster
from ._models_py3 import ScopeNamespace
from ._models_py3 import ServicePrincipalDefinition
from ._models_py3 import ServicePrincipalPatchDefinition
from ._models_py3 import SourceControlConfiguration
from ._models_py3 import SourceControlConfigurationList
from ._models_py3 import SystemData

from ._source_control_configuration_client_enums import AKSIdentityType
from ._source_control_configuration_client_enums import ComplianceStateType
from ._source_control_configuration_client_enums import CreatedByType
from ._source_control_configuration_client_enums import FluxComplianceState
from ._source_control_configuration_client_enums import KustomizationValidationType
from ._source_control_configuration_client_enums import LevelType
from ._source_control_configuration_client_enums import MessageLevelType
from ._source_control_configuration_client_enums import OperatorScopeType
from ._source_control_configuration_client_enums import OperatorType
from ._source_control_configuration_client_enums import ProvisioningState
from ._source_control_configuration_client_enums import ProvisioningStateType
from ._source_control_configuration_client_enums import ScopeType
from ._source_control_configuration_client_enums import SourceKindType
from ._patch import __all__ as _patch_all
from ._patch import *  # type: ignore # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AzureBlobDefinition",
    "AzureBlobPatchDefinition",
    "BucketDefinition",
    "BucketPatchDefinition",
    "ComplianceStatus",
    "ErrorAdditionalInfo",
    "ErrorDetail",
    "ErrorResponse",
    "Extension",
    "ExtensionPropertiesAksAssignedIdentity",
    "ExtensionStatus",
    "ExtensionsList",
    "FluxConfiguration",
    "FluxConfigurationPatch",
    "FluxConfigurationsList",
    "GitRepositoryDefinition",
    "GitRepositoryPatchDefinition",
    "HelmOperatorProperties",
    "HelmReleasePropertiesDefinition",
    "Identity",
    "KustomizationDefinition",
    "KustomizationPatchDefinition",
    "ManagedIdentityDefinition",
    "ManagedIdentityPatchDefinition",
    "ObjectReferenceDefinition",
    "ObjectStatusConditionDefinition",
    "ObjectStatusDefinition",
    "OperationStatusList",
    "OperationStatusResult",
    "PatchExtension",
    "Plan",
    "ProxyResource",
    "RepositoryRefDefinition",
    "Resource",
    "ResourceProviderOperation",
    "ResourceProviderOperationDisplay",
    "ResourceProviderOperationList",
    "Scope",
    "ScopeCluster",
    "ScopeNamespace",
    "ServicePrincipalDefinition",
    "ServicePrincipalPatchDefinition",
    "SourceControlConfiguration",
    "SourceControlConfigurationList",
    "SystemData",
    "AKSIdentityType",
    "ComplianceStateType",
    "CreatedByType",
    "FluxComplianceState",
    "KustomizationValidationType",
    "LevelType",
    "MessageLevelType",
    "OperatorScopeType",
    "OperatorType",
    "ProvisioningState",
    "ProvisioningStateType",
    "ScopeType",
    "SourceKindType",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
