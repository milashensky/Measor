all: install build_static pull_docker

install:
	@pip install -Ur requirements/base.txt
	@cd static && yarn install && cd -

build_static:
	@cd static && yarn build-prod && cd -

pull_docker:
	@docker pull milashensky/measor_tasks_runner

kill_docker:
	@docker kill measor_tasks_runner
	@docker rm measor_tasks_runner
