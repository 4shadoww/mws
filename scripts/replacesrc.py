import re
from core import script
from core import utilities as util
from core import warning_handler as war

class Algo(script.Script):
    comment0 = "siirsi \"Lähteet\" -osion oikeaan kohtaan"
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
        util.getwordlc("commons"), util.getword("commons"),
        "{{"+util.getword("refs"), "{{"+util.getwordlc("refs"),
        "<references/>", "<references />",
        "==="+util.getword("refs")+"===", "{{Käännös|", "{{käännös|"]
        nono = ["[["+util.getwordc("cat"), "{{Tynkä", "{{tynkä", "{{AAKKOSTUS", "{{DEFAULTSORT", "{{OLETUSAAKKOSTUS"]

        if util.titlein(util.getword("srcs"), page.text) and util.titlein(util.getword("exl"), page.text) and util.titlepos(util.getword("srcs"), page.text) > util.titlepos(util.getword("exl"), page.text) or util.titlein(util.getword("srcs"), page.text) and util.titlein(util.getword("li"), page.text) and util.titlepos(util.getword("srcs"), page.text) > util.titlepos(util.getword("li"), page.text):

            feed = util.listend(page.text, util.getword("srcs"), srclist, nono)

            if feed[0] == feed[1]:
                war.append_warning(self.warning0)

            if util.tagwithoutend('\n'.join(page.text[feed[0]:feed[1]])):
                war.append_warning(self.warning1)

            page.text = page.text.split("\n")
            srcsec = page.text[feed[0]:feed[1]+1]

            page.text = util.removefromlist(srcsec, page.text)
            print(page.text)
            srcsec = '\n'.join(srcsec)
            n1 = "\n"

            if util.titlein(util.getword("li"), '\n'.join(page.text)):
                if page.text[util.titleline(util.getword("li"), '\n'.join(page.text))-1] == "":
                    n1 = ""
                page.text[util.titleline(util.getword("li"), '\n'.join(page.text))] = n1+srcsec+"\n\n"+page.text[util.titleline(util.getword("li"), '\n'.join(page.text))]
            elif util.titlein(util.getword("exl"), '\n'.join(page.text)):
                if page.text[util.titleline(util.getword("exl"), '\n'.join(page.text))-1] == "":
                    n1 = ""
                page.text[util.titleline(util.getword("exl"), '\n'.join(page.text))] = n1+srcsec+"\n\n"+page.text[util.titleline(util.getword("exl"), '\n'.join(page.text))]
            page.text = '\n'.join(page.text)
            self.error_count += 1


        return self.error_count
