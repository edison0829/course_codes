# cut branch

# !/usr/bin/env python3
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
import tree
from tree import Node
from tree import Tree
import copy
from collections import Counter
import math
import time
import matplotlib.pyplot as plt

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
    if type(fh) is str:
        fh = open(fh, code)
    ret = gzip.open(fh.name, code if code.endswith("t") else code + "t") if fh.name.endswith(".gz") else fh
    if sys.version_info[0] == 2:
        if code.startswith('r'):
            ret = reader(fh)
        elif code.startswith('w'):
            ret = writer(fh)
        else:
            sys.stderr.write("I didn't understand code " + code + "\n")
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
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="input (one sentence per line strings) file")
    parser.add_argument("--grammarfile", "-g", nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="grammar file; ignored")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help="output (one tree per line) file")

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
    grammar = prepfile(args.grammarfile, 'r')
    outfile = prepfile(args.outfile, 'w')

    # for line in infile:
    # toks = line.strip().split()
    # parens = 2
    # outfile.write("(TOP (NP ")
    # for tok in toks[:-2]:
    # outfile.write("(NNP {}) (NP ".format(tok))
    # parens+=1
    # endtoks = toks[-2:]
    # for tok in endtoks:
    # outfile.write("(NNP {}) ".format(tok))
    # outfile.write(")"*parens+"\n")

    dic = {}
    count = {}
    for i in grammar:
        t = Tree.from_str(i)
        for node in t.bottomup():
            if len(node.children) != 0:
                if node.label not in count:
                    count[node.label] = []

                chil = node.label + " -> "
                tup = []
                for c in node.children:
                    chil += c.label + " "
                    tup.append(c.label)

                count[node.label].append(tuple(tup))

                if chil not in dic:
                    dic[chil] = 1
                else:
                    dic[chil] += 1

        # rule_prob:(parent, child)
        # rule_prob_dict = {(parent, child) : prob}
        rule_prob_dict = {}
        for key, value in count.items():
            sub_count = Counter(value)
            # k:children.  v:count
            for k, v in sub_count.items():
                rule_prob = [key.encode("utf-8")]
                prob = float(v) / len(value)
                for ki in k:
                    rule_prob.append(ki.encode("utf-8"))

                rule_prob = tuple(rule_prob)
                rule_prob_dict[rule_prob] = math.log(prob, 10)

    time_y = []
    length = []
    for line in infile:
        start_time = time.time()
        toks = line.strip().split()
        # break
        # line="What airline provides only connecting flights between Denver and San Francisco ?"
        # line = "The flight should be eleven a.m tomorrow ."
        # toks = line.strip().split()

        # construct chart
        # store as [tree,prob]
        chart = []
        for i in range(len(toks)):
            chart_1 = []
            for j in range(len(toks) + 1):
                chart_2 = []
                chart_1.append(chart_2)
            chart.append(chart_1)

        # CKY
        word = []
        for rule, prob in rule_prob_dict.items():
            if len(rule) == 2:
                word.append(rule[-1])

        for i in range(0, len(toks)):
            if toks[i] not in word:
                toks[i] = '<unk>'
            for rule, prob in rule_prob_dict.items():
                if rule[-1] == toks[i]:
                    # print ('('+rule[0] + ' ' + rule[1] + ')')
                    t = Tree.from_str(('(' + rule[0] + ' ' + rule[1] + ')'))
                    chart[i][i + 1].append([t.root, prob])

        # print chart

        max_prob = -500000
        # finder = {}
        for width in range(2, len(toks) + 1):
            for start in range(0, len(toks) - width + 1):
                end = start + width
                for mid in range(start + 1, end):

                    for y in chart[start][mid]:
                        for z in chart[mid][end]:
                            for rule, prob in rule_prob_dict.items():

                                if len(rule) == 3:
                                    if y[0].label == rule[1] and z[0].label == rule[2]:
                                        parent_prob = prob + y[1] + z[1]
                                        t = tree.Node(rule[0], [copy.deepcopy(y[0]), copy.deepcopy(z[0])])

                                        # cut branch
                                        if len(chart[start][end]) != 0:
                                            flag = 0
                                            for ts in chart[start][end]:
                                                if t.label == ts[0].label:
                                                    flag = 1
                                                    if parent_prob > ts[1]:
                                                        chart[start][end].remove(ts)
                                                        chart[start][end].append([t, parent_prob])
                                                        break
                                            if flag == 0:
                                                chart[start][end].append([t, parent_prob])

                                        else:
                                            chart[start][end].append([t, parent_prob])

            # best_tree=tree.Node(None)
        for i in chart[0][len(toks)]:
            if i[1] > max_prob:
                max_prob = i[1]
                best_tree = Node._subtree_str(i[0])

        if max_prob != -500000:

            print best_tree
            print max_prob
            outfile.write(best_tree + "\n")
        else:
            print "This is not a sentence"
            outfile.write(best_tree + "\n")

        end_time = time.time()
        parsing_time = end_time - start_time

        time_y.append(math.log(parsing_time))

        x = len(toks)
        length.append(math.log(x))

    print len(time_y)
    print len(length)

    plt.plot(length, time_y)


if __name__ == '__main__':
    main()

