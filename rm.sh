#!/bin/bash

set -x

kubectl delete all --all
sleep 20
minikube image rm app:latest
minikube image ls
