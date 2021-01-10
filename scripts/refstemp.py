import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "muutti {{viitteet}} -mallineen muotoon {{Viitteet}}"
    comment1 = "monikko"
    comment01 = "muutti {{Viitteet|sarakkeet}} -mallineen muotoon {{Viitteet}}"

    zero_edit = True

    def run(self, page):
        if page.text.count("<ref/>") < 1 and "{{"+util.getwordlc("refs")+"|sarakkeet}}" in page.text and "{{"+util.getword("refs")+"|sarakkeet}}" in page.text:
            self.error_count = 1
            page.text = page.text.replace("{{"+util.getwordlc("refs")+"|sarakkeet}}", "{{"+util.getword("refs")+"}}")
            page.text = page.text.replace("{{"+util.getword("refs")+"|sarakkeet}}", "{{"+util.getword("refs")+"}}")
            self.comments0 = self.comment01

        else:
            self.error_count += page.text.count("{{"+util.getwordlc("refs")+"}}")
            self.error_count += page.text.count("{{"+util.getwordlc("refs")+"|")
            page.text = page.text.replace("{{"+util.getwordlc("refs")+"}}", "{{"+util.getword("refs")+"}}")
            page.text = page.text.replace("{{"+util.getwordlc("refs")+"|", "{{"+util.getword("refs")+"|")


        return self.error_count
