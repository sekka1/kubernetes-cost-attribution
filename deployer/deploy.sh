#!/bin/bash

helm template . | kubectl apply -f -
