import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi small tagin syntaksin"
    comment1 = "korjasi small tagien syntaksit"

    zero_edit = False

    def run(self, page):
        errorlist = re.finditer(r"\<.*?small(.*?)[/\\ ]\>", page.text)
        for item in errorlist:
            if util.istag("small", item.group(0)):
                if '/' in item.group(0) and item.group(0) != '</small>':
                    page.text = page.text.replace(item.group(0), '</small>')
                    self.error_count += 1
                elif '/' not in item.group(0) and item.group(0) != '<small>':
                    if not item.group(1).isspace():
                        page.text = page.text.replace(item.group(0), '<small '+item.group(1).strip()+'>')
                    else:
                        page.text = page.text.replace(item.group(0), '<small>')
                    self.error_count += 1

        return self.error_count
