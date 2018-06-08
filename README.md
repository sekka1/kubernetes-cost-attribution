Kubernetes Cost Attribution
====================
A set of scripts to calculate the cost of each running pods on the cluster by
polling Prometheus for the CPU/Memory information and tallying it up.

## Docker

### Build

```
docker build -t garland/managed-kubernetes-billing:dev .
```

```
docker run -it \
-e USER=$USER  -e USERID=$UID \
--memory=8000m \
--cpus="1.5" \
-v ${PWD}:/opt/app \
-v /tmp:/tmp \
garland/managed-kubernetes-billing:dev bash
```

Add in your your local user so that files that are manipulated in the container has your local user's ID

```
useradd g44
su g44
bash
```

## Setup

### Install python3 pip and virtualenv

```
sudo apt install python3-pip
sudo pip3 install virtualenv

pip3 install requests
```

### Create the virtualenv
Assuming your current working directory is where this README.md file is

```
virtualenv . -p /usr/bin/python3
```

### Activate the virtualenv

```
source bin/activate
```

### Deactivate the virtualenv

```
deactivate
```

# Unittest

## Running one unit test file
```
python3 -m unittest test.test_find
```

## Running all unit tests
```
python3 -m unittest discover
```

# Running the scripts:

## Running the pod_usage script

```
export PROMETHEUS_HOST="https://prometheus.infra.prod-1.devops.bot"
export PROMETHEUS_USER="saas-kube"
export PROMETHEUS_PASSWORD=""
```

```
python3 pod_usage.py ${PROMETHEUS_HOST} ${PROMETHEUS_USER} ${PROMETHEUS_PASSWORD} <output billing csv file> <last_state.json file> <cycles to run in mins>
```

<cycles to run in mins>
How many cycles to run in minutes.

For example, I want to do the billing for the last day:
60 * 24 = 1440

I want to do billing for the last week:
60 * 24 = 1440 * 7 = 10080

### Time calculation

```
one day: 86400 (secs)
one day: 1440 (mins)
one week: 604800 (secs)
one week: 10080 (mins)
```

### Running on the cluster prod-1.k8s.devops.bot

Directory: ../prod-1.k8s.devops.bot
last_state.json: ../prod-1.k8s.devops.bot/last_state.json

We will initially start out on this date: `1515888000 = 01/14/18`

Runs will calculate a duration of one week at a time:

The billing file should be then moved to a named file for the week. The date should
be the start of the week
```
python3 pod_usage.py ${PROMETHEUS_HOST} ${PROMETHEUS_USER} ${PROMETHEUS_PASSWORD} "../prod-1.k8s.devops.bot/billing-MM-DD-YY.csv" "../prod-1.k8s.devops.bot/last_state.json" "10080"
```

## Running billing summary

python3 billing_summary.py <csv file>
