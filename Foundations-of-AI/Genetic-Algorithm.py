import random
import math


def load_file(filename="input.txt"):
    # Open input.txt file and collect size + city info 
    with open(filename, 'r') as file:
        lines = file.readlines()
        size = int(lines[0].strip())    # First line in file is size
        cities = []
            
        # Split remaining lines and convert to lists of integers for cities
        for i in range(1, size + 1):
            row = list(map(int, lines[i].strip().split()))
            cities.append(row)
            
    # Print statements for verification
    print("\nLines:", lines)
    print("\nSize:", size)
    print("\nCities:", cities)
    
    return size, cities


def CreateInitialPopulation(size, cities): 
    # Generate random (for now) permutations of paths through cities
    initial_population = []
    population_size = 50            # Population size hyperparameter
    
    # Initialize random paths (potential for initialization based on herusitic later...)
    for i in range(population_size):
        path = random.sample(cities, len(cities)) 
        initial_population.append(path)
    
    return initial_population


def FitnessValue(initial_population):
    # Calculate fitness values (euclidean distance)
    city_dist = []    
    path_dist = []    
    
    # For each path, calculate the sum of 3-D euclidean distances between each city visted
    for path in initial_population:
        city_dist.clear()    # Empty list for each path
        
        for city in range(len(path)):
            # Compute 3-D euclidean distance between path[i] and path[i+1]
            current_city = path[city]
            next_city = path[(city+1) % len(path)]    # Includes trip from last city to initial
            
            x_dist = math.pow(current_city[0] - next_city[0], 2)    # Calculate distance between x-coords
            y_dist = math.pow(current_city[1] - next_city[1], 2)    # Calculate distance between y-coords
            z_dist = math.pow(current_city[2] - next_city[2], 2)    # Calculate distance between z-coords
            
            distance = math.sqrt(x_dist + y_dist + z_dist)    
            city_dist.append(distance)
            
        path_dist.append({
            'path': path,
            'distance': sum(city_dist)
        })    
            
    return path_dist


def CreateMatingPool(path_dist):
    # Select 2 smallest path distances and keep track of path
    matingPool = []
    
    # Sort the dict by path distances and select the paths with two smallest values
    sorted_dist = sorted(path_dist, key=lambda x: x['distance'])
    parent1 = sorted_dist[0]['path']
    parent2 = sorted_dist[1]['path']
    
    # Return paths associated with minimal distances 
    matingPool.append(parent1)
    matingPool.append(parent2)
    
    return matingPool


def Crossover(Parent1, Parent2):
    # Updated crossover function 
    size = len(Parent1)
    
    Start_Index = random.randint(0, size - 2)            # Start Index hyperparameter
    End_Index = random.randint(Start_Index + 1, size)    # End Index hyperparameter
    
    child = Parent1.copy()
    
    for i in range(Start_Index, End_Index):
        child[i] = Parent2[i]
            
    # Find all cities and identify duplicates/missing
    all_cities = [tuple(city) for city in Parent1]
    seen = set()                        # Set for paths currently in child
    duplicate_indices = []              # List of indices with duplicate cities in child
    
    # Identify duplicate positions
    for i, city in enumerate(child):
        city_tuple = tuple(city)
        if city_tuple in seen:
            duplicate_indices.append(i)
        else: 
            seen.add(city_tuple)
            
    # Find missing cities
    missing_cities = []                 # List of missing cities in child
    
    for city_tuple in all_cities:
        if city_tuple not in seen:
            missing_cities.append(list(city_tuple))
    
    # Replace duplicates with missing cities
    for i, index in enumerate(duplicate_indices):
        if i < len(missing_cities):
            child[index] = missing_cities[i]
            
    return child


def Mutation(child):
    mutation_rate = 0.2           # Mutation Rate hyperparameter
    
    if random.random() > mutation_rate:
        return child
    
    mutation = random.choice(['swap', 'reverse', 'insert'])        # Mutation type possibilities
    size = len(child)
    
    if mutation == 'swap':
        # Swap two random cities
        i, j = random.sample(range(size),2 )
        child[i], child[j] = child[j], child[i]
        
    elif mutation == 'reverse':
        # Reverse a random segment of the path
        i, j = sorted(random.sample(range(size), 2))
        child[i:j+1] = reversed(child[i:j+1])
        
    elif mutation == 'insert':
        # Remove a city and insert it somewhere else
        i = random.randint(0, size-1)
        j = random.randint(0, size-1)
        city = child.pop(i)
        child.insert(j, city)
        
    return child
    

def write_output(best_path, best_distance, filename="output.txt"):
    with open(filename, 'w') as file:
        # Write the total distance of the best path
        file.write(f"{best_distance: .3f}\n")
        
        # Write each city in best path
        for city in best_path:
            file.write(f"{city[0]} {city[1]} {city[2]}\n")
            
        # Add the first city again at the end, distance was calculated with return to start
        file.write(f"{best_path[0][0]} {best_path[0][1]} {best_path[0][2]}\n")
        
    print("\nOutput written to output.txt")
    


def main():
    # Initialize the population and variables
    size, cities = load_file()
    initial_population = CreateInitialPopulation(size, cities)
    
    num_generations = 100        # Number of generations hyperparameter
    best_solution = []
    best_distance = float('inf')
    current_population = initial_population
    
    # Generate new populations 
    for generation in range(num_generations):
        # Evaluate fitness
        path_dist = FitnessValue(current_population)
        
        # Track best solution
        current_best = min(path_dist, key=lambda x: x['distance'])
        if current_best['distance'] < best_distance:
            best_distance = current_best['distance']
            best_solution = current_best['path']
            
        # Next generation
        next_population = []
        
        for i in range(len(current_population)):
            mating_pool = CreateMatingPool(path_dist)
            child = Crossover(mating_pool[0], mating_pool[1])
            child = Mutation(child)
            next_population.append(child)
            
        current_population = next_population
        
    # Write to output.txt
    write_output(best_solution, best_distance)
        
main()
    
