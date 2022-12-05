# SparklingSnakes
Application designed to handle:
- Downloading AWS S3 PE files from given region & bucket
  - Application expects (configurable) given bucket to consist of the following prefixes:
    - 0
    - 1
- Processing downloaded files using Python packages & shell commands (if necessary)
  - Files already processed (basing on their existence in database) **will** be skipped
  - Files existence on local storage is not being tracked
- Storing scrapped file metadata in database of choice

## Main technology used
- FastAPI (_v0.88.0_)
- Python (_v3.10_)
- PySpark (_v3.3.1_)
- PostgreSQL (_v15.1_)

## Prerequisites
- [Ubuntu 22.04 LTS](https://releases.ubuntu.com/22.04/) (_built on WSL2_)
- [Docker](https://www.docker.com/) (_developed using v20.10.21_)
- [Docker Compose](https://docs.docker.com/compose/) (_developed using v2.12.2_)
- [Python 3.10](https://www.python.org/downloads/release/python-3108/)
  - Python 3.11 is not yet fully supported by PySpark
  - Using [Virtualenv](https://virtualenv.pypa.io/en/latest/) for development is preferred

## Usage
Since application bases on the database which is initialized, it is expected from the user
to initialize it with tools of choice. However, the simplest use case is pre-configured.


### First use

Host ports in-use:
- 9093 (API)
    - or 8000 if it has been started without using docker
- 5432 (PostgreSQL)
- 9090, 7070 (PySpark Master node)
- 9091, 7000 (PySpark Worker A node)
- 9092, 7001 (PySpark Worker B node)

1. Build docker images
    ```sh
    make docker_build
    ```
2. Create directory for storing the downloaded files (```/s3-files```):
    ```sh
    mkdir /s3files
    ```
    - Make sure that it provides write privileges
3. Start docker containers
    ```sh
    make docker_up
    ```
4. Make sure that your default ```python3``` and ```pip``` binaries are properly set and have
   appropriate packages installed
   - Once you have selected your interpreter and/or activated virtual environment, you
      can install the requirements listed in requirements-env.txt file using either ```make install_env```
      or ```<your_pip_binary> install -r requirements-env.txt``` directly
5. Make sure that you have appropriate DB credentials set
   - ```postgres/postgres``` on ```localhost:5432``` are the defaults
   - Please set ```PGPASSWORD``` environment variable to ```postgres``` if you follow the defaults
6. Initialize the database:
    ```sh
    make init_database
    ```
7. You are now ready to use the application

### Regular use
1. Start the application
    ```sh
    make docker_up
    ```
2. Either POST the ```http://127.0.0.1:9093/processor/tasks``` endpoint using the following scheme:
    ```JSON
    {
      "region_name": "<your-s3-bucket-region>",
      "bucket_name": "<your-s3-bucket-name>",
      "files_total": 200
    }
    ```
3. Or use the OpenAPI docs by accessing the following URL: ```http://127.0.0.1:9093/docs```

Please note that larger tasks (```files_total``` parameter) might take longer time to be processed first time
and the API itself might not respond in time due to default HTTP timeout being hit.

## Links
[![Linkedin](https://brand.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg) Filip Płachecki](https://www.linkedin.com/in/filip-p%C5%82achecki-657633a5/)
