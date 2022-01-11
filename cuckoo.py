import random

class Partition:
    def __init__ (self, num):
        self.parent = []
        for i in range(num+1):
            self.parent.append(i)
    
    def find(self, node):
        return self.parent[node]
    
    def union (self, node1, node2):
        a = self.find(node1)
        b = self.find(node2)
        for i in range(len(self.parent)):
            if self.parent[i] == b:
                self.parent[i] = a
    
    def build_partition (self, hab, length):
        for i in range(1, length+1):
            selected_ngh = ngh_matrix[i][hab.coordinates[i]]
            self.union(i, selected_ngh)

    def report(self):
        result = [[] for i in range(len(self.parent))]
        for i in range(1, len(self.parent)):
            result[self.find(i)].append(i)

        j = 0
        while j < len(result):
            if result[j] == []:
                result.pop(j)
            else:
                j += 1
        return result
    

class Habitat:
    def __init__ (self, length):
        self.coordinates = [0 for i in range(length+1)]
    
    def Q (self, adj_matrix, length):
        m = 0
        k = [0 for i in range(length+1)]
        for i in range(length+1):
            for j in range(length+1):
                if adj_matrix[i][j] == 1:
                    k[i] += 1
                    m += 0.5

        p = Partition(length)
        p.build_partition(self, length)

        result = 0
        for i in range(1, length+1):
            for j in range(1, length+1):
                if p.find(i) == p.find(j):
                    result += adj_matrix[i][j] - (k[i] * k[j] / (2 * m))
        result /= (2 * m)

        if result < 0:
            return 0
        elif result > 1:
            return 1
        return result
    
    def difference (self, other, length):
        dif = []
        for i in range(length+1):
            dif.append(self.coordinates[i] - other.coordinates[i])
    


def find_neighbors (node_num, adj_matrix, length):
    neighbors = []
    for i in range(length+1):
        if adj_matrix[node_num][i] == 1:
            neighbors.append(i)
    return neighbors

def random_hab (adj_matrix, ngh_matrix, length):
    new_hab = Habitat(length)
    for i in range(1, length+1):
        neighbors = find_neighbors(i, adj_matrix, length)
        new_hab.coordinates[i] = random.randint(0, len(ngh_matrix[i])-1)
    return new_hab



    
def cuckoo_algorithm (adj_matrix, popu, iter_num, length):
    hab_list = []
    for i in range(popu):
        hab_list.append(random_hab(adj_matrix, length))

    


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

ngh_matrix = []
for i in range(nodes_num+1):
    ngh_matrix.append(find_neighbors(i, adj_matrix, nodes_num))

print(adj_matrix)
print(ngh_matrix)
for i in range(10):
    print(random_hab(adj_matrix, ngh_matrix, nodes_num).coordinates)