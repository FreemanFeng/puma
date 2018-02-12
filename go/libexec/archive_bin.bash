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

mkdir bin && cd bin

rsync -a $SRTPATH/../bin/$PROJECT .

cd /vobs/tmp && tar czf ${PROJECT}_bin.tar.gz ${PROJECT}

cp ${PROJECT}_bin.tar.gz /innova/archived/
