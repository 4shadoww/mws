import logging
import threading
import importlib
import time
import traceback

from core import config_loader
from core import api
from core.lang import lang
from core import adiffer

# Get logger
logger = logging.getLogger("infolog")

# Save lock
save_lock = threading.Lock()

# Load lock
load_lock = threading.Lock()

class Page:
  title = ""
  text = ""
  comment = ""
  basetimestamp = ""
  minor = False

  def __init__(self, title, text, timestamp):
    self.title = title
    self.text = text
    self.basetimestamp = timestamp
  
  def set_comment(self, comment):
    self.comment = comment
  
  def set_minor(self, minor):
    self.minor = minor

class holder:
  kill = False

def load_tests():
  objects = []
  # Load scripts
  for test in config_loader.config["tests"]:
    # Filter using ignored_scripts
    if test not in config_loader.config["ignored_tests"]:
      module = importlib.import_module("tests."+test)
      objects.append(module.Test())

  return objects

def load_scripts():
  objects = []
  # Load scripts
  for script in config_loader.config["scripts"]:
    # Filter using ignored_scripts
    if script not in config_loader.config["ignored_scripts"]:
      module = importlib.import_module("scripts."+script)
      objects.append(module.Algo())

  return objects

def page_loader(load_pages, loaded_pages, killer):
  for page in load_pages:
    # If kill if KeyboardInterrupt received
    if killer.kill: return
    # Get text
    textts = api.get_text(page)
    if not textts:
      logger.error("page %s not found" % page)
      continue
    # Add to loaded pages
    with load_lock:
      loaded_pages.append(Page(page, textts[0], textts[1]))

def page_saver(save_pages, killer):
  # Run until KeyboardInterrupt received
  while not killer.kill:
    # Check is pages available
    if len(save_pages) > 0:
      try:
        # Save page
        api.save_page(save_pages[0].title, save_pages[0].text, save_pages[0].comment, basetimestamp=save_pages[0].basetimestamp, minor=save_pages[0].minor)
        with save_lock:
          # Delete saved page from pages to be saved list
          del save_pages[0]
      except:
        logger.critical("cannot save page %s" % save_pages[0].title)
        logger.critical(traceback.format_exc())
      continue

    time.sleep(1)

def create_comment(comments):
  full_comment = u""
  i = 0
  for comment in comments:
    if i == 0:
      full_comment += lang[config_loader.config["lang"]]["bot"].title()+" "

    full_comment += comment

    if i == len(comments)-1:
      full_comment += "."

    elif i == len(comments)-2:
      full_comment += " "+lang[config_loader.config["lang"]]["and"]+" "

    else:
      full_comment += ", "

    i += 1
  return full_comment

def run(pages, run_tests=False):
  # TODO this function could be breaked down to smaller parts
  # And could be more maintainable
  # Killer object
  killer = holder
  # Threads
  threads = []
  # Loaded pages
  loaded_pages = []

  if run_tests:
    tests = load_tests()

  try:
    logger.info("loading scripts")
    # Load scripts
    scripts = load_scripts()
    # Start page_loader
    logger.info("staring to load pages")
    pl = threading.Thread(target=page_loader, args=(pages, loaded_pages, killer))
    pl.start()
    threads.append(pl)
    # Check is test mode enabled
    if not config_loader.config["test"] and not run_tests:
      # Pages to be saved
      save_pages = []
      # Start page_saver
      ps = threading.Thread(target=page_saver, args=(save_pages, killer))
      ps.start()
      threads.append(ps)

    # Loop
    while (len(loaded_pages) > 0 or pl.isAlive()):
      if len(loaded_pages) > 0:
        # Comments
        comments = []
        # Get page
        page = loaded_pages[0]
        oldtext = page.text
        logger.info("checking: %s" % page.title)
        with load_lock:
          del loaded_pages[0]
        for script in scripts:
          error_count = script.run(page)

          # Add comment
          if error_count > 1:
            comments.append(script.comment1)
          else:
            comments.append(script.comment0)

        # Run tests mode
        if run_tests:
          for test in tests:
            passed = test.run(page)
            if passed:
              logger.info("page %s passed test %s" % (page.title, test))
            else:
              logger.error("warning: page %s didn't pass test %s" % (page.title, test))
          
          logger.info("tests done")

        elif page.text != oldtext:
          page.comment = create_comment(comments)
          page.minor = config_loader.config["minor"]

          # Review mode
          if config_loader.config["review"]:
            adiffer.show_diff(oldtext, page.text)
            print("summary:", page.comment)
            answer = input("do you agree these changes [y/N] ")
            
            if answer.lower() == "p":
              print(page.text)
              print("summary:", page.comment)
              answer = input("do you agree these changes [y/N] ")
              if not answer.lower() == "y":
                continue
            
            elif not answer.lower() == "y":
              continue

          if not bool(config_loader.config["test"]):
            with save_lock:
              save_pages.append(page)
        
        # Don't sleep if page is checked
        continue
      
      # Sleep
      time.sleep(0.01)
    
    if not config_loader.config["test"] and not run_tests and len(save_pages) > 0:
      logger.info("saving pages")

    # Wait pages to be saved
    while(not config_loader.config["test"] and not run_tests and len(save_pages) > 0):
      time.sleep(0.1)
    # Done kill threads
    killer.kill = True
  except KeyboardInterrupt:
    logger.info("halting threads")
    killer.kill = True
    logger.info("waiting threads to halt")
    for thread in threads:
      logger.info("waiting thread %s" % str(thread))
      thread.join()
    logger.info("exiting...")
