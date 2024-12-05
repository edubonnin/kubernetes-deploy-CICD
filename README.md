# kubernetes-deploy-CICD
Despliegue de infraestructura con Kubernetes y CI/CD

Instrucciones

1.
minikube start

2.
minikube image build -t app:latest .

3.
kubectl apply -f k8s/

4.
minikube service nginx-service



kubectl exec -it postgres-f4d48766f-jgk4g -- psql -h localhost -U edu --password -p 5432 usuarios
psql -h localhost -p 5432 -U edu -d usuarios
