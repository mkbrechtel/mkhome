#!/bin/bash
ntfy_url=$1
while echo  offline
do
  curl -sN --proto-default https --retry 60 --retry-delay 1 --retry-max-time 60 --keepalive-time 1 $ntfy_url |\
    jq --unbuffered -r 'select(.event == "message" or .event == "open")|if .event == "message" then .message else "🖧 online" end';
  sleep 1;
done
