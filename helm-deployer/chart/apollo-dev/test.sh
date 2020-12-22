#!/bin/bash -e

source .buildenv

if ! docker info &>/dev/null; then
  if [ -z "$DOCKER_HOST" ] && [ "$KUBERNETES_PORT" ]; then
    export DOCKER_HOST='tcp://localhost:2375'
  fi
fi

if [[ -n "$CI_REGISTRY" && -n "$CI_REGISTRY_USER" ]]; then
  echo "Logging in to GitLab Container Registry $CI_REGISTRY with CI credentials..."
  docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  export REGISTRY=""
  export IMAGE="$CI_APPLICATION_REPOSITORY"
  export TAG=":$CI_APPLICATION_TAG"
fi

if [ -t 1 ]
then
    export MODE=-it
else
    export MODE=
fi

echo "Testing ${IMAGE} ..."

docker container run ${RUN_OPTS} ${CONTAINER_NAME}-test ${MODE} --rm ${NETWORK} ${PORT_MAP} ${VOL_MAP} ${REGISTRY}${IMAGE}${TAG} sh -c "for t in \$(ls /test*.sh); do echo Running test \$t; \$t; done;" 
