import collections
import os
import json

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
with open('features.csv', 'w') as w:
    for f in files:
        params = loadj(f.split('_')[0]+'_params.json')
        features = []
        for k in collections.OrderedDict(sorted(params.items())):
            if k == 'send_enabled':
                feature = "1.0" if params[k] else "0.0"
            elif k == 'deposit_params_min_deposit':
                feature = params[k][0]['amount']
            elif k == 'max_validators':
                feature = str(params[k])
            else:
                feature = params[k]
            features.append(feature)
        w.write(','.join(features)+'\n')
with open('labels.csv', 'w') as w:
    for f in files:
        output = loadj(f)
        last_line = output['stdout'].split('\n')[-2]
        pct = last_line.split('\t')[-1].split(' ')[1][:-1]
        w.write(pct+'\n')