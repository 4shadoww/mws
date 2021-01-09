from core import warningbase

class Warning(warningbase.Warningbase):
    wm = "tukematon viitteet malline"

    def run(self, text):
        if "<references>" in text:
            self.error_count += 1
        return self.error_count
