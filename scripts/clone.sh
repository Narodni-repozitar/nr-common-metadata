#!/usr/bin/env sh

CWD=$(pwd)

cd /tmp

git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis CI"
git clone https://github.com/Narodni-repozitar/nr-schemas.git

