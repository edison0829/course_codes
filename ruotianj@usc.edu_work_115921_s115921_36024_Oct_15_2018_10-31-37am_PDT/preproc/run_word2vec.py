from gensim.models import word2vec
import os

#PATH_TO_DATA="/Users/ken77921/Desktop/TA/2004,7-05_nyt_sentence"
PATH_TO_DATA="/Users/ken77921/Desktop/TA/2004,7-05_nyt_tok_small"

sentences_all=[]
line_count=0
with open(os.path.join(PATH_TO_DATA),'r') as doc:
	for sent_raw in doc:
		line_count+=1
		if(line_count%10000==0):
			print (line_count)
		sentence_tok=[w.lower() for w in sent_raw[:-1].split()]
		sentences_all.append(sentence_tok)
#sentences_all=word2vec.LineSentence(PATH_TO_DATA)
#print sentences_all[:10]

model=word2vec.Word2Vec(sentences_all)

word2vec_output="/Users/ken77921/Desktop/TA/nyt_word2vec"
model.save_word2vec_format(word2vec_output)
#model.most_similar(positive=['woman', 'king'], negative=['man'], topn=2) 