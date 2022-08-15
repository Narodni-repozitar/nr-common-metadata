#!/bin/bash
#
# Copyright (c) 2022 CESNET
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

cd $(dirname $0)

source .venv/bin/activate

(
  cd nr-common-metadata
  pip install -e '.[tests]'
)
