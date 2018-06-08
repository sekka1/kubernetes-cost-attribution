import json
from src import logger_config

logger = logger_config.logger

def get():
    """
    Get the cost assumptions dict
    """

    cost_assumptions_json = None
    cost_assumptions_dict = {}

    with open('./cost_assumptions/compute_cost.json', 'r') as a_file:
        cost_assumptions_json=a_file.read()

        cost_assumptions_dict = json.loads(cost_assumptions_json)

        a_file.close()

    return cost_assumptions_dict
