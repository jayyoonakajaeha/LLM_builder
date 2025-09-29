# Byte-Level Byte Pair Encoding Tokenizing
import numpy as np
from collections import Counter
import os
import struct
import json

def BBPE(path='kowiki_corpus.bin', chunk_size=1000000000,iter=10):
    if os.path.exists('vocab.json'):
        with open('vocab.json','r') as f:
            vocab = {eval(k):tuple(v) for k,v in json.load(f).items()}
    else:
        vocab = {i:(i,) for i in range(256)}

    if os.path.exists('merge_map.json'):
        with open('merge_map.json','r') as f:
            merge_map = {eval(k):v for k,v in json.load(f).items()}
    else:
        merge_map = {(i,):i for i in range(256)}
    
    for _ in range(iter):
        freq = Counter()
        prev_byte = None
        with open(path, "rb") as f:
            
            while True:
                chunk = np.frombuffer(f.read(chunk_size),dtype=np.uint32)
                if not chunk.any():
                    break

                if prev_byte is not None:
                    freq.update([(prev_byte,chunk[0])])

                freq.update(zip(chunk,chunk[1:]))

                prev_byte = chunk[-1]
                #break # 임시 종료 

            most_common = freq.most_common(1)[0][0]
            print(most_common)
            vocab[len(vocab)] = vocab[most_common[0]] + vocab[most_common[1]]
            merge_map[most_common] = len(merge_map)
        
        prev_byte = None
        prev_is_merged = False

        with open(path,"rb") as f_in, open('temp.bin',"wb") as f_out:
            while True:
                chunk = np.frombuffer(f_in.read(chunk_size),dtype=np.uint32)
                if not chunk.any():
                    break

                if prev_byte is not None and not prev_is_merged:
                    chunk = np.concatenate(([prev_byte], chunk))
                
                i = 0
                out_bytes = bytearray()
                while i < len(chunk):
                    if i < len(chunk) - 1 and (chunk[i],chunk[i+1]) in merge_map:
                        out_bytes.extend(struct.pack("<I",merge_map[(chunk[i],chunk[i+1])]))
                        if i+1 == len(chunk) - 1:
                            prev_is_merged = True
                        i+=2
                    elif i == len(chunk) -1:
                        prev_is_merged = False
                        i+=1
                    else:
                        out_bytes.extend(struct.pack("<I",chunk[i]))
                        i+=1
                f_out.write(out_bytes)
                prev_byte = chunk[-1]
                #break # 임시 종료 

        os.replace('temp.bin',path)

    with open("vocab.json", "w", encoding="utf-8") as f:
        json.dump({str(k):v for k,v in vocab.items()}, f, ensure_ascii=False)

    with open("merge_map.json", "w", encoding="utf-8") as f:
        json.dump({str(k):v for k,v in merge_map.items()}, f, ensure_ascii=False)
