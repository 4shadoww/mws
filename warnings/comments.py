from core import warningbase

class Warning(warningbase.Warningbase):
    wm = "artikkelissa on kommentti"

    error_count = 0

    def run(self, text):
        if "<!--" in text or "-->" in text:
            self.error_count += 1

        return self.error_count
