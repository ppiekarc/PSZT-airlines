import random


class PlaneAllocation(object):
    def __init__(self, file):
        self.M = None
        self.N = None
        self.crews = dict()
        self.guys = []
        self.read_input(file)

    def read_input(self, file):
        with open(file, 'r') as f:
            line = f.readline().split()
            self.M = int(line.pop())
            self.N = int(line.pop())
            for i in range(0, self.M):
                cost = int(f.readline())
                self.crews[i] = cost

    """ sprawdzenie czy osobnik spelnia warunki zadania"""
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
            while j < self.N:
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
                guy.append(v)

            self.guys.append(guy)

    """krzyzowanie - nowy osobnik posiada pierwsza polowe
        wierszow od ojca a droga od matki"""
    def crossing(self, male, female):
        child = []
        for i in range(int(self.N / 2)):
            v = dict()
            v['x'] = male[i]['x']
            v['sigma'] = male[i]['sigma']

            child.append(v)

        for i in range(int(self.N / 2), self.N):
            v = dict()
            v['x'] = female[i]['x']
            v['sigma'] = female[i]['sigma']

            child.append(v)

        return child

    """mutacja - w kazdym wierszu nowego osobnika jest
        losowanych od nowa kilka wartosci, w zaleznosci od
        parametru osobnika"""
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
        for j in range(self.N):
            s += sum(self.crews[i] for i in elem[j]['x'])

        return s

    """do nastepnego pokolenia wybierane jest mi najlepszych
        osobnikow"""
    def population_choice(self, mi):
        self.guys.sort(key=self.cost_sum)
        self.guys = self.guys[0: mi]

    def run_algorithm(self, mi, lambda_, max_iter, max_best):
        i = 0
        j = 0
        best = 0
        self.generate_init_population(mi)
        while i < max_iter:
            self.reproduction(lambda_)
            self.population_choice(mi)

            if best <= self.cost_sum(self.guys[0]):
                j += 1
                if j >= max_best:
                    break
            else:
                j = 0

            best = self.cost_sum(self.guys[0])
            i += 1


if __name__ == '__main__':
	allocator = PlaneAllocation("input.txt")
	allocator.run_algorithm(200, 80, 1501, 1000)

	""" wyswietlenie najlepszego rozwiazania """
	print("przydzial załóg(nr wiersza mowi ktory to samolot):")
	for v in allocator.guys[0]:
		print(v['x'])

	print("koszt: " + str(allocator.cost_sum(allocator.guys[0])))

