from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "Liian monta viitteet mallinetta"

    def run(self, text):
        r0 = 0
        r1 = 0
        r2 = 0
        r3 = 0
        r0 = text.count("{{"+util.getword("refs")+"}}")
        r1 = text.count("{{"+util.getwordlc("refs")+"}}")
        r2 = text.count("{{"+util.getword("refs")+"|")
        f3 = text.count("{{"+util.getwordlc("refs")+"|")

        if r0 + r1 + r2 + r3 > 1:
            self.error_count += 1

        return self.error_count
