import src.find
import unittest

class FindMachineInfoByHostname(unittest.TestCase):

    # A sample kube_pod_container_resource_limits_memory_dict
    kube_node_labels_dict = [{'metric': {'__name__': 'kube_node_labels', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'label_beta_kubernetes_io_arch': 'amd64', 'label_beta_kubernetes_io_instance_type': 'm4.large', 'label_beta_kubernetes_io_os': 'linux', 'label_failure_domain_beta_kubernetes_io_region': 'us-east-1', 'label_failure_domain_beta_kubernetes_io_zone': 'us-east-1b', 'label_k8s_info_hasPublicIP': 'false', 'label_k8s_info_instanceType': 'm4.large', 'label_k8s_info_isSpot': 'true', 'label_kops_k8s_io_instancegroup': 'spot-zone-b', 'label_kubernetes_io_hostname': 'ip-10-151-22-101.ec2.internal', 'label_kubernetes_io_role': 'node', 'label_node_role_kubernetes_io_node': '', 'label_prod_1_k8s_devops_bot_role': 'scale-zero', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal'}, 'value': [1516054280.862, '1']}, {'metric': {'__name__': 'kube_node_labels', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'label_beta_kubernetes_io_arch': 'amd64', 'label_beta_kubernetes_io_instance_type': 'm4.large', 'label_beta_kubernetes_io_os': 'linux', 'label_failure_domain_beta_kubernetes_io_region': 'us-east-1', 'label_failure_domain_beta_kubernetes_io_zone': 'us-east-1b', 'label_k8s_info_hasPublicIP': 'false', 'label_k8s_info_instanceType': 'm4.large', 'label_k8s_info_isSpot': 'true', 'label_kops_k8s_io_instancegroup': 'spot-zone-b', 'label_kubernetes_io_hostname': 'ip-10-151-22-218.ec2.internal', 'label_kubernetes_io_role': 'node', 'label_node_role_kubernetes_io_node': '', 'label_prod_1_k8s_devops_bot_role': 'scale-zero', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal'}, 'value': [1516054280.862, '1']}, {'metric': {'__name__': 'kube_node_labels', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'label_beta_kubernetes_io_arch': 'amd64', 'label_beta_kubernetes_io_instance_type': 't2.medium', 'label_beta_kubernetes_io_os': 'linux', 'label_failure_domain_beta_kubernetes_io_region': 'us-east-1', 'label_failure_domain_beta_kubernetes_io_zone': 'us-east-1a', 'label_kops_k8s_io_instancegroup': 'master-us-east-1a', 'label_kubernetes_io_hostname': 'ip-10-151-15-60.ec2.internal', 'label_kubernetes_io_role': 'master', 'label_node_role_kubernetes_io_master': '', 'namespace': 'devops', 'node': 'ip-10-151-15-60.ec2.internal'}, 'value': [1516054280.862, '1']}, {'metric': {'__name__': 'kube_node_labels', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'label_beta_kubernetes_io_arch': 'amd64', 'label_beta_kubernetes_io_instance_type': 't2.medium', 'label_beta_kubernetes_io_os': 'linux', 'label_failure_domain_beta_kubernetes_io_region': 'us-east-1', 'label_failure_domain_beta_kubernetes_io_zone': 'us-east-1b', 'label_kops_k8s_io_instancegroup': 'master-us-east-1b', 'label_kubernetes_io_hostname': 'ip-10-151-16-146.ec2.internal', 'label_kubernetes_io_role': 'master', 'label_node_role_kubernetes_io_master': '', 'namespace': 'devops', 'node': 'ip-10-151-16-146.ec2.internal'}, 'value': [1516054280.862, '1']}, {'metric': {'__name__': 'kube_node_labels', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'label_beta_kubernetes_io_arch': 'amd64', 'label_beta_kubernetes_io_instance_type': 't2.medium', 'label_beta_kubernetes_io_os': 'linux', 'label_failure_domain_beta_kubernetes_io_region': 'us-east-1', 'label_failure_domain_beta_kubernetes_io_zone': 'us-east-1c', 'label_kops_k8s_io_instancegroup': 'master-us-east-1c', 'label_kubernetes_io_hostname': 'ip-10-151-17-110.ec2.internal', 'label_kubernetes_io_role': 'master', 'label_node_role_kubernetes_io_master': '', 'namespace': 'devops', 'node': 'ip-10-151-17-110.ec2.internal'}, 'value': [1516054280.862, '1']}]


    def test_find_machine_info_by_hostname(self):
        '''Finds and get the machine info dict by a hostname'''

        hostname = 'ip-10-151-22-218.ec2.internal'

        machine_info_dict = src.find.machine_info_by_hostname(self.kube_node_labels_dict, hostname)

        self.assertEqual(machine_info_dict['arch'], "amd64")
        self.assertEqual(machine_info_dict['instance_type'], "m4.large")
        self.assertEqual(machine_info_dict['os'], "linux")
        self.assertEqual(machine_info_dict['region'], "us-east-1")
        self.assertEqual(machine_info_dict['availability_zone'], "us-east-1b")
        self.assertEqual(machine_info_dict['hasPublicIP'], "false")
        self.assertEqual(machine_info_dict['isSpot'], "true")
        self.assertEqual(machine_info_dict['kops_instancegroup'], "spot-zone-b")


    def test_find_machine_info_by_hostname_no_host(self):
        '''Finds and get the machine info dict by a hostname that does not exist'''

        hostname = 'foo-bar-host'

        machine_info_dict = src.find.machine_info_by_hostname(self.kube_node_labels_dict, hostname)

        self.assertEqual(machine_info_dict, None)

if __name__ == '__main__':
    unittest.main()
