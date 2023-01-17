# Copyright (c) 2022 CESNET
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

class NRCommonMetadataExt:
    """NR Common metadata extension."""

    def __init__(self, app, db=None):
        """
        Create an instance of the extension.
        :param app      the application
        :param db       database, not used
        """
        self.init_app(app, db=None)

    def init_app(self, app, db=None):
        """
        Initialize the extension.
        :param app      the application
        :param db       database, not used
        """
