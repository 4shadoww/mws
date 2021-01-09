from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "Luokka ei ole lopussa"

    def run(self, text):
        text = text.split("\n")
        foundcat = False
        for line in text:
            if util.getwordc("cat") in line or util.getwordlcc("cat") in line:
                foundcat = True
            elif foundcat and line != "":
                self.error_count += 1
                return self.error_count

        return self.error_count
