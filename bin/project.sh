#!/bin/sh

proj="${1}" 
env="${2}"
url="${3}"


echo "cd /opt/auto/svn/data/$proj/$env"
cd /opt/auto/svn/data/$proj/$env
echo "svn co $url ./ --username svnsync"
svn co $url ./  --username svnsync
#chown -R 7039:7039 /opt/auto/svn/data/$proj/
