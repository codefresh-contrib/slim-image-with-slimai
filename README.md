
# Progress

1. ✅ Process arguments (entrypoint)
1. ✅ Construct JSON payload (`createFlags()` / `generateRequest()`)
    * Template is in `./templates/execution.payload.json`
1. ✅ Send payload to Slim.AI (`execute()`)
1. ➖ Watch for payload changes (`watch()`)
    * Currently, it's set to skip `execute()` and a static variable is to be set (`getExecutionID`) in `main()` simply for the fact that I didn't want to send off hundreds of build requests. With this, it's simply querying the API for the data and returning it.
    * Problem: For some reason the build is failing, so I need to investigate why. I'm thinking it has to do with the payload that is being sent.
    * TODO:
        1. Get build status
        2. Get events
        3. Get build logs
1. ❌ Cleanup `./tmp` (`doTmpDir("delete)`)
1. ❌ Verify file was pushed to image registry successfully
1. ❌ Package container image + build container image


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

# Example execution (dev)

```bash
./scripts/entrypoint.sh -o <organization-id> \
 -a <api-token> \
-c <connector-id> \
-n codefresh -r cli -t latest \
-d e64398f0928281d8154c9d5db155eaf854a968730a6d20a2e72ad9ffc12760f3
```