class city:
    def __init__(self,temp,rain):
        self.temp = temp
        self.rain = rain
        self.days = 1

d = {}

while True:
    str = input()
    if str == "end":
        break
    data = str.split(" ")
    name = data[0]
    temp = float(data[1])
    rains = 1 if data[2] == "yes" else 0
    if name in d:
        t = d[name]
        t.rain += rains
        t.days += 1
        t.temp += temp
    else:
        d[name] = city(temp,rains)

cities = sorted(d.items(), key=lambda x: (-x[1].rain, x[0]))

for name,city in cities:
    temperature = city.temp / city.days
    formated = f"{temperature:.2f}"
    if formated[-1] == "0":
        formated = formated[:-1]
    print(name,formated,city.rain)