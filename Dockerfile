FROM python:3

USER root
ARG home="/root"

RUN apt-get update
RUN apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# Install GCP client
RUN curl https://sdk.cloud.google.com | bash
ENV PATH ${home}/google-cloud-sdk/bin:$PATH

# Setup requiredements
RUN mkdir -p ${home}/cache
COPY ./app/functions/requirements.txt ${home}/cache/requirements.txt
RUN pip install -r ${home}/cache/requirements.txt

## Get latest GoogleAd API
#RUN git clone https://github.com/googleads/google-ads-python ${home}/cache/google-ads-python
#RUN pip install -e ${home}/cache/google-ads-python

## Get latest FaceBook API
#RUN git clone https://github.com/facebook/facebook-python-business-sdk ${home}/cache/facebook-python-business-sdk
#RUN pip install -e ${home}/cache/facebook-python-business-sdk

## Get latest GoogleAnalytics API
#RUN git clone https://github.com/googleapis/google-api-python-client ${home}/cache/google-api-python-client
#RUN pip install -e ${home}/cache/google-api-python-client