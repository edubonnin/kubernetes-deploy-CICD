#!/bin/bash

set -x

cd app
minikube image build -t app:latest .
cd ..

kubectl apply -f k8s/database
kubectl apply -f k8s/cache

sleep 5
kubectl apply -f k8s/app

sleep 3
minikube service app-service
