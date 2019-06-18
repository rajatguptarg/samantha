![alt-text](docs/chatbot.jpg)

**Circle CI**: [![CircleCI](https://circleci.com/gh/rajatguptarg/samantha.svg?style=svg)](https://circleci.com/gh/rajatguptarg/samantha)

**Code Maintainability**: [![Maintainability](https://api.codeclimate.com/v1/badges/ea81caf4826ebdc015f8/maintainability)](https://codeclimate.com/github/rajatguptarg/samantha/maintainability)

**Code Climate Test Coverage**: [![Test Coverage](https://api.codeclimate.com/v1/badges/ea81caf4826ebdc015f8/test_coverage)](https://codeclimate.com/github/rajatguptarg/samantha/test_coverage)

**Coveralls Test Coverage**: [![Coverage Status](https://coveralls.io/repos/github/rajatguptarg/samantha/badge.svg?branch=master)](https://coveralls.io/github/rajatguptarg/samantha?branch=master)

**Travis CI**: [![Build Status](https://travis-ci.org/rajatguptarg/samantha.svg?branch=master)](https://travis-ci.org/rajatguptarg/samantha)



Bot for managing deployments and monitoring infrastructure.


## Introduction

To learn about building bots, please refer to [Setting Up Slack Bot](/docs/tutorial/README.md).

## Install

* First install the dependencies by:

    ```shell
    pip install -r requirements.txt
    ```

* Either set the following environment variables or:

    ```shell
    export SLACK_BOT_TOKEN="xoxb-xxxx-xxx-xxxx"
    export DIAG_FLOW_PROJECT_ID="xxx"
    export DIAG_FLOW_SESSION_ID="xxxx"
    export DIAG_FLOW_LANG_CODE="xx"
    export DIAG_FLOW_CREDENTIALS_FILE="xxx.json"
    export LOG_LEVEL=1
    export ANSIBLE_CONFIG="/path/to/ansible.cfg"
    export ANSIBLE_VAULT_PASS="xxxxx"
    export ANSIBLE_INVENTORY_FILE="/samantha/iaac/inventory/"
    ```

* Run the project by passing command line args:

    ```shell
    python run.py -t xoxb-xxxxx-xxxxx-xxxx -p xxx -s xxxx -lc xx -c xxxxx.json -ap xxxx -i /samantha/iaac/inventory/
    ```

    

## Build

If you want to build your own version of Samantha, you need the following:

* DiaglogFlow
* Slack Bot
* Ansible

## Architecture

The architecture of Samantha as follows:



![alt-text](docs/samantha.png)

User can choose, whether to send data to slack or to email.

## Deploy

Coming Soon!


## Onboarding

The onboaring involves adding new servers for Samantha to reach or modify the existing commands for your need. Here are list of commands for onboarding:

* [Log Fetcher](docs/onboarding/log-fetcher.md)

