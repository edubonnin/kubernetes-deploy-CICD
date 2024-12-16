#!/bin/bash

set -x

# kubectl delete pvc --all
kubectl delete all --all
# kubectl delete pv --all
sleep 5
minikube image rm app:latest
minikube image ls
