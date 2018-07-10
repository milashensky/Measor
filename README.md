# Measor

A very simple system for monitoring web applications, using raw python code with splinter in its tasks. It does not even use the database.
All tasks are run inside of docker container, for better system safety.

Inside of docker container we have splinter and headless chrome browser, so you can wrote something like this:
```python
from splinter import Browser

with Browser('chrome') as browser:
    # Visit URL
    url = "http://www.google.com"
    browser.visit(url)
    browser.fill('q', 'splinter - python acceptance testing for web applications')
    # Find and click the 'search' button
    button = browser.find_by_css('.lsb')
    # Interact with elements
    button.click()
    if browser.is_text_present('splinter.readthedocs.io'):
        print("Yes, the official website was found!")
    else:
        print("No, it wasn't found... We need to improve our SEO techniques")
```
And it will run correctly.

If you like to change docker image for your needs, maybe you should checkout branch `docker-image`.

After creating your own image you should set its name in settings.py (or local_settings.py).
```python
DOCKER_IMAGE_NAME = 'milashensky/measor_tasks_runner'
```


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
