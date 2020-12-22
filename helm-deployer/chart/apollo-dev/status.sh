#!/bin/bash

source .buildenv

docker ps -a | grep ${CONTAINER}

