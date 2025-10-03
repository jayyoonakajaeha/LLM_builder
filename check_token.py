import json
import numpy as np
def check(path='vocab.json'):
    with open(path,'r') as f:
        for k,v in json.load(f).items():
            print(f"{eval(k)} -> {v} -> {bytes(v).decode('utf-8',errors='replace')}")

