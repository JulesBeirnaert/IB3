import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from D_kogelomloopspinder_M0_WQA1 import F_S

print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file F_glijrailFaseRegelaarKlem_M0_UAH1")
print("")
print("")
print("")



#hier word kort gekeken naar de maximale kracht die de klem moet kunnen tegenhouden om de tandriem
#op zijn plaats vast te houden

opneembareKrachtGekozenKlem = 1200 #N
aangelegdeKrachtDoorRiem = F_S #N

aantalKlemmen = math.ceil(aangelegdeKrachtDoorRiem/opneembareKrachtGekozenKlem)
print("Aantal klemmen nodig per railtrolley: ", aantalKlemmen)
print(" ")
print("Is hier een veiligheidsfactor nodig?")


#----- New codeblock -----#


massaPerKlem = .5 #kg dit moet uit de catalogus gehaald worden

