all: install

install:
	@pip install -Ur requirements/base.txt

kill_docker:
	@docker kill measor_tasks_runner
	@docker rm measor_tasks_runner
