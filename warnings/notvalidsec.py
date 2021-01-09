import re

from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "osion siirto tuottaa ongelmia"

    def getsec(self, text):
        secs = []
        cut = False
        start = 0
        for l in  range(0, len(text)):
            thread_header = re.search('^== *([^=].*?) *== *$', text[l])
            if thread_header:
                if cut == True:
                    secs.append(text[start:l])
                start = l
                cut = True
            elif len(text)-1 == l:
                secs.append(text[start:l])
        return secs

    def getlen(self, sec):
        nons = True
        length = 0
        for line in reversed(sec):
            if line == "" and nons:
                continue
            else:
                length += 1
                nons = False
        return length

    def run(self, text):
        self.wm["fi"] = "osion siirto tuottaa ongelmia"
        text = text.split("\n")
        secs = self.getsec(text)

        srclist = ["*", "{{IMDb-h", "#",
        util.getwordlc("bref"), util.getword("bref"),
        util.getwordlc("wref"), util.getword("wref"),
        util.getwordlc("mref"), util.getword("mref"),
        util.getwordlc("sref"), util.getword("sref"),
        util.getwordlc("nref"), util.getword("nref"),
        util.getwordlc("commons"), util.getword("commons"),
        "{{"+util.getword("refs"), "{{"+util.getwordlc("refs"),
        "<references", "===", "{{Käännös|", "{{käännös|"]

        nono = ["[["+util.getwordc("cat"), "{{Tynkä", "{{tynkä", "{{AAKKOSTUS", "{{DEFAULTSORT", "{{OLETUSAAKKOSTUS"]

        secsl = [util.getword("srcs"), util.getword("refs"), util.getword("li"), util.getword("exl"), util.getword("seealso")]

        for l, sec in enumerate(secs):
            if len(sec) > 0 and sec[0].replace("=", "") in secsl and l != len(secs)-1:
                feed = util.listend('\n'.join(text), sec[0].replace("=", ""), srclist, nono)
                if feed[1]-feed[0]+1 != self.getlen(sec):
                    self.error_count += 1
                    self.wm = sec[0].replace("=", "") +", "+ self.wm

        return self.error_count
