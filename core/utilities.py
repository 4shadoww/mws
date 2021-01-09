import re
from core import config_loader
from core.langdict import *

warnings = {
    "war0fi": "lop ristiriita: kaksi samanlaista riviä",
}

def andop(items, text):
    for item in items:
        if item in text:
            return True
    return False

def istag(tag, data):
    if data.count("<") == 1 and data.count(">") == 1 and tag in data:
        data = re.sub('[^a-zA-Z0-9 ]', ' ', data).split()

        if data[0] == tag:
            return True
    return False


def getword(id, lang=None):
    if lang == None:
        wl = config_loader.config["lang"]
        return wl[id]

    wl = globals()[lang]
    return wl[id]

def getwordlc(id, lang=None):
    if lang == None:
        wl = config_loader.config["lang"]
        return wl[id].lower()

    wl = globals()[lang]
    return wl[id].lower()

def getwordlcc(id, lang=None):
    if lang == None:
        wl = config_loader.config["lang"]
        return wl[id].lower()+":"

    wl = globals()[lang]
    return wl[id].lower()+":"

def getwordulc(id, lang=None):
    if lang == None:
        wl = config_loader.config["lang"]
        return wl[id], wl[id].lower()

    wl = globals()[lang]
    return wl[id], wl[id].lower()

def getwordc(id, lang=None):
    if lang == None:
        wl = config_loader.config["lang"]
        return wl[id]+":"

    wl = globals()[lang]
    return wl[id]+":"

def titlein(title, text):
    titles = re.findall(r"\=.*\=", text)
    for i in titles:
        if re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', i) == re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', title):
            return True

    return False

def titleis(title, text):
    titles = re.findall(r"=(?!=)(.+?)(=+?)", text)[0]

    if titles[0].lstrip().rstrip() == title:
        return True

    return False

def titlepos(title, text):
    titles = re.findall(r"\=.*\=", text)
    for i in titles:
        if re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', i) == re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', title):
            return text.find(i)

    return False

def titleline(title, text):
    for l, line in enumerate(text.split("\n")):
        titles = re.findall(r"\=.*\=", line)
        for item in titles:
            if re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', item) == re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', title):
                return l

    return False

def zeromatch(items, text):
    for item in items:
        if item in text:
            return False

    return True

def anymatch(items, text):
    for item in items:
        if item in text:
            return True

    return False

def abandop(items, match):
    for item in items:
        if item == match:
            return True
    return False

def istitle(title):
    titles = re.findall(r"\=.*\=", title)

    if len(titles) == 1 and re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', titles[0]) == re.sub('[^a-zA-Z0-9åäöÅÄÖ]', '', title):
        return True

    return False

def titlebefore(after, before, text, subtitles=True):
    text = text.split("\n")
    nextref = False

    for line in text:
        if titlein(after, line):
            nextref = True
            continue
        if titlein(before, line) and nextref:
            return True
        elif istitle(line) and nextref:
            if not subtitles and  line.count("=") <= 4:
                return False
            elif subtitles:
                return False

    return False

def listend(text, title, listitems, nono):
    startpos = titleline(title, text)
    endpos = titleline(title, text)
    text = text.split("\n")
    belows = text[startpos:len(text)]
    tries = 0
    lasttemp = 0
    listfound = False

    for l in  range(0, len(belows)):

        if l == 0:
            continue

        if anymatch(listitems, belows[l]):
            listfound = True
            endpos = len(text)-len(belows)+l

        if belows[l] == "":
            tries += 1

        else:
            tries = 0

        if l == 3 and listfound == False:
            break

        elif tries >= 2:
            endpos = len(text)-len(belows)+l
            break

        if istitle(belows[l]) and "===" not in belows[l]:
            endpos = len(text)-len(belows)+l-1
            break

        if anymatch(listitems, belows[l]) and "{{" in belows[l] and anymatch(nono, belows[l]) == False:
            lasttemp += belows[l].count("{{")

        elif lasttemp > 0 and "{{" in belows[l]:
            lasttemp += belows[l].count("{{")

        if "}}" in belows[l] and lasttemp > 0:
            lasttemp -= belows[l].count("}}")
            endpos = len(text)-len(belows)+l
            continue

        elif lasttemp > 0:
            endpos = len(text)-len(belows)+l
            continue

        if anymatch(nono, belows[l]):
            endpos = len(text)-len(belows)+l-1
            break

        if zeromatch(listitems, belows[l]) and listfound and l+1 != len(belows) and zeromatch(listitems, belows[l+1]):
            endpos = len(text)-len(belows)+l-1
            break

    return startpos, endpos, listfound

def removefromlist(sec, listobj):
    confirmed = False
    i = 0
    startpos = None

    for l in range(0, len(listobj)):
        if i == len(sec):
            confirmed = True
            break

        if sec[i] == listobj[l]:
            if startpos == None:
                startpos = l
            i += 1
        else:
            startpos = None
            i = 0

    for l in range(0, len(sec)):
        listobj.pop(startpos)

    return listobj

def tagwithoutend(text):
    looking4end = []
    tags = re.findall("<.*?>", text)
    for tag in tags:
        data = re.sub('[^a-zA-Z0-9 ]', ' ', tag).split()
        if len(data) > 0 and "/" not in tag:
            looking4end.append(data[0])
        elif len(data) > 0 and "/" in tag:
            for l, starttag in enumerate(looking4end):
                if starttag == data[0]:
                    looking4end.pop(l)

    if len(looking4end) > 0:
        return True
    return False

def getsec(text):
    secs = []
    cut = False
    for l in  range(0, len(text)):
        thread_header = re.search('^== *([^=].*?) *== *$', text[l])
        if thread_header:
            if cut == True:
                secs.append(text[start:l])
            start = l
            cut = True
        elif len(text)-1 == l:
            secs.append(text[start:l])
    return secs

def insec(string, secn, text):
    text = text.split("\n")
    secs = getsec(text)
    for sec in secs:
        if string in '\n'.join(sec) and sec[0].replace("==", "").lstrip().rstrip() == secn:
            return True
    return False

def refindall(pattern, text):
    positions = []
    for m in re.finditer(pattern, text):
        positions.append([m.start(0), m.end(0), text[m.start(0):m.end(0)]])
    return positions

def replacepos(string, text, start, end):
    length = end - start - 1
    for i in range(length):
        text.pop(start)
    text[start] = string
    text = ''.join(text)
    text = list(text)
    return text

def reupdatelist(positions, text):
    # This isn't working. Yet, or never.
    for i in range(len(positions)):
        matches = re.finditer(positions[i][2], text)
        if len(list(matches)) > 1:
            ind = 0
            for m in re.finditer(positions[i][2], text):
                while True:
                    print(positions[i+ind][2], text[m.start(0):m.end(0)])
                    if len(positions) <= i+ind:
                        print("error: failed to update list!")
                        break

                    if positions[i+ind][2] == text[m.start(0):m.end(0)]:
                        print("dis")
                        positions[i+ind][0] = m.start(0)
                        positions[i+ind][1] = m.end(0)
                        break
                    ind += 1

        else:
            for m in re.finditer(positions[i][2], text):
                print("update")
                positions[i][0] = positions[i][0] = m.start(0)
                positions[i][1] = positions[i][1] = m.end(0)

def findtemplates(text):
    templates = []

    start = -1
    end = -1
    index = 0

    for i in range(len(text)):
        if text[i] == "{":
            index += 1
            if start == -1:
                start = i
        elif text[i] == "}":
            index -= 1
            if index == 0:
                end = i
                templates.append(text[start:end+1])
                start = -1
                end = -1
    return templates

def remove_ending(ending, string):
    string = string.rstrip()
    if string.endswith(ending):
        string = string[:-len(ending)]
    return string

def isInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
