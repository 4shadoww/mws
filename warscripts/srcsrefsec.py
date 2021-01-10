from core import warningbase
from core import utilities as util


class Warning(warningbase.Warningbase):
    wm = "Viitteet osio on Lähteet osion yläpuolella"

    def run(self, text):
        if util.titlein(util.getword("srcs"),text) and util.titlein(util.getword("refs"), text) and  util.titleline(util.getword("srcs"), text) > util.titleline(util.getword("refs"), text):
            self.error_count += 1

        return self.error_count
