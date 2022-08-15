#!/bin/bash
#
# Copyright (c) 2022 CESNET
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

set -e

cp -r nr-common-metadata/nr_common_metadata/models/*yaml nr-common-metadata-model-builder/nr_common_metadata_model_builder/models/

test -d dist && rm -rf dist

mkdir dist

# create library distribution
(
  cd nr-common-metadata
  test -d dist && rm -rf dist
  cp ../README.md .
  cat setup.cfg
  python setup.py sdist bdist_wheel
  cp dist/*.tar.gz  ../dist/
  cp dist/*.whl  ../dist/
)

# create model builder extension package
(
  cd nr-common-metadata-model-builder
  test -d dist && rm -rf dist
  cp ../README.md .
  cat setup.cfg
  python setup.py sdist bdist_wheel
  cp dist/*.tar.gz  ../dist/
  cp dist/*.whl  ../dist/
)

# just list created stuff
ls -la dist

for i in dist/*.tar.gz; do
  echo
  echo Listing $i
  tar -tf $i
done
