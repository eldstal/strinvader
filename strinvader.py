#!/usr/bin/env python3

import sys
import os
import re
import requests
import unicodedata
import argparse

def add(dic, key, val):
  if key == val: return
  if key not in dic:
    dic[key] = []
  dic[key].append(val)

def replacements(char, databases):
  ret = []
  key = ord(char)
  for n,db in databases.items():
    if key in db:
      ret += [ chr(cp) for cp in db[key] ]

  if len(ret) == 0: ret.append(char)
  return ret

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

# Documentation:
# https://www.unicode.org/Public/5.1.0/ucd/UCD.html#UnicodeData.txt
# Returns a dict of databases.
# Each database is a dictionary of codepoints.  dest -> [ src, src, ...]
# If you look up codepoint XYZW in a database, you will find all codepoints x such that norm(x) == chr(XYZW)
def make_databases():

  txt = get_unicode_data()

  upper = {}
  lower = {}
  nfc = {}
  nfd = {}
  nfkc = {}
  nfkd = {}

  rows = parse_unicode_fields(txt)
  for r in rows:
    assert(len(r) == 15)

    src_cp = int(r[0], 16)

    try:
      upper_cp = int(r[12], 16)
    except:
      upper_cp = None

    try:
      lower_cp = int(r[13], 16)
    except:
      lower_cp = None

    if lower_cp: add(lower, lower_cp, src_cp)
    if upper_cp: add(upper, upper_cp, src_cp)

    # TODO: Reimplement this if it's too slow
    src_char = chr(src_cp)
    norm_nfc  = unicodedata.normalize("NFC", src_char)
    norm_nfd  = unicodedata.normalize("NFC", src_char)
    norm_nfkc = unicodedata.normalize("NFKC", src_char)
    norm_nfkd = unicodedata.normalize("NFKD", src_char)

    if len(norm_nfc) == 1: add(nfc, ord(norm_nfc), src_cp)
    if len(norm_nfd) == 1: add(nfd, ord(norm_nfd), src_cp)
    if len(norm_nfkc) == 1: add(nfkc, ord(norm_nfkc), src_cp)
    if len(norm_nfkd) == 1: add(nfkd, ord(norm_nfkd), src_cp)


  databases = {
    "upper": upper,
    "lower": lower,
    "nfc": nfc,
    "nfd": nfd,
    "nfkc": nfkc,
    "nfkd": nfkd,

  }
  return databases


parser = argparse.ArgumentParser(description="Hack the planet")

parser.add_argument('--forms', '-f', nargs="*", default=None,
    help="Specific conversion(s) to check (lower, upper, nfc, nfd, nfkc, nfkd)")

parser.add_argument('--num', '-n', type=int, default=1,
    help="Number of alternative conversions to generate")

parser.add_argument('--text', '-t', type=str, default="",
    help="Give --num conversion options for a --text string")

parser.add_argument('--char', '-c', type=str, default="",
    help="Show all single-character denormalizations")


conf = parser.parse_args()




def main():

  databases = make_databases()

  all_forms = databases.keys()

  if conf.forms is None:
    conf.forms = all_forms

  databases = { n:db for n, db in databases.items() if n in conf.forms }

  if len(databases) == 0:
    sys.stderr.write(f"No databases selected. Possibilities are: {all_forms}")
    return

  if conf.text != "":
    options = [ replacements(c, databases) for c in conf.text ]
    for n in range(conf.num):
      # Pseudo-random for predictability and variation
      out = ""
      for c in range(len(conf.text)):
        x = options[c][(n+c) % len(options[c])]
        out += x
      print(out)

  elif conf.char != "":
    chars = [ c for c in "".join(list(set(list(conf.char)))) ]
    for c in chars:
      options = replacements(c, databases)
      print(f"{c} <- {options}")

  else:
    sys.stderr.write("Please provide either --text or --char input")
    return


if __name__ == "__main__":
  main()
