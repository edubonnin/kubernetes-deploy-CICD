# kubernetes-deploy-CICD
Despliegue de infraestructura con Kubernetes y CI/CD

# Instrucciones

## App

1.
minikube start
minikube dashboard

2.
cd app
minikube image build -t app:latest .
cd ..

3.
kubectl apply -f k8s/database
kubectl apply -f k8s/cache
kubectl apply -f k8s/app

4.
minikube service app-service

## Base de Datos

kubectl get pods
kubectl exec -it <pod> -- psql -h localhost -U edu --password -p 5432 usuarios
// psql -h localhost -p 5432 -U edu -d usuarios

### Inserción de Valores

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);

INSERT INTO usuarios (nombre, email, contraseña) VALUES ('Juan Pérez', 'juan.perez@example.com', 'password123');
INSERT INTO usuarios (nombre, email, contraseña) VALUES ('Ana Gómez', 'ana.gomez@example.com', 'contraseña456');

### Prueba de Persistencia de los Datos

kubectl delete pods <pod>

## Caché

kubectl get pods
kubectl exec -it <pod> -- redis-cli
// redis-cli -h localhost -p 6379

### Establecer Mensaje

set mensaje "Hola desde Redis"

## Monitoring

### Instalación

brew install helm

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prom-stack prometheus-community/kube-prometheus-stack --create-namespace --namespace monitoring

### Comprobación

kubectl get svc -n monitoring
kubectl port-forward svc/prom-stack-kube-prometheus-prometheus -n monitoring 9090:9090
kubectl port-forward svc/prom-stack-grafana -n monitoring 3000:80

### Obtención de Credenciales Grafana
USER --> admin
PASSWORD --> kubectl get secret --namespace monitoring prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

## Otros

### Limpieza

kubectl delete pvc --all
kubectl delete all --all
minikube image rm app:latest
minikube image ls

### Volúmenes para Static

minikube mount $(pwd)/app/static:/mnt/app-static
