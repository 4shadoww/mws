from core import warningbase

class Warning(warningbase.Warningbase):
    wm = "vain esimerkki"

    def run(self, text):
        self.error_count += 1

        return self.error_count
