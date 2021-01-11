import logging

from core import api

logger = logging.getLogger("infolog")

class Script:
    zero_edit = False
    error_count = 0
    comment0 = "edit"
    comment1 = "edit"

    def __init__(self):
        self.error_count = 0

    def run(self, page):
        return self.error_count
