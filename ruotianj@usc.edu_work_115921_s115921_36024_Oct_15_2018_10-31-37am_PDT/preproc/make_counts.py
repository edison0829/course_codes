# This script was used to create the context counts file.
# You do NOT need to run it for PS5.  It's provided so you can see what it did,
# or if you want to try using it (or a modification) for the final project.
# Usage: give it tokenized tweets (or any tokenized texts) on standard input.
# It outputs context counts on standard output.
# for example, to run on 100 tweets,
#   head -100 en_tok_from_daily10k.all2014.hashsort.toks | python allcounts.py
# to save to a file,
#   head -100 tweets.toks | python allcounts.py > counts_for_100.txt

import sys
try:
    import ujson as json
except ImportError:
    import json
from collections import defaultdict

counts = defaultdict(lambda:defaultdict(int))

def normtok(w):
    if w.startswith("http"): return "URL"
    if w.startswith("@"): return "ATMENTION"
    return w.lower()

for line in sys.stdin:
    toks = line.split()
    toks = [normtok(w) for w in toks]
    for i in range(len(toks)):
        target = toks[i]
        # if target not in ['cat','dog','cloud']: continue
        if i>0:
            context = "%s _" % toks[i-1]
            counts[target][context] += 1
        if i<len(toks)-1:
            context = "_ %s" % toks[i+1]
            counts[target][context] += 1

# context_vocab = set()
# for target,cc in counts.items():
#     context_vocab |= set(cc.iterkeys())

for target in counts:
    ccdict = dict(counts[target])
    n_occur = sum(ccdict.values())
    print "%s\t%s\t%s" % (target, n_occur, json.dumps(ccdict))

