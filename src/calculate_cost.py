from decimal import *
from src import logger_config

logger = logger_config.logger

def get_cost_per_min(compute_cost_percentage_memory,
                        compute_cost_percentage_cpu,
                        compute_cost_hour,
                        markup,
                        total_machine_memory,
                        total_machine_cpu,
                        pod_usage_memory,
                        pod_usage_cpu):
    """
    Calculate the cost per min
    """

    logger.debug("---Starting get_cost_per_min calculation---")

    logger.debug("Pod usage memory: "+str(pod_usage_memory))
    logger.debug("Pod usage cpu: "+str(pod_usage_cpu))

    compute_cost_per_hour_memory = compute_cost_percentage_memory * compute_cost_hour
    compute_cost_per_hour_cpu    = compute_cost_percentage_cpu * compute_cost_hour

    logger.debug("compute_cost_per_hour_memory: "+str(compute_cost_per_hour_memory))
    logger.debug("compute_cost_per_hour_cpu:"+str(compute_cost_per_hour_cpu))

    percent_used_memory = pod_usage_memory / total_machine_memory
    percent_used_cpu    = pod_usage_cpu / total_machine_cpu

    calculated_cost_per_hour_memory = compute_cost_per_hour_memory * percent_used_memory
    calculated_cost_per_hour_cpu    = compute_cost_per_hour_cpu * percent_used_cpu

    logger.debug("calculated_cost_per_hour_memory: "+str(calculated_cost_per_hour_memory))
    logger.debug("calculated_cost_per_hour_cpu: "+str(calculated_cost_per_hour_cpu))

    total_per_hour_with_markup_memory = calculated_cost_per_hour_memory * markup + calculated_cost_per_hour_memory
    total_per_hour_with_markup_cpu    = calculated_cost_per_hour_cpu * markup + calculated_cost_per_hour_cpu

    logger.debug("total_per_hour_with_markup_memory: "+str(total_per_hour_with_markup_memory))
    logger.debug("total_per_hour_with_markup_cpu: "+str(total_per_hour_with_markup_cpu))

    total_per_min_with_markup_memory = total_per_hour_with_markup_memory / 60
    total_per_min_with_markup_cpu    = total_per_hour_with_markup_cpu / 60

    logger.debug("total_per_min_with_markup_memory: "+str(total_per_min_with_markup_memory))
    logger.debug("total_per_min_with_markup_cpu: "+str(total_per_min_with_markup_cpu))

    getcontext()
    getcontext().prec = 7

    final_return_dict = {
        'total': Decimal(total_per_min_with_markup_memory + total_per_min_with_markup_cpu),
        'memory': Decimal(total_per_min_with_markup_memory),
        'cpu': Decimal(total_per_min_with_markup_cpu)
    }

    logger.debug("Cost calculation - final total: "+str(final_return_dict['total']))
    logger.debug("Cost calculation - final memory: "+str(final_return_dict['memory']))
    logger.debug("Cost calculation - final cpu: "+str(final_return_dict['cpu']))

    #print(final_return_dict)
    logger.debug("---Ending get_cost_per_min calculation---")

    return final_return_dict
