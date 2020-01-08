#!/bin/bash

read -p "Provide generic webhook URL (from above): " WEBHOOK_URL

read -p "Provide base64 encoded string (from above): " BASE64STRING

# Obtain OpenShift secret to pass in through webhook.
SECRET=$(oc get secret openshift -o json)

# Trigger pipeline build via webhook.
# Provide environment variables.
ENV_VARS="env:
   - name: 'Credentials'
     value: $SECRET"

# Find '<secret>'' in url and replace with $BASE64STRING.
WEBHOOK_URL="${WEBHOOK_URL/<secret>/$BASE64STRING}"

# Send request to kick off pipeline using 
curl -H "Content-Type: application/yaml" -d $ENV_VARS -X "POST" $WEBHOOK_URL
