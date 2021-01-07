FROM python:3.8-buster
LABEL maintainer="https://github.com/watanta"

# set timezone for OS by root
USER root

RUN apt update
RUN apt install -y default-jdk
RUN wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | apt-key add -
RUN sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt update
RUN apt install -y jenkins
# CMD ["systemctl", "enable","--now","jenkins"] 
# CMD ["service", "jenkins", "start"]

RUN apt install -y vim 
RUN pip install scrapy
RUN pip install pandas
RUN pip install sqlalchemy
RUN pip install lightgbm


# set timezone for Java runtime arguments
ENV JAVA_OPTS=-Duser.timezone=Asia/Tokyo

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime