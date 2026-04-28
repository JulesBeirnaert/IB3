import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp

print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file A_tandriem_M0_WQB1")
print("")
print("")
print("")


massa_robot = 1000 #kg
max_versnelling = 0.5 #m/s^2
diameter_tandenwiel = 0.220 #m door 220 te kiezen is een modulus van 10 haalbaar
hoek_ingrijping = 20 #graden
veerkracht = 500 #N dit is voorlopig een random ass waarde die ik nog moet bepalen (moet groter zijn dan krachtdruk op tandwiel) 
wrijvingsCoefficientWielen = .005 * 5 #µ voor vuile trein rails. maal veiligheid van 5 voor overgangen enz https://www.engineeringtoolbox.com/rolling-friction-resistance-d_1303.html?utm_source=chatgpt.com
wrijvingWielen = massa_robot * 9.81 * wrijvingsCoefficientWielen
krachInVoortbewegingsrichting = massa_robot * max_versnelling + wrijvingWielen #N
krachtOpTandenwiel = krachInVoortbewegingsrichting / math.cos(math.radians(hoek_ingrijping)) #N
krachtDrukOpTandenwiel = krachtOpTandenwiel * math.sin(math.radians(hoek_ingrijping)) #N
print("Kracht in voortbewegingsrichting (F_t):", krachInVoortbewegingsrichting, "N")
print("Kracht druk op tandenwiel (F_r):", krachtDrukOpTandenwiel, "N")
print("Kracht op tandenwiel (F_bn):", krachtOpTandenwiel, "N")


#----- New codeblock -----#


# tanden aantal moet groter zijn dan 17 voor een normaal tandprofiel wat standaard is 
# bij een tandriem
maximumModulus = diameter_tandenwiel * 1000 / 17
print("Maximum modulus:", maximumModulus, "m")


#----- Newcodeblock -----#


#modulus kiezen en zien dat het tandwiel ermee gemaakt kan worden, 
#aantal tanden moet groter zijn dan 17 
#en hoe groter de modulus hoe een grotere spanning die kan opvangen
gekozeModulus = 10 #mm
gekozeBreedteFactor = 15 #zie 21.4.1 puntje 4. Tabel 21.14  "staalcontrucie of vliegend rondsel"
print("Gekozen modulus:", gekozeModulus, "mm")
aantalTanden = diameter_tandenwiel * 1000 / gekozeModulus
print("Aantal tanden:", aantalTanden)


#----- Newcodeblock -----#


#hier word de buigspanning bepaald op de tandvoet
#de formule is M/W, waarbij M het buigend moment is en W het weerstandsmoment van de tand
H_Fin = 2*gekozeModulus #mm AANNAME "pak gwn de tandhoogte, dit is groter dan het wrs is maar nogsteeds is het dan inorde"
breedte = gekozeBreedteFactor * gekozeModulus + 0 # de extra factor is toegevoegd om anar boven af te ronden tot de volgende verkrijgbare breedte
afrondingsFactor = breedte - gekozeBreedteFactor * gekozeModulus #mm Vooral Nuttig voor in andere files
S_Vn = gekozeModulus # mm Kristof zei dat dit klopte

print("Breedte van het tandwiel:", breedte, "mm")

buigmomentTandvoet = (krachtOpTandenwiel *math.cos(math.radians(hoek_ingrijping)) * H_Fin) / (breedte * (S_Vn**2)/6)
print("Buigmoment op tandvoet:", buigmomentTandvoet, "N/mm^2")


#----- Newcodeblock -----#


#hier word de drukspanning bepaald op de tandvoet
drukspanningTandvoet = (krachtDrukOpTandenwiel+veerkracht)/(breedte * S_Vn)
print("Drukspanning op tandvoet:", drukspanningTandvoet, "N/mm^2")



#----- Newcodeblock -----#


#totale spanning op de tandvoet is de som van de buigmoment en drukspanning
totaleSpanningTandvoet = buigmomentTandvoet + drukspanningTandvoet
print("Totale spanning op tandvoet:", totaleSpanningTandvoet, "N/mm^2")


#----- Newcodeblock -----#


#het volgende aspect is de tanddruk tgv Hertz hiervoor ga je naar puntje 21.5.5 in de cursus
krachtOpTand = krachtOpTandenwiel + 2* veerkracht*math.cos(math.radians(hoek_ingrijping))
E_modulus_Riem = 50 #N/mm^2 tpu
E_modulus_tandwiel = 70000 #N/mm^2 voor staal
E_modulus = (2*E_modulus_Riem*E_modulus_tandwiel)/(E_modulus_Riem+E_modulus_tandwiel) #N/mm²

radiusTand = 110 #DIT ZEKER NOG EENS ONDERRZOEKEN

#omdat ik zit met een bol op vlak moet ik andere formules gebruiken zoals deze https://en.wikipedia.org/wiki/Contact_mechanics
sigmaHertz = (1/math.pi)*((6*krachtOpTand*(E_modulus**2))/(radiusTand**2))**(1/3)





massaPerLengteGekozeRiem = .68 #kg/m
maxLengteRiem = 2*6.3 + math.pi*.15 #m
print("Maximale lengte van de riem:", maxLengteRiem, "mm")
maxMassaRiem = massaPerLengteGekozeRiem * maxLengteRiem #kg
print( "max massa tanriem = ", maxMassaRiem, " kg")

