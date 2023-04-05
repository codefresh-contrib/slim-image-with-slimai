#!/bin/bash
helpMenu(){
    echo "Usage: slim-saas-build [flags...]"
    echo ""
    echo "Flags:"
    echo "  -a | --api-token        |   API token to access slim.ai (https://portal.slim.dev/settings)"
    echo "  -o | --organization-id  |   Organization ID in slim.ai"
    echo "  -c | --connector-id     |   Connector ID of slim.ai Registry"
    echo "  -d | --digest           |   Digest for the Docker image (docker image inspect <namespace>/<repo>:<tag> | jq .[].RepoDigests -c | cut -d ":" -f 2 | cut -d '\"' -f 1)"
    echo "  -n | --namespace        |   Namespace for Docker image (I.e <namespace>/<repo>:<tag>)"
    echo "  -r | --repo             |   Repo for Docker image (I.e <namespace>/<repo>:<tag>)"
    echo "  -t | --tag              |   Tag for Docker image (I.e <namespace>/<repo>:<tag>)"
    echo "  -m | --arch             |   (Optional) Image Architecture (Default: amd64)"
    echo "  -s | --operating-system |   (Optional) Image Operating System (Default: linux)"
    echo "  -p | --paths            |   (Optional) Paths on filesystem to slim in comma separated list (I.e /usr,/bin,/etc)"
}

# Run through requirements
requirements(){
    itemList=("apiToken" "organizationID" "connectorID" "digest" "namespace" "repo" "tag")
    # Iterate over required items
    for item in ${itemList[@]}; do
        # Checks the value of the item var from list to ensure a value is set
        # If item is 'paths' it does not check for this as that item is optional
        if [[ ${!item} == "" ]]; then
          echo "ERROR: Requirement ($item) not met"
          exit 1
        fi
    done
    # Iterate over optional items (Stored with default values)
    optionalItemsList=("arch=amd64" "os=linux" "paths=none")
    if [[ "$arch" == "" ]]; then
      arch="amd64"
    fi
    if [[ "$os" == "" ]]; then
      os="linux"
    fi
    if [[ $paths == "" ]]; then
      paths="none"
    fi
}

# Pre-flight
## Verify there is input
if [[ "$*" == "" ]]; then
    echo "ERROR: No flags were set"
    echo "-"
    helpMenu
    exit 1
fi
## Process flags
while [ "$1" != "" ]; do
  case $1 in
    -h | --help)            helpMenu
                            exit
                            ;;
    -o | --organization-id) shift
                            organizationID=$1
                            ;;
    -a | --api-token)       shift
                            apiToken=$1
                            ;;
    -c | --connector-id)    shift
                            connectorID=$1 
                            ;;
    -d | --digest)          shift
                            digest=$1
                            ;;
    -n | --namespace)       shift
                            namespace=$1 
                            ;;
    -r | --repo)            shift
                            repo=$1 
                            ;;
    -t | --tag)             shift
                            tag=$1 
                            ;;
    -m | --arch)            shift
                            arch=$1
                            ;;           
    -s | --operating-system) shift
                            os=$1
                            ;;
    -p | --optional-paths)  shift
                            paths=$1
                            ;;
  esac
  shift
done
## Check requirements are met
requirements
# Handoff
executionScript="python ./scripts/execution.py"
$executionScript $apiToken $organizationID $connectorID $digest $namespace $repo $tag $arch $os $paths
exit 0
