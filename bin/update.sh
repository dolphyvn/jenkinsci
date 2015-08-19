#!/bin/sh

proj="${1}" 
env="${2}"
action="${3}"

echo "cd /opt/auto/svn/data/$proj/$env"
cd /opt/auto/svn/data/$proj/$env
echo "svn cleanup"
svn cleanup
echo "svn $action --username svnsync"
svn $action --username svnsync
chown -R jenkins:jenkins /opt/auto/svn/data/$proj
chown -R jenkins:jenkins /opt/auto/svn/data/$proj/$env/.svn/*
