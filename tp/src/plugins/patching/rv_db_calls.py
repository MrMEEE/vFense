import logging
import logging.config
from vFense.db.client import db_create_close, r
from vFense.plugins.patching import *
from vFense.plugins.patching._constants import CommonAppKeys
from vFense.plugins.mightymouse import *

from vFense.errorz.error_messages import GenericResults
from vFense.core.agent import *
from vFense.operations._constants import AgentOperations
from vFense.core.tag.tagManager import *
from vFense.core.customer import *


logging.config.fileConfig('/opt/TopPatch/conf/logging.config')
logger = logging.getLogger('rvapi')


@db_create_close
def get_all_app_stats_by_tagid(username, customer_name,
                               uri, method, tag_id, conn=None):
    data = []
    try:
        inventory = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.INSTALLED,
                    x[AppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.AppsPerAgent),
                index=AppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: inventory,
                CommonAppKeys.STATUS: CommonAppKeys.INSTALLED,
                CommonAppKeys.NAME: CommonAppKeys.SOFTWAREINVENTORY
            }
        )
        os_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[AppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.AppsPerAgent),
                index=AppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: os_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.OS
            }
        )
        custom_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[CustomAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.CustomAppsPerAgent),
                index=CustomAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: custom_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.CUSTOM
            }
        )
        supported_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[SupportedAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.SupportedAppsPerAgent),
                index=SupportedAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: supported_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.SUPPORTED
            }
        )
        agent_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[AgentAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.vFenseAppsPerAgent),
                index=AgentAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: agent_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.AGENT_UPDATES
            }
        )

       # all_pending_apps = (
       #    r
       #    .table(TagsPerAgentCollection, use_outdated=True)
       #    .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
       #    .pluck(TagsPerAgentKey.AgentId)
       #    .eq_join(
       #        lambda x: [
       #            PENDING,
       #            x[AppsPerAgentKey.AgentId]
       #        ],
       #        r.table(AppCollections.AppsPerAgent),
       #        index=AppsPerAgentIndexes.StatusAndAgentId
       #    )
       #    .pluck({'right': AppsPerAgentKey.AppId})
       #    .distinct()
       #    .count()
       #    .run(conn)
       #)

       #data.append(
       #    {
       #        CommonAppKeys.COUNT: all_pending_apps,
       #        CommonAppKeys.STATUS: CommonAppKeys.PENDING,
       #        CommonAppKeys.NAME: CommonAppKeys.PENDING.capitalize()
       #    }
       #)

        results = (
            GenericResults(
                username, uri, method
            ).information_retrieved(data, len(data))
        )

        logger.info(results)

    except Exception as e:
        results = (
            GenericResults(
                username, uri, method
            ).something_broke('getting_pkg_stats', 'updates', e)
        )
        logger.exception(results)

    return(results)


@db_create_close
def get_all_avail_stats_by_tagid(username, customer_name,
                                 uri, method, tag_id, conn=None):
    data = []
    try:
        os_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[AppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.AppsPerAgent),
                index=AppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: os_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.OS
            }
        )
        custom_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[CustomAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.CustomAppsPerAgent),
                index=CustomAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: custom_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.CUSTOM
            }
        )
        supported_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[SupportedAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.SupportedAppsPerAgent),
                index=SupportedAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: supported_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.SUPPORTED
            }
        )
        agent_apps_avail = (
            r
            .table(TagsPerAgentCollection, use_outdated=True)
            .get_all(tag_id, index=TagsPerAgentIndexes.TagId)
            .pluck(TagsPerAgentKey.AgentId)
            .eq_join(
                lambda x: [
                    CommonAppKeys.AVAILABLE,
                    x[AgentAppsPerAgentKey.AgentId]
                ],
                r.table(AppCollections.vFenseAppsPerAgent),
                index=AgentAppsPerAgentIndexes.StatusAndAgentId
            )
            .pluck({'right': AppsPerAgentKey.AppId})
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: agent_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.AGENT_UPDATES
            }
        )

        results = (
            GenericResults(
                username, uri, method
            ).information_retrieved(data, len(data))
        )

        logger.info(results)

    except Exception as e:
        results = (
            GenericResults(
                username, uri, method
            ).something_broke('getting_pkg_stats', 'updates', e)
        )
        logger.exception(results)

    return(results)


@db_create_close
def get_all_app_stats_by_customer(username, customer_name,
                                  uri, method, conn=None):
    data = []
    try:
        os_apps_avail = (
            r
            .table(AppCollections.AppsPerAgent, use_outdated=True)
            .get_all(
                [
                    CommonAppKeys.AVAILABLE, customer_name
                ],
                index=AppsPerAgentIndexes.StatusAndCustomer
            )
            .pluck(AppsPerAgentKey.AppId)
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: os_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.OS
            }
        )
        custom_apps_avail = (
            r
            .table(AppCollections.CustomAppsPerAgent, use_outdated=True)
            .get_all(
                [
                    CommonAppKeys.AVAILABLE, customer_name
                ],
                index=CustomAppsPerAgentIndexes.StatusAndCustomer
            )
            .pluck(CustomAppsPerAgentKey.AppId)
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: custom_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.CUSTOM
            }
        )
        supported_apps_avail = (
            r
            .table(AppCollections.SupportedAppsPerAgent, use_outdated=True)
            .get_all(
                [
                    CommonAppKeys.AVAILABLE, customer_name
                ],
                index=SupportedAppsPerAgentIndexes.StatusAndCustomer
            )
            .pluck(SupportedAppsPerAgentKey.AppId)
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: supported_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.SUPPORTED
            }
        )
        agent_apps_avail = (
            r
            .table(AppCollections.vFenseAppsPerAgent, use_outdated=True)
            .get_all(
                [
                    CommonAppKeys.AVAILABLE, customer_name
                ],
                index=AgentAppsPerAgentIndexes.StatusAndCustomer
            )
            .pluck(AgentAppsPerAgentKey.AppId)
            .distinct()
            .count()
            .run(conn)
        )
        data.append(
            {
                CommonAppKeys.COUNT: agent_apps_avail,
                CommonAppKeys.STATUS: CommonAppKeys.AVAILABLE,
                CommonAppKeys.NAME: CommonAppKeys.AGENT_UPDATES
            }
        )

        all_pending_apps = (
            r
            .table(AppCollections.AppsPerAgent, use_outdated=True)
            .get_all(
                [
                    CommonAppKeys.PENDING, customer_name
                ],
                index=AppsPerAgentIndexes.StatusAndCustomer
            )
            .pluck((CommonAppKeys.APP_ID))
            .distinct()
            .count()
            .run(conn)
        )

        data.append(
            {
                CommonAppKeys.COUNT: all_pending_apps,
                CommonAppKeys.STATUS: CommonAppKeys.PENDING,
                CommonAppKeys.NAME: CommonAppKeys.PENDING.capitalize()
            }
        )

        results = (
            GenericResults(
                username, uri, method
            ).information_retrieved(data, len(data))
        )

        logger.info(results)

    except Exception as e:
        results = (
            GenericResults(
                username, uri, method
            ).something_broke('getting_pkg_stats', 'updates', e)
        )
        logger.exception(results)

    return(results)


@db_create_close
def delete_app_from_rv(
        app_id,
        collection=AppCollections.UniqueApplications,
        per_agent_collection=AppCollections.AppsPerAgent,
        conn=None
        ):
    completed = True
    try:
        (
            r
            .table(collection)
            .filter({AppsKey.AppId: app_id})
            .delete()
            .run(conn)
        )
        (
            r
            .table(per_agent_collection)
            .filter({AppsKey.AppId: app_id})
            .delete()
            .run(conn)
        )
        if collection == AppCollections.CustomApps:
            (
                r
                .table(FileCollections.Files)
                .filter(lambda x: x[FilesKey.AppIds].contains(app_id))
                .delete()
                .run(conn)
            )

    except Exception as e:
        logger.exception(e)
        completed = False

    return(completed)


def update_app_status(agent_id, app_id, oper_type, data):
    if oper_type == AgentOperations.INSTALL_OS_APPS or oper_type == UNINSTALL:
        update_os_app_per_agent(agent_id, app_id, data)

    elif oper_type == AgentOperations.INSTALL_CUSTOM_APPS:
        update_custom_app_per_agent(agent_id, app_id, data)

    elif oper_type == AgentOperations.INSTALL_SUPPORTED_APPS:
        update_supported_app_per_agent(agent_id, app_id, data)

    elif oper_type == AgentOperations.INSTALL_AGENT_UPDATE:
        update_agent_app_per_agent(agent_id, app_id, data)

