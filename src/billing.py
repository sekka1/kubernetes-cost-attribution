import random
import time
from src import logger_config
from src import last_state
from src import process_bill_cycle
from src import output_csv
import json
import sys
import time
import traceback
from time import sleep

logger = logger_config.logger

def run(promehtheus_info_dict, cycles_to_run, billing_csv_output_file, last_state_file_location, prometheus_counter):
    #####################################
    # Billing cycle
    #####################################
    cycle_count = 0
    t0 = time.time()

    while cycle_count < cycles_to_run:

        start_time = time.time() - 3600 # start running from an hour ago
        end_time = last_state.get_next_end_cycle_time(start_time)

        logger.info("###########################################")
        logger.info("###########################################")
        logger.info("---Starting billing cycle---")
        logger.info("###########################################")
        logger.info("###########################################")

        logger.info("Current start poll cycle time: "+str(start_time))
        logger.info("Next end poll cycle time: "+str(end_time))

        try:
            # Process this current billing cycle
            current_billing_cycle_list = process_bill_cycle.process(promehtheus_info_dict, start_time, end_time)

            output_csv.output(billing_csv_output_file, current_billing_cycle_list)
        except Exception as e:
            var = traceback.format_exc()
            logger.error(var)
            logger.error("Exiting...")
            sys.exit()


        logger.info("###########################################")
        logger.info("###########################################")
        logger.info("---Ending billing cycle---")
        logger.info("###########################################")
        logger.info("###########################################")

        cycle_count += 1

        logger.info("Sleeping for 60 seconds...")
        sleep(0.2)

    # Tracking how long this run took
    t1 = time.time()
    total_time = t1 - t0

    logger.info("Total run time (sec): "+str(total_time))
    logger.info("Total run time (min): "+str(total_time/60))
    logger.info("Total run time (hour): "+str(total_time/60/60))

    ################################
    # Summarize
    ################################

    input_csv_billing_file = billing_csv_output_file

    logger.info("Starting billing pod_usage")
    logger.warning("Starting billing pod_usage")
    logger.debug("Starting billing pod_usage")

    # Read in billing csv file
    csv_output = output_csv.read(input_csv_billing_file)

    namespace_sums_dict = {}

    # Loop through it to sum up each namespace pod costs
    for row in csv_output:
        #print(row['namespace'], row['pod'])
        if row['namespace'] in namespace_sums_dict:
            logger.debug("Is in namespace_sums_dict: "+row['namespace'])
            logger.debug("Adding into the total")

            namespace_sums_dict[row['namespace']]['total'] += float(row['cost_per_min_total'])
        else:
            logger.info("Is not namespace_sums_dict: "+row['namespace'])
            logger.debug("Adding namespace into namespace_sums_dict")

            namespace_sums_dict[row['namespace']] = {
                'total': float(row['cost_per_min_total'])
            }

    ##############################################
    # Prometheus - Output namespace's cost metrics
    ##############################################
    for namespace in namespace_sums_dict:
        print(namespace_sums_dict[namespace])
        print(namespace_sums_dict[namespace]['total'])
        prometheus_counter.labels(duration='day', namespace=namespace).inc(namespace_sums_dict[namespace]['total'])
