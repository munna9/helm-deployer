#!/bin/sh
cd charts

echo "kubeconfig: $KUBECONFIG:"
cat $KUBECONFIG

# Check to ensure values file is present for each chart
for D in */; do
    if [ ! -f ../values/${D%"/"}.yaml ]; then
        >&2 echo "values/${D%"/"}.yaml was not found"
        exit 1
    fi
done
