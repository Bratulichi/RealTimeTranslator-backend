IMAGE_NAME = wepal/realtime-translator/backend
DOCKERFILE = Dockerfile
CONTEXT = .

tag = $(shell cat $(CONTEXT)/version.txt)

IMAGE = $(IMAGE_NAME):$(tag)

all: build

build:
	@docker build -f $(DOCKERFILE) -t $(IMAGE) $(CONTEXT)

pull:
	@docker pull $(IMAGE)

push: docker-login
	@docker push $(IMAGE)

docker-login:
	@echo "Logging in to Docker registry..."
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)