import os
from transformer import get_embedding
from draw import draw
import numpy as np
from cluster import get_cluster

def run():
    def read_tokens(path, max_tokens=5000):
        data = []
        with open(path, 'r') as f:
            data = f.read().split('\n')[:-1]
        conf  = [line.split('\t')[0] for line in data]
        conf  = [float(x) for x in conf]
        token = [line.split('\t')[1] for line in data]
        return conf[:max_tokens], token[:max_tokens]
        
    def run(path):
        conf, token = read_tokens(os.path.join(path, 'AutoPhrase.txt'))
        conf = np.array(conf)
        data = get_embedding(token)
        # data = np.random.rand(1016, 1000)
        
        failed_tokens = set(np.invert(np.isfinite(data)).nonzero()[0])
        for i, idx in enumerate(sorted(failed_tokens)):
            conf = np.delete(conf, idx-i, 0)
            data = np.delete(data, idx-i, 0)
            del token[idx-i]
        draw(data, np.exp(conf**2), None, path+'embedding')
        
        cluster, tag = get_cluster(data)
        for i, _ in enumerate(tag):
            tag[i][0] = token[tag[i][0]]
        draw(data, np.exp(conf**2), cluster, path+'cluster', tag)

        with open(path+'cluster_result.txt', 'w') as f:
            for idx in range(np.min(cluster), np.max(cluster) + 1):
                ids = np.arange(len(data))[cluster==idx]
                f.write('Cluster %d:\n' % idx)
                for id in ids:
                    f.write('\t{}: {}\n'.format(token[id], conf[id]))
                f.write('\n')
    
    def run_all():
        first = True
        for root, dirs, files in os.walk('./datamining/data/'):  
            for file in files:
                if file == 'AutoPhrase.txt':
                    print(root+'/')
                    if os.path.exists(root+'/'+'cluster_result.txt'): 
                        print('Skipped.')
                        continue
                    run(root+'/')
        
    run_all()
    
run()
