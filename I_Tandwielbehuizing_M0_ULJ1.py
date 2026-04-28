import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from A_tandriem_M0_WQB1 import krachtOpTandenwiel, hoek_ingrijping, veerkracht
from B_tandwielAs_M0_WQA2 import AfstandTussenLagers, spelingTotBovensteLager, breedteTandwiel


print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file I_Tandwielbehuizing_M0_ULJ1")
print("")
print("")
print("")

#eerst word de kracht op het tandwiel bepaald (met richting). er word verondersteld dat de kracht zich enkel in het ZX vlak afspeelt
#en niet in de hoogte richting Y. 
#De gebruikte krachten komen hierbij van de tandriembepaling
# De Z richitng is de voorbewegingsrichting en de X richting is loodrecht op het tandvlak


#de totale kracht is die van de kracht op een tand en die van drukveer

krachtTandwiel = krachtOpTandenwiel #N dit onder een hoek van 20 graden (zelfde hoek al bij tandriem berekening)
KrachtTanwiel_Z = krachtTandwiel * math.cos(math.radians(hoek_ingrijping)) #N
KrachtTandwiel_X = krachtTandwiel * math.sin(math.radians(hoek_ingrijping)) #N

Veerkracht_X = veerkracht

totaleKracht_X = Veerkracht_X + KrachtTandwiel_X
totaleKracht_Z = KrachtTanwiel_Z

hoekResultante = math.degrees(math.atan(totaleKracht_X/totaleKracht_Z)) # deze hoek is tov de Z as (idem als de hoek van het tandvlak)
totaleKracht = math.sqrt(totaleKracht_X**2 + totaleKracht_Z**2)

print("Totale kracht op het tandwiel:", totaleKracht, "N")
print("Hoek van de resulterende kracht ten opzichte van de Z-as:", hoekResultante, "graden")

afstandTussenDeLagers = AfstandTussenLagers

#het grootste moment rond de basis van de behuising is wanneer het bovenste tandwiel ingrijpt
#we nemen de onderste lager aan als Y = 0 en de aangrijping gebeurd halverwegen een tandwiel

yCoordinaatAangrijping = afstandTussenDeLagers - spelingTotBovensteLager - (breedteTandwiel/2) #mm
overigeLengte = afstandTussenDeLagers - yCoordinaatAangrijping #mm

krachtBoven = totaleKracht * yCoordinaatAangrijping/afstandTussenDeLagers
krachtOnder = totaleKracht - krachtBoven
print("Kracht op het bovenste lager:", krachtBoven, "N")
print("Kracht op het onderste lager:", krachtOnder, "N")
print("")
print("Nu weten we de krachten die inwerken op debehuizing vanboven en onder in de structuur. Hiermee kan de structuur verder bepaald worden.")
