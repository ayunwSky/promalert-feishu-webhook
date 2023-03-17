#!/bin/bash

docker rmi promalert-feishu-webhook-v2:v0.0.1
docker build -t promalert-feishu-webhook-v2:v0.0.1 .
