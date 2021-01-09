import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi br tagin syntaksin tai korvasi sen {{clear}} -mallineella"
    comment1 = "korjasi br tagien syntaksit tai korvasi ne {{clear}} -mallineella"

    zero_edit = False

    def run(self, page):
        errorlist = re.findall(r"\<.*?\>", page.text)
        nono = ['abbr', 'wbr', 'ref', '<!--']
        for item in errorlist:
            if util.andop(nono, item) == False and util.istag("br", item):
                if 'clear' in item and '=' in item:
                    if 'all' in item:
                        page.text = page.text.replace(item, '{{clear}}')
                        self.error_count += 1
                    elif 'left' in item:
                        page.text = page.text.replace(item, '{{clear|left}}')
                        self.error_count += 1
                    elif 'right' in item:
                        page.text = page.text.replace(item, '{{clear|right}}')
                        self.error_count += 1
                elif '/' in item and item != '<br />' and 'clear' not in item and '=' not in item:
                    page.text = page.text.replace(item, '<br />')
                    self.error_count += 1
                elif '/' not in item and item != '<br>' and 'clear' not in item and '=' not in item:
                    page.text = page.text.replace(item, '<br>')
                    self.error_count += 1
        return self.error_count
