import re
from core import script
from core import utilities as util

class Algo(script.Script):
    comment0 = "korjasi artikkelin nimen muotoilun määritelmässä"
    comment1 = "monikko"

    zero_edit = False

    def title_any(self, title, bold):
        title_t = title.split(' ')
        low = bold.group(0).lower()
        for i in title_t:
            if i.lower() in low: return True

        return False

    def run(self, page):
        if "'" in page.title: return self.error_count

        templates = util.findtemplatesindex(page.text) + util.findlinksindex(page.text)
        titles = re.finditer(page.title, page.text)
        boldone = list(re.finditer("'{1,5}(.*?)'{1,5}", page.text))

        for bt in boldone:
            if bt.group(0).count("'") == 6 and self.title_any(page.title, bt):
                return self.error_count

        for title in titles:
            in_template = False

            start = title.start(0)
            end = title.end(0)

            for temp in templates:
                if temp[0] < start and temp[1] > end:
                    in_template = True
                    break

            if in_template: continue

            for bt in boldone:
                if bt.start(0) < start and bt.end(0) > end:
                    if (bt.group(0).count("'") == 6 and bt.group(1).lower() == page.title.lower()) or (bt.group(1).lower() != page.title.lower() and self.title_any(title.group(0), bt)):
                        return self.error_count
                    else:
                        page.text = page.text[:bt.start(0)] + "'''"+title.group(0)+"'''" + page.text[bt.end(0):]
                        self.error_count += 1
                        return self.error_count

            page.text = page.text[:start] + "'''"+title.group(0)+"'''" + page.text[end:]
            self.error_count += 1
            return self.error_count
   
        return self.error_count
