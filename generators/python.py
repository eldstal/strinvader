#!/usr/bin/env python3
#
# Generates databases for python's builtin transforms
#  py_lower
#  py_upper

import re
import os
import json
import requests
import unicodedata
import argparse
import urllib
import urllib3

def urllib_norm(txt):
  try:
    url = urllib.parse.urlparse(f"http://{txt}")
    norm = url.hostname

    # Good old unicode hostnames
    if "xn--" in norm: return txt
    if len(norm) == 0: return txt

    return norm
  except Exception as e:
    print(e)
    return txt

  return txt


def urllib3_norm(txt):
  try:
    url = urllib3.util.parse_url(f"http://{txt}")
    norm = url.hostname

    # Good old unicode hostnames
    if "xn--" in norm: return txt
    if len(norm) == 0: return txt

    return norm
  except:
    return txt

  return txt


def add(dic, key, val):
  if key == val: return
  if key not in dic:
    dic[key] = []
  if val not in dic[key]:
    dic[key].append(val)



def make_single_database(codepoints, norm_func):

  db = { "single": {}, "multi": {} }

  for src_cp in codepoints:
    norm_str = norm_func(chr(src_cp))

    if norm_str is None: continue

    if chr(src_cp) not in norm_str:
      if len(norm_str) == 1: add(db["single"], norm_str, src_cp)
      else:                  add(db["multi"],  norm_str, src_cp)

  return db


def make_databases():

  codepoint_file = os.path.dirname(__file__)
  codepoint_file = os.path.join(codepoint_file, "codepoints.json")
  cp = json.load(open(codepoint_file, "r"))

  return {
    "py_lower": make_single_database(cp, lambda txt: txt.lower()),
    "py_upper": make_single_database(cp, lambda txt: txt.upper()),
    "py_urllib": make_single_database(cp, urllib_norm),
    "py_urllib3": make_single_database(cp, urllib3_norm)
  }



def main():

  default_dir = os.path.dirname(__file__)
  default_dir = os.path.abspath(default_dir)
  default_dir = os.path.dirname(default_dir)
  default_dir = os.path.join(default_dir, "databases")

  parser = argparse.ArgumentParser(description="Generate unicode normalization databases")

  parser.add_argument('--database-dir', '-d', type=str, default=default_dir,
      help="Target directory where json files are written")

  conf = parser.parse_args()

  databases = make_databases()

  for name in databases.keys():
    print(name)
    dbfile = open(os.path.join(conf.database_dir, f"{name}.json"), "w")
    dbfile.write(json.dumps(databases[name]))
    dbfile.close()


if __name__ == "__main__":
  main()
