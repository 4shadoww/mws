import re
from core import script
from core import utilities as util
from core import warning_handler as war

class Algo(script.Script):
    comment0 = "siirsi \"Katso myös\" -osion oikeaan kohtaan"
    comment1 = "monikko"

    warning0 = "siirretty vain otsikko"
    warning1 = "tagi ilman loppua"

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

        if util.titlein(util.getword("seealso"), page.text) and util.titlein(util.getword("srcs"), page.text) and util.titlepos(util.getword("seealso"), page.text) > util.titlepos(util.getword("srcs"), page.text):
            feed = util.listend(page.text, util.getword("seealso"), srclist, nono)

            if feed[0] == feed[1]:
                war.append_warning(self.warning0)

            if util.tagwithoutend('\n'.join(page.text[feed[0]:feed[1]])):
                war.append_warning(self.warning1)

            page.text = page.text.split("\n")
            seealsoec = page.text[feed[0]:feed[1]+1]
            page.text = util.removefromlist(seealsoec, page.text)

            n1 = "\n"
            seealsoec = '\n'.join(seealsoec)
            if page.text[util.titleline(util.getword("srcs"), '\n'.join(page.text))-1] == "":
                n1 = ""
            page.text[util.titleline(util.getword("srcs"), '\n'.join(page.text))] = n1+seealsoec+"\n\n"+page.text[util.titleline(util.getword("srcs"), '\n'.join(page.text))]
            page.text = '\n'.join(page.text)
            self.error_count += 1

        return self.error_count
