#!/usr/bin/env python
# makes a demo grammar that is compliant with HW4 in form but completely ignores the
# input data (the grammar from the class slides is output instead)

import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit
import tree
import operator

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


def main():
  parser = argparse.ArgumentParser(description="ignore input; make a demo grammar that is compliant in form",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (ignored)")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file (grammar)")

  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  workdir = tempfile.mkdtemp(prefix=os.path.basename(__file__), dir=os.getenv('TMPDIR', '/tmp'))

  def cleanwork():
    shutil.rmtree(workdir, ignore_errors=True)
  if args.debug:
    print(workdir)
  else:
    atexit.register(cleanwork)


  infile = prepfile(args.infile, 'r')
  out_dict = []
  for line in infile:
      t = tree.Tree.from_str(line)
      for i in t.bottomup():
          if i.children:
             out_dict.append([i.label,[j.label for j in i.children]])
  keys = set([i[0] for i in out_dict])
  prob_dict = {}
  times_dict = {}
  for key in keys:
    key_count = 0
    values = []
    for rule in out_dict:
        if rule[0] == key:
            values.append(rule[1])
            key_count += 1
    for value in values:
        sub_count = 0
        for rule in out_dict:
            if [key,value] == rule:
                sub_count += 1
        prob_dict[key + ' -> ' + ' '.join(value)] = sub_count/float(key_count)
        times_dict[key + ' -> ' + ' '.join(value)] = sub_count
  print 'rules in total:'
  print len(times_dict)
  print 'most frequent rule:'
  print  max(times_dict.iteritems(), key=operator.itemgetter(1))[0],max(times_dict.iteritems(), key=operator.itemgetter(1))[1]
  out = []
  for key, value in prob_dict.iteritems():
      out.append(key+' # '+ str(value))

  outfile = prepfile(args.outfile, 'w')

  outfile.write('\n'.join(out))

if __name__ == '__main__':
  main()
