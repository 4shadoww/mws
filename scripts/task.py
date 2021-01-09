import re

from core import script

class Algo(script.Script):
    comment0 = "poisti mallineen \"Maailman vanhimmat elävät\""

    def run(self, page):

        results = re.finditer(r"\{\{[Mm]alline:[Mm]aailman vanhimmat elävät(\|.*?|.*?)\}\}\n", page.text, re.MULTILINE)
        for match in results:
            page.text = page.text.replace(match.group(0), '')
            self.error_count = 1


        return self.error_count + 1
