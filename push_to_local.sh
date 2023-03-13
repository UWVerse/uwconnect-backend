#!/bin/bash -e
#Usage ./push_to_local.sh <commit_message>
git add .
git commit -m "$1"
git push