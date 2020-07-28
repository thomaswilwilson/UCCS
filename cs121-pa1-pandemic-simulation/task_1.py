city = ["I0", "I1", "S", "R"]

def count_infected(city):
    num_infected = 0
    for i in city:
        if i == "I0" or i == "I1":
            num_infected += 1
    return num_infected

print(count_infected(city))