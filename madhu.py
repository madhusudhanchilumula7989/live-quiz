services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: librarydb
      MYSQL_USER: libuser
      MYSQL_PASSWORD: libpass

  wordpress:
    image: wordpress:latest
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: librarydb
      WORDPRESS_DB_USER: libuser
      WORDPRESS_DB_PASSWORD: libpass


docker --version
docker compose version

docker pull mysql:8.0
docker pull wordpress:latest
docker images
docker compose down
docker compose up -d
docker compose ps




# ==========================================
# KUBERNETES LAB PRACTICAL
# Library Management Application
# ==========================================

# 1. START MINIKUBE CLUSTER
minikube start --driver=docker

# 2. CHECK CLUSTER STATUS
minikube status
kubectl get nodes

# 3. CREATE DEPLOYMENT WITH 2 REPLICAS
kubectl create deployment library-app --image=nginx:1.27 --replicas=2

# 4. VERIFY DEPLOYMENT AND PODS
kubectl get deployments
kubectl get pods

# 5. EXPOSE APPLICATION USING NODEPORT
kubectl expose deployment library-app --type=NodePort --port=80 --target-port=80

# 6. CHECK SERVICE
kubectl get services

# 7. OPEN APPLICATION IN BROWSER
minikube service library-app

# 8. SCALE FROM 2 TO 5 REPLICAS
kubectl scale deployment library-app --replicas=5

# 9. VERIFY 5 REPLICAS
kubectl get deployments
kubectl get pods

# 10. AUTOMATIC POD RECREATION
kubectl get pods

# Automatically select and delete one library-app Pod
$pod = kubectl get pods -l app=library-app -o jsonpath="{.items[0].metadata.name}"
kubectl delete pod $pod

# Verify automatic recreation
kubectl get pods -w




# ==========================================
# NAGIOS - COMPLETE LAB PRACTICAL
# ==========================================

# 1. PULL NAGIOS IMAGE
docker pull jasonrivers/nagios:latest

# 2. REMOVE OLD CONTAINER IF IT EXISTS
docker rm -f nagios 2>$null

# 3. RUN NAGIOS ON PORT 8081
docker run -d --name nagios -p 8081:80 jasonrivers/nagios:latest

# 4. CHECK CONTAINER
docker ps

# 5. WAIT FOR NAGIOS TO START
Start-Sleep -Seconds 10

# 6. CHECK NAGIOS CONFIGURATION FILES
docker exec nagios ls /opt/nagios/etc/objects/

# 7. CHECK AVAILABLE MONITORING PLUGINS
docker exec nagios ls /opt/nagios/libexec/

# 8. ADD WORDPRESS HTTP MONITORING
@'

define service {
    use                     local-service
    host_name               localhost
    service_description     WordPress HTTP
    check_command           check_http!-I host.docker.internal -p 8082 -H host.docker.internal
}

'@ | docker exec -i nagios bash -c "cat >> /opt/nagios/etc/objects/localhost.cfg"

# 9. START WORDPRESS AND MYSQL
docker compose -f C:\Users\user\library-portal\docker-compose.yml up -d

# 10. CHECK WORDPRESS CONTAINERS
docker compose -f C:\Users\user\library-portal\docker-compose.yml ps

# 11. TEST HTTP MONITORING
docker exec nagios /opt/nagios/libexec/check_http -I host.docker.internal -p 8082 -H host.docker.internal

# 12. ADD CPU MONITORING
@'

define service {
    use                     local-service
    host_name               localhost
    service_description     CPU Load
    check_command           check_load!5.0,4.0,3.0!10.0,6.0,4.0
}

'@ | docker exec -i nagios bash -c "cat >> /opt/nagios/etc/objects/localhost.cfg"

# 13. ADD DISK MONITORING
@'

define service {
    use                     local-service
    host_name               localhost
    service_description     Disk Usage
    check_command           check_disk!20%!10%!/
}

'@ | docker exec -i nagios bash -c "cat >> /opt/nagios/etc/objects/localhost.cfg"

# 14. VALIDATE CONFIGURATION
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg

# 15. RESTART NAGIOS CONTAINER
docker restart nagios

# 16. CHECK CONTAINER STATUS
docker ps

# 17. CHECK NAGIOS LOGS
docker logs --tail 50 nagios

# 18. CHECK HTTP CONFIGURATION
docker exec nagios bash -c "grep -n -A 8 -B 3 'WordPress HTTP' /opt/nagios/etc/objects/localhost.cfg"

# 19. CHECK HTTP AGAIN
docker exec nagios /opt/nagios/libexec/check_http -I host.docker.internal -p 8082

# 20. FINAL VERIFICATION
docker ps
docker port nagios
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg

# ==========================================
# OPEN DASHBOARD
# http://localhost:8081
#
# Username: nagiosadmin
# Password: nagios
# ==========================================
sudo apt update

sudo apt install openjdk-17-jdk git tomcat10 tomcat10-admin -y

java -version
git --version

sudo systemctl start tomcat10
sudo systemctl enable tomcat10
sudo systemctl status tomcat10


cd ~

git clone https://github.com/deepthisagar7/library-management.git

cd library-management

ls -la


