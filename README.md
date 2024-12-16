# kubernetes-deploy-CICD

---

## 📝 Índice

- [Acerca del Proyecto](#acerca-del-proyecto)
- [Set Up](#set-up)
- [Uso](#uso)
- [Limpieza del Sistema](#limpieza)
- [Autores](#autores)

## 🧐 Acerca del Proyecto <a name="acerca-del-proyecto"></a>

Este proyecto tiene como objetivo diseñar, implementar y desplegar una infraestructura completa utilizando Kubernetes como orquestador de contenedores y un pipeline de CI/CD para la automatización del desarrollo y despliegue continuo.

## 🏁 Set Up <a name="set-up"></a>

### App 

1. **Inicialización**

```bash
cd scripts
```
```bash
./init.sh
```

2. **Levantamiento de servicios**

```bash
./build.sh
```

### Base de Datos

1. **Conectarse al Pod correspondiente**

```bash
kubectl get pods
```

```bash
kubectl exec -it <pod> -- psql -h localhost -U edu --password -p 5432 usuarios
```

2. **Insertar los Valores**

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

#### Prueba de Persistencia de los Datos

```bash
kubectl get pods
```
```bash
kubectl delete pods <pod>
```

Una vez ejecutados los comandos anteriores, comprobar que, efectivamente, el pod se ha vuelto a levantar (mirar tiempo de vida volviendo a ejecutar un 'kubectl get pods') y que recargando la web-app los datos persisten.

### Caché

```bash
kubectl get pods
```
```bash
kubectl exec -it <pod> -- redis-cli
```

#### Establecer Mensaje en Redis

```bash
set mensaje "Hola desde Redis"
```

### Monitoring

#### Instalación

En MacOS, ejectuar los siguientes comandos. Instalar primero el gestor de paquetes *homebrew* en el caso de que no disponer de él.

```bash
brew install helm
```
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
```bash
helm repo update
```
```bash
helm install prom-stack prometheus-community/kube-prometheus-stack --create-namespace --namespace monitoring
```

#### Comprobación

```bash
kubectl get svc -n monitoring
```

1. Hacer un port-forward del pod de prometheus

```bash
kubectl port-forward svc/prom-stack-kube-prometheus-prometheus -n monitoring 9090:9090
```

2. Acceder a prometheus mediante la dirección 'localhost:9090'

3. Hacer un port-forward del pod de grafana

```bash
kubectl port-forward svc/prom-stack-grafana -n monitoring 3000:80
```

4. Acceder a grafana' mediante la dirección 'localhost:3000'

### Obtención de Credenciales Grafana
USER --> 'admin'


PASSWORD --> se obtiene mediante el siguiente comando:
```bash
kubectl get secret --namespace monitoring prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

## 🎈 Uso <a name="uso"></a>

Una vez que los pods estén levantados, recargar la página que el servicio de la aplicación muestra en el navegador.

La aplicación muestra:

- Estado de la conexión a la base de datos
- Estado de la conexión a Redis
- Datos almacenados en la tabla usuarios
- Mensaje obtenido desde Redis

## 🧹 Limpieza del Sistema <a name="clean"></a>

Ejectuar los siguientes scripts para hacer una limpieza de los servicios levantados e imagánes en el clúster.

```bash
cd scipts
```
```bash
./clean.sh
```

Para una limpieza más exhaustiva que también elimine el clúster de Kubernetes ejecutar el siguiente comando:

```bash
minikube delete
```

## ✍️ Autores <a name="autores"></a>

Eduardo Bonnín Narváez - [GitHub](https://github.com/edubonnin)