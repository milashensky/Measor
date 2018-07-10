all: install pull_docker

install:
	@pip install -Ur requirements/base.txt

pull_docker:
	@docker pull milashensky/measor_tasks_runner

kill_docker:
	@docker kill measor_tasks_runner
	@docker rm measor_tasks_runner
