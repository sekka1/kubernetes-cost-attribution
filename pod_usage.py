import sys
import time
import traceback
from time import sleep
from src import billing
from src import logger_config
from prometheus_client import start_http_server, Counter
import schedule

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
start_minus_seconds = int(sys.argv[7])

# Prometheus - Start up the server to expose the metrics.
start_http_server(9101)
prometheus_counter = Counter('kubernetes_cost_attribution', 'namespace cost', ['namespace_name', 'duration'])

def job():
    billing.run(promehtheus_info_dict, cycles_to_run, start_minus_seconds, billing_csv_output_file, last_state_file_location, prometheus_counter)

schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
