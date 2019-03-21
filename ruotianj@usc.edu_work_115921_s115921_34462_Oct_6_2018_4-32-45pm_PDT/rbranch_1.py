#!/usr/bin/env python3
# right branching "parser"
# from  boilerplate code by Jon May (jonmay@isi.edu)
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
import math
import time


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
  parser = argparse.ArgumentParser(description="trivial right-branching parser that ignores any grammar passed in",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input (one sentence per line strings) file")
  parser.add_argument("--grammarfile", "-g", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="grammar file; ignored")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output (one tree per line) file")




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
  gramfile = prepfile(args.grammarfile, 'r')
  outfile = prepfile(args.outfile, 'w')
  prob_dict = {}
  keys = []
  smoothing = []
  for line in gramfile:
    toks = line.strip().split(' # ')
    prob_dict[toks[0]] = math.log10(float(toks[1]))
    keys.append(toks[0].strip().split(' -> '))
  #     smoothing
    if ' ' not in toks[0].strip().split(' -> ')[1] and float(toks[1]) == 1.0:
      smoothing.append(toks[0].strip().split(' -> ')[0])
  print (smoothing)
  time_L = []
  len_L = []
  for line in infile:
    then = time.time()
    toks = line.strip().split()
    len_L.append(len(toks))
    L = []
    for i in range(len(toks)):
        cur_row = []
        cur_grid = []
        for k in range(i):
            cur_row.append([])
        for key in keys:
            if toks[i] == key[1]:
                cur_grid.append([key[0],prob_dict[key[0]+' -> '+key[1]]])
        if cur_grid == []:
            for key in keys:
                if key[1] == '<unk>':
                    cur_grid.append([key[0], prob_dict[key[0] + ' -> ' + key[1]]])
        for sm in smoothing:
            cur_grid.append([sm,-5])
        cur_row.append(cur_grid)
        for k in range(len(toks)-i-1):
            cur_row.append([])
        L.append(cur_row)

    for step in range(1,len(L)):
        for i in range(len(L)-step):
            for j in range(i,i+step):
                for head in L[i][j]:
                    for tail in L[j+1][step+i]:
                        for key in keys:
                            if head[0]+' '+tail[0] == key[1]:
                                new_prob = prob_dict[key[0]+' -> '+key[1]]+head[1]+tail[1]
                                if key[0] in [el[0] for el in L[i][step+i]]:
                                    for e in range(len(L[i][step+i])):
                                        if key[0]==L[i][step+i][e][0]:
                                            if L[i][step+i][e][1] < new_prob:
                                                L[i][step+i][e] = [key[0],new_prob,[[i,j],[j+1,step+i],key[1].split(' ')]]
                                else:
                                    L[i][step+i].append([key[0],new_prob,[[i,j],[j+1,step+i],key[1].split(' ')]])

    # cur = []
    # cur_probb = -10000
    # for i in L[index[0]][index[1]]:
    #     if i[0] == 'TOP' or i[0] == 'S':
    #         cur = [i]
    #         cur_probb = i[1]
    top = []
    for i in L[0][-1]:
        if i[0] == 'TOP':
            top = [i]
            break
    print (top)
    def parser(top,L,index,line):
        if len(top[0]) != 3:
            return '('+top[0][0] + ' '+ line[index[0]]+')'
        else:
            for ele in L[top[0][2][0][0]][top[0][2][0][1]]:
                if ele[0] == top[0][2][2][0]:
                    left_p = [ele]
            left = parser(left_p,L,[top[0][2][0][0],top[0][2][0][1]],line)
            for ele in L[top[0][2][1][0]][top[0][2][1][1]]:
                if ele[0] == top[0][2][2][1]:
                    right_p = [ele]
            right = parser(right_p,L,[top[0][2][1][0],top[0][2][1][1]],line)
            return  '(' + top[0][0] + ' ' + left+' '+right+')'
    if top:
        out = parser(top,L,[0,-1],toks)
        outfile.write(out)
        outfile.write("\n")

    else:
        outfile.write("\n")
  # import pylab
  # import matplotlib.pyplot as plt
  # fig = plt.figure()
  # ax = fig.add_subplot(2, 1, 1)
  # line, = ax.plot(len_L,time_L,"o")
  # ax.set_yscale('log')
  # pylab.show()



    # parens = 2
    # outfile.write("(TOP (NP ")
    # for tok in toks[:-2]:
    #   outfile.write("(NNP {}) (NP ".format(tok))
    #   parens+=1
    # endtoks = toks[-2:]
    # for tok in endtoks:
    #   outfile.write("(NNP {}) ".format(tok))
    # outfile.write(")"*parens+"\n")


if __name__ == '__main__':
  main()
