import os

basedir = os.path.abspath(os.path.dirname(__file__))
direct = os.path.join(basedir, 'metro_list.txt')
print(direct)

with open('C:\\Project\\rent_project\\webapp\\ads\\metro_list.txt', encoding="utf8", newline='') as f:
    metro = [(line.strip(), line.strip()) for line in f.readlines()]
