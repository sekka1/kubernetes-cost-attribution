Kubernetes Cost Attribution
===========================

# Overview
Kubernetes Cost Attribution is an application to help you attribute the cost of what
each namespace is accruing based on the pods that are running in that namespace
and the nodes it is using.


# Installation

## Quick install with Google Cloud Marketplace

Get up and running with a few clicks! Install this `Kubernetes Cost Attribution` app to a Google
Kubernetes Engine cluster using Google Cloud Marketplace. Follow the on-screen
instructions:
*TODO: link to solution details page*

## Command line instructions

Follow these instructions to install `Kubernetes Cost Attribution` from the command line.

### Prerequisites

- Setup cluster
  - Permissions
- Setup kubectl
- Setup helm
- Install Application Resource
- Acquire License

### Commands

Set environment variables (modify if necessary):
```
export APP_INSTANCE_NAME=nginx-1
export NAMESPACE=default
```

Expand manifest template:
```
helm template . --set APP_INSTANCE_NAME=$APP_INSTANCE_NAME,NAMESPACE=$NAMESPACE > expanded.yaml
```

Run kubectl:
```
kubectl apply -f expanded.yaml
```

*TODO: fix instructions*

# Backups

*TODO: instructions for backups*

# Upgrades

*TODO: instructions for upgrades*
