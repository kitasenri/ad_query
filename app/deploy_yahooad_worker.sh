#!/bin/zsh

FUNCTION_NAME="yahoo_ad_worker"

## SETTINGS
RUNTIME="python37"
MEMORY="1024MB"
TIMEOUT="540s"
REGION="asia-northeast1"
ENV_FILE="./env_yahooad.yaml"
PUBSUB_NAME="topic_yahoo_ad_worker"

## OPTIONS
OPTIONS="--runtime=${RUNTIME} --memory=${MEMORY} --timeout=${TIMEOUT} --region=${REGION} --env-vars-file ${ENV_FILE} --trigger-topic ${PUBSUB_NAME}"

## DEPLOY COMMAND
gcloud functions deploy ${FUNCTION_NAME} ${OPTIONS}
