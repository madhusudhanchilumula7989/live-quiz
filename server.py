
# ============================================================
# Q1: AWS EC2 - MAVEN JAVA APPLICATION USING DOCKER
# ============================================================

# STEP 1: LAUNCH UBUNTU EC2 INSTANCE MANUALLY IN AWS CONSOLE
# Open inbound port 22 (SSH).
# Launch Ubuntu 24.04 instance.
# Download your PEM key.

# STEP 2: CONNECT FROM WINDOWS POWERSHELL
cd $HOME\Downloads

ssh -i .\vehicle-rental.pem ubuntu@YOUR_EC2_PUBLIC_IP

# ------------------------------------------------------------
# NOW YOU ARE INSIDE EC2 UBUNTU
# COPY AND EXECUTE THE FOLLOWING COMMANDS
# ------------------------------------------------------------

sudo apt update -y
sudo apt upgrade -y

sudo apt install git docker.io openjdk-17-jdk maven -y

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ubuntu

# Refresh Docker group membership
newgrp docker

# Verify installations
git --version
docker --version
java -version
mvn -version

# Clone GitHub repository
git clone https://github.com/haleema91/LAB-INTERNAL-II-OVR1.git

cd LAB-INTERNAL-II-OVR1

# Maven build operations
mvn clean
mvn compile
mvn test
mvn package
mvn install

# Check generated JAR
ls -lh target/

# Create Dockerfile
cat > Dockerfile <<'EOF'
FROM maven:3.9.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]
EOF

# Build Docker image
docker build -t vehicle-rental:latest .

# Check image
docker images

# Run Java application
docker run -d --name vehicle-rental-container vehicle-rental:latest

# Verify container
docker ps
docker ps -a

# Check application logs
docker logs vehicle-rental-container

# Stop container
docker stop vehicle-rental-container

# Start container
docker start vehicle-rental-container

# Remove container if required
docker rm -f vehicle-rental-container

# Exit EC2
exit


# ============================================================
# Q2: KUBERNETES - MINIKUBE + NGINX + NAGIOS
# ============================================================

# Run these commands in WINDOWS POWERSHELL

# Install Minikube and kubectl if not installed
winget install Kubernetes.minikube
winget install Kubernetes.kubectl

# Start Docker Desktop manually before continuing

# Start Minikube
minikube start --driver=docker

# Verify cluster
minikube status
kubectl cluster-info
kubectl get nodes

# Create Nginx deployment with 3 replicas
kubectl create deployment nginx --image=nginx --replicas=3

# Verify deployment
kubectl get deployments
kubectl get pods

# Expose deployment through NodePort
kubectl expose deployment nginx --type=NodePort --port=6060 --target-port=80 --name=nginx-service

# Assign NodePort 30060
kubectl patch service nginx-service -p '{"spec":{"ports":[{"port":6060,"targetPort":80,"nodePort":30060}]}}'

# Verify service
kubectl get services
kubectl describe service nginx-service

# Access application
minikube service nginx-service --url

# Scale from 3 to 5 replicas
kubectl scale deployment nginx --replicas=5

# Verify scaling
kubectl get deployments
kubectl get pods
kubectl get pods -w

# View all resources
kubectl get all

# View pod details
kubectl describe pods

# View events
kubectl get events

# ------------------------------------------------------------
# NAGIOS INSTALLATION USING DOCKER
# ------------------------------------------------------------

# Pull Nagios image
docker pull jasonrivers/nagios:latest

# Run Nagios
docker run -d --name nagios -p 8080:80 jasonrivers/nagios:latest

# Verify container
docker ps

# Check Nagios logs
docker logs nagios

# Access Nagios
# http://localhost:8080
# Username: nagiosadmin
# Password: nagios

# Forward Kubernetes service port to host
# Run in a separate PowerShell terminal and keep running:
# kubectl port-forward --address 0.0.0.0 service/nginx-service 6060:6060

# Configure Nagios to monitor Nginx
docker exec nagios bash -c "cat > /opt/nagios/etc/objects/vehicle.cfg <<'EOF'
define host {
    use linux-server
    host_name vehicle-rental
    alias Vehicle Rental Application
    address host.docker.internal
}
define service {
    use generic-service
    host_name vehicle-rental
    service_description Nginx HTTP
    check_command check_http!-p 6060
}
EOF"

# Register configuration
docker exec nagios bash -c "echo 'cfg_file=/opt/nagios/etc/objects/vehicle.cfg' >> /opt/nagios/etc/nagios.cfg"

# Validate Nagios configuration
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg

# Restart Nagios
docker exec nagios service nagios restart

# Check Nagios status
docker exec nagios service nagios status

# View logs
docker logs nagios


# ============================================================
# Q3: JENKINS - FREESTYLE PROJECT + MAVEN + GITHUB
# ============================================================

# Run Jenkins using Docker

docker pull jenkins/jenkins:lts

# Create persistent volume
docker volume create jenkins_home

# Run Jenkins container
docker run -d --name jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Check Jenkins
docker ps

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Open Jenkins
# http://localhost:8081

# Complete initial setup manually:
# Install suggested plugins
# Create administrator account

# JENKINS UI CONFIGURATION:
#
# Manage Jenkins -> Plugins
# Install:
# Git plugin
# Maven Integration plugin
# GitHub plugin
# Build Pipeline plugin
#
# Manage Jenkins -> Tools
# Configure JDK:
# Name: JDK17
#
# Configure Maven:
# Name: Maven3
# Enable automatic installation if needed
#
# Dashboard -> New Item
# Project Name: Vehicle-Rental
# Select: Freestyle Project
#
# Source Code Management -> Git
# Repository URL:
# https://github.com/haleema91/LAB-INTERNAL-II-OVR1.git
#
# Branch:
# */main
#
# Build Steps -> Invoke top-level Maven targets
# Maven Version: Maven3
# Goals:
# clean install test
#
# Build Triggers:
# Enable GitHub hook trigger for GITScm polling
#
# Post-build Actions:
# Archive the artifacts
# Files to archive:
# target/*.jar
#
# Save -> Build Now
#
# Console Output -> Verify build
#
# Pipeline View:
# New Item -> Build Pipeline View
# Select Vehicle-Rental as initial job
#
# GITHUB WEBHOOK:
# GitHub Repository -> Settings -> Webhooks -> Add webhook
#
# Payload URL:
# https://YOUR_PUBLIC_JENKINS_URL/github-webhook/
#
# Content type: application/json
# Event: Just the push event
#
# NOTE: Jenkins must be publicly reachable for GitHub webhook.

# Jenkins troubleshooting commands
docker logs jenkins
docker ps -a
docker inspect jenkins

# Restart Jenkins
docker restart jenkins

# Check Jenkins password again
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword


# ============================================================
# Q4: DOCKER COMPOSE - WORDPRESS + MYSQL
# ============================================================

# Create project folder
mkdir vehicle-rental-compose

cd vehicle-rental-compose

# Create Docker Compose file
@'
services:
  mysql:
    image: mysql:8.0
    container_name: vehicle-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: vehicledb
      MYSQL_USER: vehicleuser
      MYSQL_PASSWORD: vehicle123
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-proot123"]
      interval: 10s
      timeout: 5s
      retries: 5

  wordpress:
    image: wordpress:latest
    container_name: vehicle-wordpress
    restart: always
    ports:
      - "8085:80"
    environment:
      WORDPRESS_DB_HOST: mysql:3306
      WORDPRESS_DB_USER: vehicleuser
      WORDPRESS_DB_PASSWORD: vehicle123
      WORDPRESS_DB_NAME: vehicledb
    depends_on:
      mysql:
        condition: service_healthy
    volumes:
      - wordpress_data:/var/www/html

volumes:
  mysql_data:
  wordpress_data:
'@ | Set-Content -Encoding ASCII docker-compose.yml

# Validate YAML configuration
docker compose config

# Download images and start containers
docker compose up -d

# Check containers
docker compose ps

# Check images
docker images

# Check logs
docker compose logs

# MySQL logs
docker compose logs mysql

# WordPress logs
docker compose logs wordpress

# Follow live logs
docker compose logs -f

# Access MySQL container
docker exec -it vehicle-mysql bash

# Inside MySQL container:
# mysql -u root -p
# Password: root123
# SHOW DATABASES;
# USE vehicledb;
# SHOW TABLES;
# EXIT;
# exit

# Check WordPress container
docker exec -it vehicle-wordpress bash

# Exit container
exit

# Access website
# http://localhost:8085

# Stop containers
docker compose stop

# Start containers
docker compose start

# Restart containers
docker compose restart

# Stop and remove containers (preserve volumes)
docker compose down

# Start again
docker compose up -d

# List persistent volumes
docker volume ls

# Remove containers AND volumes (DATA WILL BE LOST)
# Use only if you intentionally want a fresh installation:
docker compose down -v


# ============================================================
# FINAL VERIFICATION - ALL EXPERIMENTS
# ============================================================

# Docker containers
docker ps -a

# Docker images
docker images

# Docker volumes
docker volume ls

# Docker networks
docker network ls

# Kubernetes deployments
kubectl get deployments

# Kubernetes pods
kubectl get pods

# Kubernetes services
kubectl get services

# Kubernetes all resources
kubectl get all

# Minikube status
minikube status

# Jenkins logs
docker logs jenkins

# Nagios logs
docker logs nagios

# Docker Compose status
docker compose ps







services:
  db:
    image: mysql:8.0
    container_name: vehicle-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: vehicledb
      MYSQL_USER: vehicleuser
      MYSQL_PASSWORD: vehicle123
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    container_name: vehicle-wordpress
    restart: always
    ports:
      - "8081:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: vehicleuser
      WORDPRESS_DB_PASSWORD: vehicle123
      WORDPRESS_DB_NAME: vehicledb
    depends_on:
      - db
    volumes:
      - wordpress_data:/var/www/html

volumes:
  db_data:
  wordpress_data:
