from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "tasolla 3 lähteet osio"

    def run(self, text):
        for line in text.split("\n"):
            if util.titlein(util.getword("srcs"), line) and "===" in line:
                self.error_count += 1

        return self.error_count
