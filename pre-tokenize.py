import numpy as np
import json

def jsonl2txt(path='wiki_00.jsonl', out_path='wiki_00.txt'):
    with open(path,'r') as f, open(out_path,'w') as out:
        for line in f:
            data = json.loads(line)
            out.write(data['text'] + '<doc>')

def txt2bin(chunk_size=1000000000):
    with open('kowiki_corpus.txt','rb') as f, open('kowiki_corpus.bin','wb') as out:
        while True:
            data = f.read(chunk_size)
            if not data:
                break

            token = np.frombuffer(data, dtype=np.uint8).astype(np.uint32)
            token.tofile(out)
            
def check_bin(chunk_size=2000):
    with open('kowiki_corpus.bin','rb') as f:
        print(bytes(np.frombuffer(f.read(chunk_size),dtype=np.uint32).astype(np.uint8)).decode('utf-8',errors='replace'))

