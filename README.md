1. Downloads files from git repository
2. Build the Docker image using the Dockerfile by running the following command: 
sudo docker build -t newimage:latest .
3. After the Docker image is built successfully, run it using the following command:
docker run -p 8080:8080 <image-name>
4. This command runs the Docker container and maps the container's port 8080 to the host's port 8080 so that you can access the application at http://localhost:8080 in your web browser.
