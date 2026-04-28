import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from H_verbindingsstructuur_M0_ULE6 import krachtOpElkOphangpunt


print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file J_ophangingsglijkarretjes_WQE2")
print("")
print("")
print("")



#in dit bestand worden de karretjes bepaald die de tandlatsecties omhooghouden en bevestigen aan de portieken
print("krachten in punten 1-4 zijn gelijk aan: ", krachtOpElkOphangpunt)
print("")



kracht_Y1 = krachtOpElkOphangpunt
kracht_Y2 = krachtOpElkOphangpunt

kracht_R3 = 2*(kracht_Y1 + kracht_Y2)
kracht_R5 = kracht_Y1 + kracht_Y2

print(f"Kracht Y1 = {kracht_Y1:.2f} N")
print(f"Kracht Y2 = {kracht_Y2:.2f} N")
print(f"Kracht R3 = {kracht_R3:.2f} N")
print(f"Kracht R5 = {kracht_R5:.2f} N")


