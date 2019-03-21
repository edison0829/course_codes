import ujson as json
from collections import defaultdict

tw = [(w,int(c)) for w,c,_ in (L.split("\t") for L in open("twcounts"))]
nyt= [(w,int(c)) for w,c,_ in (L.split("\t") for L in open("nytcounts"))]

tw_words = sorted([(w,c) for w,c in tw if c>100], key=lambda (w,c): -c)
nyt_words = sorted([(w,c) for w,c in nyt if c>100], key=lambda (w,c): -c)

twcounts = dict(tw)
nytcounts = dict(nyt)

def allwords():
    for i in range(min([len(tw_words), len(nyt_words)])):
        yield tw_words[i][0]
        yield nyt_words[i][0]

# thresh = 100
vocab = set()
for w in allwords():
    # if w not in vocab and twcounts.get(w,0) > thresh and nytcounts.get(w,0) > thresh:
    #     vocab.add(w)
    vocab.add(w)
    if len(vocab)==4000: break

# with open("vocab",'w') as f:
#     counts = [(w, twcounts.get(w,0), nytcounts.get(w,0)) for w in vocab]
#     counts.sort(key=lambda (w,c1,c2): -(c1*c2))
#     for w,c1,c2 in counts:
#         print>>f, w, c1,c2
with open("vocab",'w') as f:
    #counts = [(w, twcounts.get(w,0)) for w in vocab]
    counts = [(w, nytcounts.get(w,0)) for w in vocab]
    counts.sort(key=lambda (w,c1): -(c1))
    counts = [(w,c) for w,c in counts if c>0]
    for w,c1 in counts:
        print>>f, w, c1

def filter(infile,outfile, vocab):
    print "%s -> %s" % (infile,outfile)
    ctx_numwords = defaultdict(int)
    out = open(outfile,'w')

    w_count = {}
    w_cc = {}
    for line in open(infile):
        w,c,cc = line.split("\t")
        if w not in vocab: continue
        cc = json.loads(cc)
        for ctx in cc: ctx_numwords[ctx] += 1
        w_cc[w] = cc
        w_count[w] = c

    for w,cc in w_cc.items():
        for ctx in cc.keys():
            if ctx_numwords[ctx] <= 1:
                del cc[ctx]
        print>>out, "%s\t%s\t%s" % (w, w_count[w], json.dumps(w_cc[w]))

    out.close()


filter("twcounts", "twcounts.trimmed", vocab)
filter("nytcounts", "nytcounts.trimmed", vocab)

filter("twcounts", "twcounts.university_cat_dog", set(["university","cat","dog"]))
filter("nytcounts", "nytcounts.university_cat_dog", set(["university","cat","dog"]))

#filter("twcounts", "twcounts.cloud_cat_dog", set(["cloud","cat","dog"]))
#filter("nytcounts", "nytcounts.cloud_cat_dog", set(["cloud","cat","dog"]))