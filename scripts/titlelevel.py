import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "siirsi otsikon oikealle tasolle"
    comment1 = "siirsi otsikkoja oikealle tasolle"

    zero_edit = False

    def run(self, page):
        page.text = page.text.split("\n")
        for l in range(0, len(page.text)):
            if util.istitle(page.text[l]) and page.text[l].count("=") <= 2:
                self.error_count += 1
                page.text[l] = page.text[l].replace("=", "")
                page.text[l] = "=="+page.text[l]+"=="

        page.text = '\n'.join(page.text)


        return self.error_count
