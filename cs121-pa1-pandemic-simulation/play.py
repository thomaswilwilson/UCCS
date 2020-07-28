city = ["I0", "I1", "S", "R"]
city_1 = ["S", "S", "S", "I0"]

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


def gets_infected_at_position(city, position, infection_rate):
        if has_an_infected_neighbor(city, position) == True:
            
            immunity_level = random.random()
            if immunity_level > infection_rate:
                infected = False
            else:
                print("made it furtherran")
                infected = True
    else:
        infected = False
    return infected

def simulate_one_day(city, infection_rate):
        old  = city[:]
    for i in range(len(city)):
        if old[i] == "I1":
            city[i] = "I0"

        elif old[i] == "I0":
            city[i] = "R"

        elif old[i] == "R":
            city[i] = "R"

        else:
            if (gets_infected_at_position(old, i, infection_rate)) == True:
                print("guy")
                city[i] = "I1"
    return city

