#vocab_file_path="./vocab_dog_cat_university"
vocab_file_path="./vocab"

#word2vec_file_path="./nyt_word2vec.4k"
word2vec_file_path="./nyt_word2vec"

#word2vec_out_path="./nyt_word2vec.university_cat_dog"
word2vec_out_path="./nyt_word2vec.4k"

vocab=set()
with open(vocab_file_path) as vocab_fin:
	for line in vocab_fin:
		#print line
		w,freq=line.split(' ')
		vocab.add(w)

f_out=open(word2vec_out_path,"w")

with open(word2vec_file_path) as f_in:
	for line in f_in:
		#print line 
		w_emb=line.split(' ')
		if(w_emb[0] in vocab):
			f_out.write(line)