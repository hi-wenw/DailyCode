f = open('log.txt', 'r')
data = f.read().strip().split('\n')

for i in data:
    if 'INFO' in i:
        print(i)
