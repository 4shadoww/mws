import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "lihavoi artikkelin nimen määritelmässä"
    comment1 = "monikko"

    zero_edit = False

    def run(self, page):
        templates = re.finditer("{{.*?}}", page.text)
        titles = re.finditer(page.title, page.text)
        boldone = re.finditer("'{1,5}"+page.title+"'{1,5}", page.text)

        for title in titles:
            in_template = False

            start = title.start(0)
            end = title.end(0)

            for temp in templates:
                if temp.start(0) < start and temp.end(0) > end:

                    in_template = True
                    break

            if in_template: continue

            for bt in boldone:
                if bt.start(0) < start and bt.end(0) > end:
                    if bt.group(0).count("'") == 6:
                        return self.error_count
                    else:
                        page.text = page.text[:bt.start(0)] + "'''"+title.group(0)+"'''" + page.text[bt.end(0):]
                        self.error_count += 1
                        return self.error_count

            page.text = page.text[:title.start(0)] + "'''"+title.group(0)+"'''" + page.text[title.end(0):]
            self.error_count += 1
            return self.error_count
   
        return self.error_count
