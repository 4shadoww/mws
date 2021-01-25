import re
import string
import random

class Commentparser:
    data_holder = []

    def unid(self):
        return len(self.data_holder)

    def commentid(self, string):
        return "__!COMMENTID"+str(self.unid())

    def endat(self, string, ending):
        if string.endswith(ending):
            return len(string)-len(ending)
        return 0

    def startat(self, string, starting):
        if string.startswith(starting):
            return len(starting)
        return 0

    def parse_comments(self, text):
        comments = re.findall("<!--.*?-->", text, re.DOTALL)
        for comment in comments:
            parsedcomment = self.commentid(comment)
            self.data_holder.append([parsedcomment, comment])
            text = text.replace(comment, parsedcomment)

        return text

    def hide_comments(self, text):
        text = self.parse_comments(text)
        return text

    def restore_comments(self, text):
        for i in self.data_holder:
            print(i)
            text = text.replace(i[0], i[1], 1)
        return text

    def clear(self):
        self.data_holder = []
