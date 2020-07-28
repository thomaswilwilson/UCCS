city = ["I0", "I1", "S", "R"]
def count_infected(city):
    count_infected = 0
    for i in city:
        if i == "I0" or i == "I1":
            count_infected += 1
    return count_infected

print(count_infected)