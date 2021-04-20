#!/usr/bin/env python3
#
# Generates six databases, based on the unicode standard:
#  lower
#  upper
#  nfc
#  nfd
#  nkfc
#  nkfd

import re
import os
import json
import requests
import unicodedata
import argparse

def add(dic, key, val):
  if key == val: return
  if key not in dic:
    dic[key] = []
  if val not in dic[key]:
    dic[key].append(val)


def parse_unicode_fields(txt):
  lines = txt.split("\n")
  ret = []
  for l in lines:
    # Away with the comments
    l = re.sub("(.*)#.*", r"\1", l)
    l = l.strip()

    # Whatever to you and your empty lines
    if l == "": continue

    # Semicolon-separated CSV
    ret.append(l.split(";"))

  return ret


def get_unicode_data(filename="UnicodeData.txt"):
  if not os.path.isfile(filename):
    print("Downloading UnicodeData.txt...")
    resp = requests.get("https://www.unicode.org/Public/9.0.0/ucd/UnicodeData.txt")
    open(filename, "w+").write(resp.text)

  return open(filename, "r").read()

def make_single_database(codepoints, norm_func):

  db = { "single": {}, "multi": {} }

  for src_cp in codepoints:
    norm_str = norm_func(chr(src_cp))

    if norm_str is None: continue

    if chr(src_cp) not in norm_str:
      if len(norm_str) == 1: add(db["single"], norm_str, src_cp)
      else:                  add(db["multi"],  norm_str, src_cp)

  return db

# Documentation:
# https://www.unicode.org/Public/5.1.0/ucd/UCD.html#UnicodeData.txt
def make_databases():

  rows = parse_unicode_fields(get_unicode_data())

  cp = []
  to_lower = {}
  to_upper = {}

  for r in rows:
    src_cp = int(r[0], 16)
    cp.append(src_cp)

    try:
      to_upper[chr(src_cp)] = chr(int(r[12], 16))
    except:
      to_upper[chr(src_cp)] = None

    try:
      to_lower[chr(src_cp)] = chr(int(r[13], 16))
    except:
      to_lower[chr(src_cp)] = None


  return {
    "lower": make_single_database(cp, lambda txt: to_lower[txt]),
    "upper": make_single_database(cp, lambda txt: to_upper[txt]),
    "nfc" : make_single_database(cp, lambda txt: unicodedata.normalize("NFC", txt)),
    "nfd" : make_single_database(cp, lambda txt: unicodedata.normalize("NFD", txt)),
    "nfkc" : make_single_database(cp, lambda txt: unicodedata.normalize("NFKC", txt)),
    "nfkd" : make_single_database(cp, lambda txt: unicodedata.normalize("NFKD", txt)),
  }



def main():

  default_dir = os.path.dirname(__file__)
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
