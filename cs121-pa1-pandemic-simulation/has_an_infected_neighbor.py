city = ["I0", "I1", "S", "R"]

def has_an_infected_neighbor(city, position):
    for i in range(len(city)):
        if (city[i - 1] == "I0" or city[i - 1] == "I1") or (city[i + 1] == "I0" or city[i + 1] == "I1"):
            neighbor_infected = True
            #if city[(i +1) % len(city)] or city[(i - 1) % len]
    return neighbor_infected

print(has_an_infected_neighbor(city, 2))
