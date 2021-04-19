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
  if val not in dic[key]:
    dic[key].append(val)

# Returns a list of possible string replacement tuples [ (dst, src) ]
def multi_char_replacements(text, databases):
  ret = []
  for form,db in databases.items():
    if "multi" not in db: continue

    for key,val in db["multi"].items():
      dst = "".join(map(chr, key))
      if dst in text:
        src = map(chr, val)
        for s in src:
          #print(f"{dst} <- {s}")
          ret.append((dst, s))
  return ret

def multi_char_replacement_lists(text, databases):
  ret = {}
  for form,db in databases.items():
    if "multi" not in db: continue

    for key,val in db["multi"].items():
      dst = "".join(map(chr, key))
      if dst in text:
        src = map(chr, val)
        for s in src:
          add(ret, dst, s)
  return ret

def multi_char_replace(text, databases, offset=0):
  options = multi_char_replacements(text, databases)

  i = 0   # Used to choose which replacements to enable
  chunks = [ (text, "text") ]
  for dst,src in options:
    for c in range(len(chunks)):
      t,mode = chunks[c]
      if mode != "text": continue

      if dst not in t: continue
      if i % 10 != offset: continue

      new_chunk = (src, "multi")
      pieces = [ (subt, "text") for subt in t.split(dst) ]

      #print(f"replacing {dst} in {t} with {src}")
      #print(pieces)

      replacement = [ pieces[0] ]
      for i in range(1,len(pieces)):
        replacement += [new_chunk]
        replacement += [pieces[i]]

      chunks = chunks[:c] + replacement + chunks[c+1:]
    i += 1


  # Split up all the "text" chunks into single characters
  # In the end, there should be only "single" and "multi" chunks.
  def split(chunk):
    t,mode = chunk
    if mode != "text": return [chunk]
    return [ (c, "single") for c in t ]

  def flatten(lstlst):
    ret = []
    for e in lstlst:
      if type(e) == list:
        ret += e
      else:
        ret.append(e)
    return ret

  complete = flatten(map(split, chunks))

  return complete


def single_codepoint_replacements(char, databases):
  ret = []
  key = ord(char)
  for n,db in databases.items():
    if "single" not in db: continue

    if key in db["single"]:
      ret += db["single"][key]

  if len(ret) == 0: ret.append(char)
  return list(set(ret))

def single_char_replacements(char, databases):
  codepoints = single_codepoint_replacements(char, databases)
  return list(map(chr, codepoints))

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

  upper = { "single": {}, "multi": {}}
  lower = { "single": {}, "multi": {}}
  nfc = { "single": {}, "multi": {}}
  nfd = { "single": {}, "multi": {}}
  nfkc = { "single": {}, "multi": {}}
  nfkd = { "single": {}, "multi": {}}

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

    src_char = chr(src_cp)
    norm_nfc  = tuple(map(ord, unicodedata.normalize("NFC", src_char)))
    norm_nfd  = tuple(map(ord, unicodedata.normalize("NFC", src_char)))
    norm_nfkc = tuple(map(ord, unicodedata.normalize("NFKC", src_char)))
    norm_nfkd = tuple(map(ord, unicodedata.normalize("NFKD", src_char)))

    if len(norm_nfc) == 1: add(nfc["single"],   norm_nfc[0], src_cp)
    else:                  add(nfc["multi"],    norm_nfc, src_cp)

    if len(norm_nfd) == 1: add(nfd["single"],   norm_nfd[0], src_cp)
    else:                  add(nfd["multi"],    norm_nfd, src_cp)

    if len(norm_nfkc) == 1: add(nfkc["single"],  norm_nfkc[0], src_cp)
    else:                   add(nfkc["multi"],   norm_nfkc,    src_cp)

    if len(norm_nfkd) == 1: add(nfkd["single"], norm_nfkd[0], src_cp)
    else:                   add(nfkd["multi"],  norm_nfkd, src_cp)


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

parser.add_argument('--no-single', '-S', action="store_true",
    help="Disable single-codepoint replacements (one-to-one normalizations)")

parser.add_argument('--no-multi', '-M', action="store_true",
    help="Disable multi-codepoint replacements (e.g. ligatures)")

parser.add_argument('--show-codepoints', '-C', action="store_true",
    help="In char mode, also show numeric (hex) codepoints")


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

    
    for n in range(conf.num):
      out = ""

      # Candidates contains tuples of
      # (char, "single") for single characters and
      # (text, "multi") for chosen multi-char replacements

      # First pass: Perform as many multi-char replacements as possible
      # Second pass: Perform single-char replacements for what's left

      # Here's a default result for the first pass, with no multi-char replacements
      chunks = [ (c, "single") for c in conf.text ]
      if not conf.no_multi:
        chunks = multi_char_replace(conf.text, databases, n)

      if not conf.no_single:
        # Pseudo-random for predictability and variation
        for chunk_idx in range(len(chunks)):
          c,mode = chunks[chunk_idx]
          if mode != "single": continue

          single_options = single_char_replacements(c, databases)
          x = single_options[(n+chunk_idx) % len(single_options)]
          chunks[chunk_idx] = (x, "single")

      out = "".join([ txt for txt,mode in chunks ])

      print(out)

  elif conf.char != "":
    if not conf.no_single:
      chars = [ c for c in "".join(list(set(list(conf.char)))) ]
      for c in chars:
        codepoints = single_codepoint_replacements(c, databases)
        if conf.show_codepoints:
          options = [ (chr(c), f"U+{c:04x}") for c in codepoints ]
        else:
          options = [ chr(c) for c in codepoints ]
        print(f"{c} <- {options}")

    if not conf.no_multi:
      matches = multi_char_replacement_lists(conf.char, databases)
      for s,denorms in matches.items():
        if conf.show_codepoints:
          options = [ (c, f"U+{ord(c):04x}") for c in denorms ]
        else:
          options = [ c for c in denorms ]
        print(f"{s} <- {options}")

  else:
    sys.stderr.write("Please provide either --text or --char input")
    return


if __name__ == "__main__":
  main()
