#!/bin/bash
project=$1
shift
output=$1
shift
params=$@

ulimit -c unlimited

SRTPATH=$(cd "$(dirname "$0")"; pwd)

if [ -z "$output" ]; then
    output=$SRTPATH/../output
    if [ ! -d $output ]; then
        mkdir -p $output
    fi
fi

timestamp=`date +%Y%m%d_%H%M%S`

export PATH=$SRTPATH/../bin:$PATH

cd $output && pybot $params $SRTPATH/../testing/$project/testcases
