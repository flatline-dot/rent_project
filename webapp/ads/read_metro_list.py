import os

basedir = os.path.abspath(os.path.dirname(__file__))
direct = os.path.join(basedir, 'metro_list.txt')

with open(direct, encoding="utf8", newline='') as f:
    metro = [(line.strip(), line.strip()) for line in f.readlines()]
