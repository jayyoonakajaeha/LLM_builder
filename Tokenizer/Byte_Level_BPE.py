raw_corpus = ["hello world",
"hello 😊",
"한글 토큰화 연습",
"banana 🍌 banana"
]

corpus = ""
for sentence in raw_corpus:
    corpus += f'{sentence}\n\n'

corpus_byte = list(corpus.encode("utf-8"))
vocab = {i:(i,) for i in range(256)}
print(corpus_byte)

def merge_and_replace(corpus_byte,vocab):
    frequency = {}

    for i in range(len(corpus_byte)-1):
        token = tuple(corpus_byte[i:i+2])
        if token not in frequency:
            frequency[token] = 1
        else:
            frequency[token] += 1

    max_freq = [k for k, v in frequency.items() if v == max(frequency.values())]

    for m in max_freq:
        vocab[len(vocab)] = vocab[m[0]] + vocab[m[1]]

    i = 0
    corpus_new = []
    print("corpus_byte length:",len(corpus_byte))
    while i <= len(corpus_byte)-1:
        flag = 0
        if i< len(corpus_byte)-1:
            token = vocab[corpus_byte[i]] + vocab[corpus_byte[i+1]]
        else:
            token = None
        for k, v in vocab.items():
            if v == token:
                corpus_new.append(k)
                i+=2
                flag = 1
        if flag:
            continue
        corpus_new.append(corpus_byte[i])
        i+=1
    
    return corpus_new, vocab

iter = 4
for i in range(iter):
    corpus_byte, vocab = merge_and_replace(corpus_byte, vocab)
    print(corpus_byte)
print(vocab)

for t in corpus_byte:
    b = bytes(list(vocab[t]))
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        s = b.decode("utf-8",errors="replace")
    print(t,list(vocab[t]),s)
