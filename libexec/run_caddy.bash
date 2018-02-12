#!/bin/bash

port=$1

ulimit -n 8192

SRTPATH=$(cd "$(dirname "$0")"; pwd)

timestamp=`date +%Y%m%d_%H%M%S`

export PATH=$SRTPATH/../bin:$PATH

if [ -z "$port" ]; then
    caddy
else
    caddy -port $port
fi
