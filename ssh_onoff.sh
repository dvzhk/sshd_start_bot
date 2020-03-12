#!/bin/bash
#Необходимо обеспечить, чтобы скрипт запускался с правами, позволяющими запускать/останавливать сервисы
#Например добавить с помощью visudo:
# user_running_script ALL=(ALL)NOPASSWD:/path/to/ssh_onoff.sh

SERVICE=ssh
#SERVICE=cups
STATUS=$(service $SERVICE status)
PATTERN='active (running)'


#if grep -q "$PATTERN" <<< "$STATUS"; then
#    echo Started
#else
#    echo Stopped
#fi

if [[ "$STATUS" == *"$PATTERN"* ]]; then
  if service $SERVICE stop; then
    echo Stopped.
  else
    echo Failed.
  fi

else
  if service $SERVICE start; then
    echo Started
  else
    echo Failed.
  fi
fi
