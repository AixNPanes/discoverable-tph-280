.PHONY: c clean \
	f format \
	h help \
	publish \
	wheel

h: help
c: clean
f: format

help:
	@echo "Options:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# If this pukes trying to import paho, try running 'poetry install'
# Or on Raspberry PI try export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
MODULE_VERSION=$(shell poetry run python3 -c 'import toml;print(toml.loads(open("pyproject.toml", "r").read())["tool"]["poetry"]["version"])' )
MODULE_USER=aixnpanes
MODULE_NAME=discoverable-tph-280
MODULE_DIR=$(shell echo $(MODULE_NAME) | tr '-' '_')
MODULE_TEST=$(MODULE_NAME)-test
MODULE_TAG=$(shell echo "$(MODULE_NAME)" | tr '-' '_')
MODULE_TAG_LATEST=$(shell echo $(MODULE_NAME) | tr '-' '_')
PYTHON_VERSION=3.$(shell find /usr/bin/ /usr/local/bin -name 'python3.*' | sed -e '/-config/d' -e 's/.*python3.//'|sort -n -u|tail -1)
SERVICE_NAME=tph_280

all: install_hooks toc multiarch_image publish ## Install all necessary items

install_hooks: ## Install the git hooks
	poetry run pre-commit install

toc: *.md ## Runs 'doctoc' to format the Table of Contents for the README files
	doctoc $?

multiarch_image: wheel ## Makes a multi-architecture docker image for linux/arm64, linux/amd64 and linux/arm/v7 and pushes it to dockerhub, if this fails try docker buildx create --name mybuilder; docker buildx use mybuilder; docker buildx inspect --bootstrap ALSO docker login
	docker system prune --force
	docker buildx build --no-cache --build-arg application_version=${MODULE_VERSION} --platform linux/arm64,linux/amd64,linux/arm/v7 --push -t $(MODULE_USER)/$(MODULE_TAG):$(MODULE_VERSION) -t $(MODULE_USER)/$(MODULE_TAG):latest .
	make local

wheel: clean format ## Builds a wheel for our modules. 'poetry' bakes the dependencies into the wheel metadata.
	poetry build

clean: ## Cleans out stale wheels, generated tar files, .pyc and .pyo files
	rm -fv dist/*.tar dist/*.whl
	find . -iname '*.py[co]' -delete

format: install_poetry ## Runs 'black' on all our python source files
	poetry run black --line-length 79 $(MODULE_DIR)

install_poetry:
	poetry >/dev/null|| pip$(PYTHON_VERSION) install poetry black

local: wheel requirements.txt ## Makes a docker image for only the architecture we're running on. Does not push to dockerhub.
	docker buildx build --load -t $(MODULE_USER)/$(MODULE_TAG):$(MODULE_VERSION) -f Dockerfile.testing .
	docker tag $(MODULE_USER)/$(MODULE_TAG):$(MODULE_VERSION) $(MODULE_USER)/$(MODULE_TAG):latest

# We use this to enable the Dockerfile.testing have a separate layer for the
# dependencies so we don't have to reinstall every time we test a new change.
# Our wheel includes its dependencies in the metadata so you don't need a
# requirements.txt file to use them
requirements.txt: wheel poetry.lock pyproject.toml Makefile ## Builds a requirements.txt to Dockerfile.testing can cache installing the python dependencies. poetry includes the deps in our wheel metadata, requirements.txt is not needed other than for test images.
	poetry export -o requirements.txt


publish: ## Publishes the module to pypi --- if this fails use poetry config pypi-token.pypi [token], log in to pypi.org and get an API token
	poetry publish

testing: ## Builds a local image for testing
	docker buildx build -f Dockerfile.testing . --load -t $(MODULE_USER)/$(MODULE_TAG):$(MODULE_VERSION) -t $(MODULE_USER)/$(MODULE_TAG):latest

install: ## Install wheel
	sudo pip$(PYTHON_VERSION) install $(MODULE_NAME) --upgrade
	[ -f /usr/local/bin/$(SERVICE_NAME).service ] || ( \
		sudo cp $(SERVICE_NAME).service /etc/systemd/system/ && \
		sudo chmod u+rx /etc/systemd/system/$(SERVICE_NAME).service && \
		sudo systemctl daemon-reload && \
		sudo systemctl restart $(SERVICE_NAME) \
		)
