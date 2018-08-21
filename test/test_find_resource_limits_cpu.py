import src.find
import unittest

class FindResourceLimitsCPU(unittest.TestCase):

    # A sample kube_pod_container_resource_limits_cpu_cores_dict
    kube_pod_container_resource_limits_cpu_cores_dict = [{'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'addon-resizer', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'kube-state-metrics-6d465b4b54-w552f'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'alertmanager', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'alertmanager-6658498fb6-zrgsp'}, 'value': [1516046108.524, '1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'butterfly', 'exported_namespace': 'garland', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'butterfly-1-nvc2t'}, 'value': [1516046108.524, '1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'butterfly', 'exported_namespace': 'jason-monroe', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'butterfly-2-xcktw'}, 'value': [1516046108.524, '1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'cluster-autoscaler', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'cluster-autoscaler-79ddf8fdbd-l28z5'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'configmap-reload', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'alertmanager-6658498fb6-zrgsp'}, 'value': [1516046108.524, '0.005']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'configmap-reload', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'prometheus-54744d9cdb-4zdv6'}, 'value': [1516046108.524, '0.005']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'default-http-backend', 'exported_namespace': 'infrastructure', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'default-http-backend-59b65899db-w94k6'}, 'value': [1516046108.524, '0.01']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'default-http-backend', 'exported_namespace': 'infrastructure', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'ingress-default-backend-7df589f6bf-zx5t2'}, 'value': [1516046108.524, '0.01']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kube-lego', 'exported_namespace': 'infrastructure', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'kube-lego-64f6d4f695-bbs59'}, 'value': [1516046108.524, '0.5']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kube-state-metrics', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'kube-state-metrics-6d465b4b54-w552f'}, 'value': [1516046108.524, '0.105']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kubernetes-dashboard', 'exported_namespace': 'gawkbox-demo', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-16-146.ec2.internal', 'pod': 'kubernetes-dashboard-7cf4ddccb9-2dgdw'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kubernetes-dashboard', 'exported_namespace': 'gawkbox-dev', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-15-60.ec2.internal', 'pod': 'kubernetes-dashboard-7cf4ddccb9-p8mkc'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kubernetes-dashboard', 'exported_namespace': 'gawkbox-prod', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-17-110.ec2.internal', 'pod': 'kubernetes-dashboard-7cf4ddccb9-pl8rb'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'kubernetes-dashboard', 'exported_namespace': 'gawkbox-spinnaker', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-17-110.ec2.internal', 'pod': 'kubernetes-dashboard-7cf4ddccb9-2md7v'}, 'value': [1516046108.524, '0.1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'nginx-ingress-controller', 'exported_namespace': 'infrastructure', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'ingress-controller-598465c54-v7zhx'}, 'value': [1516046108.524, '2']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'node-exporter', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'node-exporter-xtd2c'}, 'value': [1516046108.524, '1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'node-exporter', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'node-exporter-gxsgh'}, 'value': [1516046108.524, '1']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'prometheus', 'exported_namespace': 'devops', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-101.ec2.internal', 'pod': 'prometheus-54744d9cdb-4zdv6'}, 'value': [1516046108.524, '8']}, {'metric': {'__name__': 'kube_pod_container_resource_limits_cpu_cores', 'container': 'server', 'exported_namespace': 'infrastructure', 'instance': '100.96.39.71:8080', 'job': 'kube-state-metrics', 'namespace': 'devops', 'node': 'ip-10-151-22-218.ec2.internal', 'pod': 'alb-ingress-controller-7777d769dd-rcsq6'}, 'value': [1516046108.524, '0.5']}]

    def test_find_pods_resource_limits_cpu_cores(self):
        '''Finds the cpu core value for a given pod'''

        exported_namespace = 'garland'
        node = 'ip-10-151-22-218.ec2.internal'
        pod = 'butterfly-1-nvc2t'

        cpu_core = src.find.pods_resource_limits_cpu_cores(
                    self.kube_pod_container_resource_limits_cpu_cores_dict,
                    exported_namespace,
                    node,
                    pod
                    )

        self.assertEqual(cpu_core, 1)

    def test_find_pods_resource_limits_cpu_cores_no_pod(self):
        '''Finds the cpu core value for a given pod which does not exist'''

        exported_namespace = 'garland'
        node = 'ip-10-151-22-218.ec2.internal'
        pod = 'foo-bar-pod'

        cpu_core = src.find.pods_resource_limits_cpu_cores(
                    self.kube_pod_container_resource_limits_cpu_cores_dict,
                    exported_namespace,
                    node,
                    pod
                    )

        self.assertEqual(cpu_core, 1.0000112233)

if __name__ == '__main__':
    unittest.main()
