#!/bin/bash
project=$1
shift
output=$1
shift
params=$@

SRTPATH=$(cd "$(dirname "$0")"; pwd)

if [ -z "$project" ]; then
    project=ucstart
fi

if [ -z "$output" ]; then
    output=$SRTPATH/../output
    if [ ! -d $output ]; then
        mkdir -p $output
    fi
fi

./run_robot.bash $project $output --loglevel INFO -e disable $params
