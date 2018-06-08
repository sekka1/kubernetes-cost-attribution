import json
from src import logger_config

logger = logger_config.logger

#
# The last state files holds:
#   last_poll_time: unix_timestamp
#
# The last state file holds the last query end time
# To do the next cycle of query, 60 seconds should be added to it
#

def get(last_state_file_location):
    """
    Get the last_state.json file and return a dict
    """

    last_state_json = None
    last_state_dict = {}

    with open(last_state_file_location, 'r') as a_file:
        last_state_json=a_file.read()

        last_state_dict = json.loads(last_state_json)

        a_file.close()

    return last_state_dict

def get_next_end_cycle_time(last_poll_time):
    """
    This returns the next cycle time to poll to

    This would be set as the end time
    """

    return last_poll_time + 60

def set(last_state_file_location, end_poll_time):
    """
    Set the last_state.json file with the new time
    """

    output_dict = {'last_poll_time': end_poll_time}

    with open(last_state_file_location, 'w') as a_file:
        json.dump(output_dict, a_file)

        a_file.close()
