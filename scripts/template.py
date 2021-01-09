import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "yksikkö"
    comment1 = "monikko"

    zero_edit = True

    def run(self, page):
        return self.error_count
