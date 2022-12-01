# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "network vpn-gateway show",
)
class Show(AAZCommand):
    """Get the details of a site-to-site VPN gateway.

    :example: Get the details of a site-to-site VPN gateway.
        az network vpn-gateway show -n MyVPNGateway -g MyRG
    """

    _aaz_info = {
        "version": "2022-05-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.network/vpngateways/{}", "2022-05-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.name = AAZStrArg(
            options=["-n", "--name"],
            help="Name of the VPN gateway.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.VpnGatewaysGet(ctx=self.ctx)()
        self.post_operations()

    # @register_callback
    def pre_operations(self):
        pass

    # @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class VpnGatewaysGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/vpnGateways/{gatewayName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "gatewayName", self.ctx.args.name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2022-05-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.etag = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.id = AAZStrType()
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.bgp_settings = AAZObjectType(
                serialized_name="bgpSettings",
            )
            properties.connections = AAZListType()
            properties.enable_bgp_route_translation_for_nat = AAZBoolType(
                serialized_name="enableBgpRouteTranslationForNat",
            )
            properties.ip_configurations = AAZListType(
                serialized_name="ipConfigurations",
                flags={"read_only": True},
            )
            properties.is_routing_preference_internet = AAZBoolType(
                serialized_name="isRoutingPreferenceInternet",
            )
            properties.nat_rules = AAZListType(
                serialized_name="natRules",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.virtual_hub = AAZObjectType(
                serialized_name="virtualHub",
            )
            properties.vpn_gateway_scale_unit = AAZIntType(
                serialized_name="vpnGatewayScaleUnit",
            )

            bgp_settings = cls._schema_on_200.properties.bgp_settings
            bgp_settings.asn = AAZIntType()
            bgp_settings.bgp_peering_address = AAZStrType(
                serialized_name="bgpPeeringAddress",
            )
            bgp_settings.bgp_peering_addresses = AAZListType(
                serialized_name="bgpPeeringAddresses",
            )
            bgp_settings.peer_weight = AAZIntType(
                serialized_name="peerWeight",
            )

            bgp_peering_addresses = cls._schema_on_200.properties.bgp_settings.bgp_peering_addresses
            bgp_peering_addresses.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.bgp_settings.bgp_peering_addresses.Element
            _element.custom_bgp_ip_addresses = AAZListType(
                serialized_name="customBgpIpAddresses",
            )
            _element.default_bgp_ip_addresses = AAZListType(
                serialized_name="defaultBgpIpAddresses",
                flags={"read_only": True},
            )
            _element.ipconfiguration_id = AAZStrType(
                serialized_name="ipconfigurationId",
            )
            _element.tunnel_ip_addresses = AAZListType(
                serialized_name="tunnelIpAddresses",
                flags={"read_only": True},
            )

            custom_bgp_ip_addresses = cls._schema_on_200.properties.bgp_settings.bgp_peering_addresses.Element.custom_bgp_ip_addresses
            custom_bgp_ip_addresses.Element = AAZStrType()

            default_bgp_ip_addresses = cls._schema_on_200.properties.bgp_settings.bgp_peering_addresses.Element.default_bgp_ip_addresses
            default_bgp_ip_addresses.Element = AAZStrType(
                flags={"read_only": True},
            )

            tunnel_ip_addresses = cls._schema_on_200.properties.bgp_settings.bgp_peering_addresses.Element.tunnel_ip_addresses
            tunnel_ip_addresses.Element = AAZStrType(
                flags={"read_only": True},
            )

            connections = cls._schema_on_200.properties.connections
            connections.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.connections.Element
            _element.etag = AAZStrType(
                flags={"read_only": True},
            )
            _element.id = AAZStrType()
            _element.name = AAZStrType()
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )

            properties = cls._schema_on_200.properties.connections.Element.properties
            properties.connection_bandwidth = AAZIntType(
                serialized_name="connectionBandwidth",
            )
            properties.connection_status = AAZStrType(
                serialized_name="connectionStatus",
                flags={"read_only": True},
            )
            properties.dpd_timeout_seconds = AAZIntType(
                serialized_name="dpdTimeoutSeconds",
            )
            properties.egress_bytes_transferred = AAZIntType(
                serialized_name="egressBytesTransferred",
                flags={"read_only": True},
            )
            properties.enable_bgp = AAZBoolType(
                serialized_name="enableBgp",
            )
            properties.enable_internet_security = AAZBoolType(
                serialized_name="enableInternetSecurity",
            )
            properties.enable_rate_limiting = AAZBoolType(
                serialized_name="enableRateLimiting",
            )
            properties.ingress_bytes_transferred = AAZIntType(
                serialized_name="ingressBytesTransferred",
                flags={"read_only": True},
            )
            properties.ipsec_policies = AAZListType(
                serialized_name="ipsecPolicies",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.remote_vpn_site = AAZObjectType(
                serialized_name="remoteVpnSite",
            )
            _build_schema_sub_resource_read(properties.remote_vpn_site)
            properties.routing_configuration = AAZObjectType(
                serialized_name="routingConfiguration",
            )
            properties.routing_weight = AAZIntType(
                serialized_name="routingWeight",
            )
            properties.shared_key = AAZStrType(
                serialized_name="sharedKey",
            )
            properties.traffic_selector_policies = AAZListType(
                serialized_name="trafficSelectorPolicies",
            )
            properties.use_local_azure_ip_address = AAZBoolType(
                serialized_name="useLocalAzureIpAddress",
            )
            properties.use_policy_based_traffic_selectors = AAZBoolType(
                serialized_name="usePolicyBasedTrafficSelectors",
            )
            properties.vpn_connection_protocol_type = AAZStrType(
                serialized_name="vpnConnectionProtocolType",
            )
            properties.vpn_link_connections = AAZListType(
                serialized_name="vpnLinkConnections",
            )

            ipsec_policies = cls._schema_on_200.properties.connections.Element.properties.ipsec_policies
            ipsec_policies.Element = AAZObjectType()
            _build_schema_ipsec_policy_read(ipsec_policies.Element)

            routing_configuration = cls._schema_on_200.properties.connections.Element.properties.routing_configuration
            routing_configuration.associated_route_table = AAZObjectType(
                serialized_name="associatedRouteTable",
            )
            _build_schema_sub_resource_read(routing_configuration.associated_route_table)
            routing_configuration.inbound_route_map = AAZObjectType(
                serialized_name="inboundRouteMap",
            )
            _build_schema_sub_resource_read(routing_configuration.inbound_route_map)
            routing_configuration.outbound_route_map = AAZObjectType(
                serialized_name="outboundRouteMap",
            )
            _build_schema_sub_resource_read(routing_configuration.outbound_route_map)
            routing_configuration.propagated_route_tables = AAZObjectType(
                serialized_name="propagatedRouteTables",
            )
            routing_configuration.vnet_routes = AAZObjectType(
                serialized_name="vnetRoutes",
            )

            propagated_route_tables = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.propagated_route_tables
            propagated_route_tables.ids = AAZListType()
            propagated_route_tables.labels = AAZListType()

            ids = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.propagated_route_tables.ids
            ids.Element = AAZObjectType()
            _build_schema_sub_resource_read(ids.Element)

            labels = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.propagated_route_tables.labels
            labels.Element = AAZStrType()

            vnet_routes = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes
            vnet_routes.bgp_connections = AAZListType(
                serialized_name="bgpConnections",
                flags={"read_only": True},
            )
            vnet_routes.static_routes = AAZListType(
                serialized_name="staticRoutes",
            )
            vnet_routes.static_routes_config = AAZObjectType(
                serialized_name="staticRoutesConfig",
            )

            bgp_connections = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes.bgp_connections
            bgp_connections.Element = AAZObjectType()
            _build_schema_sub_resource_read(bgp_connections.Element)

            static_routes = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes.static_routes
            static_routes.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes.static_routes.Element
            _element.address_prefixes = AAZListType(
                serialized_name="addressPrefixes",
            )
            _element.name = AAZStrType()
            _element.next_hop_ip_address = AAZStrType(
                serialized_name="nextHopIpAddress",
            )

            address_prefixes = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes.static_routes.Element.address_prefixes
            address_prefixes.Element = AAZStrType()

            static_routes_config = cls._schema_on_200.properties.connections.Element.properties.routing_configuration.vnet_routes.static_routes_config
            static_routes_config.propagate_static_routes = AAZBoolType(
                serialized_name="propagateStaticRoutes",
                flags={"read_only": True},
            )
            static_routes_config.vnet_local_route_override_criteria = AAZStrType(
                serialized_name="vnetLocalRouteOverrideCriteria",
            )

            traffic_selector_policies = cls._schema_on_200.properties.connections.Element.properties.traffic_selector_policies
            traffic_selector_policies.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.connections.Element.properties.traffic_selector_policies.Element
            _element.local_address_ranges = AAZListType(
                serialized_name="localAddressRanges",
                flags={"required": True},
            )
            _element.remote_address_ranges = AAZListType(
                serialized_name="remoteAddressRanges",
                flags={"required": True},
            )

            local_address_ranges = cls._schema_on_200.properties.connections.Element.properties.traffic_selector_policies.Element.local_address_ranges
            local_address_ranges.Element = AAZStrType()

            remote_address_ranges = cls._schema_on_200.properties.connections.Element.properties.traffic_selector_policies.Element.remote_address_ranges
            remote_address_ranges.Element = AAZStrType()

            vpn_link_connections = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections
            vpn_link_connections.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element
            _element.etag = AAZStrType(
                flags={"read_only": True},
            )
            _element.id = AAZStrType()
            _element.name = AAZStrType()
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties
            properties.connection_bandwidth = AAZIntType(
                serialized_name="connectionBandwidth",
            )
            properties.connection_status = AAZStrType(
                serialized_name="connectionStatus",
                flags={"read_only": True},
            )
            properties.egress_bytes_transferred = AAZIntType(
                serialized_name="egressBytesTransferred",
                flags={"read_only": True},
            )
            properties.egress_nat_rules = AAZListType(
                serialized_name="egressNatRules",
            )
            properties.enable_bgp = AAZBoolType(
                serialized_name="enableBgp",
            )
            properties.enable_rate_limiting = AAZBoolType(
                serialized_name="enableRateLimiting",
            )
            properties.ingress_bytes_transferred = AAZIntType(
                serialized_name="ingressBytesTransferred",
                flags={"read_only": True},
            )
            properties.ingress_nat_rules = AAZListType(
                serialized_name="ingressNatRules",
            )
            properties.ipsec_policies = AAZListType(
                serialized_name="ipsecPolicies",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.routing_weight = AAZIntType(
                serialized_name="routingWeight",
            )
            properties.shared_key = AAZStrType(
                serialized_name="sharedKey",
            )
            properties.use_local_azure_ip_address = AAZBoolType(
                serialized_name="useLocalAzureIpAddress",
            )
            properties.use_policy_based_traffic_selectors = AAZBoolType(
                serialized_name="usePolicyBasedTrafficSelectors",
            )
            properties.vpn_connection_protocol_type = AAZStrType(
                serialized_name="vpnConnectionProtocolType",
            )
            properties.vpn_gateway_custom_bgp_addresses = AAZListType(
                serialized_name="vpnGatewayCustomBgpAddresses",
            )
            properties.vpn_link_connection_mode = AAZStrType(
                serialized_name="vpnLinkConnectionMode",
            )
            properties.vpn_site_link = AAZObjectType(
                serialized_name="vpnSiteLink",
            )
            _build_schema_sub_resource_read(properties.vpn_site_link)

            egress_nat_rules = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties.egress_nat_rules
            egress_nat_rules.Element = AAZObjectType()
            _build_schema_sub_resource_read(egress_nat_rules.Element)

            ingress_nat_rules = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties.ingress_nat_rules
            ingress_nat_rules.Element = AAZObjectType()
            _build_schema_sub_resource_read(ingress_nat_rules.Element)

            ipsec_policies = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties.ipsec_policies
            ipsec_policies.Element = AAZObjectType()
            _build_schema_ipsec_policy_read(ipsec_policies.Element)

            vpn_gateway_custom_bgp_addresses = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties.vpn_gateway_custom_bgp_addresses
            vpn_gateway_custom_bgp_addresses.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.connections.Element.properties.vpn_link_connections.Element.properties.vpn_gateway_custom_bgp_addresses.Element
            _element.custom_bgp_ip_address = AAZStrType(
                serialized_name="customBgpIpAddress",
                flags={"required": True},
            )
            _element.ip_configuration_id = AAZStrType(
                serialized_name="ipConfigurationId",
                flags={"required": True},
            )

            ip_configurations = cls._schema_on_200.properties.ip_configurations
            ip_configurations.Element = AAZObjectType(
                flags={"read_only": True},
            )

            _element = cls._schema_on_200.properties.ip_configurations.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.private_ip_address = AAZStrType(
                serialized_name="privateIpAddress",
                flags={"read_only": True},
            )
            _element.public_ip_address = AAZStrType(
                serialized_name="publicIpAddress",
                flags={"read_only": True},
            )

            nat_rules = cls._schema_on_200.properties.nat_rules
            nat_rules.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.nat_rules.Element
            _element.etag = AAZStrType(
                flags={"read_only": True},
            )
            _element.id = AAZStrType()
            _element.name = AAZStrType()
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties.nat_rules.Element.properties
            properties.egress_vpn_site_link_connections = AAZListType(
                serialized_name="egressVpnSiteLinkConnections",
                flags={"read_only": True},
            )
            properties.external_mappings = AAZListType(
                serialized_name="externalMappings",
            )
            properties.ingress_vpn_site_link_connections = AAZListType(
                serialized_name="ingressVpnSiteLinkConnections",
                flags={"read_only": True},
            )
            properties.internal_mappings = AAZListType(
                serialized_name="internalMappings",
            )
            properties.ip_configuration_id = AAZStrType(
                serialized_name="ipConfigurationId",
            )
            properties.mode = AAZStrType()
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.type = AAZStrType()

            egress_vpn_site_link_connections = cls._schema_on_200.properties.nat_rules.Element.properties.egress_vpn_site_link_connections
            egress_vpn_site_link_connections.Element = AAZObjectType()
            _build_schema_sub_resource_read(egress_vpn_site_link_connections.Element)

            external_mappings = cls._schema_on_200.properties.nat_rules.Element.properties.external_mappings
            external_mappings.Element = AAZObjectType()
            _build_schema_vpn_nat_rule_mapping_read(external_mappings.Element)

            ingress_vpn_site_link_connections = cls._schema_on_200.properties.nat_rules.Element.properties.ingress_vpn_site_link_connections
            ingress_vpn_site_link_connections.Element = AAZObjectType()
            _build_schema_sub_resource_read(ingress_vpn_site_link_connections.Element)

            internal_mappings = cls._schema_on_200.properties.nat_rules.Element.properties.internal_mappings
            internal_mappings.Element = AAZObjectType()
            _build_schema_vpn_nat_rule_mapping_read(internal_mappings.Element)

            virtual_hub = cls._schema_on_200.properties.virtual_hub
            virtual_hub.id = AAZStrType()

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


_schema_ipsec_policy_read = None


def _build_schema_ipsec_policy_read(_schema):
    global _schema_ipsec_policy_read
    if _schema_ipsec_policy_read is not None:
        _schema.dh_group = _schema_ipsec_policy_read.dh_group
        _schema.ike_encryption = _schema_ipsec_policy_read.ike_encryption
        _schema.ike_integrity = _schema_ipsec_policy_read.ike_integrity
        _schema.ipsec_encryption = _schema_ipsec_policy_read.ipsec_encryption
        _schema.ipsec_integrity = _schema_ipsec_policy_read.ipsec_integrity
        _schema.pfs_group = _schema_ipsec_policy_read.pfs_group
        _schema.sa_data_size_kilobytes = _schema_ipsec_policy_read.sa_data_size_kilobytes
        _schema.sa_life_time_seconds = _schema_ipsec_policy_read.sa_life_time_seconds
        return

    _schema_ipsec_policy_read = AAZObjectType()

    ipsec_policy_read = _schema_ipsec_policy_read
    ipsec_policy_read.dh_group = AAZStrType(
        serialized_name="dhGroup",
        flags={"required": True},
    )
    ipsec_policy_read.ike_encryption = AAZStrType(
        serialized_name="ikeEncryption",
        flags={"required": True},
    )
    ipsec_policy_read.ike_integrity = AAZStrType(
        serialized_name="ikeIntegrity",
        flags={"required": True},
    )
    ipsec_policy_read.ipsec_encryption = AAZStrType(
        serialized_name="ipsecEncryption",
        flags={"required": True},
    )
    ipsec_policy_read.ipsec_integrity = AAZStrType(
        serialized_name="ipsecIntegrity",
        flags={"required": True},
    )
    ipsec_policy_read.pfs_group = AAZStrType(
        serialized_name="pfsGroup",
        flags={"required": True},
    )
    ipsec_policy_read.sa_data_size_kilobytes = AAZIntType(
        serialized_name="saDataSizeKilobytes",
        flags={"required": True},
    )
    ipsec_policy_read.sa_life_time_seconds = AAZIntType(
        serialized_name="saLifeTimeSeconds",
        flags={"required": True},
    )

    _schema.dh_group = _schema_ipsec_policy_read.dh_group
    _schema.ike_encryption = _schema_ipsec_policy_read.ike_encryption
    _schema.ike_integrity = _schema_ipsec_policy_read.ike_integrity
    _schema.ipsec_encryption = _schema_ipsec_policy_read.ipsec_encryption
    _schema.ipsec_integrity = _schema_ipsec_policy_read.ipsec_integrity
    _schema.pfs_group = _schema_ipsec_policy_read.pfs_group
    _schema.sa_data_size_kilobytes = _schema_ipsec_policy_read.sa_data_size_kilobytes
    _schema.sa_life_time_seconds = _schema_ipsec_policy_read.sa_life_time_seconds


_schema_sub_resource_read = None


def _build_schema_sub_resource_read(_schema):
    global _schema_sub_resource_read
    if _schema_sub_resource_read is not None:
        _schema.id = _schema_sub_resource_read.id
        return

    _schema_sub_resource_read = AAZObjectType()

    sub_resource_read = _schema_sub_resource_read
    sub_resource_read.id = AAZStrType()

    _schema.id = _schema_sub_resource_read.id


_schema_vpn_nat_rule_mapping_read = None


def _build_schema_vpn_nat_rule_mapping_read(_schema):
    global _schema_vpn_nat_rule_mapping_read
    if _schema_vpn_nat_rule_mapping_read is not None:
        _schema.address_space = _schema_vpn_nat_rule_mapping_read.address_space
        _schema.port_range = _schema_vpn_nat_rule_mapping_read.port_range
        return

    _schema_vpn_nat_rule_mapping_read = AAZObjectType()

    vpn_nat_rule_mapping_read = _schema_vpn_nat_rule_mapping_read
    vpn_nat_rule_mapping_read.address_space = AAZStrType(
        serialized_name="addressSpace",
    )
    vpn_nat_rule_mapping_read.port_range = AAZStrType(
        serialized_name="portRange",
    )

    _schema.address_space = _schema_vpn_nat_rule_mapping_read.address_space
    _schema.port_range = _schema_vpn_nat_rule_mapping_read.port_range


__all__ = ["Show"]
