#!/bin/bash
# Image details
imageNamespace=""
imageRepo=""
imageTag=""
imageDigest="" # docker image inspect <namespace>/<repo>:<tag> | jq .[].RepoDigests -c | cut -d : -f 2 | cut -d '"' -f 1)
# Slim details
slimOrganizationID=""
slimAPIToken=""
slimConnectorID=""

#####################
runtimeImage="mstantoncf/slim-saas-build"
docker run --rm $runtimeImage \
-o $slimOrganizationToken -a $slimAPIToken -c $slimConnectorID \
-n $imageNamespace -r $imageRepo -t $imageTag -d $imageDigest