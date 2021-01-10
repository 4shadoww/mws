from core import warningbase

class Warning(warningbase.Warningbase):
    wm = "Tason kaksi osio ilman sisältöä"

    def run(self, text):
        text = text.split("\n")
        nextcontent = False
        foundcontent = False
        for line in text:
            if line.count("=") == 4  and line.count("==") == 2 and not nextcontent:
                nextcontent = True
                foundcontent = False
            elif line.count("=") == 4 and line.count("==") == 2 and nextcontent and not foundcontent:
                self.error_count += 1
                nextcontent = True
                foundcontent = False
            elif line != "":
                foundcontent = True

        return self.error_count
