#!/usr/bin/env python
from random import randint as r
scramble = ""
m=b=9
for u in range(20):
	c=b;b=m
	while c+b-4 and m==c or m==b:
		m=r(0,5)
	scramble += "URFBLD"[m]+" '2"[r(0,2)]+" "
scramble=scramble.replace("  "," ")[:-1]
print scramble

