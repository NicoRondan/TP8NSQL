FROM python:latest
WORKDIR /src
COPY . /src
RUN pip3 install flask firebase-admin 
EXPOSE 5000