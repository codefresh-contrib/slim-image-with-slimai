# codefresh-contrib/slim-image-with-slimai

This repo is the source for the [Slim.AI SaaS Build for Codefresh image](#docker-image-location). This README covers information such as how to use the image, current limitations, and development work on the image.

# Table of Contents

- [Quick Start](#quick-start)
- [Docker image location](#docker-image-location)
- [Limitations](#limitations)
    - [Single image namespace/repo:tag](#single-image-namespacerepotag)
    - [Single connector ID](#single-connector-id)
    - [Image digest requires manually grabbing](#image-digest-requires-manually-grabbing)
         - [Codefresh platform](#codefresh-platform)
         - [Outside Codefresh platform](#outside-codefresh-platform)
    - [Slim.AI Organization ID](#slimai-organization-id)
    - [Image must be pushed to your target's connector](#image-must-be-pushed-to-your-targets-connector)
- [Development](#development)


# Quick Start

A very simple script (`./run.sh`) is available for quickly testing this image. Simply modify the variables under "Image details" and "Slim details" and execute the script.

# Docker image location

You can currently use this image as `mstantoncf/slim-saas-build` or build your own:

```bash
docker build -t $imageName -f Dockerfile .
```

# Limitations

Currently, the below categories are limitations of this image

### Single image namespace/repo:tag

While the image can *technically* be slightly modified to use a target/destination namespace/repo:tag, the image is only configured to use the same namespace/repo:tag combination for both target/desination. The only difference is that the destination appends `-slim`.
### Single connector ID

While it can be easily updated, the image currently only supports using a single connector ID. Which means that you'll need to make sure that the connector has access to the target and destination namespace/repo.

### Image digest requires manually grabbing

#### Codefresh platform
If you are using this image on the Codefresh platform, there is no manual intervention needed as the image digest is provided through a varaible. For details: <https://codefresh.io/docs/docs/pipelines/variables/#step-member-variables>

#### Outside Codefresh platform
Currently, there is no way for the image to know the image digest of the target image. Therefore, it must manually be provided using the `-d | --digest` flag. That being said, you can easily collect the target image digest by running: `docker image inspect <namespace>/<repo>:<tag> | jq .[].RepoDigests -c | cut -d : -f 2 | cut -d '"' -f 1` (This assumes the image is already pulled to the local machine)
### Slim.AI Organization ID

This isn't neccisarly a limitation of the image as much as it is of Slim.AI as there isn't an easy way to fetch the Organization ID. The easiest way to get this detail (from what we've found) is to:

1. Navigate to https://portal.slim.dev/home (Make sure to login)
1. Open your browser's "Dev Tools" and go to the "Network" tab
1. Refresh the page
1. Search for one of the following requests: `all`, `collections`, `namespaces`
1. While inside the "Headers" tab for one of the above requests, you should see the a "Request URL" pattern similar to: `https://portal.slim.dev/bff/orgs/rko.XXXXXXXXXXXXXXXXXXXXXXXXXXX/<Request-Name>` where:
   * `<Request-Name>` - The name of the request collected form the step above
   * `rko.XXXXXXXXXXXXXXXXXXXXXXXXXXX` - Your Organization ID

Hopefully there will be an easier way to collect the Organization ID in a future release (or there already is) but this is what we found to be the easiest and simplest way to collect this information.

### Image must be pushed to your target's connector

This isn't fully a limitation as it's more or so expected behavior as since this is using the Slim.AI (SaaS) platform, it's expected that the image is available via the target's connector. This means that you must push your image to the registry first, and then run this image. Otherwise, the image will throw an error as the target image does not exist.

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


