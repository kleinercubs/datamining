import os 
import matplotlib
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np

def transform(highdim_data):
    tsne = TSNE(init='pca', random_state=0)
    # tsne = TSNE()
    tsne.fit_transform(highdim_data)
    return tsne.embedding_
    
def normalize(data):
    if np.max(data) == np.min(data):
        return np.zeros_like(data)[:, None]
    else: 
        return ((data - np.min(data))/(np.max(data) - np.min(data)))[:, None]
    
def draw(data, conf, cluster=None, path=None, tag=None):
    assert(len(data.shape) == 2 and len(conf.shape) == 1 and len(conf) == len(data) and (cluster is None or (len(cluster.shape) == 1 and len(data) == len(cluster))))
    data = transform(data)
    if cluster is None:
        plt.scatter(data[:, 0], data[:, 1], c=np.concatenate((normalize(data[:, 0]), normalize(data[:, 1]), np.ones((len(data), 1))/1.3), axis=1), alpha=normalize(conf))
    else:
        hue = normalize(cluster)
        plt.scatter(data[:, 0], data[:, 1], c=matplotlib.colors.hsv_to_rgb(np.concatenate((hue*0.8, np.ones_like(hue), np.ones_like(hue)), axis=1)), alpha=normalize(conf))
    if tag is not None:
        for x in tag: 
            plt.text(data[x[1]][0], data[x[1]][1], str(x[2]) + ': ' + x[0])
    if path: plt.savefig(path+'_result', dpi=1000)
    plt.show()
    plt.close()
    
def test():
    def test_transform():
        data = np.arange(10).reshape(-1, 1)*np.ones((10, 10))
        print(data)
        data = transform(data)
        print(data)
        plt.scatter(data[:, 0], data[:, 1])
        plt.show()
            
    def test_draw1():   
        result = np.random.rand(100, 2)
        label = np.arange(100) / 10
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, color= plt.cm.Set1(label / 10.),alpha = 1)
        plt.show()
        
    def test_draw2():   
        result = np.random.rand(100, 2)
        label = np.arange(100)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=[label], cmap='viridis', alpha = (1-label/100))
        plt.show()
        
    def test_draw3():   # that's good!
        result = np.random.rand(100, 3)
        label = np.arange(100)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=result, alpha=(1-label/100))
        plt.show()
        
    def test_draw4():
        result = np.random.rand(100, 2)
        label = np.arange(100)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=matplotlib.colors.hsv_to_rgb(np.concatenate((x[:, None], np.ones((100, 1)), y[:, None]*0.4+0.6), axis=1)))
        plt.show()
        
    def test_draw5():
        result = np.random.rand(100, 2)
        label = np.arange(100)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=np.concatenate((result, np.ones((100, 1))/1.3), axis=1), alpha=1)
        plt.show()
        
    def test_draw6():
        result = np.random.rand(100, 2)
        label = np.arange(100)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=np.concatenate((((x+y)/2)[:,None], result), axis=1))
        plt.show()
        
    def test_draw7():
        result = np.random.rand(100, 2)
        label = np.arange(100).reshape(-1, 1)
        x = result[:, 0]
        y = result[:, 1]
        plt.scatter(x, y, c=matplotlib.colors.hsv_to_rgb(np.concatenate((x[:, None], (1-label/100), y[:, None]*0.3+0.7), axis=1)))
        plt.show()
        
    def test_draw8():
        result = np.random.rand(100, 2)
        label = np.arange(100).reshape(-1, 1)
        x = result[:, 0]
        y = result[:, 1]
        hue = np.random.randint(0, 5, (100, 1))/4
        plt.scatter(x, y, c=matplotlib.colors.hsv_to_rgb(np.concatenate((hue, np.ones((100, 1)), np.ones((100, 1))), axis=1)), alpha=(1-label/100))
        plt.show()
