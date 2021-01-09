import re
import html
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
        refs = re.findall(r"\<ref>.*?\</ref>", page.text)

        for hit in refs:
            link = str(hit)
            orglink = link
            link = link.replace('<ref>', '').replace('</ref>', '')
            matches = re.search(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}', link)
            if 'http://' not in link and 'https://' not in link and matches != None and 'ref' not in link and '@' not in link and '{' not in link[0:2] and '[' not in link[1:2] and 'ftp://' not in link and "'" not in link[0:2]:
                if '[' in link and ']' in  link:
                    linkpartlist = link.split('.')
                    if ' ' in linkpartlist[0][1:] or ' ' in linkpartlist[1][0:1]:
                        continue
                    if len(linkpartlist) >= 3 and 'w' in linkpartlist[0] and linkpartlist[0] != 'www':
                        if '[' not in linkpartlist[0][0:1] and any((char in linkpartlist[0]) for char in characters):
                            if any((char in linkpartlist[0]) for char in special):
                                logger.info('fixreflinks: special mark found getting out')
                                continue
                        else:
                            if len(linkpartlist[0]) != 3 or '[' in linkpartlist[0]:
                                linkpartlist[0] = 'www'
                                time = 0
                                finallink = ''
                                for item in linkpartlist:
                                    time += 1
                                    if time != len(linkpartlist):
                                        finallink = finallink+item+'.'
                                    else:
                                        finallink = finallink+item
                                link = '<ref>[http://'+finallink+'</ref>'
                                logger.info('fixreflink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                                fixedlinks.append(link)
                                invalidlinks.append(orglink)
                            else:
                                logger.info('www fix error: '+ str(linkpartlist))

                    else:
                        link = link.replace('[','')
                        link = '<ref>[http://'+link+'</ref>'
                        logger.info('fixreflink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                        fixedlinks.append(link)
                        invalidlinks.append(orglink)
                else:
                    linkpartlist = link.split('.')
                    if ' ' in linkpartlist[0][1:] or ' ' in linkpartlist[1][0:1]:
                        continue
                    if len(linkpartlist) >= 3 and 'w' in linkpartlist[0] and linkpartlist[0] != 'www':
                        if any((char in linkpartlist[0]) for char in characters):
                            if any((char in linkpartlist[0]) for char in special):
                                continue
                        else:
                            print(linkpartlist[0])
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
                                link = '<ref>http://'+finallink+'</ref>'
                                logger.info('fixreflink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                                fixedlinks.append(link)
                                invalidlinks.append(orglink)

                            else:
                                logger.info('www fix error: '+ str(linkpartlist))

                    else:
                        link = '<ref>http://'+link+'</ref>'
                        logger.info('fixreflink invalid link found: '+page.title+'\n'+orglink+' --> '+link)
                        fixedlinks.append(link)
                        invalidlinks.append(orglink)

        for fixedlink, invalidlink in zip(fixedlinks, invalidlinks):
            self.error_count += 1
            i =  html.unescape(str(invalidlink))
            f = html.unescape(str(fixedlink))
            page.text = page.text.replace(i, f)

        return self.error_count
