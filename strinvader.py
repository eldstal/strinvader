#!/usr/bin/env python3

import sys
import os
import re
import glob
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

# Returns a list of possible string replacement tuples [ (dst, src) ]
def multi_char_replacements(text, databases):
  ret = []
  for form,db in databases.items():
    if "multi" not in db: continue

    for dst,val in db["multi"].items():
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

    for dst,val in db["multi"].items():
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
  key = char
  for n,db in databases.items():
    if "single" not in db: continue

    if key in db["single"]:
      ret += db["single"][key]

  if len(ret) == 0: ret.append(ord(char))
  return list(set(ret))

def single_char_replacements(char, databases):
  codepoints = single_codepoint_replacements(char, databases)
  return list(map(chr, codepoints))




def load_databases(conf):
  databases = {}

  pattern = os.path.join(conf.database_dir, "*.json")
  dbfiles = glob.glob(pattern)

  for dbfile in dbfiles:
    name = os.path.basename(dbfile).split(".json")[0]
    data = json.load(open(dbfile, "r"))
    if "single" not in data or "multi" not in data:
      sys.stderr.write(f"Database {dbfile} appears to be invalid.\n")
      continue
    databases[name] = data
  return databases


def main():

  default_dir = os.path.dirname(__file__)
  default_dir = os.path.join(default_dir, "databases")

  parser = argparse.ArgumentParser(description="Hack the planet")

  parser.add_argument('--database-dir', '-d', type=str, default=default_dir,
      help="Target directory where database json files are found")

  parser.add_argument('--forms', '-f', nargs="*", default=None,
      help="Specific normalization form(s) to check. See --list for supported forms.")

  parser.add_argument('--list', '-l', action="store_true",
      help="List all supported normalization forms and then exit")

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

  databases = load_databases(conf)

  all_forms = databases.keys()

  if conf.list:
    for f in all_forms:
      print(f)
    return

  if conf.forms is None:
    conf.forms = all_forms

  databases = { n:db for n, db in databases.items() if n in conf.forms }

  if len(databases) == 0:
    sys.stderr.write(f"No databases selected. Possibilities are: {all_forms}\n")
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

      chars = []
      taken_chars = set()
      for c in conf.char:
        if c in taken_chars: continue
        taken_chars.add(c)
        chars.append(c)

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
    sys.stderr.write("Please provide either --text or --char input\n")
    return


if __name__ == "__main__":
  main()
