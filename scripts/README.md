# Scripts directory

In this directory there are a few files which are critical for the image

# Directory tree

```bash
scripts
├── README.md # This file
├── entrypoint-dev.sh # entry point for development work
├── entrypoint.sh # entrypoint for docker image
├── execution.py # Python script for handling all logic and API calls for the image
└── requirements.txt # Requirements for python script
```

## Entrypoint script

Script which ensures all arguments have been set before running `execution.py`

See the [Development](../README.md#development) section of the main README for additional details on `entrypoint-dev.sh`.

## Execution script

The execution script accepts the input from `entrypoint(-dev).sh` and then generates a JSON payload to send to the Slim.AI engine, then monitors the status of the execution. Based on the final status of the execution which is returned, it will report either success or fail statuses.

## Requirements file

This is merely a simple list of requirements for `execution.py`. This can be generated using `pip freeze > requirements.txt` inside of this directory and the `pip install -r requirements.txt` is ran during the building of the image to ensure the dependencies are installed. This process can probably be automated and/or included in the image itself.
