import src.calculate_cost
import unittest

class CalculateCost(unittest.TestCase):

    def test_calculate_cost_get_full_machine(self):
        '''Calculate the cost of the compute based on a full machine usage'''

        compute_cost_percentage_memory = 0.50
        compute_cost_percentage_cpu    = 0.50
        compute_cost_hour              = 0.0301

        markup                         = 0.20

        total_machine_memory           = 8075688000
        total_machine_cpu              = 2

        pod_usage_memory               = 8075688000
        pod_usage_cpu                  = 2

        cost_per_min = src.calculate_cost.get_cost_per_min(compute_cost_percentage_memory,
                                compute_cost_percentage_cpu,
                                compute_cost_hour,
                                markup,
                                total_machine_memory,
                                total_machine_cpu,
                                pod_usage_memory,
                                pod_usage_cpu
                                )

        self.assertEqual(cost_per_min['total'], 0.000602)
        self.assertEqual(cost_per_min['memory'], 0.000301)
        self.assertEqual(cost_per_min['cpu'], 0.000301)

    def test_calculate_cost_get_one(self):
        '''Calculate the cost of the compute based less than a full machine usage'''

        compute_cost_percentage_memory = 0.50
        compute_cost_percentage_cpu    = 0.50
        compute_cost_hour              = 0.0301

        markup                         = 0.20

        total_machine_memory           = 8075688000
        total_machine_cpu              = 2

        pod_usage_memory               = 262144000
        pod_usage_cpu                  = 0.1

        cost_per_min = src.calculate_cost.get_cost_per_min(compute_cost_percentage_memory,
                                compute_cost_percentage_cpu,
                                compute_cost_hour,
                                markup,
                                total_machine_memory,
                                total_machine_cpu,
                                pod_usage_memory,
                                pod_usage_cpu
                                )

        self.assertEqual(cost_per_min['total'], 0.0000248207271504297834869255667822329769478528760373592376708984375)
        self.assertEqual(cost_per_min['memory'], 0.000009770727150429781891565438056712622483246377669274806976318359375)
        self.assertEqual(cost_per_min['cpu'], 0.000015050000000000001595360128725520354464606498368084430694580078125)

    def test_calculate_cost_get_two(self):
        '''Calculate the cost of the compute with 100% cpu and 0% memory'''

        compute_cost_percentage_memory = 0.50
        compute_cost_percentage_cpu    = 0.50
        compute_cost_hour              = 0.0301

        markup                         = 0.20

        total_machine_memory           = 8075688000
        total_machine_cpu              = 2

        pod_usage_memory               = 0
        pod_usage_cpu                  = 2

        cost_per_min = src.calculate_cost.get_cost_per_min(compute_cost_percentage_memory,
                                compute_cost_percentage_cpu,
                                compute_cost_hour,
                                markup,
                                total_machine_memory,
                                total_machine_cpu,
                                pod_usage_memory,
                                pod_usage_cpu
                                )

        self.assertEqual(cost_per_min['total'], 0.0003009999999999999980258846843383935265592299401760101318359375)
        self.assertEqual(cost_per_min['memory'], 0)
        self.assertEqual(cost_per_min['cpu'], 0.0003009999999999999980258846843383935265592299401760101318359375)

    def test_calculate_cost_get_three(self):
        '''Calculate the cost of the compute with 0% cpu and 100% memory'''

        compute_cost_percentage_memory = 0.50
        compute_cost_percentage_cpu    = 0.50
        compute_cost_hour              = 0.0301

        markup                         = 0.20

        total_machine_memory           = 8075688000
        total_machine_cpu              = 2

        pod_usage_memory               = 8075688000
        pod_usage_cpu                  = 0

        cost_per_min = src.calculate_cost.get_cost_per_min(compute_cost_percentage_memory,
                                compute_cost_percentage_cpu,
                                compute_cost_hour,
                                markup,
                                total_machine_memory,
                                total_machine_cpu,
                                pod_usage_memory,
                                pod_usage_cpu
                                )

        self.assertEqual(cost_per_min['total'], 0.0003009999999999999980258846843383935265592299401760101318359375)
        self.assertEqual(cost_per_min['memory'], 0.0003009999999999999980258846843383935265592299401760101318359375)
        self.assertEqual(cost_per_min['cpu'], 0)

if __name__ == '__main__':
    unittest.main()
