# Measor

A very simple system for monitoring web applications, using raw python code with splinter in its tasks. It does not even use the database.
All tasks are run inside of docker container, for better system safety.

### How to start

* Install docker. You can find the install information by clicking on  [this link](https://docs.docker.com/install/).
* Clone repository
* Install requirements and clone docker image of runner:
`make`
* Create user:
`./manage.py create_user`
* Start:
`./manage.py runserver`
* Create first task and enjoy!
