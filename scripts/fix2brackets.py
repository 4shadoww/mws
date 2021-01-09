import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "poisti ylimääräiset hakasulkeet ulkoisesta linkistä"
    comment1 = "poisti ylimääräiset hakasulkeet ulkoisista linkeistä"

    zero_edit = False

    def run(self, page):
        nono = [util.getwordc("file"), util.getwordc("file", lang="en"), util.getwordc("img"), util.getwordc("img", lang="en")]

        textlist = page.text.split('\n')
        for l, line in enumerate(textlist):
            matches = re.findall(r"\[.*?\]", line)
            for match in matches:
                if 'https://' in match and match.count("[") < 2 and "|" not in match or 'http://' in match and match.count("[") < 2 and "|" not in match:
                    if match.count("[") >= 2 or match.count("]") >= 2:
                        newmatch = "["+match.replace("[", "").replace("]", "")+"]"
                        textlist[l] = textlist[l].replace(match, newmatch)
                        self.error_count += 1

        page.text = '\n'.join(textlist)

        return self.error_count
