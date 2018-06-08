import sys
import traceback
import json
from src import logger_config
from src import output_csv

logger = logger_config.logger

if len(sys.argv) == 1:
    sys.exit(1, 'Requires 1 input arguments')

# Params:
input_csv_billing_file = sys.argv[1]

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

# Output in a json format
namespace_sums_json = json.dumps(namespace_sums_dict)
print(namespace_sums_json)
