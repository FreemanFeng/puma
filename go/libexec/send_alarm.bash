#!/bin/bash
data=$1
shift
host=$1
shift
port=$1

if [ -z "$host" ]; then
    host=localhost
fi

if [ -z "$port" ]; then
    port=8088
fi

curl -H "Content-Type: application/json" --data @$data $host:$port/auto/dingding
