#!/usr/bin/env sh

TARGET=$1

setup_git() {
  echo "SETUP GIT"
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  echo "COMMIT_WEBSITE_FILES"
  git add -A
  git commit --message "Github build: $GITHUB_RUN_NUMBER"
}

upload_files() {
  echo "UPLOAD_FILES"
  Address="https://${GH_TOKEN}@github.com/Narodni-repozitar/nr-schemas.git"
  echo $Address
  git remote add origin-pages $Address
  git push --set-upstream origin-pages
}

echo "Target: $TARGET"
cd $TARGET
setup_git
commit_website_files
upload_files