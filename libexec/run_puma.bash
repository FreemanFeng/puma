#!/bin/bash

app=$@

SRTPATH=$(cd "$(dirname "$0")"; pwd)

timestamp=`date +%Y%m%d_%H%M%S`

export PATH=$SRTPATH/../bin:$PATH

python $SRTPATH/../src/run.py $app
