import re

pattern = re.compile('nb_drones: [1-9]')
b = "nb_drones: 1"
print(re.fullmatch(pattern, b))
