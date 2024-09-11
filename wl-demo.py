import wL as wLpy

myWL = wLpy.wL()
myWL.dict = {'example' : ['pêche_au_thon', 'chocolatine'], 'city' : {'Toulouse' : {'population' : 510000, 'loc' : 'south-west'}, 'Paris' : {'population' : 2380000, 'loc' : 'north'}}}
print(myWL.pack())

moWL = wLpy.wL()
moWL.unpack(file = myWL.pack())
print(moWL.get())

# moWL.info()