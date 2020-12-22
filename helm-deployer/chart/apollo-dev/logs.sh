#!/bin/bash

source .buildenv

docker container logs -f ${CONTAINER}

