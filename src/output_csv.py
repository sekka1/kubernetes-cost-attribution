import csv
from src import logger_config

logger = logger_config.logger

def output(billing_csv_output_file, output_list):
    """
    takes in a list and outputs each dict row to a csv file

    When updating the fieldnames, the read() fieldnames needs
    to be updated as wll.
    """

    with open(billing_csv_output_file, 'a') as csvfile:
        fieldnames = ['namespace',
                        'start_time',
                        'end_time',
                        'node',
                        'pod',
                        'memory_bytes_limit',
                        'cpu_core_limit',
                        'machine_spot_or_on_demand',
                        'instance_type',
                        'instance_hourly_cost',
                        'cost_assumptions_memory_percentage',
                        'cost_assumptions_cpu_percentage',
                        'instance_markup',
                        'instance_total_memory',
                        'instance_total_cpu',
                        'cost_per_min_total',
                        'cost_per_min_memory',
                        'cost_per_min_cpu'
                        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader()

        for a_row in output_list:
            writer.writerow(a_row)

def read(billing_csv_file):
    """
    reads a billing_csv output file and returns a list

    https://docs.python.org/2/library/csv.html
    """

    return_list = []

    with open(billing_csv_file) as csvfile:
        fieldnames = ['namespace',
                        'start_time',
                        'end_time',
                        'node',
                        'pod',
                        'memory_bytes_limit',
                        'cpu_core_limit',
                        'machine_spot_or_on_demand',
                        'instance_type',
                        'instance_hourly_cost',
                        'cost_assumptions_memory_percentage',
                        'cost_assumptions_cpu_percentage',
                        'instance_markup',
                        'instance_total_memory',
                        'instance_total_cpu',
                        'cost_per_min_total',
                        'cost_per_min_memory',
                        'cost_per_min_cpu'
                        ]

        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        # Put all of the items into the return list
        # the csvfile will close once it is out of this with block
        for row in reader:
            #print(row['namespace'], row['pod'])
            return_list.append(row)

        return return_list
