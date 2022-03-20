# DynamoDBStandalone
Standalone DynamoDB application for remote testing, based off of dynamodb-local.

## Description

Dynamodb-local is a great tool for integration testing. You don't need to mock out 
your API calls, you just point to your local endpoint and use real API calls. Because Dynamodb-local is 
intended to run on your local development machine, it runs a wide-open webserver that accepts any mock AWS 
credentials. 

But what if you want to perform integration testing across microservices? What if there is no local 
development machine? I built this package to include a deployable docker container that puts a Nginx 
reverse proxy in front of the Jetty webserver provided by Dynamodb-local. This way, security can be configured 
and you're not running a wide open API endpoint over the internet. You get a Dynamodb endpoint complete 
outside of the AWS cloud.

## What's Included

* A docker container that deploys dynamodb-local and nginx
* An HTTP port 80 endpoint, that is secured with a basic auth key.
* Example Python code for how to call the API.

## To-do/Nice-to-have's

* A script to generate a cert, and HTTPS/SSL configuration.
* A script to pull down integration API keys from a password safe or key store.

## Prerequisites

### Docker

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html
https://docs.docker.com/get-docker/

## Docker-compose

https://docs.docker.com/compose/install/

# Usage

Build and run.

``` bash
$ docker-compose up
```

## Example

![Example usage](https://github.com/gnelabs/DynamoDBStandalone/blob/main/example_usage.gif?raw=true)