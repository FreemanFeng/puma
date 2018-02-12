#!/bin/bash

params=$*

SRTPATH=$(cd "$(dirname "$0")"; pwd)

export GOROOT=/vobs/tools/go
export GOPATH=$SRTPATH/../go

$GOROOT/bin/go $params
