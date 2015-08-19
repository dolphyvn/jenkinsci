#!/bin/sh

JAVA_HOME=/opt/java
ANT_HOME=/opt/ant
export ANT_HOME
export JAVA_HOME
PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$PATH
export PATH

proj="${1}" 
env="${2}"

echo "cd /opt/auto/svn/data/$proj/$env"

cd /opt/auto/svn/data/$proj/$env

echo "ant -f build.xml clean"

/opt/ant/bin/ant -f build.xml clean

echo "ant -f build.xml -Djavac.debug=$debug -Ddist.jar=bin/$proj.jar jar "

/opt/ant/bin/ant -f build.xml -Djavac.debug=$debug -Ddist.jar=bin/$proj.jar jar
rm -rif /opt/auto/svn/data/$proj/$env/build
chown -R jenkins:jenkins /opt/auto/svn/data/$proj
