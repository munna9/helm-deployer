#!/bin/bash

source .buildenv

docker image push ${REGISTRY}${IMAGE}${TAG}

