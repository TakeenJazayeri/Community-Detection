import random as rn

class Chromosome:
    def __init__ (self, length):
        self.genes = [0 for i in range(length+1)]

def random_chro (adj_matrix, length):
    new_chro = Chromosome(length)

    for i in range(1, length+1):
        neighbors = []
        for j in range(length+1):
            if adj_matrix[i][j] == 1:
                neighbors.append(j)
        new_chro.genes[i] = neighbors[rn.randint(0, len(neighbors)-1)]
    
    return new_chro

def genetic (adj_matrix, popu, iter_num):
    skip

file_address = input('add file address:\n')
try:
    file = open(file_address, 'r')
except IOError:
    print('There is a problem with file address.')

first_line = file.readline()
nodes_num = int(first_line[:-1])

adj_matrix = []
for i in range(nodes_num+1):
    new_row = []
    for j in range(nodes_num+1):
        new_row.append(0)
    adj_matrix.append(new_row)

file_content = file.read().replace("\n", " ").split()
i = 0
while i < len(file_content):
    x, y = int(file_content[i]), int(file_content[i+1])
    adj_matrix[x][y] = 1
    adj_matrix[y][x] = 1
    i += 2
file.close()

print(random_chro(adj_matrix, nodes_num).genes)