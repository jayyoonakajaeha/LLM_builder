import numpy as np

def txt2bin(chunk_size=1000000000):
    with open('kowiki_corpus.txt','rb') as f, open('kowiki_corpus.bin','wb') as out:
        while True:
            data = f.read(chunk_size)
            if not data:
                break

            token = np.frombuffer(data, dtype=np.uint8).astype(np.uint32)
            token.tofile(out)
    f.close()
    out.close()
            
def check_bin(chunk_size=2000):
    with open('kowiki_corpus.bin','rb') as f:
        print(bytes(np.frombuffer(f.read(chunk_size),dtype=np.uint32).astype(np.uint8)).decode('utf-8',errors='replace'))
    f.close()
