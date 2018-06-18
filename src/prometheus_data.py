import sys
import time
import traceback
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.auth import HTTPBasicAuth
from src import logger_config

logger = logger_config.logger

def get_kube_node_labels_dict(promehtheus_info_dict, start_time, end_time):
    """
    Getting the kube_node_labels info
    """

    logger.debug("Running def get_kube_node_labels_dict")

    results = {}

    t0 = time.time()
    try:
        response = requests_retry_session().get('{0}/api/v1/query'.format(promehtheus_info_dict['base_url']),
                                 params={
                                    'query': 'kube_node_labels',
                                    'start': start_time,
                                    'end': end_time
                                    },
                                 auth=HTTPBasicAuth(promehtheus_info_dict['auth_user'], promehtheus_info_dict['auth_password'])
                                 )

        results = response.json()['data']['result']

        kube_node_labels_dict = {}

        print("XXXXXX")
        print("prometheus_data.get_kube_node_labels_dict()")
        print(results)

        if results == []:
            logger.error("No results from: get_kube_node_labels_dict")
            #sys.exit()

        # for row in results:
        #     for key, value in row['metric'].items():
        #         print(key)
        #         print(value)
    except Exception as x:
        logger.error("here")
        logger.error('It failed:', x.__class__.__name__)
        var = traceback.format_exc()
        logger.error(var)
        logger.error("Exiting...")
        sys.exit()
    # else:
    #     logger.info('Retry worked (status code): '+str(response.status_code))
    finally:
        t1 = time.time()
        total_time = t1 - t0
        logger.info("Query time: "+str(total_time))

    return results

def get_kube_pod_info_dict(promehtheus_info_dict, start_time, end_time):
    """
    Gettting the kube_pod_info info
    """

    results = {}

    t0 = time.time()
    try:
        response = requests_retry_session().get('{0}/api/v1/query'.format(promehtheus_info_dict['base_url']),
                                 params={
                                    'query': 'kube_pod_info',
                                    'start': start_time,
                                    'end': end_time
                                    },
                                 auth=HTTPBasicAuth(promehtheus_info_dict['auth_user'], promehtheus_info_dict['auth_password'])
                                 )

        results = response.json()['data']['result']

    # for row in results:
    #     print("namespace: "+row['metric']['exported_namespace'])
    #     print("node: "+row['metric']['node'])
    #     print("pod name: "+row['metric']['pod'])
    #     print("------------")
    except Exception as x:
        logger.error("here")
        logger.error('It failed:', x.__class__.__name__)
        var = traceback.format_exc()
        logger.error(var)
        logger.error("Exiting...")
        sys.exit()
    # else:
    #     logger.info('Retry worked (status code): '+str(response.status_code))
    finally:
        t1 = time.time()
        total_time = t1 - t0
        logger.info("Query time: "+str(total_time))

    return results

def get_kube_pod_container_resource_limits_cpu_cores_dict(promehtheus_info_dict, start_time, end_time):
    """
    Getting kube_pod_container_resource_limits_cpu_cores info
    """

    results = {}

    t0 = time.time()
    try:
        response = requests_retry_session().get('{0}/api/v1/query'.format(promehtheus_info_dict['base_url']),
                                 params={
                                    'query': 'kube_pod_container_resource_limits_cpu_cores',
                                    'start': start_time,
                                    'end': end_time
                                    },
                                 auth=HTTPBasicAuth(promehtheus_info_dict['auth_user'], promehtheus_info_dict['auth_password'])
                                 )

        results = response.json()['data']['result']

    except Exception as x:
        logger.error("here")
        logger.error('It failed:', x.__class__.__name__)
        var = traceback.format_exc()
        logger.error(var)
        logger.error("Exiting...")
        sys.exit()
    # else:
    #     logger.info('Retry worked (status code): '+str(response.status_code))
    finally:
        t1 = time.time()
        total_time = t1 - t0
        logger.info("Query time: "+str(total_time))

    return results

def get_kube_pod_container_resource_limits_memory_bytes_dict(promehtheus_info_dict, start_time, end_time):
    """
    Getting kube_pod_container_resource_limits_memory_bytes info
    """

    results = {}

    t0 = time.time()
    try:
        response = requests_retry_session().get('{0}/api/v1/query'.format(promehtheus_info_dict['base_url']),
                                 params={
                                    'query': 'kube_pod_container_resource_limits_memory_bytes',
                                    'start': start_time,
                                    'end': end_time
                                    },
                                 auth=HTTPBasicAuth(promehtheus_info_dict['auth_user'], promehtheus_info_dict['auth_password'])
                                 )

        results = response.json()['data']['result']

    except Exception as x:
        logger.error("here")
        logger.error('It failed:', x.__class__.__name__)
        print(results)
        var = traceback.format_exc()
        logger.error(var)
        logger.error("Exiting...")
        sys.exit()
    # else:
    #     logger.info('Retry worked (status code): '+str(response.status_code))
    finally:
        t1 = time.time()
        total_time = t1 - t0
        logger.info("Query time: "+str(total_time))

    return results

# https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry
def requests_retry_session(
    retries=40,
    backoff_factor=10,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
