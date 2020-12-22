#!/bin/sh

cd charts

# Build a gitlab ci yaml file containing a job for each deployment
cat << EOF
image: "registry.gitlab.com/gitlab-org/cluster-integration/auto-deploy-image:v0.8.3"
stages:
  - deploy
EOF

for A in */; do
    app=${A%"/"}
    app_caps=$(echo "${app}" | tr '[a-z]' '[A-Z]')
    app_disabled_var="DISABLE_${app_caps}"

    # Check if app is disabled (DISABLE_FOO=true) and if so, skip to the next.
    if [ "$(eval echo \$${app_disabled_var})" == "true" ]; then continue; fi
    
    # Generate the deployment pipeline
    cat << EOF
deploy ${app}:
  stage: deploy
  variables:    
    HELM_UPGRADE_VALUES_FILE: ../../values/${app}.yaml
  environment:
    name: ${app}
    url: https://${URL_PREFIX}${app}.${EP_SUBDOMAIN}.ep.shell.com
    on_stop: stop ${app}
  script:
    - cd charts/${app}
    - auto-deploy initialize_tiller
    - helm init --client-only
    - helm repo add stable https://charts.helm.sh/stable
    - auto-deploy check_kube_domain
    - auto-deploy download_chart
    - auto-deploy ensure_namespace
    - auto-deploy create_secret
    - auto-deploy deploy
    - auto-deploy persist_environment_url
stop ${app}:
  stage: deploy
  environment:
    name: ${app}
    action: stop
  when: manual
  script:
    - auto-deploy initialize_tiller
    - auto-deploy destroy
EOF
done
