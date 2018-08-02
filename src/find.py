from src import logger_config

logger = logger_config.logger

def pods_resource_limits_cpu_cores(kube_pod_container_resource_limits_cpu_cores_dict,
                                    exported_namespace,
                                    node,
                                    pod):
    """
    Finds the pods resource_limits_cpu_cores for a pod
    """

    cpu_core_limit = 1.0000112233

    for row in kube_pod_container_resource_limits_cpu_cores_dict:

        # Check if the fields are in the dict before proceeding
        if 'node' in row['metric'] and 'exported_namespace' in row['metric'] and 'pod' in row['metric']:

            if ((row['metric']['exported_namespace'] == exported_namespace) and
                (row['metric']['node'] == node) and
                (row['metric']['pod'] == pod)):

                cpu_core_limit = float(row['value'][1])
                break

    if cpu_core_limit == 1.0000112233:
        logger.error("Did not find a cpu limit for (setting default value to 1.0000112233) - exported_namespace: "+exported_namespace+", pod: "+pod)

    return cpu_core_limit

def pods_resource_limits_memory_bytes(kube_pod_container_resource_limits_memory_bytes_dict,
                                    exported_namespace,
                                    node,
                                    pod):
    """
    Finds the pods kube_pod_container_resource_limits_memory_bytes for a pod
    """

    memory_bytes_limit = 1.0000445566

    for row in kube_pod_container_resource_limits_memory_bytes_dict:

        # Check if the fields are in the dict before proceeding
        if 'node' in row['metric'] and 'exported_namespace' in row['metric'] and 'pod' in row['metric']:

            if ((row['metric']['exported_namespace'] == exported_namespace) and
                (row['metric']['node'] == node) and
                (row['metric']['pod'] == pod)):

                memory_bytes_limit = int(row['value'][1])
                break

    if memory_bytes_limit == 1.0000445566:
        logger.error("Did not find a memory limit for (setting default value to 1.0000445566) - exported_namespace: "+exported_namespace+", pod: "+pod)

    return memory_bytes_limit

def machine_info_by_hostname(kube_node_labels_dict, hostname):
    """
    get a machine info dict via the fqdn
    """

    machine_info_dict = None

    for row in kube_node_labels_dict:
        if row['metric']['label_kubernetes_io_hostname'] == hostname.replace(".ec2.internal", "") or row['metric']['label_kubernetes_io_hostname'] == hostname:
            print(row)
            machine_info_dict = {}
            machine_info_dict['arch'] = row['metric']['label_beta_kubernetes_io_arch']
            machine_info_dict['instance_type'] = row['metric']['label_k8s_info_instanceType']
            machine_info_dict['os'] = row['metric']['label_beta_kubernetes_io_os']
            machine_info_dict['region'] = row['metric']['label_failure_domain_beta_kubernetes_io_region']
            machine_info_dict['availability_zone'] = row['metric']['label_failure_domain_beta_kubernetes_io_zone']
            machine_info_dict['hasPublicIP'] = row['metric']['label_k8s_info_hasPublicIP']
            machine_info_dict['isSpot'] = row['metric']['label_k8s_info_isSpot']
            machine_info_dict['kops_instancegroup'] = row['metric']['label_kops_k8s_io_instancegroup']

    return machine_info_dict
