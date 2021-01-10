import re
import logging

from core import script
from core import utilities as util

# Get logger
logger = logging.getLogger("infolog")


class Algo(script.Script):
    comment0 =  "poisti ylimääräisen pystyviivan"
    comment1 = "poisti ylimääräiset pystyviivat"

    zero_edit = True

    def run(self, page):
        brackets = re.findall(r"\[(.*?)\]", page.text)
        for item in brackets:
            if '||' in item and util.getword("img") not in item and util.getword("file")  not in item and 'Image:' not in item and 'File:' not in item:
                self.error_count += 1
                olditem = '['+item+']]'
                item = '['+item+']]'
                item = item.replace('||', '|')
                logger.info('twovlines invalid link found: '+page.title()+'\n'+olditem+' --> '+item)
                page.text = page.text.replace(olditem, item)


        return self.error_count
