from core import test

class Test(test.Test):
  def run(self, page):
    return "test" in page.text
