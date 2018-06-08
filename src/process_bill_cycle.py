from src import logger_config
from src import prometheus_data
from src import find
from src import cost_assumptions
from src import calculate_cost

logger = logger_config.logger

def process(promehtheus_info_dict, start_time, end_time):
    """
    Process the billing cycle for this minute

    Returns a list including all of the detailed billing info for this cycle
    """

    # Dict holding the current billing cycles information
    current_billing_cycle_list = []

    # Dict holding the current period's billing information
    kube_pod_info_dict = {}
    kube_node_labels_dict = {}
    kube_pod_container_resource_limits_cpu_cores_dict = {}
    kube_pod_container_resource_limits_memory_bytes_dict = {}

    # Getting the values
    kube_pod_info_dict = prometheus_data.get_kube_pod_info_dict(promehtheus_info_dict, start_time, end_time)
    kube_node_labels_dict = prometheus_data.get_kube_node_labels_dict(promehtheus_info_dict, start_time, end_time)
    kube_pod_container_resource_limits_cpu_cores_dict = prometheus_data.get_kube_pod_container_resource_limits_cpu_cores_dict(promehtheus_info_dict, start_time, end_time)
    kube_pod_container_resource_limits_memory_bytes_dict = prometheus_data.get_kube_pod_container_resource_limits_memory_bytes_dict(promehtheus_info_dict, start_time, end_time)

    # Get cost assumption file(s)
    cost_assumptions_dict = cost_assumptions.get()
    #print(cost_assumptions_dict)

    #
    # Loop through the list of pods and calculate how much each pod cost per min
    #
    # Everytime we touch anything in this loop we have to verify the numbers match up to
    # what is calculated in the purple top right section of this spread sheet:
    # https://docs.google.com/spreadsheets/d/1r05JBmegiQ9LiFy9nHixmd2PdFSKp6Bi_a6O-xfRcRw/edit#gid=0
    #
    for pod_row in kube_pod_info_dict:

        exported_namespace = pod_row['metric']['exported_namespace']
        node = pod_row['metric']['node']
        pod = pod_row['metric']['pod']

        # if (exported_namespace != 'kube-system' and
        #     exported_namespace != 'devops' and
        #     exported_namespace != 'infrastructure'):
        if (exported_namespace != 'kube-system'):

            logger.info("exported_namespace - "+exported_namespace)
            logger.info("node - "+node)
            logger.info("pod - "+pod)

            # Get cpu core limit
            cpu_core_limit = find.pods_resource_limits_cpu_cores(kube_pod_container_resource_limits_cpu_cores_dict,
                                                                exported_namespace,
                                                                node,
                                                                pod)

            # Get memory limit bytes
            memory_bytes_limit = find.pods_resource_limits_memory_bytes(kube_pod_container_resource_limits_memory_bytes_dict,
                                                               exported_namespace,
                                                               node,
                                                               pod)

            # Get machine info dict
            machine_info_dict = find.machine_info_by_hostname(kube_node_labels_dict, node)

            machine_spot_or_on_demand = None
            if machine_info_dict['isSpot'] == "true":
                machine_spot_or_on_demand = 'spot'
            else:
                machine_spot_or_on_demand = 'on_demand'

            logger.info("cpu core limit: "+str(cpu_core_limit))
            logger.info("memory bytes limit: "+str(memory_bytes_limit))

            logger.info("machine_spot_or_on_demand: "+machine_spot_or_on_demand)
            logger.info("machine type: "+machine_info_dict['instance_type'])
            logger.info("machine hourly cost: "+str(cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['hourly_cost'][machine_spot_or_on_demand]))

            logger.info("cost_assumptions_dict memory_percentage: "+str(cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['memory_percentage']))
            logger.info("cost_assumptions_dict cpu percentage: "+str(cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['cpu_percentage']))

            logger.info("machine mark up: "+str(cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['markup']))
            logger.info("ec2 Machine total memory: "+str(cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['memory']))
            logger.info("ec2 Machine total cpu: "+str(cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['cpu']))

            current_pod_info = {
                'namespace': exported_namespace,
                'start_time': start_time,
                'end_time': end_time,
                'node': node,
                'pod': pod,
                'memory_bytes_limit': memory_bytes_limit,
                'cpu_core_limit': cpu_core_limit,
                'machine_spot_or_on_demand': machine_spot_or_on_demand,
                'instance_type': machine_info_dict['instance_type'],
                'instance_hourly_cost': cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['hourly_cost'][machine_spot_or_on_demand],
                'cost_assumptions_memory_percentage': cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['memory_percentage'],
                'cost_assumptions_cpu_percentage': cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['cpu_percentage'],
                'instance_markup': cost_assumptions_dict['namespaces'][exported_namespace][machine_info_dict['instance_type']]['markup'],
                'instance_total_memory': cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['memory'],
                'instance_total_cpu': cost_assumptions_dict['ec2_info'][machine_info_dict['instance_type']]['cpu']
            }

            cost_per_min_dict = calculate_cost.get_cost_per_min(
                                    current_pod_info['cost_assumptions_memory_percentage'],
                                    current_pod_info['cost_assumptions_cpu_percentage'],
                                    current_pod_info['instance_hourly_cost'],
                                    current_pod_info['instance_markup'],
                                    current_pod_info['instance_total_memory'],
                                    current_pod_info['instance_total_cpu'],
                                    current_pod_info['memory_bytes_limit'],
                                    current_pod_info['cpu_core_limit']
                                    )

            logger.info("cost_per_min_dict - total: "+str(cost_per_min_dict['total']))
            logger.info("cost_per_min_dict - memory: "+str(cost_per_min_dict['memory']))
            logger.info("cost_per_min_dict - cpu: "+str(cost_per_min_dict['cpu']))

            # Adding the calculated cost into the dict
            current_pod_info['cost_per_min_total'] = cost_per_min_dict['total']
            current_pod_info['cost_per_min_memory'] = cost_per_min_dict['memory']
            current_pod_info['cost_per_min_cpu'] = cost_per_min_dict['cpu']

            current_billing_cycle_list.append(current_pod_info)

            logger.info(current_pod_info)

            logger.info("###################################################################")

    return current_billing_cycle_list
