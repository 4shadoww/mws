import re
from core import script
from core import utilities as util
from core import warning_handler as war

class Algo(script.Script):
    comment0 = "muutti \"Katso myös\" -osion muotoon \"Aiheesta muualla\""
    comment1 = "monikko"

    warning0 = "aiheesta muualla osio ristiriita"
    warning1 = "siirretty vain otsikko"
    warning2 = "tagi ilman loppua"

    zero_edit = False

    def run(self, page):
        srclist = ["*", "{{IMDb-h", "#",
        util.getwordlc("bref"), util.getword("bref"),
        util.getwordlc("wref"), util.getword("wref"),
        util.getwordlc("mref"), util.getword("mref"),
        util.getwordlc("sref"), util.getword("sref"),
        util.getwordlc("nref"), util.getword("nref"),
        util.getwordlc("commons"), util.getword("commons")]
        nono = ["[["+util.getwordc("cat"), "{{Tynkä", "{{tynkä", "{{AAKKOSTUS", "{{DEFAULTSORT", "{{OLETUSAAKKOSTUS"]

        if util.titlein(util.getword("seealso"), page.text) and "http://" in page.text and util.titlein(util.getword("exl"), page.text) == False or util.titlein(util.getword("seealso"), page.text) and "https://" in page.text and util.titlein(util.getword("exl"), page.text) == False:
            feed = util.listend(page.text, util.getword("seealso"), srclist, nono)

            if feed[0] == feed[1]:
                war.append_warning(self.warning1)

            if util.tagwithoutend('\n'.join(page.text[feed[0]:feed[1]])):
                war.append_warning(self.warning2)

            page.text = page.text.split("\n")
            seealsosec = '\n'.join(page.text[feed[0]:feed[1]+1])

            if "[[" in seealsosec and "http://" in seealsosec or "[[" in seealsosec and "https://" in seealsosec:
                war.append_warning(self.warning0)
            if "http://" in seealsosec or "https://" in seealsosec:
                page.text[feed[0]] = "=="+util.getword("exl")+"=="
                self.error_count += 1

            page.text = '\n'.join(page.text)
        return self.error_count
