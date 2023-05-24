1. Downloads files from git repository
2. Go to the Dockerfile folder. Create a Docker image using Dockerfile by running the following command:
sudo docker build -t myimage .
3. After the Docker image is built successfully, run it using the following command:
docker run -p 8080:8080 myimage 
4. This command starts the Docker container. You can access the application at http://0.0.0.0:8080/api/docs in your web browser.
