import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from A_tandriem_M0_WQB1 import gekozeModulus, gekozeBreedteFactor, afrondingsFactor, veerkracht
from D_kogelomloopspinder_M0_WQA1 import lengte, F_S


print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file C_ondersteuningsplaat_M0_ULA1")
print("")
print("")
print("")

#deze code is bedoeld om te bekenen of de houdplaat voor de tandriem voldoende stevig is
#of deze niet zal buigen of buckelen onder de inwerkende krachten van het systeem

#hieronder staan de variablen die al bepaald kunnen worden, de rest zal nog bepaald moeten worden via
#verder overleg of berekeningen
gekozenModulusTandriem = gekozeModulus
breedteVanHetGeheel = gekozenModulusTandriem *gekozeBreedteFactor + afrondingsFactor # mm
lengteVanHetPlatteDeel = 6300 # mm, dit is momenteel een schating aangezien secties 6 meter zijn plus overlap
diameterVanDeAfronding = 150 # mm, momentele schatting, gebasseerd op de hoogte van het spindel deel
EersteAannameDiktePlaat = 10 # mm


print("Breedte van het geheel:", breedteVanHetGeheel, "mm")





finaleDiktePlaat = 12 # mm, deze waarde zal nog aangepast moeten worden op basis van de berekeningen

volumePlatteDeel = breedteVanHetGeheel * lengteVanHetPlatteDeel * finaleDiktePlaat #mm³
dichtheidStaal = 0.00000785 #kg/mm³
E = 210000.0 # N/mm²
massaPlatteDeel = volumePlatteDeel * dichtheidStaal #kg


volumeHolleCylinder = math.pi * (((diameterVanDeAfronding/2)**2)-((diameterVanDeAfronding/2)-finaleDiktePlaat)**2) * lengteVanHetPlatteDeel #mm³
massaHolleCylinder = volumeHolleCylinder * dichtheidStaal #kg

volumeZijplaat = finaleDiktePlaat * (diameterVanDeAfronding - finaleDiktePlaat) * lengteVanHetPlatteDeel
massaZijplaat = volumeZijplaat * dichtheidStaal




#----- NEW BLOCK -----


#hieronder word het traagheidsmoment over het geheel van de plaat bepaald dit word op intervallen van 1mm gedaan. (de dikte van elke sectie is dus telkens 1mm)
#vervolgens word de plaat op verdeeld in 3 stukken. namelijk het midden zonder ribben (de breedte van de lenfte van de kogelomloopspindel)
#en de 2 zijkanten met schuine ribben

X = 0 # dit is de variabelen over de afstand die varieerd tussen 0 en de lengte van het platte deel
interval = 1 #mm



lengteMiddenStuk = lengte
lengteZijkant = (lengteVanHetPlatteDeel - lengteMiddenStuk) / 2
hoekVanRibben = math.atan(diameterVanDeAfronding/(lengteZijkant))


#voor de ribben word een staaf genomen met een vierkant als doorsnede
breedteRibben = 10 # mm
hoogteRibben = (breedteRibben-0) / math.cos(hoekVanRibben) # mm



#voor de hoogte van het zwaartepunt van de ribben moet er eerste bepaald worden welk van de 2 stukken. het ereste stuk is van 0 tot lengteZijkant en het tweede stuk is van lengteZijkant + lengteMiddenStuk tot lengteVanHetPlatteDeel
#bij het eerste deel zal de rico negatief zijn en bij het tweede deel positief
ricoEersteStuk = math.tan(hoekVanRibben)
ricoTweedeStuk = -math.tan(hoekVanRibben)


if X <= lengteZijkant:
    hoogteZwaartepuntRibben = diameterVanDeAfronding - finaleDiktePlaat- (ricoEersteStuk * X) # mm
else:
    if X >= lengteZijkant + lengteMiddenStuk:
        hoogteZwaartepuntRibben = diameterVanDeAfronding - finaleDiktePlaat- (ricoTweedeStuk * (X - (lengteZijkant + lengteMiddenStuk))) # mm
    else:
        hoogteZwaartepuntRibben = finaleDiktePlaat /2 # mm

if hoogteZwaartepuntRibben != finaleDiktePlaat/2:
    oppervlakteRibben = breedteRibben * hoogteRibben # mm²
else:
    oppervlakteRibben = 0 # mm²


oppervlaktePlaat = breedteVanHetGeheel * finaleDiktePlaat # mm²
hoogteZwaartepuntPlaat = finaleDiktePlaat / 2 # mm

areaYRib = hoogteZwaartepuntRibben * oppervlakteRibben # mm³
areaYPlate = hoogteZwaartepuntPlaat * oppervlaktePlaat # mm³

gemeenZwaartepunt = (areaYPlate + areaYRib)/(oppervlaktePlaat + oppervlakteRibben)

momentOfInertiaRib = (oppervlakteRibben * hoogteRibben**2)/(12) + oppervlakteRibben * ((hoogteZwaartepuntRibben - gemeenZwaartepunt)**2) # is zo geschreven dat deze 0 word als deze buiten de zijkanten range valt
momentOfInertiaPlate = (breedteVanHetGeheel * finaleDiktePlaat ** 3)/12 + oppervlaktePlaat * (abs(hoogteZwaartepuntPlaat - gemeenZwaartepunt)**2)


totalMomentOfInertia = 2 * momentOfInertiaRib + momentOfInertiaPlate








# ----- CHAT GPT ZIJN LUS VOOR TRAAGHEIDSMOMENT, GEBASEERD OP MIJN CODE!-----

# ------------------ ITERATIE OVER X + OPSLAAN ------------------

# Lijstjes voor opslag die je in het volgende deel van je code kunt gebruiken
X_values = []
I_values = []
ybar_values = []        # neutrale as per X
c_top_values = []       # afstand tot bovenste uiterste vezel
c_bottom_values = []    # afstand tot onderste uiterste vezel


# Itereren van 0 tot en met lengteVanHetPlatteDeel (stap = interval)
for X in range(0, int(lengteVanHetPlatteDeel) + 1, int(interval)):

    # --- 1. Bepaal de theoretische hoogte van het zwaartepunt van de ribben per zone ---
    if X <= lengteZijkant:
        # links
        afstand_vanaf_rand = X
        hoogteZwaartepuntRibben = (diameterVanDeAfronding - finaleDiktePlaat) - (ricoEersteStuk * afstand_vanaf_rand)
    elif X >= lengteZijkant + lengteMiddenStuk:
        # rechts (symmetrisch, afstand vanaf rechterrand)
        afstand_vanaf_rand = lengteVanHetPlatteDeel - X
        hoogteZwaartepuntRibben = (diameterVanDeAfronding - finaleDiktePlaat) - (ricoEersteStuk * afstand_vanaf_rand)
    else:
        # midden: geen ribben, zet zwaartepunt op neutraalvlak plaat
        hoogteZwaartepuntRibben = finaleDiktePlaat / 2

    # --- 2. FILTER: De "Makkelijke Manier" ---
    # We berekenen waar de onderkant van de ribbe zich bevindt: Zwaartepunt - helft van de hoogte
    onderkantRib = hoogteZwaartepuntRibben - (hoogteRibben / 2)

    # De ribbe telt enkel mee als deze boven de plaat uitsteekt
    if (X <= lengteZijkant or X >= (lengteZijkant + lengteMiddenStuk)) and (onderkantRib > finaleDiktePlaat):
        oppervlakteRibben = breedteRibben * hoogteRibben  # mm²
    else:
        # Als de ribbe de plaat raakt of in het middenstuk zit: negeer de ribbe volledig
        oppervlakteRibben = 0  # mm²
        hoogteZwaartepuntRibben = finaleDiktePlaat / 2 # Reset voor de Steiner berekening

    # --- 3. Plaat-gegevens ---
    oppervlaktePlaat = breedteVanHetGeheel * finaleDiktePlaat  # mm²
    hoogteZwaartepuntPlaat = finaleDiktePlaat / 2  # mm

    # --- 3a. zijplaat-gegevens ---
    oppervlakteZijplaat = finaleDiktePlaat * (diameterVanDeAfronding-finaleDiktePlaat)
    hoogteZwaartepuntZijplaat = finaleDiktePlaat + ((diameterVanDeAfronding - finaleDiktePlaat)/2)

    # --- 4. Gemeen zwaartepunt (Neutraalvlak van de gecombineerde doorsnede) ---
    areaYRib = hoogteZwaartepuntRibben * oppervlakteRibben  # mm³
    areaYPlate = hoogteZwaartepuntPlaat * oppervlaktePlaat  # mm³
    areaYSideplate = hoogteZwaartepuntZijplaat * oppervlakteZijplaat
    
    totaalOppervlak = oppervlaktePlaat + oppervlakteRibben + oppervlakteZijplaat
    gemeenZwaartepunt = (areaYPlate + areaYRib + areaYSideplate) / totaalOppervlak
    ybar_values.append(gemeenZwaartepunt)

    # --- 5. Traagheidsmoment ribben (Eigen traagheid + Steiner) ---
    if oppervlakteRibben > 0:
        momentOfInertiaRib = (oppervlakteRibben * hoogteRibben**2) / 12 + \
                             oppervlakteRibben * ((hoogteZwaartepuntRibben - gemeenZwaartepunt) ** 2)
    else:
        momentOfInertiaRib = 0

    # --- 6. Traagheidsmoment plaat (Eigen traagheid + Steiner) ---
    momentOfInertiaPlate = (breedteVanHetGeheel * finaleDiktePlaat**3) / 12 + \
                           oppervlaktePlaat * ((hoogteZwaartepuntPlaat - gemeenZwaartepunt) ** 2)
    
    # --- 6a. Traagheidsmoment Zijplaat (Eigen traagheid + Steiner) ---
    momentOfInertiaSideplate = (finaleDiktePlaat * (diameterVanDeAfronding - finaleDiktePlaat)**3)/12 + oppervlakteZijplaat * ((hoogteZwaartepuntZijplaat - gemeenZwaartepunt)**2)

    # --- 7. Totaal (Traagheidsmoment op locatie X) ---
    totalMomentOfInertia =  momentOfInertiaRib + momentOfInertiaPlate + momentOfInertiaSideplate

    # --- Opslaan in de lijsten voor verdere berekeningen ---
    X_values.append(X)
    I_values.append(totalMomentOfInertia)

    # ---- UITERSTE VEZELS BEPALEN ----
    y_bottom = 0  # referentie = onderkant plaat

    y_top_plate = finaleDiktePlaat

    # Als rib aanwezig is, kan deze hoger uitsteken dan de plaat
    if oppervlakteRibben > 0:
        y_top_rib = hoogteZwaartepuntRibben + hoogteRibben / 2
    else:
        y_top_rib = y_top_plate

    y_top = max(y_top_plate, y_top_rib)
    y_top = diameterVanDeAfronding

    # Afstanden tot neutrale as
    c_top = y_top - gemeenZwaartepunt
    c_bottom = gemeenZwaartepunt - y_bottom

    # Opslaan
    c_top_values.append(c_top)
    c_bottom_values.append(c_bottom)


# --- PLOT CODE ---
plt.figure(figsize=(10, 5))
plt.plot(X_values, I_values, label="Traagheidsmoment $I_{xx}$")

plt.title("Verloop van het Traagheidsmoment over de lengte van de plaat")
plt.xlabel("Afstand X [mm]")
plt.ylabel("Traagheidsmoment $I$ [mm$^4$]")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()









# ----- HIERONDER WORDEN DE KRACHTENINWERKINGEN EN DE LOCATIE HIERVAN BEPAALD -----

# ----- AANNAMES -----
# het is een statische situatie
# doorbuiging loodrecht op het tandvalk word onderzocht
# krachten met de veren worden bepaald met onderandere de push for movement force in de datasheet van de guidetrolley


aangrijpingspuntTandwiel = lengteVanHetPlatteDeel/2 # mm,  deze locatie kan gebruikt worden voor verschillende punten te onderzoekne van de plaat
krachtAangrijpingspunt = 2 * veerkracht # N de kracht moet nog uitgezocht worden

#via moment rond punt 2 kan kracht 1 en kracht 2 berekend worden
resultKracht2 = krachtAangrijpingspunt * aangrijpingspuntTandwiel / lengteVanHetPlatteDeel #N, moment rond 1
resultKracht1 = krachtAangrijpingspunt - resultKracht2 #N, krachten evenwicht


# de krachten resulterend door de spanning van de tandriem over de structuur moet ook zeker inrekening gebracht worden
# omdat deze tandriem stationair is zal de kracht van boven en vanonder even groot zijn namelijk F_Spanning. de resulterende kracht is dus 
# 2 keer de spanning. met als aangrijpingspunt de helft van afrondingsdiameter

SpankrachtResultante = 2 * F_S
spankrachtAangrijpingspunt = diameterVanDeAfronding / 2

# deze kracht kan verplaatst worden naar het midden van de plaat zelf namelijk dikte van de plaat delen door 2. echter zal hierdoor een inter moment optreden

internMomentDoorSpankracht = (spankrachtAangrijpingspunt - (finaleDiktePlaat/2)) * SpankrachtResultante
# deze kan aan beiden zijkanten gebruikt worden met een ander teken gewoon




# ----- hieronder volgt een CHAT GPT versie van mijn V(x) diagram -----



# ---- Discretisatie ----
interval = 1  # mm
X_values = np.arange(0, lengteVanHetPlatteDeel + interval, interval)

V_values = []

# ---- 1) DATA (voor integratie later) ----
for X in X_values:
    if X < aangrijpingspuntTandwiel:
        V = resultKracht1
    else:
        V = resultKracht1 - krachtAangrijpingspunt
    V_values.append(V)

# ---- 2) PLOT (mooie sprongen) ----
V_plot_x = [0, 0]                   # start op X-as, dan sprong omhoog
V_plot_y = [0, resultKracht1]

# horizontale stukken uit V_values
for i in range(len(X_values)):
    V_plot_x.append(X_values[i])
    V_plot_y.append(V_values[i])

# sprong terug naar 0 op het einde (rechter steun)
V_plot_x.append(lengteVanHetPlatteDeel)
V_plot_y.append(0)

plt.figure(figsize=(10,5))
plt.plot(V_plot_x, V_plot_y)

plt.title("Dwarskracht V(x) met correcte sprongen")
plt.xlabel("Afstand X [mm]")
plt.ylabel("Dwarskracht V [N]")

plt.grid(True)
plt.show()

# ---- Tijdelijk momentdiagram M(x) uit V(x) ----

M_values = [0]  # Start: M(0) = 0 (tijdelijk)

for i in range(len(X_values) - 1):
    dx = X_values[i+1] - X_values[i]  # mm

    # trapeziumregel: M(i+1) = M(i) + gemiddelde V * dx
    dM = 0.5 * (V_values[i] + V_values[i+1]) * dx  # N*mm
    M_values.append(M_values[-1] + dM)

# =========================================================
# ---- Interne momenten door spankracht toevoegen ----
# Linker uiteinde:  -internMomentDoorSpankracht
# Rechter uiteinde: +internMomentDoorSpankracht
# =========================================================

internMomentDoorSpankracht = (spankrachtAangrijpingspunt - (finaleDiktePlaat/2)) * SpankrachtResultante  # N*mm

# Kopie maken zodat je het tijdelijke diagram behoudt
M_metInterneMomenten = M_values.copy()

# 1) Sprong op x=0: momentdiagram verschuift overal omlaag
for i in range(len(M_metInterneMomenten)):
    M_metInterneMomenten[i] += -internMomentDoorSpankracht

# 2) Sprong op x=L: terug omhoog met dezelfde grootte (enkel om zichtbaar te tekenen)
# We maken een extra punt net na L om de verticale sprong te tonen
epsilon = 1e-6  # mm
X_plot_M = list(X_values) + [lengteVanHetPlatteDeel + epsilon]
M_plot_M = list(M_metInterneMomenten) + [M_metInterneMomenten[-1] + internMomentDoorSpankracht]

# ---- Plot M(x) ----
plt.figure(figsize=(10,5))
plt.plot(X_plot_M, M_plot_M)

plt.title("Buigmoment M(x) (Z-belasting + interne eindmomenten door spankracht)")
plt.xlabel("Afstand X [mm]")
plt.ylabel("Buigmoment M [N·mm]")

plt.grid(True)
plt.show()

print("internMomentDoorSpankracht =", internMomentDoorSpankracht, "N·mm")
print("M_tijdelijk(0) =", M_values[0], "N·mm")
print("M_tijdelijk(L) =", M_values[-1], "N·mm (moet ~0 zijn bij scharnier/rol zonder eindmomenten)")
print("M_metInterneMomenten(0) =", M_metInterneMomenten[0], "N·mm (zou ~ -internMomentDoorSpankracht zijn)")
print("M_metInterneMomenten(L) =", M_metInterneMomenten[-1], "N·mm (voor de sprong op L)")







# ============================================================
# BUIGSPANNING UIT M(x), I(x), c_top(x), c_bottom(x)
# Alleen Z-buiging, geen axiale kracht N/A
# Units:
#   M in N*mm, I in mm^4, c in mm  =>  sigma in N/mm^2 = MPa
# Vereist (zelfde lengte):
#   X_values, M_values, I_values, c_top_values, c_bottom_values
# ============================================================

# ---- omzetten naar numpy (makkelijk rekenen) ----
X = np.array(X_values, dtype=float)
M = np.array(M_values, dtype=float)
I = np.array(I_values, dtype=float)
c_top = np.array(c_top_values, dtype=float)
c_bottom = np.array(c_bottom_values, dtype=float)

# ---- buigspanningen (teken volgens jouw conventie) ----
sigma_top = (M * c_top) / I          # N/mm² (MPa)
sigma_bottom = -(M * c_bottom) / I   # N/mm² (MPa)  -> minteken omdat onderkant tegengesteld

# ---- kritische spanning (grootste absolute waarde) ----
sigma_crit = np.maximum(np.abs(sigma_top), np.abs(sigma_bottom))

# ---- maximum zoeken ----
indexMax = int(np.argmax(sigma_crit))
X_max = X[indexMax]
sigma_max = float(sigma_crit[indexMax])  # N/mm² = MPa

print(f"Max spanning = {sigma_max:.2f} N/mm² (= {sigma_max:.2f} MPa) op X = {X_max:.0f} mm")

# ---- plot ----
plt.figure(figsize=(10,5))
plt.plot(X, sigma_top, label="σ_top")
plt.plot(X, sigma_bottom, label="σ_bottom")
plt.plot(X, sigma_crit, "--", label="σ_crit")

# maximum aanduiden
plt.scatter([X_max], [sigma_max], zorder=5)
plt.annotate(
    f"max = {sigma_max:.1f} N/mm²\n= {sigma_max:.1f} MPa\nX = {X_max:.0f} mm",
    xy=(X_max, sigma_max),
    xytext=(10, 10),
    textcoords="offset points"
)

plt.title("Buigspanningen over de lengte (alleen Z-buiging)")
plt.xlabel("X [mm]")
plt.ylabel("Spanning [N/mm²] (= MPa)")
plt.grid(True)
plt.legend()
plt.show()






# ============================================================
# DOORBUIGING BEREKENEN UIT M(x) EN I(x)
# EI w''(x) = M(x)
# Numerieke integratie (2x trapeziumregel)
# Units:
#   M  -> N·mm
#   I  -> mm^4
#   E  -> N/mm^2     Al eerder gedefinieerd
#   w  -> mm
# ============================================================



# -------- Data omzetten naar numpy --------
X = np.array(X_values, dtype=float)
dx = X[1] - X[0]   # mm (bij jou 1 mm)

# Gebruik het correcte momentdiagram
M = np.array(M_metInterneMomenten, dtype=float)   # of M_values indien gewenst
I = np.array(I_values, dtype=float)

# -------- Stap 1: kromming --------
# kappa = w'' = M / (E I)
kappa = M / (E * I)   # 1/mm

# -------- Stap 2: helling θ(x) --------
theta = np.zeros_like(X)   # w'(x)

for i in range(len(X)-1):
    theta[i+1] = theta[i] + 0.5 * (kappa[i] + kappa[i+1]) * dx

# -------- Stap 3: doorbuiging w(x) --------
w = np.zeros_like(X)

for i in range(len(X)-1):
    w[i+1] = w[i] + 0.5 * (theta[i] + theta[i+1]) * dx

# -------- Randvoorwaarden (simply supported) --------
# w(0) = 0 is al voldaan
# Corrigeer zodat ook w(L) = 0
w = w - (w[-1] / X[-1]) * X

# -------- Resultaten --------
w_max = np.max(np.abs(w))
x_wmax = X[np.argmax(np.abs(w))]

print(f"Maximale doorbuiging = {w_max:.3f} mm op X = {x_wmax:.0f} mm")

# -------- Plot --------
plt.figure(figsize=(10,5))
plt.plot(X, w)
plt.title("Doorbuiging w(x)")
plt.xlabel("X [mm]")
plt.ylabel("w [mm]")
plt.grid(True)
plt.show()