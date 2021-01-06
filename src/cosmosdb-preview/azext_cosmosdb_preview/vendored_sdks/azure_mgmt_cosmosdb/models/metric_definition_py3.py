# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MetricDefinition(Model):
    """The definition of a metric.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar metric_availabilities: The list of metric availabilities for the
     account.
    :vartype metric_availabilities:
     list[~azure.mgmt.cosmosdb.models.MetricAvailability]
    :ivar primary_aggregation_type: The primary aggregation type of the
     metric. Possible values include: 'None', 'Average', 'Total', 'Minimum',
     'Maximum', 'Last'
    :vartype primary_aggregation_type: str or
     ~azure.mgmt.cosmosdb.models.PrimaryAggregationType
    :param unit: The unit of the metric. Possible values include: 'Count',
     'Bytes', 'Seconds', 'Percent', 'CountPerSecond', 'BytesPerSecond',
     'Milliseconds'
    :type unit: str or ~azure.mgmt.cosmosdb.models.UnitType
    :ivar resource_uri: The resource uri of the database.
    :vartype resource_uri: str
    :ivar name: The name information for the metric.
    :vartype name: ~azure.mgmt.cosmosdb.models.MetricName
    """

    _validation = {
        'metric_availabilities': {'readonly': True},
        'primary_aggregation_type': {'readonly': True},
        'resource_uri': {'readonly': True},
        'name': {'readonly': True},
    }

    _attribute_map = {
        'metric_availabilities': {'key': 'metricAvailabilities', 'type': '[MetricAvailability]'},
        'primary_aggregation_type': {'key': 'primaryAggregationType', 'type': 'str'},
        'unit': {'key': 'unit', 'type': 'str'},
        'resource_uri': {'key': 'resourceUri', 'type': 'str'},
        'name': {'key': 'name', 'type': 'MetricName'},
    }

    def __init__(self, *, unit=None, **kwargs) -> None:
        super(MetricDefinition, self).__init__(**kwargs)
        self.metric_availabilities = None
        self.primary_aggregation_type = None
        self.unit = unit
        self.resource_uri = None
        self.name = None