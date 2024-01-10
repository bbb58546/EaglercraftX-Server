# Dockerfile
FROM ubuntu:latest

RUN apt-get update && \
   apt-get install -y tmux git default-jdk wget && \
   rm -rf /var/lib/apt/lists/*
