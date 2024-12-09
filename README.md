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
kubectl apply -f k8s/app

4.
minikube service app-service

## Base de Datos

5.
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

redis-cli -h localhost -p 6379

### Establecer Mensaje

set mensaje "Hola desde Redis"




kubectl delete all --all
minikube image rm app:latest
minikube image ls