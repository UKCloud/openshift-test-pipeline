#!/bin/bash
read -p "Provide generic webhook URL (from above): " WEBHOOK_URL

read -p "Provide random secret (from above): " RANDOMSECRET

# Obtain OpenShift secrets to pass in through webhook.
USERNAME=$(oc get secret openshift -o jsonpath={.data.username} | base64 -d)
USERPASS=$(oc get secret openshift -o jsonpath={.data.userpass} | base64 -d)
ADMINUSER=$(oc get secret openshift -o jsonpath={.data.adminuser} | base64 -d)
ADMINPASS=$(oc get secret openshift -o jsonpath={.data.adminpass} | base64 -d)
BASTIONIP=$(oc get secret openshift -o jsonpath={.data.bastionip} | base64 -d)
DOMAINSUFFIX=$(oc get secret openshift -o jsonpath={.data.domainsuffix} | base64 -d)
MULTINETWORK=$(oc get secret openshift -o jsonpath={.data.multinetwork} | base64 -d)
# Command doesn't decode to preserve SSH key format.
SSH_KEY=$(oc get secret openshift -o jsonpath={.data.sshkey})

# Trigger pipeline build via webhook.
# Provide environment variables.

ENV_VARS="env:
   - name: 'Username'
     value: '$USERNAME'
   - name: 'Userpass'
     value: '$USERPASS'
   - name: 'Adminuser'
     value: '$ADMINUSER'
   - name: 'Adminpass'
     value: '$ADMINPASS'
   - name: 'Bastionip'
     value: '$BASTIONIP'
   - name: 'Domainsuffix'
     value: '$DOMAINSUFFIX'
   - name: 'Multinetwork'
     value: '$MULTINETWORK'
   - name: 'Sshkey'
     value: '$SSH_KEY'"

# Find '<secret>' in url and replace with $RANDOMSTRING.
WEBHOOK_URL="${WEBHOOK_URL/<secret>/$RANDOMSECRET}"

# Send request to kick off pipeline using 
curl -H "Content-Type: application/yaml" -d "$ENV_VARS" -X "POST" "$WEBHOOK_URL"
