import sys
import time
import traceback
from time import sleep
from src import billing
from src import logger_config
from prometheus_client import start_http_server, Gauge, Counter
import schedule
import rook

rook.start(token='babfa4263f8d4041e74885b4c340f3e30377378752f50dfcfd5b48e61fd39ff2')

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
start_minutes_ago = int(sys.argv[6])

# Prometheus - Start up the server to expose the metrics.
start_http_server(9101)
prometheus_counter = Gauge('kubernetes_cost_attribution', 'namespace cost', ['namespace_name', 'duration'])

def job():
    billing.run(promehtheus_info_dict, start_minutes_ago, billing_csv_output_file, last_state_file_location, prometheus_counter)

schedule.every(start_minutes_ago).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
