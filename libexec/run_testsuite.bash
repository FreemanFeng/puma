#!/bin/bash
project=$1
shift
suite=$1
shift
output=$1
shift
params=$@

SRTPATH=$(cd "$(dirname "$0")"; pwd)

if [ -z "$output" ]; then
    output=$SRTPATH/../output
    if [ ! -d $output ]; then
        mkdir -p $output
    fi
fi

./run_robot.bash $project $output -s $suite --loglevel INFO $params
