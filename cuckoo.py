import random
from pandas import DataFrame
from sklearn.cluster import KMeans

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
    
    def build_partition (self, cuc, length):
        for i in range(1, length+1):
            selected_ngh = ngh_matrix[i][cuc.habitat[i]]
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
    

class Cuckoo:
    def __init__ (self, length):
        self.habitat = [0 for i in range(length+1)]
    
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
        dif_sum = 0
        for i in range(length+1):
            dif = self.habitat[i] - other.habitat[i]
            if dif >= 0:
                dif_sum += dif
            else:
                dif_sum -= dif
        return dif_sum

    def spawn (self, adj_matrix, ngh_matrix, my_egg_num, my_ELR, length):
        my_egg_list = []
        while len(my_egg_list) < my_egg_num:
            new_egg = Cuckoo(length)
            for i in range(1, length+1):
                new_egg.habitat[i] = self.habitat[i]
                if random.randint(0, 3) == 0:
                    change = random.randint(0, 4)
                    new_egg.habitat[i] = (new_egg.habitat[i] + change) % len(ngh_matrix[i])

            if self.difference(new_egg, length) < my_ELR:
                my_egg_list.append(new_egg)

        return my_egg_list
    


def find_neighbors (node_num, adj_matrix, length):
    neighbors = []
    for i in range(length+1):
        if adj_matrix[node_num][i] == 1:
            neighbors.append(i)
    return neighbors

def random_cuc (adj_matrix, ngh_matrix, length):
    new_cuc = Cuckoo(length)
    for i in range(1, length+1):
        neighbors = find_neighbors(i, adj_matrix, length)
        new_cuc.habitat[i] = random.randint(0, len(ngh_matrix[i])-1)
    return new_cuc

def set_egg_and_ELR (var_low, var_high, alpha, popu):
    egg_num = []
    total_num = 0
    ELR = []

    for i in range(popu):
        egg_num.append(random.randint(var_low, var_high))
        total_num += egg_num[i]
    
    for i in range(popu):
        ELR.append(alpha * (egg_num[i] / total_num) * (var_high - var_low))
    
    return egg_num, ELR


def choosing_best_eggs (egg_list, popu, length):
    egg_list_Q = []
    for i in range(len(egg_list)):
        egg_list_Q.append(egg_list[i].Q(adj_matrix, length))

    two_sort(egg_list_Q, egg_list)
    egg_list = egg_list[:popu]
    egg_list_Q = egg_list_Q[:popu]

    return egg_list, egg_list_Q


def migration_dest (cuc_list, cuc_list_Q, ngh_matrix, popu, length):
    Xs = [""]
    coordinates = [[]]
    for i in range(1, length+1):
        Xs.append("x" + str(i))
        coordinates.append([])
    
    for cuckoo in cuc_list:
        for i in range(1, length+1):
            coordinates[i].append(cuckoo.habitat[i])
    
    data = {}
    for i in range(1, length+1):
        data.update({Xs[i]: coordinates[i]})
    
    df = DataFrame(data, columns=Xs[1:])
    kmeans = KMeans(n_clusters=3).fit(df)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    Q_sum = [0, 0, 0]
    for i in range(popu):
        Q_sum[labels[i]] += cuc_list_Q[i]
    
    if Q_sum[0] > Q_sum[1] and Q_sum[0] > Q_sum[2]:
        dest_arr = centers[0]
    elif Q_sum[1] > Q_sum[2]:
        dest_arr = centers[1]
    else:
        dest_arr = centers[2]

    dest = [0]
    for i in range(1, length+1):
        dest.append(dest_arr[i-1])
        dest[i] = int(round(dest[i], 0) % len(ngh_matrix[i]))

    return dest


def migration (cuc_list, dest, length):
    best_cuc = Cuckoo(length)
    best_cuc.habitat = dest

    for cuc in cuc_list:
        diff = cuc.difference(best_cuc, length)
        prob = max(round(diff / length, 0)*2, 1)
        for i in range(length):
            if random.random() < prob:
                cuc.habitat[i] = best_cuc.habitat[i]


def two_sort (arr1, arr2):
    if len(arr1) > 1:
        mid = len(arr1)//2
        L1 = arr1[:mid]
        L2 = arr2[:mid]
        R1 = arr1[mid:]
        R2 = arr2[mid:]
        two_sort(L1, L2)
        two_sort(R1, R2)
  
        i = j = k = 0
        while i < len(L1) and j < len(R1):
            if L1[i] > R1[j]:
                arr1[k] = L1[i]
                arr2[k] = L2[i]
                i += 1
            else:
                arr1[k] = R1[j]
                arr2[k] = R2[j]
                j += 1
            k += 1
  
        while i < len(L1):
            arr1[k] = L1[i]
            arr2[k] = L2[i]
            i += 1
            k += 1
  
        while j < len(R1):
            arr1[k] = R1[j]
            arr2[k] = R2[j]
            j += 1
            k += 1


    
def cuckoo_algorithm (adj_matrix, ngh_matrix, popu, iter_num, var_low, var_high, alpha, length):
    cuc_list = []
    for i in range(popu):
        cuc_list.append(random_cuc(adj_matrix, ngh_matrix, length))
    
    best_cuc = Cuckoo(length)
    max_Q = 0

    for count in range(iter_num):
        egg_num, ELR = set_egg_and_ELR (var_low, var_high, alpha, popu)

        egg_list = []
        for i in range(popu):
            my_egg_list = cuc_list[i].spawn(adj_matrix, ngh_matrix, egg_num[i], ELR[i], length)
            for egg in my_egg_list:
                if random.randint(0, 2) != 0:
                    egg_list.append(egg)
        
        cuc_list_Q = []
        cuc_list, cuc_list_Q = choosing_best_eggs(egg_list, popu, length)

        if cuc_list_Q[0] > max_Q:
            max_Q = cuc_list_Q[0]
            for i in range(length+1):
                best_cuc.habitat[i] = cuc_list[0].habitat[i]

        if count < iter_num - 1:
            dest = migration_dest(cuc_list, cuc_list_Q, ngh_matrix, popu, length)
            migration(cuc_list, dest, length)
        
        if count % 10 == 0:
            print("number of iterations =", count, " / max value = ", max_Q)

    p = Partition(length)
    p.build_partition(best_cuc, length)
    best_patitioning = p.report()

    return max_Q, best_patitioning

    


file_address = input('add file address:\n')
try:
    file = open(file_address, 'r')
except IOError:
    print('There is a problem with file address.')

first_line = file.readline()
nodes_num = int(first_line[:-1])

adj_matrix = [[0 for j in range(nodes_num+1)] for i in range(nodes_num+1)]

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

max_value, best_patitioning = cuckoo_algorithm (adj_matrix, ngh_matrix, 10, 100, 5, 8, 20, nodes_num)
print("Best partitioning = ", best_patitioning, " / Q = ", max_value)