package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"reflect"
	"strconv"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"github.com/golang/glog"
	"k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

// optional - local kubeconfig for testing
var kubeconfig = flag.String("kubeconfig", "", "Path to a kubeconfig file")

func main() {

	// send logs to stderr so we can use 'kubectl logs'
	flag.Set("logtostderr", "true")
	flag.Set("v", "3")
	flag.Parse()

	config, err := getConfig(*kubeconfig)
	if err != nil {
		glog.Errorf("Failed to load client config: %v", err)
		return
	}

	// build the Kubernetes clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		glog.Errorf("Failed to create kubernetes client: %v", err)
		return
	}

	nodes, err := getAllNodes(clientset)

	for _, n := range nodes.Items {
		glog.V(3).Infof("Found nodes: %s/%s", n.Name, n.UID)
	}

	//recordMetrics()
	go update(clientset)

	http.Handle("/metrics", promhttp.Handler())
	http.ListenAndServe(":9101", nil)
}

func getConfig(kubeconfig string) (*rest.Config, error) {
	if kubeconfig != "" {
		return clientcmd.BuildConfigFromFlags("", kubeconfig)
	}

	return rest.InClusterConfig()
}

func getAllNodes(clientset *kubernetes.Clientset) (*v1.NodeList, error) {

	// list nodes
	nodes, err := clientset.CoreV1().Nodes().List(metav1.ListOptions{})
	if err != nil {
		glog.Errorf("Failed to retrieve nodes: %v", err)
		return nil, err
	}

	return nodes, nil
}

func getAllPods(clientset *kubernetes.Clientset) (*v1.PodList, error) {

	//fmt.Println(reflect.TypeOf(clientset))

	// setup list options
	listOptions := metav1.ListOptions{
		LabelSelector: "",
		FieldSelector: "",
	}

	// list pods
	pods, err := clientset.CoreV1().Pods("").List(listOptions)
	if err != nil {
		glog.Errorf("Failed to retrieve pods: %v", err)
		return nil, err
	}

	//fmt.Print(pods.Items[0])
	//fmt.Printf("%+v\n", pods)

	//fmt.Println(reflect.TypeOf(pods))

	return pods, nil
}

func PrettyPrint(v interface{}) (err error) {
	b, err := json.MarshalIndent(v, "", "  ")
	if err == nil {
		fmt.Println(string(b))
	}
	return
}

func update(clientset *kubernetes.Clientset) {

	// divisor := resource.Quantity{}
	// divisor = resource.MustParse("1")

	namespaceCostMap := make(map[string]float64)

	var nodeList nodeList

	for {
		nodes, err := getAllNodes(clientset)
		if err != nil {
			glog.Errorf("Failed to retrieve nodes: %v", err)
			return
		}

		fmt.Println(reflect.TypeOf(nodes))

		for _, n := range nodes.Items {
			//PrettyPrint(n.Status.Capacity)
			glog.V(3).Infof("Found nodes: %s/%s", n.Name, n.UID)

			var node nodeInfo
			node.name = n.Name
			node.cpuCapacity = n.Status.Capacity.Cpu().MilliValue()
			node.memoryCapacity = n.Status.Capacity.Memory().Value()
			node.computeCostPerHour = 0.0475

			glog.V(3).Infof("Node CPU Capacity: %s", strconv.FormatInt(node.cpuCapacity, 10))
			glog.V(3).Infof("Node Memory Capacity: %s", strconv.FormatInt(node.memoryCapacity, 10))

			nodeList.node = append(nodeList.node, node)
		}

		fmt.Println("nodeList.node")
		for _, n := range nodeList.node {
			fmt.Println(n)
		}

		pods, err := getAllPods(clientset)
		if err != nil {
			glog.Errorf("Failed to retrieve pods: %v", err)
			return
		}

		for _, p := range pods.Items {
			if p.Status.Phase == "Running" {
				//PrettyPrint(p)
				//fmt.Println(reflect.TypeOf(p.Spec.Containers))
				glog.V(3).Infof("Found pods: %s/%s/%s/%s", p.Namespace, p.Name, p.UID, p.Spec.NodeName)

				for _, c := range p.Spec.Containers {
					glog.V(3).Infof("Found container: %s", c.Name)
					//fmt.Println(reflect.TypeOf(c.Resources.Limits.Memory))
					//fmt.Println(reflect.TypeOf(c))
					//PrettyPrint(c.Resources.Limits)
					//fmt.Println(c.Resources.Limits.Memory.Value())
					// for k, l := range c.Resources.Limits {
					// 	fmt.Println(k)
					// 	fmt.Println(l)
					// 	// PrettyPrint(k)
					// 	// PrettyPrint(l)
					// }

					var cpuLimit int64 = c.Resources.Limits.Cpu().MilliValue()
					var cpuRequest int64 = c.Resources.Requests.Cpu().MilliValue()
					var memoryLimit int64 = c.Resources.Limits.Memory().Value()
					var memoryRequest int64 = c.Resources.Requests.Memory().Value()

					glog.V(3).Infof("CPU Limit: %s", strconv.FormatInt(cpuLimit, 10))
					glog.V(3).Infof("Memory Limit: %s", strconv.FormatInt(memoryLimit, 10))
					glog.V(3).Infof("CPU Requests: %s", strconv.FormatInt(cpuRequest, 10))
					glog.V(3).Infof("Memory Requests: %s", strconv.FormatInt(memoryRequest, 10))

					//fmt.Println(reflect.TypeOf(cpuLimit))

					nodeInfo, err := getNodeInfo(nodeList, p.Spec.NodeName)
					if err != nil {
						glog.Errorf("Failed to retrieve nodes: %v", err)
						return
					}

					var podUsageMemory int64 = memoryLimit
					var podUsageCpu int64 = cpuLimit

					cost := calculatePodCost(nodeInfo, podUsageMemory, podUsageCpu)

					podCostMetric.With(prometheus.Labels{"namespace_name": p.Namespace, "pod_name": p.Name, "duration": "minute"}).Set(cost.minuteCpu + cost.minuteMemory)

					// Add this pod to the total
					namespaceCostMap[p.Namespace] += cost.minuteCpu + cost.minuteMemory
				}
			}

		}

		// hdFailures.With(prometheus.Labels{"device": "/dev/sda"}).Inc()
		// namespaceCost.With(prometheus.Labels{"namespace_name": "foo", "duration": "bar"}).Set(4.2)
		// namespaceCost.With(prometheus.Labels{"namespace_name": "foo2", "duration": "bar"}).Set(5.2)

		for k, ns := range namespaceCostMap {
			// fmt.Println(k)
			// fmt.Println(strconv.FormatFloat(ns, 'f', 6, 64))
			namespaceCost.With(prometheus.Labels{"namespace_name": k, "duration": "minute"}).Set(ns)

			// reset the counter to zero
			namespaceCostMap[k] = 0
		}

		time.Sleep(60 * time.Second)
	}
}

// // https://github.com/kubernetes/kubernetes/blob/master/pkg/api/resource/helpers.go
// // convertResourceCPUToInt converts cpu value to the format of divisor and returns
// // ceiling of the value.
// func convertResourceCPUToInt(cpu *resource.Quantity, divisor resource.Quantity) (int64, error) {
// 	c := int64(math.Ceil(float64(cpu.MilliValue()) / float64(divisor.MilliValue())))
// 	//b := float64(math.Ceil(float64(cpu.Value()) / float64(divisor.Value())))
// 	fmt.Println(cpu.MilliValue())
// 	return c, nil
// }
//
// // convertResourceMemoryToInt converts memory value to the format of divisor and returns
// // ceiling of the value.
// func convertResourceMemoryToInt(memory *resource.Quantity, divisor resource.Quantity) (int64, error) {
// 	m := int64(math.Ceil(float64(memory.Value()) / float64(divisor.Value())))
// 	return m, nil
// }
//
// // convertResourceEphemeralStorageToInt converts ephemeral storage value to the format of divisor and returns
// // ceiling of the value.
// func convertResourceEphemeralStorageToInt(ephemeralStorage *resource.Quantity, divisor resource.Quantity) (int64, error) {
// 	m := int64(math.Ceil(float64(ephemeralStorage.Value()) / float64(divisor.Value())))
// 	return m, nil
// }

func recordMetrics() {
	go func() {
		for {
			cpuTemp.Set(65.3)
			hdFailures.With(prometheus.Labels{"device": "/dev/sda"}).Inc()
			namespaceCost.With(prometheus.Labels{"namespace_name": "foo", "duration": "bar"}).Set(4.2)
			namespaceCost.With(prometheus.Labels{"namespace_name": "foo2", "duration": "bar"}).Set(5.2)
			time.Sleep(2 * time.Second)
		}
	}()
}

type podCost struct {
	minuteMemory float64
	hourMemory   float64
	dayMemory    float64
	monthMemory  float64
	minuteCpu    float64
	hourCpu      float64
	dayCpu       float64
	monthCpu     float64
}

type nodeInfo struct {
	name               string
	cpuCapacity        int64
	memoryCapacity     int64
	computeCostPerHour float64
}

type nodeList struct {
	node []nodeInfo
}

func calculatePodCost(node nodeInfo, podUsageMemory int64, podUsageCpu int64) podCost {

	cost := podCost{}

	computeCostPerHourMemory := node.computeCostPerHour * 0.5
	computeCostPerHourCpu := node.computeCostPerHour * 0.5

	percentUsedMemory := float64(podUsageMemory) / float64(node.memoryCapacity)
	percentUsedCpu := float64(podUsageCpu) / float64(node.cpuCapacity)

	cost.hourMemory = computeCostPerHourMemory * float64(percentUsedMemory)
	cost.hourCpu = computeCostPerHourCpu * float64(percentUsedCpu)

	cost.minuteMemory = cost.hourMemory / 60
	cost.minuteCpu = cost.hourCpu / 60

	cost.dayMemory = cost.hourMemory * 24
	cost.dayCpu = cost.hourCpu * 24

	cost.monthMemory = cost.dayMemory * 30
	cost.monthCpu = cost.dayCpu * 30

	glog.V(3).Infof("Cost per minute memory: %s", strconv.FormatFloat(cost.minuteMemory, 'f', 6, 64))
	glog.V(3).Infof("Cost per minute cpu: %s", strconv.FormatFloat(cost.minuteCpu, 'f', 6, 64))

	glog.V(3).Infof("Cost per hour memory: %s", strconv.FormatFloat(cost.hourMemory, 'f', 6, 64))
	glog.V(3).Infof("Cost per hour cpu: %s", strconv.FormatFloat(cost.hourCpu, 'f', 6, 64))

	glog.V(3).Infof("Cost per day memory: %s", strconv.FormatFloat(cost.dayMemory, 'f', 6, 64))
	glog.V(3).Infof("Cost per day cpu: %s", strconv.FormatFloat(cost.dayCpu, 'f', 6, 64))

	glog.V(3).Infof("Cost per month memory: %s", strconv.FormatFloat(cost.monthMemory, 'f', 6, 64))
	glog.V(3).Infof("Cost per month cpu: %s", strconv.FormatFloat(cost.monthCpu, 'f', 6, 64))

	return cost
}

func getNodeInfo(nodes nodeList, nodeName string) (nodeInfo, error) {

	info := nodeInfo{}

	for _, n := range nodes.node {
		if n.name == nodeName {
			info = n
		}
	}

	return info, nil
}

var (
	cpuTemp = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cpu_temperature_celsius",
		Help: "Current temperature of the CPU.",
	})
	hdFailures = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "hd_errors_total",
		Help: "Number of hard-disk errors.",
	},
		[]string{"device"},
	)
	namespaceCost = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "mk_namespace_cost",
		Help: "ManagedKube - The cost of the namespace.",
	},
		[]string{"namespace_name", "duration"},
	)
	podCostMetric = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "mk_pod_cost",
		Help: "ManagedKube - The cost of the pod.",
	},
		[]string{"pod_name", "namespace_name", "duration"},
	)
	totalNumberOfPods = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "mk_total_number_of_pods",
		Help: "ManagedKube - The total number of running pods.",
	},
		[]string{"namespace_name"},
	)
)

func init() {
	// Metrics have to be registered to be exposed:
	prometheus.MustRegister(cpuTemp)
	prometheus.MustRegister(hdFailures)
	prometheus.MustRegister(namespaceCost)
	prometheus.MustRegister(podCostMetric)
	prometheus.MustRegister(totalNumberOfPods)
}
