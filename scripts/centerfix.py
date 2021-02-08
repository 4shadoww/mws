import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi center tagin syntaksin"
    comment1 = "korjasi center tagien syntaksit"

    zero_edit = False

    def run(self, page):
        errorlist = re.finditer(r"\<.*?center(.*?)[/\\ ]\>", page.text)
        for item in errorlist:
            if util.istag("center", item.group(0)):
                if '/' in item.group(0) and item.group(0) != '</center>':
                    page.text = page.text.replace(item.group(0), '</center>')
                    self.error_count += 1
                elif '/' not in item.group(0) and item.group(0) != '<center>':
                    if not item.group(1).isspace():
                        page.text = page.text.replace(item.group(0), '<center '+item.group(1).strip()+'>')
                    else:
                        page.text = page.text.replace(item.group(0), '<center>')
                    self.error_count += 1

        return self.error_count
