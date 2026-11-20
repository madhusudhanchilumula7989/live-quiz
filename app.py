# ==========================================
# 1. UPDATE UBUNTU
# ==========================================

sudo apt update -y
sudo apt upgrade -y

# ==========================================
# 2. INSTALL DEPENDENCIES
# ==========================================

sudo apt install -y curl wget git unzip nano ca-certificates gnupg

# ==========================================
# 3. ADD DOCKER GPG KEY
# ==========================================

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
-o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

# ==========================================
# 4. ADD DOCKER REPOSITORY
# ==========================================

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# ==========================================
# 5. INSTALL DOCKER
# ==========================================

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# ==========================================
# 6. START AND ENABLE DOCKER
# ==========================================

sudo systemctl enable --now docker

# ==========================================
# 7. GIVE USER DOCKER PERMISSIONS
# ==========================================

sudo usermod -aG docker $USER

newgrp docker

# ==========================================
# 8. VERIFY DOCKER INSTALLATION
# ==========================================

docker --version
docker compose version

# ==========================================
# 9. TEST DOCKER
# ==========================================

docker run hello-world

# ==========================================
# 10. PULL DOCKER IMAGE
# ==========================================

docker pull YOUR_DOCKER_IMAGE:latest

# ==========================================
# 11. RUN DOCKER CONTAINER
# ==========================================

docker run -d \
--name my-container \
-p 8000:8000 \
--restart unless-stopped \
YOUR_DOCKER_IMAGE:latest

# ==========================================
# 12. VERIFY RUNNING CONTAINER
# ==========================================

docker ps

# ==========================================
# 13. CHECK CONTAINER LOGS
# ==========================================

docker logs my-container

# ==========================================
# 14. CHECK PUBLIC IP
# ==========================================

curl -4 ifconfig.me

# ==========================================
# 15. CHECK DOCKER DISK USAGE
# ==========================================

docker system df
