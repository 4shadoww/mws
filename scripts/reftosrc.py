import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "yksikkö"
    comment1 = "monikko"

    comment00 = "siirsi \"Viitteet\" -osion oikealle tasolle"
    comment01 = "muutti \"Viitteet\" -osion muotoon \"Lähteet\""

    zero_edit = False

    def run(self, page):
        page.textlist = page.text.split('\n')

        for l, line in enumerate(page.textlist):
            matches = re.findall(r"\=.*\=", line)

            if len(matches) == 0:
                continue
            if util.getword("refs") in matches[0] and util.titlein(util.getword("srcs"), page.text) and matches[0].count("=") <= 4:
                page.textlist[l] = "===Viitteet==="
                error = 0
                self.error_count += 1

            elif util.getword("refs") in matches[0] and util.titlein(util.getword("srcs"), page.text) == False:
                page.textlist[l] = "==Lähteet=="
                error = 1
                self.error_count += 1

        page.text = '\n'.join(page.textlist)

        if self.error_count > 0 and error == 0:
            self.comment0 = self.comment00
        elif self.error_count > 0 and error == 1:
            self.comment0 = self.comment01


        return self.error_count
