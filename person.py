s = str()
s1 = str()
f = open('test.txt', 'r')

l = ['\'''\'' + item[:-2] + '\'''\'' for item in f]
s = ",".join(l)
s1 = str(s)
json={'items': s1}
print(s1)
print(json)















