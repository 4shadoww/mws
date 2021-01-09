import re
import logging
from core import script
from core import utilities as util

# Get logger
logger = logging.getLogger("infolog")

class Algo(script.Script):
    comment0 = "korjasi linkin"
    comment1 = "korjasi linkkejä"

    zero_edit = False

    def run(self, page):
        linkpartlist = []
        fixedlinks = []
        invalidlinks = []
        characters = 'abcdefghijklmnopqrstuvxyzäöABCDEFGHIJKLMNOPQRSTUVXYZŽÄÖ!?*[]{}()0123456789'
        special = '!?*[]{}()'
        twobrackets = re.findall(r"\[(\S+)\]", page.text)
        for hit in twobrackets:
            link = str(hit)
            matches = re.search(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}', link)
            if 'http://' not in link and 'https://' not in link and matches != None and 'ref' not in link and '@' not in link and '[' not in link and '{' not in link[0:2]:
                orglink = '['+link+']'
                self.error_count += 1
                linkpartlist = link.split('.')

                if len(linkpartlist) >= 3 and 'w' in linkpartlist[0] and linkpartlist[0] != 'www':
                    if any((char in linkpartlist[0]) for char in characters):
                        if any((char in linkpartlist[0]) for char in special):
                            continue
                    else:
                        if len(linkpartlist[0]) != 3:
                            linkpartlist[0] = 'www'
                            time = 0
                            finallink = ''
                            for item in linkpartlist:
                                time += 1
                                if time != len(linkpartlist):
                                    finallink = finallink+item+'.'
                                else:
                                    finallink = finallink+item
                            link = '[http://'+finallink+']'
                            logger.info('fixblink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                            page.text = page.text.replace(orglink, link)
                            fixedlinks.append(link)
                            invalidlinks.append(orglink)
                        else:
                            logger.error('www fix error')

                else:
                    link = '[http://'+link+']'
                    logger.info('fixblink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                    fixedlinks.append(link)
                    invalidlinks.append(orglink)
                    page.text = page.text.replace(orglink, link)

        return self.error_count
