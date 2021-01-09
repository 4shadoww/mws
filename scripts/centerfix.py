import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi center tagin syntaksin"
    comment1 = "korjasi center tagien syntaksit"

    zero_edit = True

    def run(self, page):
        errorlist = re.findall(r"\<.*?\>", page.text)
        for item in errorlist:
            if util.istag("center", item):
                if '/' in item and item != '</center>':
                    page.text = page.text.replace(item, '</center>')
                    self.error_count += 1
                elif '/' not in item and item != '<center>':
                    page.text = page.text.replace(item, '<center>')
                    self.error_count += 1

        return self.error_count
