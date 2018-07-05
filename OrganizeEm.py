import random

def multi_image_reference_fitness(ground_truths, dna_object):
    '''
    Compares fitness based on multiple images.
    '''
    fitness = 0.0
    g_images = []
    for g in dna_object:
        if g.gene_type == "image":
            g_images.append(g.pixels)
    sum_img = []
    index = 0
    n = []
    for img in ground_truths:
        x = image_wrapper.compare_images(img, g_images[index])
        sum_img = sum_img + x
        n = n + img
        index = index + 1
    s = sum(sum_img)
    n = len(n)
    fitness = (1.0 - (s / n)) * 100.0
    return (fitness)


class DoubleHelix(object):
    """DNA builder object"""
    def __init__(self, phenotypes):
        self.data = phenotypes

    def build(self):
        used_keys = []
        genes = []
        for pt in self.data:
            occurance = used_keys.count(pt)
            if occurance > 0:
                number = '_' + str(occurance + 1)
            else:
                number = ''
            if pt == '3D_gene':
                verts = (1, 2, 2)
                g = ModelGene(verts, 0.0, 0.1)

            g.label = pt + number
            genes.append(g)
            used_keys.append(pt)
        return (DNA(genes))


class DNA(object):
    """docstring for dna"""
    def __init__(self, genes, id_num=0):
        self.id_num = id_num
        self.genes = genes
        self.fitness = 0.0
        self.fitness_function = None

    def mutation(self, odds):
        for gene in self.genes:
            gene.mutate(odds)

    def get_fitness(self, target_object):
        # TODO
        self.fitness = self.fitness_function(target_object, self.genes)
        return (self.fitness)


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
        Gene.__init__(self, "image_gene", 0.5, limit=True)
        self.min_ = min_ # min and max movement or "speed"
        self.max_ = max_
        self.pixels = pixels
        self.gene_type = "image"
        self.limit = limit


    def mutate(self, odds):
        new = []
        for p in self.pixels:
            if self.lucky(odds):
                r = random.uniform(self.min_, self.max_)
                p = p + (random.choice([-r, r]))
                if self.limit:
                    if p > 1.0:
                        p = 1.0
                    if p < 0.0:
                        p = 0.0
            new.append(p)
        self.pixels = new


class ModelGene(Gene):
    """docstring for 3D objects"""
    def __init__(self, vertices, min_, max_, limit=False, bounds=[1.0, -1.0]):
        '''
        Note: only takes vertices in a flat list!
        '''
        Gene.__init__(self, "3D_gene", 0.5)
        self.min_ = min_ # min and max movement or "speed"
        self.max_ = max_
        self.vertices = vertices
        self.gene_type = "polygon"
        self.limit = limit
        self.bounds = bounds


    def mutate(self, odds):
        new = []
        for p in self.vertices:
            if self.lucky(odds):
                r = random.uniform(self.min_, self.max_)
                p = p + (random.choice([-r, r]))
                if self.limit:
                    if p > self.bounds[0]:
                        p = self.bounds[0]
                    if p < self.bounds[1]:
                        p = self.bounds[1]
            new.append(p)
        self.vertices = new


class Population(object):
    """docstring for Population"""
    def __init__(self, size=100):
        self.size = size

    def generate(self, phenotypes=['3D_gene', 'clr_texture']):
        self.populus = []
        count = 0
        while count < self.size:
            dna = DoubleHelix(phenotypes).build()
            self.populus.append(dna)
            count = count + 1

    def cull(self, percent):
        # todo
        # keep top x percent of the population
        pass
        
