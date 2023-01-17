# Copyright (c) 2022 CESNET
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from flask import Blueprint

def create_blueprint(app):
    """Blueprint for the routes and resources provided by NR-common-metadata."""
    return Blueprint(
        "invenio_app_rdm",
        __name__,
        template_folder="templates",
        static_folder="static",
    )
