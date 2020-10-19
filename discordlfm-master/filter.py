
import sys,getopt

infile = open("swears.txt","r")
swears = list(infile.readlines());

for i in range(len(swears)):
    swears[i] = swears[i].replace("\n","")

def censor(s):
    vow = ['a','e','i','o','u']
    res = ""
    first = True
    for i in s:
        if first and i.lower() in vow:
            res += '*'
            first = False
        else:
            res+=i
    return res

s = sys.argv[1]

for swear in swears:
    while(swear in s.lower()):
        idx = s.lower().find(swear)
        s = s[:idx] + censor(s[idx:idx+len(swear)]) + s[idx+len(swear):]
infile.close()
print(s)
