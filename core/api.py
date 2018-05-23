import json
from urllib.request import urlopen
from urllib.parse import urlencode
import traceback
import logging

from core import session

logger = logging.getLogger("infolog")

def parameter_maker(values):
  if type(values) != list:
    return values

  final_str = ""
  for i in range(len(values)):
    final_str += str(values[i])

    if i < len(values) - 1:
      final_str += "|"

  return final_str


def get_token(token_type):
  params = {
    "action": "query",
    "meta": "tokens",
    "type": parameter_maker(token_type)
  }
  return session.session.get(params)["query"]["tokens"]

def get_text(title):
  params = {
    "action": "query",
    "prop": "revisions",
    "titles": title,
    "rvprop": "content|timestamp",
  }
  query = session.session.get(params)["query"]["pages"]
  for pageid in query:
    if pageid == "-1":
      return False
    if "revisions" not in query[pageid]:
      return False
    return (query[pageid]["revisions"][0]["*"], query[pageid]["revisions"][0]["timestamp"])

  return False

def save_page(title, text, comment, basetimestamp=None, minor=False):
  params = {
    "action": "edit",
    "title": title,
    "text": text,
    "summary": comment,
    "minor": minor,
    "bot": True,
    "token": get_token(["csrf"])["csrftoken"]
  }
  if basetimestamp:
    params["basetimestamp"] = basetimestamp
  session.session.post(params)
  return True
