import wL as wLpy
from time import time

as_range = 1000

print('wL Demo /')

myWL = wLpy.wL()
myWL.dict = {'example' : ['pêche_au_thon', 'chocolatine'], 'city' : {'Toulouse' : {'population' : 510000, 'loc' : 'south-west'}, 'Paris' : {'population' : 2380000, 'loc' : 'north'}}}
packed = myWL.pack()
print(packed)

moWL = wLpy.wL()
moWL.unpack(file = myWL.pack())
print(moWL.get())
print(moWL.exportXML())

# wL_info()

print('wL Demo / PERFS')
print(f' - range({as_range})')
print('wL Demo / pack.perfs /')
as_time  = time()
for _ in range(as_range):
    myWL.pack()
total_time = round(1000 * (time() - as_time)) / 1000
print(f' - Done in {total_time} seconds. \n')
print('wL Demo / unpack.perfs /')
as_time  = time()
for _ in range(as_range):
    myWL.unpack(packed)
total_time = round(1000 * (time() - as_time)) / 1000
print(f' - Done in {total_time} seconds, for {len(packed) * as_range} chr. \n')

print('wL Demo / \n')
