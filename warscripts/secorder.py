from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "väärä osio järjestys"

    def run(self, text):
        titles = [
        util.getword("seealso"),
        util.getword("srcs"),
        util.getword("refs"),
        util.getword("li"),
        util.getword("exl")]

        after = 0
        before = 1
        while True:
            if after > len(titles)-2:
                break
            if before > len(titles)-1:
                break

            if util.titlein(titles[after], text) == False:
                after += 1
                if after == before:
                    before += 1
                continue
            elif util.titlein(titles[before], text) == False:
                before += 1
                continue
            if util.titlebefore(titles[after], titles[before], text) == False:
                self.error_count += 1
                break
            after += 1
            before += 1


        return self.error_count
