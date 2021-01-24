import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "muutti englanninkielisen termin suomenkieliseksi"
    comment1 = "muutti englanninkieliset termin suomenkielisiksi"

    zero_edit = True

    def run(self, page):
        self.error_count += page.text.count("[[Category:")
        self.error_count += page.text.count("[[category:")
        #self.error_count += page.text.count("[[File:")
        #self.error_count += page.text.count("[[file:")
        #self.error_count += page.text.count("[[Image:")
        #self.error_count += page.text.count("[[image:")
        self.error_count += page.text.count("{{Reflist")
        self.error_count += page.text.count("{{reflist")
        self.error_count += page.text.count("{{Reflist|")
        self.error_count += page.text.count("{{reflist|")

        page.text = page.text.replace("[[Category:", "[["+util.getwordc("cat"))#.replace("[[File:", "[["+util.getwordc("file")).replace("[[Image:", "[["+util.getwordc("img"))
        page.text = page.text.replace("[[category:", "[["+util.getwordc("cat"))#.replace("[[file:", "[["+util.getwordc("file")).replace("[[image:", "[["+util.getwordc("img"))
        page.text = page.text.replace("{{Reflist", "{{"+util.getword("refs")).replace("{{reflist", "{{"+util.getword("refs")).replace("{{Reflist|", "{{"+util.getword("refs")+"|").replace("{{reflist|", "{{"+util.getword("refs")+"|")

        return self.error_count
