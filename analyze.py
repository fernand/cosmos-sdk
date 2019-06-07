import os
import json
import shutil

def writej(obj, f_path, overwrite=True):
    if os.path.exists(f_path):
        if overwrite:
            os.remove(f_path)
        else:
            return
    with open(f_path, 'w') as f:
        json.dump(obj, f)

def loadj(f_path):
    if not os.path.exists(f_path):
        return None
    else:
        with open(f_path) as f:
            return json.load(f)

files = [p for p in os.listdir() if p.endswith('output.json')]
cvg = {}
for f in files:
    output = loadj(f)
    if output['stderr'] != '':
        print(output['stderr'])
    last_line = output['stdout'].split('\n')[-2]
    pct = float(last_line.split('\t')[-1].split(' ')[1][:-1])
    cvg[f] = pct
for k,v in sorted(cvg.items(), key=lambda kv: kv[1], reverse=True)[:20]:
    print(k, v)
