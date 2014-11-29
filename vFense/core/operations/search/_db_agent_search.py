from vFense.db.client import db_create_close, r
from vFense.core.decorators import catch_it, time_it
from vFense.core.operations.search._constants import OperationSearchValues
from vFense.core.agent._db_model import AgentKeys, AgentCollections

from vFense.core.operations._db_model import (
    AgentOperationKey, AgentOperationIndexes,
    OperationCollections, OperationPerAgentKey, OperationPerAgentIndexes,
    OperationPerAppKey, OperationPerAppIndexes
)

from vFense.core.operations.status_codes import AgentOperationCodes
from vFense.search._db_base import FetchBase

class FetchAgentOperations(FetchBase):
    def __init__(self, sort_key=AgentOperationKey.CreatedTime, **kwargs):
        super(FetchAgentOperations, self).__init__(**kwargs)
        self.sort_key = sort_key

    @time_it
    @catch_it((0, []))
    @db_create_close
    def all(self, conn=None):
        """Fetch all operations
        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> operation = FetchAgentOperations(view_name)
            >>> operation.all()

        Returns:
            List
            [
                {
                    "agents_expired_count": 0,
                    "agents_total_count": 1,
                    "tag_id": null,
                    "agents_completed_with_errors_count": 0,
                    "created_by": "admin",
                    "agents_pending_pickup_count": 0,
                    "completed_time": 1398092303,
                    "operation_status": 6006,
                    "agents_completed_count": 1,
                    "operation_id": "6c0209d5-b350-48b7-808a-158ddacb6940",
                    "created_time": 1398092302,
                    "agents_pending_results_count": 0,
                    "operation": "install_os_apps",
                    "updated_time": 1398092303,
                    "agents_failed_count": 0,
                    "view_name": "default"
                }
            ]
        """
        count = 0
        data = []
        base_filter = self._set_agent_operation_base_query()
        base_time_merge = self._set_base_time_merge()
        count = (
            base_filter
            .count()
            .run(conn)
        )

        data = list(
            base_filter
            .order_by(self.sort(self.sort_key))
            .skip(self.offset)
            .limit(self.count)
            .merge(base_time_merge)
            .run(conn)
        )

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def by_agentid(self, agent_id, conn=None):
        """Fetch all operations by agent id
        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> agent_id = '6c0209d5-b350-48b7-808a-158ddacb6940'
            >>> operation = FetchAgentOperations(view_name)
            >>> operation.by_agentid(agent_id)

        Returns:
            List
            [
                {
                    "agents_expired_count": 0,
                    "agents_total_count": 1,
                    "tag_id": null,
                    "agents_completed_with_errors_count": 0,
                    "created_by": "admin",
                    "agents_pending_pickup_count": 0,
                    "completed_time": 1398092303,
                    "operation_status": 6006,
                    "agents_completed_count": 1,
                    "operation_id": "6c0209d5-b350-48b7-808a-158ddacb6940",
                    "created_time": 1398092302,
                    "agents_pending_results_count": 0,
                    "operation": "install_os_apps",
                    "updated_time": 1398092303,
                    "agents_failed_count": 0,
                    "view_name": "default"
                }
            ]
        """
        count = 0
        data = []
        base_time_merge = self._set_base_time_merge()
        count = (
            r
            .table(OperationCollections.Agent)
            .get_all(
                agent_id,
                index=AgentOperationIndexes.AgentIds
            )
            .count()
            .run(conn)
        )

        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(
                agent_id,
                index=AgentOperationIndexes.AgentIds
            )
            .order_by(self.sort(self.sort_key))
            .skip(self.offset)
            .limit(self.count)
            .merge(base_time_merge)
            .run(conn)
        )

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def by_tagid(self, tag_id, conn=None):
        """Fetch all operations by tag id
        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> tag_id = '78076908-e93f-4116-8d49-ad42b4ad0297'
            >>> operation = FetchAgentOperations(view_name)
            >>> operation.by_tagid(tag_id)

        Returns:
            List [count, data]
            [
                1,
                [
                    {
                        "agents_expired_count": 0,
                        "cpu_throttle": "normal",
                        "agents_total_count": 2,
                        "plugin": "rv",
                        "tag_id": "78076908-e93f-4116-8d49-ad42b4ad0297",
                        "agents_completed_with_errors_count": 0,
                        "action_performed_on": "tag",
                        "created_by": "admin",
                        "agents_pending_pickup_count": 0,
                        "completed_time": 1398110835,
                        "operation_status": 6006,
                        "agents_completed_count": 2,
                        "operation_id": "d6956a46-165f-49b6-a3df-872a1453ab88",
                        "created_time": 1398110770,
                        "agents_pending_results_count": 0,
                        "operation": "install_os_apps",
                        "updated_time": 1398110835,
                        "net_throttle": 0,
                        "agents_failed_count": 0,
                        "restart": "none",
                        "view_name": "default"
                    }
                ]
            ]
        """
        count = 0
        data = []
        base_time_merge = self._set_base_time_merge()
        count = (
            r
            .table(OperationCollections.Agent)
            .get_all(tag_id, index=AgentOperationKey.TagId)
            .count()
            .run(conn)
        )

        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(tag_id, index=AgentOperationKey.TagId)
            .order_by(self.sort(self.sort_key))
            .skip(self.offset)
            .limit(self.count)
            .merge(base_time_merge)
            .run(conn)
        )

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def by_operation(self, action, conn=None):
        """Fetch all operations by action
        Args:
            action (str) The action the operation will perform.
                examples... reboot, shutdown, install_os_apps

        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> operation = FetchAgentOperations(view_name)
            >>> action = 'install_os_apps'
            >>> operation.by_operation(action)
        Returns:
            List of dictionaries
            [
                {
                    "agents_expired_count": 0,
                    "created_time": 1398126651,
                    "agents_pending_results_count": 0,
                    "operation": "install_os_apps",
                    "net_throttle": 0,
                    "view_name": "default",
                    "cpu_throttle": "normal",
                    "agents_total_count": 1,
                    "agents_completed_with_errors_count": 0,
                    "action_performed_on": "agent",
                    "agent_ids": [
                        "33ba8521-b2e5-47dc-9bdc-0f1e3384049d"
                    ],
                    "created_by": "admin",
                    "tag_id": null,
                    "completed_time": 0,
                    "agents_completed_count": 0,
                    "agents_pending_pickup_count": 1,
                    "restart": "none",
                    "plugin": "rv",
                    "updated_time": 1398126651,
                    "operation_status": 6009,
                    "operation_id": "267486ef-850f-47e7-a0c4-0da5d5a38efb",
                    "agents_failed_count": 0
                }
            ]
        """
        count = 0
        data = []
        base_time_merge = self._set_base_time_merge()
        count = (
            r
            .table(OperationCollections.Agent)
            .get_all(
                [action, self.view_name],
                index=AgentOperationIndexes.OperationAndView
            )
            .count()
            .run(conn)
        )

        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(
                [action, self.view_name],
                index=AgentOperationIndexes.OperationAndView
            )
            .order_by(self.sort(self.sort_key))
            .skip(self.offset)
            .limit(self.count)
            .merge(base_time_merge)
            .run(conn)
        )

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def install_operation_by_id(self, operation_id, conn=None):
        """Fetch install operation by operation id
        Args:
            operation_id (str) 36 character UUID.

        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> operation = FetchAgentOperations(view_name)
            >>> operation_id = 'd6956a46-165f-49b6-a3df-872a1453ab88'
            >>> operation.install_operation_by_id(operation_id)

        Returns:
            Dictionary
            {
                "agents_expired_count": 0,
                "agents": [
                    {
                        "status": 6502,
                        "picked_up_time": 1398118321,
                        "errors": null,
                        "display_name": null,
                        "apps_failed_count": 0,
                        "apps_completed_count": 1,
                        "completed_time": 1398118775,
                        "applications": [
                            {
                                "errors": null,
                                "app_name": "libssl1.0.0",
                                "results": 6002,
                                "app_id": "c5fc13cb20b231eb03b225cc0cb1371240450afaf151ed63ef12df77766ca1cf",
                                "apps_removed": [
                                    {
                                        "version": "1.0.1-4ubuntu5.10",
                                        "name": "libssl1.0.0"
                                    }
                                ],
                                "app_version": "1.0.1-4ubuntu5.12",
                                "results_received_time": 1398118775
                            }
                        ],
                        "apps_pending_count": 0,
                        "agent_id": "33ba8521-b2e5-47dc-9bdc-0f1e3384049d",
                        "computer_name": "ubuntu",
                        "apps_total_count": 1,
                        "operation_id": "48854d9d-a705-45d2-bab6-a448bc75f7d2",
                        "expired_time": 0
                    }
                ],
                "created_time": 1398118321,
                "agents_pending_results_count": 0,
                "operation": "install_os_apps",
                "net_throttle": 0,
                "view_name": "default",
                "cpu_throttle": "normal",
                "agents_total_count": 1,
                "agents_completed_with_errors_count": 0,
                "action_performed_on": "agent",
                "agent_ids": [
                    "33ba8521-b2e5-47dc-9bdc-0f1e3384049d"
                ],
                "created_by": "admin",
                "tag_id": null,
                "completed_time": 1398118775,
                "agents_completed_count": 1,
                "agents_pending_pickup_count": 0,
                "restart": "none",
                "plugin": "rv",
                "updated_time": 1398118775,
                "operation_status": 6006,
                "operation_id": "48854d9d-a705-45d2-bab6-a448bc75f7d2",
                "agents_failed_count": 0
            }
        """
        count = 0
        data = []
        merge = self._set_install_operation_merge()
        data = (
            r
            .table(OperationCollections.Agent)
            .get(operation_id)
            .merge(merge)
            .run(conn)
        )
        if data:
            count = 1

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def by_id(self, operation_id, conn=None):
        """Fetch operation by operation id
        Args:
            operation_id (str) 36 character UUID.

        Basic Usage:
            >>> from vFense.core.operations.search._db_agent_search import FetchAgentOperations
            >>> view_name = 'default'
            >>> operation = FetchAgentOperations(view_name)
            >>> operation_id = 'd6956a46-165f-49b6-a3df-872a1453ab88'
            >>> operation.by_id(operation_id)

        Returns:
            Dictionary
            {
                "agents_expired_count": 0,
                "agents": [
                    {
                        "status": 6501,
                        "picked_up_time": 0,
                        "errors": null,
                        "display_name": null,
                        "expired_time": 0,
                        "completed_time": 0,
                        "agent_id": "33ba8521-b2e5-47dc-9bdc-0f1e3384049d",
                        "computer_name": "ubuntu",
                    }
                ],
                "created_time": 1398110770,
                "agents_pending_results_count": 0,
                "operation": "updatesapplications",
                "net_throttle": null,
                "view_name": "default",
                "cpu_throttle": null,
                "agents_total_count": 1,
                "agents_completed_with_errors_count": 0,
                "action_performed_on": "agent",
                "created_by": "admin",
                "tag_id": null,
                "completed_time": 0,
                "agents_completed_count": 0,
                "agents_pending_pickup_count": 1,
                "restart": null,
                "plugin": "rv",
                "updated_time": 1398110770,
                "operation_status": 6009,
                "operation_id": "58d37cf8-c1a9-460d-a7c6-0c8f896970b4",
                "agents_failed_count": 0
            }
        """
        count = 0
        data = []
        merge = self._set_operation_per_agent_merge()
        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(
                operation_id,
                index=AgentOperationIndexes.OperationId
            )
            .merge(merge)
            .run(conn)
        )
        if data:
            data = data[0]
            count = 1

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def install_operation_for_email_alert(self, operation_id, conn=None):
        count = 0
        data = []
        merge = self._set_install_operation_email_alert_merge()
        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(
                operation_id,
                index=AgentOperationIndexes.OperationId
            )
            .merge(merge)
            .run(conn)
        )
        if data:
            data = data[0]
            count = 1

        return(count, data)

    @time_it
    @catch_it((0, []))
    @db_create_close
    def operation_for_email_alert(self, operation_id, conn=None):
        count = 0
        data = []
        merge = self._set_operation_for_email_alert_merge()
        data = list(
            r
            .table(OperationCollections.Agent)
            .get_all(
                operation_id,
                index=AgentOperationIndexes.OperationId
            )
            .merge(merge)
            .run(conn)
        )
        if data:
            data = data[0]
            count = 1

        return(count, data)


    def _set_operation_for_email_alert_merge(self, oper_id, conn=None):
        agent_pluck = self._set_agent_collection_pluck()
        merge = (
            {
                AgentOperationKey.CreatedTime: (
                    r.row[AgentOperationKey.CreatedTime].to_epoch_time()
                ),
                AgentOperationKey.CompletedTime: (
                    r.row[AgentOperationKey.CompletedTime].to_epoch_time()
                ),
                OperationSearchValues.AGENTS: (
                    r
                    .table(OperationCollections.OperationPerAgent)
                    .get_all(
                        r.row[AgentOperationKey.OperationId],
                        index=OperationPerAgentIndexes.OperationId
                    )
                    .coerce_to('array')
                    .eq_join(
                        OperationPerAgentKey.AgentId,
                        r.table(AgentCollections.Agents)
                    )
                    .zip()
                    .pluck(agent_pluck)
                    .map(lambda x:
                        {
                            OperationPerAgentKey.PickedUpTime: (
                                x[OperationPerAgentKey.PickedUpTime].to_epoch_time()
                            ),
                            OperationPerAgentKey.CompletedTime: (
                                x[OperationPerAgentKey.CompletedTime].to_epoch_time()
                            ),
                        }
                    )
                )
            }
        )

        return merge

    def _set_base_time_merge(self):
        merge = (
            {
                AgentOperationKey.CreatedTime: (
                    r.row[AgentOperationKey.CreatedTime].to_epoch_time()
                ),
                AgentOperationKey.UpdatedTime: (
                    r.row[AgentOperationKey.UpdatedTime].to_epoch_time()
                ),
                AgentOperationKey.CompletedTime: (
                    r.row[AgentOperationKey.CompletedTime].to_epoch_time()
                ),
            }
        )

        return merge

    def _set_base_time_joined_agent_merge(self):
        merge = (
            {
                AgentOperationKey.CreatedTime: (
                    r.row[AgentOperationKey.CreatedTime].to_epoch_time()
                ),
                AgentOperationKey.UpdatedTime: (
                    r.row[AgentOperationKey.UpdatedTime].to_epoch_time()
                ),
                AgentOperationKey.CompletedTime: (
                    r.row[AgentOperationKey.CompletedTime].to_epoch_time()
                ),
                OperationPerAgentKey.PickedUpTime: (
                    r.row[OperationPerAgentKey.PickedUpTime].to_epoch_time()
                ),
                OperationPerAgentKey.ExpiredTime: (
                    r.row[OperationPerAgentKey.ExpiredTime].to_epoch_time()
                ),
            }
        )

        return merge

    def _set_install_operation_email_alert_merge(self):
        agent_pluck = self._set_agent_collection_pluck()
        app_without = self._set_app_collection_without()
        merge = (
            {
                AgentOperationKey.CreatedTime: (
                    r.row[AgentOperationKey.CreatedTime].to_iso8601()
                ),
                AgentOperationKey.UpdatedTime: (
                    r.row[AgentOperationKey.UpdatedTime].to_iso8601()
                ),
                AgentOperationKey.CompletedTime: (
                    r.row[AgentOperationKey.CompletedTime].to_iso8601()
                ),
                OperationSearchValues.AGENTS: (
                    r
                    .table(OperationCollections.OperationPerAgent)
                    .get_all(
                        r.row[AgentOperationKey.OperationId],
                        index=OperationPerAgentIndexes.OperationId
                    )
                    .coerce_to('array')
                    .eq_join(
                        OperationPerAgentKey.AgentId,
                        r.table(AgentCollections.Agents)
                    )
                    .zip()
                    .pluck(agent_pluck)
                    .merge(lambda x:
                        {
                            OperationPerAgentKey.PickedUpTime: (
                                x[OperationPerAgentKey.PickedUpTime].to_iso8601()
                            ),
                            OperationPerAgentKey.CompletedTime: (
                                x[OperationPerAgentKey.CompletedTime].to_iso8601()
                            ),
                            OperationSearchValues.APPLICATIONS_FAILED: (
                                r
                                .table(OperationCollections.OperationPerApp)
                                .get_all(
                                    [
                                        x[AgentOperationKey.OperationId],
                                        x[OperationPerAgentKey.AgentId]
                                    ],
                                    index=OperationPerAppIndexes.OperationIdAndAgentId
                                )
                                .filter(
                                    lambda y:
                                    y[OperationPerAppKey.Results] ==
                                    AgentOperationCodes.ResultsReceivedWithErrors
                                )
                                .coerce_to('array')
                                .merge(lambda y:
                                    {
                                        OperationPerAppKey.ResultsReceivedTime: (
                                            y[OperationPerAppKey.ResultsReceivedTime].to_iso8601()
                                        )
                                    }
                                )
                                .without(app_without)
                            ),
                            OperationSearchValues.APPLICATIONS_PASSED: (
                                r
                                .table(OperationCollections.OperationPerApp)
                                .get_all(
                                    [
                                        x[AgentOperationKey.OperationId],
                                        x[OperationPerAgentKey.AgentId]
                                    ],
                                    index=OperationPerAppIndexes.OperationIdAndAgentId
                                )
                                .filter(
                                    lambda y:
                                    y[OperationPerAppKey.Results] ==
                                    AgentOperationCodes.ResultsReceived
                                )
                                .coerce_to('array')
                                .merge(lambda y:
                                    {
                                        OperationPerAppKey.ResultsReceivedTime: (
                                            y[OperationPerAppKey.ResultsReceivedTime].to_iso8601()
                                        )
                                    }
                                )
                                .without(app_without)
                            )
                        }
                    )
                )
            }
        )
        return merge

    def _set_operation_per_agent_merge(self):
        agent_pluck = self._set_agent_collection_pluck()
        merge = (
            {
                AgentOperationKey.CreatedTime: r.row[AgentOperationKey.CreatedTime].to_epoch_time(),
                AgentOperationKey.UpdatedTime: r.row[AgentOperationKey.UpdatedTime].to_epoch_time(),
                AgentOperationKey.CompletedTime: r.row[AgentOperationKey.CompletedTime].to_epoch_time(),
                OperationSearchValues.AGENTS: (
                    r
                    .table(OperationCollections.OperationPerAgent)
                    .get_all(
                        r.row[AgentOperationKey.OperationId],
                        index=OperationPerAgentIndexes.OperationId
                    )
                    .coerce_to('array')
                    .eq_join(OperationPerAgentKey.AgentId, r.table(AgentCollections.Agents))
                    .zip()
                    .pluck(agent_pluck)
                    .merge(lambda x:
                        {
                            OperationPerAgentKey.PickedUpTime: x[OperationPerAgentKey.PickedUpTime].to_epoch_time(),
                            OperationPerAgentKey.CompletedTime: x[OperationPerAgentKey.CompletedTime].to_epoch_time(),
                            OperationPerAgentKey.ExpiredTime: x[OperationPerAgentKey.ExpiredTime].to_epoch_time(),
                        }
                    )
                )
            }
        )

        return merge

    def _set_install_operation_merge(self):
        agent_pluck = self._set_agent_collection_pluck()
        app_without = self._set_app_collection_without()
        merge = (
            {
                AgentOperationKey.CreatedTime: r.row[AgentOperationKey.CreatedTime].to_epoch_time(),
                AgentOperationKey.UpdatedTime: r.row[AgentOperationKey.UpdatedTime].to_epoch_time(),
                AgentOperationKey.CompletedTime: r.row[AgentOperationKey.CompletedTime].to_epoch_time(),
                OperationSearchValues.AGENTS: (
                    r
                    .table(OperationCollections.OperationPerAgent)
                    .get_all(
                        r.row[AgentOperationKey.OperationId],
                        index=OperationPerAgentIndexes.OperationId
                    )
                    .coerce_to('array')
                    .eq_join(OperationPerAgentKey.AgentId, r.table(AgentCollections.Agents))
                    .zip()
                    .pluck(agent_pluck)
                    .merge(
                        lambda x:
                        {
                            OperationPerAgentKey.PickedUpTime: x[OperationPerAgentKey.PickedUpTime].to_epoch_time(),
                            OperationPerAgentKey.CompletedTime: x[OperationPerAgentKey.CompletedTime].to_epoch_time(),
                            OperationPerAgentKey.ExpiredTime: x[OperationPerAgentKey.ExpiredTime].to_epoch_time(),
                            OperationSearchValues.APPLICATIONS: (
                                r
                                .table(OperationCollections.OperationPerApp)
                                .get_all(
                                    [
                                        x[AgentOperationKey.OperationId],
                                        x[OperationPerAgentKey.AgentId]
                                    ],
                                    index=OperationPerAppIndexes.OperationIdAndAgentId
                                )
                                .coerce_to('array')
                                .without(app_without)
                                .merge(lambda y:
                                    {
                                        OperationPerAppKey.ResultsReceivedTime: y[OperationPerAppKey.ResultsReceivedTime].to_epoch_time()
                                    }
                                )
                            )
                        }
                    )
                )
            }
        )

        return merge

    def _set_agent_operation_base_query(self):
        base_filter = (
            r
            .table(OperationCollections.Agent)
        )
        if self.view_name:
            base_filter = (
                r
                .table(OperationCollections.Agent)
                .get_all(
                    self.view_name,
                    index=AgentOperationIndexes.ViewName
                )
            )

        return base_filter

    def _set_operation_per_agent_base_query(self):
        base_filter = (
            r
            .table(OperationCollections.OperationPerAgent)
        )
        if self.view_name:
            base_filter = (
                r
                .table(OperationCollections.OperationPerAgent)
                .get_all(
                    self.view_name,
                    index=OperationPerAgentIndexes.ViewName
                )
            )

        return base_filter

    def _set_agent_collection_pluck(self):
        pluck = (
            [
                AgentOperationKey.OperationId,
                AgentOperationKey.Operation,
                AgentOperationKey.OperationStatus,
                AgentOperationKey.CreatedTime,
                AgentOperationKey.CreatedBy,
                AgentOperationKey.CompletedTime,
                AgentOperationKey.AgentsTotalCount,
                AgentOperationKey.AgentsFailedCount,
                AgentOperationKey.AgentsCompletedCount,
                AgentOperationKey.AgentsCompletedWithErrorsCount,
                OperationPerAgentKey.PickedUpTime,
                OperationPerAgentKey.CompletedTime,
                OperationPerAgentKey.ExpiredTime,
                OperationPerAgentKey.AppsTotalCount,
                OperationPerAgentKey.AppsPendingCount,
                OperationPerAgentKey.AppsFailedCount,
                OperationPerAgentKey.AppsCompletedCount,
                OperationPerAgentKey.Errors,
                OperationPerAgentKey.Status,
                OperationPerAgentKey.AgentId,
                AgentKeys.ComputerName,
                AgentKeys.DisplayName,
            ]
        )
        return pluck

    def _set_app_collection_without(self):
        without = (
            [
                OperationPerAppKey.AgentId,
                OperationPerAppKey.ViewName,
                OperationPerAppKey.Id,
                OperationPerAppKey.OperationId,
            ]
        )
        return without
