from core import script

class Algo(script.Script):

  def run(self, page):
    page.text = page.replace("test", "test test")
    return self.error_count
