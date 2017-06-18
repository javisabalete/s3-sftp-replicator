FROM amazonlinux:latest

ENV PROJ_PATH /root/proj

WORKDIR $PROJ_PATH

RUN curl -O -s https://bootstrap.pypa.io/get-pip.py && python get-pip.py

RUN yum install -y python27-devel libffi-devel openssl-devel gcc zip

RUN pip install virtualenv
RUN virtualenv $PROJ_PATH
RUN source $PROJ_PATH/bin/activate