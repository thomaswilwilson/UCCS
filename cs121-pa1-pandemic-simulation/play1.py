city = ["I0", "I1", "S", "R"]
city_1 = ["S", "S", "S", "I0"]

def has_an_infected_neighbor(city, position):
    if (city[position - 1] == "I0" or city[position - 1] == "I1") or (city[position + 1] == "I0" or city[position + 1] == "I1"):
        neighbor_infected = True
    return neighbor_infected

print(has_an_infected_neighbor(city, 1))