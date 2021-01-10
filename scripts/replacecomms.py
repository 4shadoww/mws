import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "siirsi Commonscat -mallineen \"Aiheesta muualla\" -osioon"
    comment1 = "monikko"

    zero_edit = False

    def run(self, page):
        template = None
        if "{{commonscat|" in page.text and util.titlein(util.getword("exl"), page.text) and not util.insec("{{commonscat|", util.getword("exl"), page.text) or "{{Commonscat|" in page.text and util.titlein(util.getword("exl"), page.text) and not util.insec("{{Commonscat|", util.getword("exl"), page.text):
            page.text = page.text.split("\n")
            for l in range(0, len(page.text)):
                if "{{commonscat|" in page.text[l] or "{{Commonscat|" in page.text[l]:
                    template = page.text[l]
                    page.text.pop(l)
                    break
            if template != None:
                self.error_count += 1
                page.text[util.titleline(util.getword("exl"), '\n'.join(page.text))] = page.text[util.titleline(util.getword("exl"), '\n'.join(page.text))] +"\n"+template
            page.text = '\n'.join(page.text)


        return self.error_count
