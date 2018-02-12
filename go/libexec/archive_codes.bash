#!/bin/bash

SRTPATH=$(cd "$(dirname "$0")"; pwd)

PROJECT=quantum

cd /vobs/tmp

if [ -d /vobs/tmp/$PROJECT ]; then
    rm -rf /vobs/tmp/$PROJECT
fi

mkdir $PROJECT && cd $PROJECT

rsync -a $SRTPATH/../libexec .
rsync -a $SRTPATH/../data .

mkdir -p src

rsync -a $SRTPATH/../src/$PROJECT src/

cd /vobs/tmp && tar czf ${PROJECT}_src.tar.gz ${PROJECT}

cp ${PROJECT}_src.tar.gz /innova/archived/
