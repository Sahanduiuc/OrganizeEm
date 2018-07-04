import random

class DoubleHelix(object):
    """DNA builder object"""
    def __init__(self, raw_data):
        self.data = raw_data

    def build(self):
        genes = []
        for key in self.data:
            if key == 'image':
                g = ImageGene(self.data[key], 0.0, 0.1)
                genes.append({key:g})
        return (DNA(genes))

class DNA(object):
    """docstring for dna"""
    def __init__(self, genes, id_num=0):
        self.id_num = id_num
        self.genes = genes
        self.fitness = 0.0

    def mutation(self, odds):
        for gene in self.genes:
            for key in gene:
                gene[key].mutate(odds)

    def get_fitness(self):
        pass
        
        
class Gene(object):
    """docstring for Gene"""
    def __init__(self, label, default):
        self.label = label
        self.default = default
        self.mutate_function = None

    def lucky(self, odds):
        luck = random.uniform(0.0, 1.0)
        if luck < odds:
            return (True)
        else:
            return (False)


class ImageGene(Gene):
    """docstring for ImgGene"""
    def __init__(self, pixels, min_, max_):
        '''
        Note: only takes pixels in a flat list with values 0.0-1.0
        No image type objects allowed!
        '''
        Gene.__init__(self, "image_gene", 0.5)
        self.min_ = min_ # min and max movement or "speed"
        self.max_ = max_
        self.pixels = pixels


    def mutate(self, odds):
        new = []
        for p in self.pixels:
            if self.lucky(odds):
                r = random.uniform(self.min_, self.max_)
                p = p + (random.choice([-r, r]))
                if p > 1.0:
                    p = 1.0
                if p < 0.0:
                    p = 0.0
            new.append(p)
        self.pixels = new
