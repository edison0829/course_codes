import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    # L = start_scores.shape[0]
    # assert end_scores.shape[0] == L
    # assert trans_scores.shape[0] == L
    # assert trans_scores.shape[1] == L
    # assert emission_scores.shape[1] == L
    # N = emission_scores.shape[0]

    # initial value:
    (N,L) = emission_scores.shape
    T= []
    for i in range(N):
        t = []
        for j in range(L):
            t.append([])
        T.append(t)
    for j in range(L):
        T[0][j] = [1,[j],start_scores[j]+emission_scores[0,j]]
    # recursive:
    for i in range(1,N):
        for j in range(L):
            trans_score = -np.inf
            pos = []
            for k in range(L):
                cur_score = trans_scores[k,j] +T[i-1][k][2]
                if cur_score >= trans_score:
                    trans_score = cur_score
                    pos = [k,j]
            cur_seq = T[i-1][pos[0]][1] + [j]
            cur_score = trans_score + emission_scores[i,j]
            T[i][j] = [i+1,cur_seq,cur_score]
    for j in range(L):
        T[N-1][j][2] += end_scores[j]
    # output
    out_seq = []
    out_score = -np.inf
    for j in range(L):
        cur_score = T[N-1][j][2]
        if cur_score >= out_score:
            out_score = cur_score
            out_seq = T[N-1][j][1]
    return out_score,out_seq

    # y = []
    # for i in xrange(N):
    #     # stupid sequence
    #     y.append(i % L)
    # # score set to 0
    # return (0.0, y)
