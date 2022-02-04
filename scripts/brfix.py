import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi br tagin syntaksin tai korvasi sen {{clear}} -mallineella"
    comment1 = "korjasi br tagien syntaksit tai korvasi ne {{clear}} -mallineella"

    zero_edit = False
    zero_change = 0

    def run(self, page):

        errorlist = re.findall(r"\<.*?\>", page.text)
        nono = ['abbr', 'wbr', 'ref', '<!--']
        for item in errorlist:
            if util.andop(nono, item) == False and util.istag("br", item):
                if 'clear' in item and '=' in item:
                    if 'all' in item:
                        page.text = page.text.replace(item, '{{clear}}', 1)
                        self.error_count += 1
                        self.zero_change = 1
                    elif 'left' in item:
                        page.text = page.text.replace(item, '{{clear|left}}', 1)
                        self.error_count += 1
                        self.zero_change = 1
                    elif 'right' in item:
                        page.text = page.text.replace(item, '{{clear|right}}', 1)
                        self.error_count += 1
                        self.zero_change = 1
                elif '/' in item and item != '<br />' and 'clear' not in item and '=' not in item:
                    if item != '<br/>':
                        self.zero_change = 1
                    else:
                        self.zero_change = 0
                    page.text = page.text.replace(item, '<br />', 1)
                    self.error_count += 1
                elif '/' not in item and item != '<br>' and 'clear' not in item and '=' not in item:
                    page.text = page.text.replace(item, '<br>', 1)
                    self.error_count += 1
                    self.zero_change = 1

        if self.zero_change == 1:
            self.zero_edit = False
        else:
            self.zero_edit = True

        return self.error_count
