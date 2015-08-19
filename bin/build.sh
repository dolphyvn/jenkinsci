#!/bin/sh
#isdebug=$1
#debug="false"
#if [ "true" = "$isdebug" ]
#then
#  debug="true"
#fi
echo "ant -f build.xml clean"
/opt/ant/bin/ant -f build.xml clean
echo "ant -f build.xml -Djavac.debug=$debug -Ddist.jar=bin/AvayaService.jar jar "
/opt/ant/bin/ant -f build.xml -Djavac.debug=$debug -Ddist.jar=bin/PromotionService.jar jar
