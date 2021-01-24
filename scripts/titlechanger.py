import re
from core import script
from core import utilities as util
from core import warning_handler as war

class Algo(script.Script):
    comment0 = "muutti osion oikean nimiseksi"
    comment1 = "muutti osioita oikean nimisiksi"

    warning0 = "otsikko ei tasolla 2"

    zero_edit = False

    def run(self, page):
        titles2change = [["Ulkoiset linkit", "Aiheesta muualla"], ["Ulkoiset linkit:", "Aiheesta muualla"], ["Asiasta muualla", "Aiheesta muualla"],
                         ["Lähteet:", "Lähteet"], ["Lähde:", "Lähteet"], ["Lähde", "Lähteet"], ["Lähdeviitteet", "Lähteet"], ["Viitteet:", "Viitteet"], ["Lähteitä", "Lähteet"]]

        page.text = page.text.split("\n")
        i = 0
        for line in page.text:
            for title in titles2change:
                if util.istitle(line) and util.titleis(title[0], line):
                    if line.count("=") == 4:
                        page.text[i] = "=="+title[1]+"=="
                        self.error_count += 1
                        break
                    else:
                        war.append_warning(self.warning0)
            i += 1
        page.text = '\n'.join(page.text)


        return self.error_count
