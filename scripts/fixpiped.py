import logging
import re
from core import script
from core import utilities as util

# Get logger
logger = logging.getLogger("infolog")

class Algo(script.Script):
    comment0 = "poisti wikipedian sisäisestä linkistä tekstin jossa se on sama kuin linkki"
    comment1 = "poisti wikipedian sisäisistä linkeistä tekstin joissa se on sama kuin linkki"

    zero_edit = True

    def run(self, page):
        searchtext = page.text.replace(' ', '_')
        twobrackets = re.findall(r"\[(\S+?)\]", searchtext )

        for item in twobrackets:
            fixeditem = None
            originalitem = item
            if '|' in item:
                item = item.replace('[', '').replace(']', '')
                item = item.split('|')

                if item[0] == item[1]:
                    fixeditem = '['+str(item[0])+''
                    fixeditem = fixeditem.replace('_', ' ')
                if fixeditem != None:
                    self.error_count += 1
                    originalitem = originalitem.replace('_', ' ')
                    logger.info('fixpiped invalid links found: '+page.title+'\n'+originalitem+'] --> '+fixeditem+']')
                    page.text = page.text.replace(str(originalitem), str(fixeditem))

        return self.error_count
