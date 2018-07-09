FROM ubuntu:16.04

# Install prerequisites
RUN apt-get update && apt-get install -y \
curl

RUN apt-get update \
    && apt-get install -y software-properties-common curl \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get remove -y software-properties-common \
    && apt autoremove -y \
    && apt-get update \
    && apt-get install -y python3.6 \
    && curl -o /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py" \
    && python3.6 /tmp/get-pip.py \
    && apt-get remove -y curl \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

FROM markadams/chromium-xvfb

RUN apt-get install -y git
RUN apt-get update && apt-get install -y \
    python python-pip curl unzip libgconf-2-4

RUN apt-get install -y python3 \
    && apt-get install -y python3-pip

ENV CHROMEDRIVER_VERSION 2.31

RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
  && unzip "chromedriver_linux64.zip" -d /usr/local/bin \
  && rm "chromedriver_linux64.zip"

# RUN git clone https://github.com/milashensky/Measor.git /usr/src/app

COPY . /usr/src/app
WORKDIR /usr/src/app

# RUN git checkout docker-image
RUN pip install -r requirements.txt
RUN pip3 install -r requirements.txt


CMD ["python3", "app.py"]
