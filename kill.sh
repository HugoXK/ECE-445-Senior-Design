#!/bin/bash

port=$1
pid=$(lsof -t -i:$port)

if [ ! -z "$pid" ]; then
    echo "kill $pid"
    kill $pid
else 
    echo "no process"
fi