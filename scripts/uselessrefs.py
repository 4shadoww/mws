import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "poisti turhan \"Viitteet\" tai \"Lähteet\" -osion"
    comment1 = "monikko"

    zero_edit = False

    def run(self, page):
        nono = ["{{iihfranking"]
        if page.text.count("<ref/>") == 0 and page.text.count("<ref />") == 0 and page.text.count("<ref>") == 0:
            self.error_count += 1
            if util.titlein(util.getword("refs"), page.text):
                page.text = page.text.split("\n")
                for l, line in enumerate(page.text):
                    if util.titlein(util.getword("refs"), line):
                        page.text.pop(l)
                        break
                for l, line in enumerate(page.text):
                    if "{{"+util.getword("refs") in line or "{{"+util.getwordlc("refs") in line or "<references" in line:
                        page.text.pop(l)
                        break
            else:
                page.text = page.text.split("\n")
                for l, line in enumerate(page.text):
                    if util.titlein(util.getword("srcs"), line):
                        page.text.pop(l)
                        break
                for l, line in enumerate(page.text):
                    if "{{"+util.getword("refs") in line or "{{"+util.getwordlc("refs") in line or "<references" in line:
                        page.text.pop(l)
                        break
            page.text = '\n'.join(page.text)

        return self.error_count
