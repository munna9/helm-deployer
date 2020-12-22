#!/bin/sh

# Get (the first thousand) CI/CD variables from src project
variables=$(curl --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" "https://gitlab.ep.shell.com/api/v4/projects/${SRC_ID}/variables?per_page=1000" | jq -c '.[]')

# Tell bash to iterate on newlines only
OLD_IFS=${IFS}
IFS=$'\n'

# Post each one to the dst project's rest endpoint
for variable_json in ${variables}; do
    curl --request POST \
        --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        --header "Content-Type: application/json" \
        -d "${variable_json}" \
        "https://gitlab.ep.shell.com/api/v4/projects/${DST_ID}/variables/"
done

# Restore original IFS
IFS=${OLD_IFS}
