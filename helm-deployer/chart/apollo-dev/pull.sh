#!/bin/bash

source .buildenv

docker image pull ${REGISTRY}${IMAGE}${TAG}

