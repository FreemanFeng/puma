#!/bin/bash

SRTPATH=$(cd "$(dirname "$0")"; pwd)

timestamp=`date +%Y%m%d_%H%M%S`

export PATH=$SRTPATH/../bin:$PATH

cd $SRTPATH/../testing && python TestLibrary.py
