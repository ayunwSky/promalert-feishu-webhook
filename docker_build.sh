#!/bin/bash
# *******************************************
# -*- CreateTime  :  2023/03/15 09:55:22
# -*- Author      :  Allen_Jol
# -*- FileName    :  docker_build.sh
# *******************************************

DATE=$(date +'%Y%m%d')
TIMESTAMP=$(date +%s)

docker build -t promalert-feishu-webhook:${DATE}-v${TIMESTAMP} .
sed -i "s@TAG@${DATE}-v${TIMESTAMP}@g" docker-compose.yml
