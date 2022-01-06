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
    
    def build_partition (self, chro, length):
        for i in range(length+1):
            self.union(i, chro.genes[i])

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
    

class Chromosome:
    def __init__ (self, length):
        self.genes = [0 for i in range(length+1)]
    
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

    def crossover (self, other, length):
        new_chro = Chromosome(length)
        for i in range(length+1):
            random_int = random.randint(0, 1)
            if random_int == 0:
                new_chro.genes[i] = self.genes[i]
            else:
                new_chro.genes[i] = other.genes[i]
        return new_chro
    
    def mutation (self, adj_matrix, length, mutation_possibility):
        new_chro = Chromosome(length)
        for i in range(1, length+1):
            random_float = random.uniform(0, 1)
            if random_float <= mutation_possibility:
                neighbors = find_neighber(i, adj_matrix, length)
                new_chro.genes[i] = neighbors[random.randint(0, len(neighbors)-1)]
            else:
                new_chro.genes[i]=self.genes[i]
        return new_chro




def find_neighber (node_num, adj_matrix, length):
    neighbors = []
    for i in range(length+1):
        if adj_matrix[nodes_num][i] == 1:
            neighbors.append(i)
    return neighbors

def random_chro (adj_matrix, length):
    new_chro = Chromosome(length)
    for i in range(1, length+1):
        neighbors = find_neighber(i, adj_matrix, length)
        new_chro.genes[i] = neighbors[random.randint(0, len(neighbors)-1)]
    return new_chro

def choose_parent (chro_list, popu, length):
    Q_list = []
    maximum = 0
    sum2 = 0
    for i in range(popu):
        Q_list.append(chro_list[i].Q(adj_matrix, length))
        sum2 += (Q_list[i] * Q_list[i])
        if Q_list[i] > Q_list[maximum]:
            maximum = i
    
    possibility = []
    for i in range(popu):
        possibility.append((Q_list[i] * Q_list[i]) / sum2)

    choosed_parents = []
    for i in range((2 * popu) - 2):
        random_float = random.uniform(0, 1)
        for j in range(popu):
            random_float -= possibility[j]
            if random_float <= 0:
                choosed_parents.append(j)
                break
    
    return Q_list[maximum], maximum, choosed_parents



def genetic (adj_matrix, popu, iter_num, length, mutation_possibility):
    chro_list = []
    for i in range(popu):
        chro_list.append(random_chro(adj_matrix, length))

    max_value, maximum = 0, 0
    for i in range(iter_num):
        max_value, maximum, parents_list = choose_parent(chro_list, popu, length)
        new_chro_list = [chro_list[maximum]]
        for j in range(0, (2 * popu) - 2, 2):
            new_chro_list.append(chro_list[parents_list[j]].crossover(chro_list[parents_list[j + 1]], length))
        for k in range(1, popu):
            new_chro_list[k] = new_chro_list[k].mutation(adj_matrix, length, mutation_possibility)
        chro_list = new_chro_list

        if i % 200 == 0:
            print("number of iterations =", i, " / max value = ", chro_list[maximum].Q(adj_matrix, length))
    
    p = Partition(length)
    p.build_partition(chro_list[maximum], length)
    best_patitioning = p.report()

    return max_value, best_patitioning
    
    

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

max_value, best_patitioning = genetic(adj_matrix, 50, 10000, nodes_num, 0.04)
print("Best partitioning = ", best_patitioning, " / Q = ", max_value)