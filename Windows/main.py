import random

def genetic_algorithm(num_cities, coordinates, distances):
    population_size = 10000
    num_generations = 500
    mutation_rate = 0.01

    def total_distance(route):
        total = 0
        for i in range(num_cities - 1):
            city1 = route[i]
            city2 = route[i + 1]
            total += distances[city1][city2]
        total += distances[route[-1]][route[0]]
        return total

    def gen_initial_population():
        return [random.sample(range(num_cities), num_cities) for _ in range(population_size)]

    def crossover(parent1, parent2):
        crossover_point = random.randint(0, num_cities - 1)
        child = parent1[:crossover_point]
        remaining = [gene for gene in parent2 if gene not in child]
        child += remaining
        return child

    def mutate(route):
        for i in range(num_cities):
            if random.random() < mutation_rate:
                j = random.randint(0, num_cities - 1)
                route[i], route[j] = route[j], route[i]

    population = gen_initial_population()
    for _ in range(num_generations):
        population = sorted(population, key=lambda x: total_distance(x))
        selected_parents = population[:population_size // 2]
        offspring = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.choices(selected_parents, k=2)
            child = crossover(parent1, parent2)
            mutate(child)
            offspring.append(child)
        population = selected_parents + offspring
    best_route = min(population, key=lambda x: total_distance(x))
    return best_route

def read_input():
    type_of_input = input().strip()
    num_cities = int(input())
    coordinates = [tuple(map(float, input().split())) for _ in range(num_cities)]
    distances = [list(map(float, input().split())) for _ in range(num_cities)]
    return type_of_input, num_cities, coordinates, distances

def main():
    _, num_cities, coordinates, distances = read_input()
    best_tour = genetic_algorithm(num_cities, coordinates, distances)
    print(" ".join(map(str, best_tour)))

if __name__ == "__main__":
    main()
