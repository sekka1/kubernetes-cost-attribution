import sys
import time
import traceback
from src import logger_config
from src import last_state
from src import process_bill_cycle
from src import output_csv
from time import sleep

logger = logger_config.logger

logger.info("Starting billing pod_usage")
logger.warning("Starting billing pod_usage")
logger.debug("Starting billing pod_usage")

if len(sys.argv) == 6:
    sys.exit(1, 'Requires 6 input arguments')

promehtheus_info_dict = {
    "base_url": sys.argv[1],
    "auth_user": sys.argv[2],
    "auth_password": sys.argv[3]
}
billing_csv_output_file = sys.argv[4]
last_state_file_location = sys.argv[5]
cycles_to_run = int(sys.argv[6])

#####################################
# Billing cycle
#####################################

cycle_count = 0
t0 = time.time()

while cycle_count < cycles_to_run:
    # Get last_state.json
    last_state_dict = last_state.get(last_state_file_location)

    start_time = last_state_dict['last_poll_time']
    end_time = last_state.get_next_end_cycle_time(last_state_dict['last_poll_time'])

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


    # Setting the new value for the last_state.json file
    last_state.set(last_state_file_location, end_time)

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
