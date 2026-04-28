import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from C_ondersteuningsplaat_M0_ULA1 import breedteVanHetGeheel, lengteVanHetPlatteDeel, diameterVanDeAfronding, massaPlatteDeel, massaHolleCylinder, massaZijplaat
from B_tandwielAs_M0_WQA2 import spelingTussenTandwielen
from D_kogelomloopspinder_M0_WQA1 import massa as massaSpindel
from F_glijrailFaseRegelaarKlem_M0_UAH1 import massaPerKlem, aantalKlemmen
from A_tandriem_M0_WQB1 import maxMassaRiem
from E_glijrailsFaseRegelaar_M0_WRA1 import massaPerRail


print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file H_verbindingsstructuur_M0_ULE6")
print("")
print("")
print("")

# Z-richting is de bewegings richting, Y-richting is de hoogte, X-richting is loodrecht op het tandvlak


#hieronder worden de berekeningen van de connector structuur tussen twee tandlatten gemaakt

afstandTussen2ondersteuningspuntenZ_Richting = (lengteVanHetPlatteDeel - 6000) 
print(f"Afstand tussen de twee ondersteuningspunten: {afstandTussen2ondersteuningspuntenZ_Richting:.2f} mm")

spelingScharnierPuntenTotPlaat = 5 # mm, arbitrair gekozen voor voldoende speling maar compact ontwerp
afstandTussen2scharnierpuntenY_Richting = breedteVanHetGeheel + 2*spelingScharnierPuntenTotPlaat
minimumLengteScharnierArm = diameterVanDeAfronding/2 + 20 #mm de 20 is arbitrair voor compact ontwerp met minimaal moment
print(f"Afstand tussen de twee scharnierpunten: {afstandTussen2scharnierpuntenY_Richting:.2f} mm")
print(f"Minimum lengte van de scharnier arm: {minimumLengteScharnierArm:.2f} mm")



#hieronder worden de YZ coordinaten van de 4 ondersteuningspunten bepaald. 2x voor beide configuraties
#aanname punt 1 heeft coordinaat (0,a) en punt 4 heeft coordinaten (b,0) met beide (z,y) >= 0

print("\n--- Outcomes coresponding to the image ---")
punt1_Z = 0
punt1_Y = 2*spelingScharnierPuntenTotPlaat + 2*breedteVanHetGeheel + spelingTussenTandwielen

punt2_Z = 0
punt2_Y = punt1_Y - 2*spelingScharnierPuntenTotPlaat - breedteVanHetGeheel

punt3_Z = afstandTussen2ondersteuningspuntenZ_Richting
punt3_Y = breedteVanHetGeheel + 2*spelingScharnierPuntenTotPlaat

punt4_Z = punt3_Z
punt4_Y = 0
print(f"Punt 1 coordinaten: (Z: {punt1_Z:.2f} mm, Y: {punt1_Y:.2f} mm)")
print(f"Punt 2 coordinaten: (Z: {punt2_Z:.2f} mm, Y: {punt2_Y:.2f} mm)")
print(f"Punt 3 coordinaten: (Z: {punt3_Z:.2f} mm, Y: {punt3_Y:.2f} mm)")
print(f"Punt 4 coordinaten: (Z: {punt4_Z:.2f} mm, Y: {punt4_Y:.2f} mm)")

#voor punten 5, 6, 7 & 8 word terug een (0,0) stelsel genomen met 8 de coordinaten (0,0)

punt8_Z = 0
punt8_Y = 0

punt7_Z = punt8_Z
punt7_Y = punt8_Y + 2*spelingScharnierPuntenTotPlaat + breedteVanHetGeheel

punt6_Z = afstandTussen2ondersteuningspuntenZ_Richting
punt6_Y = breedteVanHetGeheel + spelingTussenTandwielen

punt5_Z = punt6_Z
punt5_Y = 2*spelingScharnierPuntenTotPlaat + 2*breedteVanHetGeheel + spelingTussenTandwielen
print("")
print(f"Punt 5 coordinaten: (Z: {punt5_Z:.2f} mm, Y: {punt5_Y:.2f} mm)")
print(f"Punt 6 coordinaten: (Z: {punt6_Z:.2f} mm, Y: {punt6_Y:.2f} mm)")
print(f"Punt 7 coordinaten: (Z: {punt7_Z:.2f} mm, Y: {punt7_Y:.2f} mm)")
print(f"Punt 8 coordinaten: (Z: {punt8_Z:.2f} mm, Y: {punt8_Y:.2f} mm)")


print("")



#hieronder word het totale gewicht van een tandlatsectie berekend, om zo de krachten te kunnen bepalen
# de verschillende onderdelen zijn: plaat, riem, kogelspindel, glijrails + karretjes + klemmen voor de faseverschuiving
#cylinders op de uiteindes en schuine balken
totaleMassaTandlatSectie = massaSpindel + massaPerKlem * aantalKlemmen * 2 + maxMassaRiem + massaPlatteDeel + 2 * massaHolleCylinder + 2 * massaPerRail + massaZijplaat #kg
bedrijfsFactor = 1.2
totaleMassaTandlatSectieMetFactor = totaleMassaTandlatSectie * bedrijfsFactor
print(f"Totale massa van een tandlatsectie: {totaleMassaTandlatSectie:.2f} kg")
print(f"Totale massa van een tandlatsectie met bedrijfsfactor: {totaleMassaTandlatSectieMetFactor:.2f} kg")



#vanaf hier word gerekend met de totale massa met bedrijfsfactor erbij!!!!

massaAanElkOphangpunt = totaleMassaTandlatSectieMetFactor/4 #kg (geldeeld door 4 omdat er 4 ophangpunten symetrisch verdeeld zijn)
krachtOpElkOphangpunt = massaAanElkOphangpunt * 9.81 #N
print(f"Kracht op elk ophangpunt: {krachtOpElkOphangpunt:.2f} N")











# image print op het einde zodat hij verder niet stalt
img = mpimg.imread("locationsHangPoints.jpeg")
plt.imshow(img) 
plt.axis("off") 
plt.show()


img = mpimg.imread("krachtenOphangpuntUitwerking.jpeg")
plt.imshow(img)
plt.axis("off")
plt.show()