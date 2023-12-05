import os


class TransportationProblemSolver:
    def __init__(self, file_name):
        self.file_name = file_name

    @staticmethod
    def northwest_corner_method(costs, supply, demand):
        num_suppliers = len(supply)
        num_consumers = len(demand)

        allocated = [[0 for _ in range(num_consumers)] for _ in range(num_suppliers)]

        i = 0
        j = 0

        while i < num_suppliers and j < num_consumers:
            if supply[i] > 0 and demand[j] > 0:
                allocated[i][j] = min(supply[i], demand[j])
                supply[i] -= allocated[i][j]
                demand[j] -= allocated[i][j]
                if supply[i] == 0:
                    i += 1
                if demand[j] == 0:
                    j += 1
            else:
                if supply[i] == 0:
                    i += 1
                if demand[j] == 0:
                    j += 1

        return allocated

    @staticmethod
    def calculate_potentials(costs, allocated):
        num_suppliers = len(costs)
        num_consumers = len(costs[0])
        potentials_suppliers = [0] * num_suppliers
        potentials_consumers = [0] * num_consumers

        potentials_suppliers[0] = 0

        for i in range(num_suppliers):
            for j in range(num_consumers):
                if allocated[i][j] > 0:
                    if potentials_consumers[j] == 0:
                        potentials_consumers[j] = costs[i][j] - potentials_suppliers[i]
                    else:
                        potentials_suppliers[i] = costs[i][j] - potentials_consumers[j]
                elif allocated[i][j] == 0:
                    if potentials_consumers[j] == 0:
                        potentials_consumers[j] = costs[i][j] - potentials_suppliers[i]
                    else:
                        potentials_suppliers[i] = costs[i][j] - potentials_consumers[j]
                elif allocated[i][j] < 0:
                    print(f"Ошибка: allocated[{i}][{j}] имеет отрицательное значение {allocated[i][j]}")
                    return None, None

        return potentials_suppliers, potentials_consumers


    # Метод для перевірки оптимальності
    @staticmethod
    def is_optimal(costs, allocated, potentials_suppliers, potentials_consumers):
        num_suppliers = len(costs)
        num_consumers = len(costs[0])

        for i in range(num_suppliers):
            for j in range(num_consumers):
                if allocated[i][j] == 0:
                    if costs[i][j] - potentials_suppliers[i] - potentials_consumers[j] < 0:
                        return False

        return True


    # Метод для покращення опорного плану
    @staticmethod
    def improve_plan(costs, allocated, potentials_suppliers, potentials_consumers):
        num_suppliers = len(costs)
        num_consumers = len(costs[0])
        min_cost = float('inf')
        min_i = -1
        min_j = -1

        for i in range(num_suppliers):
            for j in range(num_consumers):
                if allocated[i][j] == 0:
                    cost = costs[i][j] - potentials_suppliers[i] - potentials_consumers[j]
                    if cost < min_cost:
                        min_cost = cost
                        min_i = i
                        min_j = j

        return min_i, min_j

    def read_data_from_file(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            costs = []
            supply = []
            demand = []

            for line in lines:
                data = line.split()
                if len(data) > 1:
                    if data[0] == 'COSTS':
                        costs.append([int(cost) for cost in data[1:]])
                    elif data[0] == 'SUPPLY':
                        supply.extend([int(s) for s in data[1:]])
                    elif data[0] == 'DEMAND':
                        demand.extend([int(d) for d in data[1:]])

            return costs, supply, demand

    def print_initial_plan(self):
        costs, supply, demand = self.read_data_from_file()
        initial_plan = self.northwest_corner_method(costs, supply, demand)
        print("Початковий опірний план (північно-західний кут):")
        for row in initial_plan:
            print(row)

    def print_optimal_plan(self):
        costs, supply, demand = self.read_data_from_file()
        initial_plan = self.northwest_corner_method(costs, supply, demand)
        iteration = 1
        while True:
            potentials_suppliers, potentials_consumers = self.calculate_potentials(costs, initial_plan)
            if self.is_optimal(costs, initial_plan, potentials_suppliers, potentials_consumers):
                break
            i, j = self.improve_plan(costs, initial_plan, potentials_suppliers, potentials_consumers)
            initial_plan[i][j] = min(supply[i], demand[j])
            supply[i] -= initial_plan[i][j]
            demand[j] -= initial_plan[i][j]
            print(f"Iteration {iteration}: Supply: {supply}, Demand: {demand}")
            iteration += 1
        print("\nОптимальний план (метод потенціалів):")
        for row in initial_plan:
            print(row)

    @staticmethod
    def edit_file(file_name):
        os.system(f'notepad {file_name}')

file_name = 'data_file.txt'
solver = TransportationProblemSolver(file_name)

while True:
    print("Меню:")
    print("1. Редагувати файл")
    print("2. Вивести початковий опірний план")
    print("3. Вивести оптимальний план")
    print("4. Вихід")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        solver.edit_file('data_file.txt')
    elif choice == '2':
        solver.print_initial_plan()
    elif choice == '3':
        solver.print_optimal_plan()
    elif choice == '4':
        break
    else:
        print("Виберіть правильну опцію.")