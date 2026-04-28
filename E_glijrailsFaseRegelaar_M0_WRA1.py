import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from D_kogelomloopspinder_M0_WQA1 import F_S
from C_ondersteuningsplaat_M0_ULA1 import diameterVanDeAfronding
from D_kogelomloopspinder_M0_WQA1 import lengte, afstandTotPlaat as spindelAfstandTotPlaat

print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file E_glijrailsFaseRegelaar_M0_WRA1")
print("")
print("")
print("")




#in deze code word bekeken naar het tedragen moment/kracht van de glijrail met karretje
#bekijk zeker het VLD van deze glijrail 

# de grootste factor is het moment gecreeerd door de spankracht vande riem
lengte #mm
afstandTotPlaat = diameterVanDeAfronding * 0.001 #m, Dit is de afstand van de afronding in de plaat (zie die code/vld)




#----- New codeblock -----#

#de aanname is dat de kogelomloopspindel de volledige spankracht opneemt. terwijl het karretje het moment opvangd. 
#terwijl voor de glijrailklem word er van uit gegaan dat de spindel door rotatie geen kracht meer draagt en deze door de klem zal moeten gedragen worden

momentDoorSpankracht = F_S * afstandTotPlaat #Nm positief
momentDoorSpindel = F_S * spindelAfstandTotPlaat * -1 * 0.001 #Nm negatief
resterendMoment = momentDoorSpankracht + momentDoorSpindel #Nm

print( "het resterend moment dat door het karretje moet opgevangen worden is ", resterendMoment, " Nm. dit is een van de dingen waar moet naar gekeken worden in de catalogus.")




# moet hier een veiligheidsfactor bij komen? of moet ik gwn een rail kiezen die een grotere Newtonage aankan?



massaPerMeterGekozeRail = 8 #kg/m dit moet uit de catalogus gehaald worden en is momenteel een schatting
massaPerRail = massaPerMeterGekozeRail * (lengte/1000) #kg


