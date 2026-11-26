https://github.com/priyankahotkar/springboot-jenkins-docker
:: 1. Clone GitHub repository
git clone https://github.com/priyankahotkar/springboot-jenkins-docker.git

:: 2. Enter project directory
cd springboot-jenkins-docker

:: 3. Check Java and Maven
java -version
mvn -version

:: 4. Clean previous build files
mvn clean

:: 5. Compile Java source code
mvn compile

:: 6. Run test cases
mvn test

:: 7. Build the application
mvn clean package

:: 8. Check generated JAR file
dir target

:: 9. Run application using embedded Tomcat on port 9090
java -jar target\demo-0.0.1-SNAPSHOT.jar --server.port=9090

:: 10. Open browser
:: http://localhost:9090

:: 11. Stop application
:: Press CTRL + C


:: 1. Navigate to project directory
cd "C:\Users\user\OneDrive\Desktop\practice se\springboot-jenkins-docker"

:: 2. Check Docker installation
docker --version

:: 3. Check Docker engine
docker ps

:: 4. List project files
dir

:: 5. Build Docker image
docker build -t springboot-demo .

:: 6. List Docker images
docker images

:: 7. Run Docker container on port 9091
docker run -d --name springboot-container -p 9091:8080 springboot-demo

:: 8. Check running containers
docker ps

:: 9. View container logs
docker logs springboot-container

:: 10. Stop container
docker stop springboot-container

:: 11. Start container
docker start springboot-container

:: 12. Remove container
docker rm -f springboot-container

:: 13. Remove Docker image (optional)
docker rmi springboot-demo


:: 1. Navigate to project directory
cd "C:\Users\user\OneDrive\Desktop\practice se\springboot-jenkins-docker"

:: 2. Check Docker version
docker --version

:: 3. Build Docker image
docker build -t springboot-demo .

:: 4. View local images
docker images

:: 5. Login to Docker Hub
docker login

:: 6. Tag image with Docker Hub username
docker tag springboot-demo YOUR_USERNAME/springboot-demo:latest

:: 7. Verify tagged image
docker images

:: 8. Push image to Docker Hub
docker push YOUR_USERNAME/springboot-demo:latest

:: 9. Logout from Docker Hub (optional)
docker logout


:: ==========================================
:: PULL AND RUN IMAGE ON ANOTHER MACHINE
:: ==========================================

:: 10. Login to Docker Hub (if repository is private)
docker login

:: 11. Pull image from Docker Hub
docker pull YOUR_USERNAME/springboot-demo:latest

:: 12. Verify downloaded image
docker images

:: 13. Run container on port 9093
docker run -d --name springboot-pulled -p 9093:8080 YOUR_USERNAME/springboot-demo:latest

:: 14. Check running containers
docker ps

:: 15. View container logs
docker logs springboot-pulled

:: 16. Open application in browser
:: http://localhost:9093

:: 17. Stop container
docker stop springboot-pulled

:: 18. Remove container
docker rm springboot-pulled

:: 19. Logout (optional)
docker logout



:: ==========================================
:: KUBERNETES USING MINIKUBE
:: ==========================================

:: 1. Navigate to project directory
cd "C:\Users\user\OneDrive\Desktop\practice se\springboot-jenkins-docker"

:: 2. Check Minikube version
minikube version

:: 3. Check kubectl version
kubectl version --client

:: 4. Check Docker version
docker --version

:: 5. Start Minikube cluster using Docker driver
minikube start --driver=docker

:: 6. Check Minikube status
minikube status

:: 7. Check Kubernetes nodes
kubectl get nodes

:: 8. Check all Pods
kubectl get pods -A


:: ==========================================
:: CREATE KUBERNETES DEPLOYMENT
:: ==========================================

:: 9. Create Deployment with 2 replicas
kubectl create deployment springboot-deployment --image=YOUR_USERNAME/springboot-demo:latest --replicas=2

:: 10. View Deployments
kubectl get deployments

:: 11. View Pods
kubectl get pods

:: 12. Get detailed Deployment information
kubectl describe deployment springboot-deployment

:: 13. View Pods with node information
kubectl get pods -o wide

:: 14. View application logs
kubectl logs deployment/springboot-deployment


:: ==========================================
:: CREATE KUBERNETES SERVICE
:: ==========================================

:: 15. Create NodePort Service
:: Service port = 9095, Container port = 8080
kubectl expose deployment springboot-deployment --type=NodePort --port=9095 --target-port=8080

:: 16. View Services
kubectl get services

:: 17. Get detailed Service information
kubectl describe service springboot-deployment

:: 18. Get Minikube application URL
minikube service springboot-deployment --url

:: 19. Open the URL displayed in CMD in your browser


:: ==========================================
:: KUBERNETES SCALING
:: ==========================================

:: 20. Increase replicas to 3
kubectl scale deployment springboot-deployment --replicas=3

:: 21. Verify replica count
kubectl get deployments

:: 22. Check Pods
kubectl get pods


:: ==========================================
:: KUBERNETES CLEANUP
:: ==========================================

:: 23. Delete Service
kubectl delete service springboot-deployment

:: 24. Delete Deployment
kubectl delete deployment springboot-deployment

:: 25. Verify resources are deleted
kubectl get all

:: 26. Stop Minikube cluster
minikube stop


:: ==========================================
:: START KUBERNETES AGAIN
:: ==========================================

:: 27. Start Minikube
minikube start --driver=docker

:: 28. Check cluster nodes
kubectl get nodes

:: 29. Check cluster status
minikube status
# ==========================================
# DOCKER COMPOSE - CUSTOM IMAGE + MYSQL
# ==========================================

# 1. Create docker-compose.yml
# Add the following content:

services:
  app:
    image: your-dockerhub-username/your-image:latest
    container_name: my-app
    ports:
      - "8080:8080"
    depends_on:
      - db

  db:
    image: mysql:8
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: studentdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:


# 2. Pull images
docker compose pull

# 3. Start all containers in background
docker compose up -d

# 4. Check running containers
docker compose ps

# 5. View all logs
docker compose logs

# 6. View application logs
docker compose logs -f app

# 7. View database logs
docker compose logs -f db

# 8. Build custom image (if building locally)
docker compose build

# 9. Restart services
docker compose restart

# 10. Stop containers
docker compose stop

# 11. Start stopped containers
docker compose start

# 12. Stop and remove containers
docker compose down

# 13. Stop and remove containers + volumes
docker compose down -v

# 14. Validate compose file
docker compose config

# 15. Execute MySQL shell inside database container
docker exec -it mysql-db mysql -uroot -proot

# 16. List all containers
docker ps -a

# 17. List Docker images
docker images

# ==========================================
# IMPORTANT VIVA POINTS
# ==========================================
# Service       : Application or database definition
# Image         : Blueprint for creating a container
# Container     : Running instance of an image
# Ports         : Connect host port to container port
# Volumes       : Persist database data
# depends_on    : Defines service startup dependency
# Environment   : Pass configuration variables
# Database host : db
# Database port : 3306
# App port      : 8080
# ==========================================


# ==========================================
# KUBERNETES - NGINX WITH 2 REPLICAS
# ==========================================

# 1. Start Minikube
minikube start

# 2. Create deployment with 2 replicas
kubectl create deployment nginx-deployment --image=nginx

# 3. Scale deployment to 2 replicas
kubectl scale deployment nginx-deployment --replicas=2

# 4. Check deployments
kubectl get deployments

# 5. Check running pods
kubectl get pods

# 6. Expose deployment using NodePort
kubectl expose deployment nginx-deployment --type=NodePort --port=80

# 7. Check services
kubectl get services

# 8. Get detailed deployment information
kubectl describe deployment nginx-deployment

# 9. Get detailed pod information
kubectl describe pods

# 10. Open Nginx in browser (Minikube)
minikube service nginx-deployment

# 11. View logs
kubectl logs deployment/nginx-deployment

# 12. Delete service
kubectl delete service nginx-deployment

# 13. Delete deployment and its pods
kubectl delete deployment nginx-deployment

# 14. Stop Minikube
minikube stop

# ==========================================
# IMPORTANT KUBECTL COMMANDS
# ==========================================

# List all pods
kubectl get pods

# List all deployments
kubectl get deployments

# List all services
kubectl get services

# List all resources
kubectl get all

# Scale to 3 replicas
kubectl scale deployment nginx-deployment --replicas=3

# Delete a pod
kubectl delete pod <pod-name>

# ==========================================





Q1 (a) Functional and Non-Functional Requirements
System: Food Ordering System

A Food Ordering System allows students and faculty to order food online, make digital payments, receive real-time order status updates, and choose between dine-in and takeaway options. Administrators can manage the menu.
1. Functional Requirements
Functional requirements describe what the system should do.
1. User Registration and Login: Students and faculty should be able to register and log in to the system.
2. View Menu: Users should be able to view available food items, prices, and descriptions.
3. Place Orders: Users should be able to select food items and place food orders.
4. Digital Payments: The system should support online payments through digital payment methods.
5. Order Tracking: Users should receive real-time updates about their order status (Placed, Preparing, Ready, Delivered).
6. Dine-in and Takeaway: Users should be able to choose either dine-in or takeaway options.
7. Menu Management: Administrators should be able to add, update, and delete food items.
8. Order Management: Administrators should be able to view and manage customer orders.
9. Order Confirmation: The system should generate order confirmation after successful placement and payment.
10. Non-Functional Requirements
Non-functional requirements describe how the system should perform.
1. Performance: The system should respond quickly to user requests and process orders without unnecessary delays.
2. Security: User information and payment details should be protected from unauthorized access.
3. Reliability: The system should operate continuously without frequent failures.
4. Usability: The system should have a simple and user-friendly interface.
5. Scalability: The system should support an increasing number of students and faculty users.
6. Availability: The system should be available whenever users need to place orders.
7. Maintainability: The system should allow easy updates and modifications.
8. Accuracy: The system should accurately calculate bills, process payments, and update order statuses.
Difference between Functional and Non-Functional Requirements
Functional Requirements	Non-Functional Requirements
Describe what the system does.	Describe how the system performs.
Define system features.	Define quality attributes.
Example: Place an order.	Example: Fast response time.
Example: Online payment.	Example: Secure payment.
Example: Manage menu.	Example: System reliability.
