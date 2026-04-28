import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp


print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file D_kogelomloopspinder_M0_WQA1")
print("")
print("")
print("")


#om te beginnen definieer ik de gekende eigenschappen van het vld voor rek
F_S = 4000 #N de spankracht die op de riem word gezet VRAGEN AAN KRISTOF VOOR RICHTLIJN
E_Modulus = 210000 #N/mm^2 het elasticiteitsmodulus van het materiaal
diameter = 10 #mm de diameter van de spindel
oppervlakte = math.pi * (diameter/2)**2 #mm² doorsnede oppervlakte van de spinder


# maximale spanning in de spindel
sigma_axMax = F_S / oppervlakte #N/mm^2 maximale axiale spanning in de spindel

if sigma_axMax > E_Modulus:
    print("Waarschuwing: De maximale axiale spanning overschrijdt het elasticiteitsmodulus. De spindel zal plastisch vervormen.")   
else:
    print("De maximale axiale spanning is binnen het elasticiteitsmodulus. De spindel zal elastisch vervormen.")                

print(f"Maximale axiale spanning in de spindel: {sigma_axMax:.2f} N/mm^2")



#----- New codeblock -----#



# hier word berekend wat de doorbuiging van de spindel is onder zijn eigen gewicht
#AANNAME: de 2 moeren worden weg gedacht waardoor de spindel enkel door zijn lagers, over de volledige lengte
#word ondersteund, dit is het slechtste scenario. dus met de moeren er op zal het beter zijn en dus ook inorde

massaPerVolume = 7.85 * 10**-6 #kg/mm^3 dichtheid van staal
lengte = 800 #mm lengte van de spindel, arbitrair gekozen
volume = oppervlakte * lengte #mm^3 volume van de spindel
massa = massaPerVolume * volume #kg massa van de spindel
gewicht = massa * 9.81 #N gewicht van de spindel    

traagheidsmoment = (math.pi* diameter**4) / 64 #mm^4 traagheidsmoment van de spindel cilinder aanname tabel 11_3

maxMoment = gewicht * (lengte / 2) #N*mm maximale moment aan het midden van de spindel

#zie tabel 11.6 voor onderstaande berekeningen

doorbuiging = gewicht * lengte**3 / (48 * E_Modulus * traagheidsmoment) #mm
print(f"Doorbuiging van de spindel onder zijn eigen gewicht: {doorbuiging:.2f} mm")
hellingshoek = math.atan((gewicht * lengte**2)/(16 * E_Modulus * traagheidsmoment)) #radianen
hellingshoek_graden = math.degrees(hellingshoek) #graden
print(f"Hellingshoek van de spindel onder zijn eigen gewicht: {hellingshoek_graden:.2f} graden")
print(f"Hellingshoek van de spindel onder zijn eigen gewicht: {hellingshoek:.5f} radianen")
print(" ")
print("tabel 11.5 heeft het over toelaatbare vervorming om deze waarde mee te vergelijken")





# Bij de gekoze lagering moet gezien worden wat de afstand tot de plaat is gemeten van het middelpunt van de spindel. dit is belangrijk voor het moment op het karretje

# EERSTE AANNAME
afstandTotPlaat = diameter / 2 + 40 #mm
