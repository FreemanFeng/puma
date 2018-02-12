#!/bin/bash

SRTPATH=$(cd "$(dirname "$0")"; pwd)

################################################
# 需安装go并设置环境变量 https://golang.org/dl/
# export GOROOT=/vobs/tools/go
# export GOPATH=$SRTPATH/../
################################################
export GOROOT=/vobs/tools/go
export GOPATH=$SRTPATH/../

rm -rf  $SRTPATH/../src/github.com/pquerna/ffjson
go get -u github.com/pquerna/ffjson

rm -rf  $SRTPATH/../src/github.com/satori/go.uuid
go get -u github.com/satori/go.uuid

rm -rf  $SRTPATH/../src/github.com/boltdb/bolt
go get -u github.com/boltdb/bolt

# Build Caddy
rm -rf  $SRTPATH/../src/github.com/mholt/caddy/caddy
go get -u github.com/mholt/caddy/caddy

rm -rf  $SRTPATH/../src/github.com/caddyserver/builds
go get -u github.com/caddyserver/builds

cd $SRTPATH/../src/github.com/mholt/caddy/caddy
go run build.go
if [ -f ./caddy ]; then
    rsync -a caddy $SRTPATH/../../bin/
    rsync -a caddy $SRTPATH/../bin/
fi
cd $SRTPATH
