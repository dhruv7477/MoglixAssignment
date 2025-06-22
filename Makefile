.PHONY: build run stop clean

# Build the Docker image
build:
	docker build -t document-qa .

# Run the container with both services
run: stop
	docker run -d \
		-p 8000:8000 \
		-p 8501:8501 \
		--name document-qa-container \
		document-qa

# Stop the running container
stop:
	docker stop document-qa-container
	docker rm document-qa-container

# Clean up containers and images
clean: stop
	docker rmi document-qa