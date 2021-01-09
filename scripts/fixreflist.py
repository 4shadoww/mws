import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "yksikkö"
    comment1 = "monikko"

    zero_edit = True

    def addrefs0(self, text, article):
        srclist = ["*", "{{IMDb-h", "#",
        util.getwordlc("bref"), util.getword("bref"),
        util.getwordlc("wref"), util.getword("wref"),
        util.getwordlc("mref"), util.getword("mref"),
        util.getwordlc("sref"), util.getword("sref"),
        util.getwordlc("nref"), util.getword("nref"),
        util.getwordlc("commons"), util.getword("commons"),
        "{{"+util.getword("refs"), "{{"+util.getwordlc("refs"),
        "<references", "{{Käännös|", "{{käännös|"]

        nono = ["[["+util.getwordc("cat"), "{{Tynkä", "{{tynkä", "{{AAKKOSTUS", "{{DEFAULTSORT", "{{OLETUSAAKKOSTUS"]

        feed = util.listend(text, util.getword("srcs"), srclist, nono)

        if util.tagwithoutend('\n'.join(text[feed[0]:feed[1]])):
            warning(self.warnings[config.lang+"01"])

        if feed[0] == feed[1]:
            warning(self.warnings[config.lang+"00"])

        if feed[1] != None and feed[2] == False:
            self.error_count += 1
            text = text.split("\n")
            nl00 = "\n"
            if text[feed[0]] == "":
                nl00 = ""
            text[feed[0]] = text[feed[0]]+nl00+"{{"+util.getword("refs")+"}}"
            text = '\n'.join(text)
            self.comments[config.lang+"0"] = self.comments[config.lang+"01"]

        elif feed[1] != None and feed[2]:
            nl0 = "\n"
            nl1 = ""
            self.error_count += 1
            text = text.split("\n")
            if text[feed[1]] != "":
                nl0 = "\n\n"
            if text[feed[1]+1] != "":
                nl1 += "\n\n"

            text[feed[1]] = text[feed[1]]+"\n\n"+"==="+util.getword("refs")+"===\n"+"{{"+util.getword("refs")+"}}"+nl1
            text = '\n'.join(text)
            self.comments[config.lang+"0"] = self.comments[config.lang+"00"]

        return text

    def addrefs1(self, text, article):
        targetline = None

        pos = None
        nono = ["{{", util.getwordc("cat"),
        util.getwordlcc("cat"),]

        unwanted = ["{{"+util.getword("commons"), "{{"+util.getwordlc("commons"), "*", "#",
        "<ref>", "</ref>", "\n", "\t", "\b", "\a", "\r", "|}"]

        text = text.split("\n")
        firstcat = len(text)
        for l, line in enumerate(text):
            if util.getwordlcc("cat") in line or util.getwordc("cat") in line:
                firstcat = l
                pos = l
                break

        for l, line in reversed(list(enumerate(text[:firstcat]))):
            if util.anymatch(unwanted, line):
                minus = len(text)-l
                pos = len(text)-minus+1
                break

            elif util.zeromatch(nono, line) and util.zeromatch(nono, text[l-1]) and line != "":
                minus = len(text)-l
                pos = len(text)-minus+1
                break

        if pos == len(text):
            pos -= 1

        if pos != None:
            nl = ""
            if text[pos] != "":
                nl = "\n"
            text[pos] = text[pos]+nl+"\n=="+util.getword("srcs")+"==\n{{"+util.getword("refs")+"}}\n"

        text = '\n'.join(text)
        self.error_count += 1
        self.comments[config.lang+"0"] = self.comments[config.lang+"02"]

        return text

    def addrefs2(self, text, article):
        line = util.titleline(util.getword("refs"), text)
        text = text.split("\n")
        text[line] = text[line]+"\n{{"+util.getword("refs")+"}}"
        self.error_count += 1
        self.comments[config.lang+"0"] = self.comments[config.lang+"01"]
        text = '\n'.join(text)
        return text

    def addrefs3(self, text, article):
        srclist = ["*", "{{IMDb-h", "#",
        util.getwordlc("bref"), util.getword("bref"),
        util.getwordlc("wref"), util.getword("wref"),
        util.getwordlc("mref"), util.getword("mref"),
        util.getwordlc("sref"), util.getword("sref"),
        util.getwordlc("nref"), util.getword("nref"),
        util.getwordlc("commons"), util.getword("commons"),
        "{{"+util.getword("refs"), "{{"+util.getwordlc("refs"),
        "<references", "{{Käännös|", "{{käännös|"]

        nono = ["[["+util.getwordc("cat"), "{{Tynkä", "{{tynkä", "{{AAKKOSTUS", "{{DEFAULTSORT", "{{OLETUSAAKKOSTUS"]

        text = text.split("\n")

        feed0 = util.listend('\n'.join(text), util.getword("refs"), srclist, nono)

        if feed0[0] == feed0[1]:
            warning(self.warnings[config.lang+"00"])

        refsec = '\n'.join(text[feed0[0]:feed0[1]+1])


        for l,t in zip(range(feed0[0], feed0[1]+1), range(0, feed0[1]-feed0[0]+1)):
            text.pop(l-t)


        feed = util.listend('\n'.join(text), util.getword("srcs"), srclist, nono)

        if util.tagwithoutend('\n'.join(text[feed[0]:feed[1]])):
            warning(self.warnings[config.lang+"01"])

        if feed[0] == feed[1]:
            warning(self.warnings[config.lang+"00"])

        if feed[1] != None:
            nl0 = "\n"
            nl1 = "\n"
            self.error_count += 1

            text[feed[1]] = text[feed[1]]+nl0+refsec+"\n"+nl1
            text = '\n'.join(text)
            self.comments[config.lang+"0"] = self.comments[config.lang+"03"]
        return text

    def run(self, page):
        article = page.title

        nono = ["<references/>", "<references />", "<references>",
        "{{"+util.getword("refs"), "{{"+util.getwordlc("refs"), "{{reflist", "{{Reflist"]

        if util.titlein(util.getword("refs"), page.text) and util.titlein(util.getword("srcs"), page.text) and not util.titlebefore(util.getword("srcs"), util.getword("refs"), page.text, subtitles=False):
            page.text = self.addrefs3(page.text, article)

        if "<ref>" not in page.text and "</ref>" not in page.text:
            return page.text, self.error_count

        if util.andop(nono, page.text):
            return page.text, self.error_count

        elif util.titlein(util.getword("refs"), page.text) and util.titlein(util.getword("srcs"), page.text) and "{{"+util.getword("refs") not in page.text and "{{"+util.getwordlc("refs") not in page.text:
            page.text = self.addrefs2(page.text, article)
        elif util.titlein(util.getword("srcs"), page.text) and "{{"+util.getword("refs") not in page.text and "{{"+util.getwordlc("refs") not in page.text:
            page.text = self.addrefs0(page.text, article)

        elif util.titlein(util.getword("srcs"), page.text) == False:
            page.text = self.addrefs1(page.text, article)

        return self.error_count
