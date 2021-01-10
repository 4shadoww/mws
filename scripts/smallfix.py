import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi small tagin syntaksin"
    comment1 = "korjasi small tagien syntaksit"

    zero_edit = False

    def run(self, page):
        errorlist = re.findall(r"\<.*?\>", page.text)
        for item in errorlist:
            if util.istag("small", item):
                if '/' in item and item != '</small>':
                    page.text = page.text.replace(item, '</small>')
                    self.error_count += 1
                elif '/' not in item and item != '<small>':
                    page.text = page.text.replace(item, '<small>')
                    self.error_count += 1

        return self.error_count
