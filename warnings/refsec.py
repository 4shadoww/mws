from core import warningbase
from core import utilities as util

class Warning(warningbase.Warningbase):
    wm = "artikkelissa on viitteet osio tai malline, mutta ei yhtään <ref> tagia"

    def run(self, text):
        if util.titlein(util.getword("refs"), text) and "<ref" not in text:
            self.error_count += 1

        if "{{"+util.getword("refs")+"|" in text and "<ref" not in text or "{{"+util.getwordlc("refs")+"|" in text and "<ref" not in text:
            self.error_count += 1

        if "{{"+util.getword("refs")+"}}" in text and "<ref" not in text or "{{"+util.getwordlc("refs")+"}}" in text and "<ref" not in text:
            self.error_count += 1

        return self.error_count
