# kubernetes-deploy-CICD
Despliegue de infraestructura con Kubernetes y CI/CD

# Instrucciones

## App

### Puesta en marcha

1.
```bash
cd scripts
```

2.
```bash
./init.sh
```

3.
```bash
./build.sh
```

## Base de Datos

```bash
kubectl get pods
kubectl exec -it <pod> -- psql -h localhost -U edu --password -p 5432 usuarios
```

### Inserción de Valores

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);
```

```sql
INSERT INTO usuarios (nombre, email, contraseña) VALUES ('Juan Pérez', 'juan.perez@example.com', 'password123');
INSERT INTO usuarios (nombre, email, contraseña) VALUES ('Ana Gómez', 'ana.gomez@example.com', 'contraseña456');
```

### Prueba de Persistencia de los Datos

```bash
kubectl get pods
kubectl delete pods <pod>
```

## Caché

```bash
kubectl get pods
kubectl exec -it <pod> -- redis-cli
```

### Establecer Mensaje

```bash
set mensaje "Hola desde Redis"
```

## Monitoring

### Instalación

```bash
brew install helm

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prom-stack prometheus-community/kube-prometheus-stack --create-namespace --namespace monitoring
```

### Comprobación

```bash
kubectl get svc -n monitoring
kubectl port-forward svc/prom-stack-kube-prometheus-prometheus -n monitoring 9090:9090
kubectl port-forward svc/prom-stack-grafana -n monitoring 3000:80
```

### Obtención de Credenciales Grafana
USER --> admin

PASSWORD --> kubectl get secret --namespace monitoring prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

## Otros

### Limpieza

```bash
cd scipts
./clean.sh
```

### Volúmenes para Static

```bash
# minikube mount $(pwd)/app/static:/mnt/app-static
```
