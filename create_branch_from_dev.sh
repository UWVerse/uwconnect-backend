#!/bin/bash -e
git remote add upstream git@github.com:UWVerse/uwconnect-backend.git || true
git fetch upstream
git checkout -b "$1" upstream/dev
git push --set-upstream origin "$1"