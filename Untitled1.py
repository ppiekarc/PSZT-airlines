
# coding: utf-8

# In[15]:



# coding: utf-8

# In[1]:


import random
import os
import matplotlib.pyplot as plt

# @TODO Zmiana liczby analizowanych dni obslugi (wierszy) (czyli dni np na 14)
# @TODO Sprawdzenie czy ostatni i pierwszy dzien spelniaja warunki zadania (tzn czy mozna zapetlic przydzial na kolejne dni aby zostaly spelnione
# warunki zadania
# @TODO dodanie rysowania wartosci najlepszej wartosci funkcji celu w kolejnych pokoleniach

os.chdir('C:\\Users\joann\OneDrive\Desktop\eiti\pszt_projekt')
#UWAGA PRZYPADKOWO LICZBY DNI JEST RÓWNA LICZBIE SAMLOTÓW! DO ZMIANY I PARAMETRYZACJI

class PlaneAllocation(object):
    def __init__(self, file):
        self.M = None #wszystkie dostępne załogi
        self.N = None #samoloty
        self.num_of_days = None
        self.crews = dict()
        self.guys = []
        self.read_input(file)

    def read_input(self, file):
        with open(file, 'r') as f:
            line = f.readline().split()
            self.num_of_days = int(line.pop())
            self.M = int(line.pop())
            self.N = int(line.pop())
            for i in range(0, self.M):
                cost = int(f.readline())
                self.crews[i] = cost

    """ sprawdzenie czy osobnik spelnia warunki zadania"""
    """ stosowane PO krzyzowaniu i mutacji na potomnych osobnikach.
    Osobnicy pierwszej populacji są tworzeni w sposób spełniający wymagania zadania"""
    @staticmethod
    def check_guy(guy):
        intersection = list(set(guy[0]['x']).intersection(guy[1]['x']))
        for i in range(2, len(guy)):
            if list(set(intersection).intersection(guy[i]['x'])):
                return False

            intersection = list(set(guy[i]['x']).intersection(guy[i - 1]['x']))

        return True

    def generate_init_population(self, mi):
        intersection = None
        for i in range(mi):
            guy = []
            j = 0
            state = 0
            while j < self.num_of_days:
                v = dict()
                v['x'] = random.sample(range(self.M), self.N)
                if state == 2:
                    inter2 = list(set(intersection).intersection(v['x']))
                    if inter2:
                        continue

                    state = 1

                if state == 1:
                    tmp = list(set(guy[-1]['x']).intersection(v['x']))
                    if len(tmp) > int(self.M / 2):
                        continue

                    intersection = tmp
                    state = 2

                if state == 0:
                    state = 1

                j += 1
                v['sigma'] = random.choice(range(int(self.N/2)))
				#sigma ma wartość od 0 do liczby dni/2. TODO: Sigma powinna być sparametryzowana.
                guy.append(v)

            self.guys.append(guy)




    """krzyzowanie - nowy osobnik posiada pierwsza polowe
        wierszow od ojca a droga od matki"""
    def crossing(self, male, female):
        child = []
        division_line=random.randint(1, 8)
        for i in range(division_line):
            v = dict()
            v['x'] = male[i]['x']
            v['sigma'] = male[i]['sigma']

            child.append(v)

        for i in range(division_line, self.num_of_days):
            v = dict()
            v['x'] = female[i]['x']
            v['sigma'] = female[i]['sigma']

            child.append(v)

        return child

    """mutacja - w kazdym wierszu nowego osobnika jest
        losowanych od nowa kilka wartosci, w zaleznosci od
        parametru osobnika - sigma"""
    def mutation(self, child):
        for v in child:
            if v['sigma'] == 0:
                continue

            to_change = random.sample(v['x'], v['sigma'])
            saved = list(set(v['x']).difference(to_change))
            to_rand = set(range(self.M)).difference(saved)
            v['x'] = saved + random.sample(to_rand, v['sigma'])

    def reproduction(self, lambda_):
        tmp_generation = random.sample(self.guys, lambda_)
        for i in range(lambda_):
            child = self.crossing(tmp_generation[i], tmp_generation[(i + 1) % lambda_])
            self.mutation(child)
            if self.check_guy(child):
                self.guys.append(child)

    def cost_sum(self, elem):
        s = 0
        for j in range(self.num_of_days):
            s += sum(self.crews[i] for i in elem[j]['x'])

        return s

    # @TODO dodanie opcji algortm ruletki
    """do nastepnego pokolenia wybierane jest mi najlepszych
        osobnikow"""
    def population_choice(self, mi):
        self.guys.sort(key=self.cost_sum)
        self.guys = self.guys[0: mi]

    def run_algorithm(self):
        mi, lambda_=[int(x) for x in input("Zadaj mi i lambde: ").split()]
        max_iter, max_best=[int(y) for y in input("Zadaj max_iter i warunek stopu: ").split()]
        var=1
        i = 0
        j = 0
        best = 0
        avgguy=[]
        sum_=0
        results=[]
        self.generate_init_population(mi)
        while i < max_iter:
            self.reproduction(lambda_)
            self.population_choice(mi)
            
            if best <= self.cost_sum(self.guys[0]):
                j += 1
                if j >= max_best:
                    if var>0:
                        continuation=input('Czy chcesz kontynuowac? Y/N ')
                        if continuation=='Y':
                            var=0
                        if continuation=='N': 
                            break
            else:
                j = 0
            
            sum_=sum_+self.cost_sum(self.guys[0])
            avgguy.append(sum_/(i+1))
            
            best = self.cost_sum(self.guys[0])
            results.append(best)
            if i%500==0:
                print("Working on it...",i,"->",best)
            i += 1
        plt.figure(figsize=(7,7))
        plt.plot(results)
        plt.plot(avgguy)
        plt.ylabel('Koszt')
        plt.xlabel('Iteracje')
        plt.show()
        
if __name__ == '__main__':
    allocator = PlaneAllocation("input.txt")
    allocator.run_algorithm()
    #mi- początkowa populacja, lambda- liczba potomków, max iter, max_best- warunek stopu- liczba iteracji bez poprawy

    """ wyswietlenie najlepszego rozwiazania """
    print("przydzial załóg(nr kolumny mowi ktory to samolot):")
    for v in allocator.guys[0]:
        print(v['x'])

    print("koszt: " + str(allocator.cost_sum(allocator.guys[0])))

