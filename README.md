
# Progress

1. ✅ Process arguments (entrypoint)
1. ✅ Construct JSON payload (`createFlags()` / `generateRequest()`)
    * Template is in `./templates/execution.payload.json`
1. ✅ Send payload to Slim.AI (`execute()`)
1. ✅ Watch for payload changes (`watch()`)
    * Problem: For some reason the build is failing, so I need to investigate why. I'm thinking it has to do with the payload that is being sent.
    * TODO:
        1. ✅ Get build status (`watch()`)
        2. ✅ Get events (Only reports when `results(<execution-id>, true)` as the events don't really give you much unless there is a failure)
        3. ✅ Get build logs (`getLogs()`)
1. ✅ Cleanup `./tmp` (`doTmpDir("delete)`)
1. ✅ Debug why executions are failing
1. ✅ Verify file was pushed to image registry successfully
1. ✅ Package container image + build container image

# Quick Start

A very simple script (`./run.sh`) is available for quickly testing this image. Simply modify the variables under "Image details" and "Slim details" and execute the script.

# Development

## Usage

```bash
Usage: slim-saas-build [flags...]

Flags:
  -a | --api-token        |   API token to access slim.ai (https://portal.slim.dev/settings)
  -o | --organization-id  |   Organization ID in slim.ai
  -c | --connector-id     |   Connector ID of slim.ai Registry
  -d | --digest           |   Digest for the Docker image (docker image inspect <namespace>/<repo>:<tag> | jq .[].RepoDigests -c | cut -d : -f 2 | cut -d '"' -f 1)
  -n | --namespace        |   Namespace for Docker image (I.e <namespace>/<repo>:<tag>)
  -r | --repo             |   Repo for Docker image (I.e <namespace>/<repo>:<tag>)
  -t | --tag              |   Tag for Docker image (I.e <namespace>/<repo>:<tag>)
  -m | --arch             |   (Optional) Image Architecture (Default: amd64)
  -s | --operating-system |   (Optional) Image Operating System (Default: linux)
  -p | --paths            |   (Optional) Paths on filesystem to slim in comma separated list (I.e /usr,/bin,/etc
```

## Example execution

```bash
# Build image
docker build -t slim-saas-build -f Dockerfile .
# Run slim-saas-build
docker run --rm slim-saas-build -o <organization-id> \
 -a <api-token> \
-c <connector-id> \
-n codefresh -r cli -t latest \
-d e64398f0928281d8154c9d5db155eaf854a968730a6d20a2e72ad9ffc12760f3
```
## Notes

If you would like to use `entrypoint.sh` locally, make sure to use `entrypoint-dev.sh` as this contains the correct paths. `entrypoint.sh` is set up for usage inside the container image.


