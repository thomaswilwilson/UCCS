city = ["I0", "I0", "S"]

import sir
import util
import random

def has_an_infected_neighbor(city, position):
    if position == 0:
        if (city[len(city) - 1] == "I0" or city[len(city) - 1] == "I1") or (city[position + 1] == "I0" or city[position + 1] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    elif position == (len(city) - 1):
        if (city[position - 1] == "I0" or city[position - 1] == "I1") or (city[0] == "I0" or city[0] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    else:
        if (city[position - 1] == "I0" or city[position - 1] == "I1") or (city[position + 1] == "I0" or city[position + 1] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    return neighbor_infected

print(has_an_infected_neighbor(city, 0))

def gets_infected_at_position(city, position, infection_rate):

    if has_an_infected_neighbor(city, position) == True:
            random.seed(sir.TEST_SEED)
            immunity_level = random.random()
            if immunity_level > infection_rate:
                infected = False
            else:
                infected = True
    else:
        infected = False

    return infected

print(gets_infected_at_position(city, 2, 0.5))

