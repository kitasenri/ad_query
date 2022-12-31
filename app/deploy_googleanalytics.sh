#!/bin/zsh

FUNCTION_NAME="google_analytics"

## SETTINGS
RUNTIME="python37"
MEMORY="1024MB"
TIMEOUT="300s"
REGION="asia-northeast1"
ENV_FILE="./env_googleanalytics.yaml"
PUBSUB_NAME="topic_google_analytics"

## OPTIONS
OPTIONS="--runtime=${RUNTIME} --memory=${MEMORY} --timeout=${TIMEOUT} --region=${REGION} --env-vars-file ${ENV_FILE} --trigger-topic ${PUBSUB_NAME}"

## DEPLOY COMMAND
gcloud functions deploy ${FUNCTION_NAME} ${OPTIONS}
