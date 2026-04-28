import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from A_tandriem_M0_WQB1 import diameter_tandenwiel, gekozeBreedteFactor, gekozeModulus, afrondingsFactor, veerkracht, krachtOpTandenwiel, hoek_ingrijping



print("#-----------------#")
print("")
print("Hieronder volgen de waardes van file B_tandwielAs_M0_WQA2")
print("")
print("")
print("")

maxSnelheidRobot = 1.5 # m/s
diameterTandwiel = diameter_tandenwiel #m door 220 te kiezen is een modulus van 10 haalbaar 
#gekozen materiaal zijn eigenschappen zijn hieronder gegeven. die zijn nodig voor de minimale diameter te bepalen
#gekozen materiaal is "staal" idk yet 
sigma_bToelaatbaar = 275 #N/mm²
tau_tToelaatbaar = 160 #N/mm²
phi = sigma_bToelaatbaar/tau_tToelaatbaar # dit staat op pagina 367 aanname is dat de torsie statische of zwellend is en de buiging wisselend




# MOGELIJK 220 op M10 haalbaar te maken voor tandriem compatibiliteit

maxRotatiesnelheid = maxSnelheidRobot / (math.pi * diameterTandwiel) # rotatiesnelheid in omwentelingen per seconde
print(f"Maximale rotatiesnelheid: {maxRotatiesnelheid:.2f} omwentelingen per seconde")

spelingTussenTandwielen = 50 # mm, de afstand tussende 2 tandwielen op de ene as
breedteTandwiel = gekozeModulus*gekozeBreedteFactor + afrondingsFactor # mm, de breedte van 1 tandwiel volgens de berekening in MO_WQB1
spelingTotBovensteLager = 5 # mm, arbitrair gekozen
spelingTotOndersteLager = 2 # mm, arbitrair gekozen
AfstandTussenLagers = 2*breedteTandwiel + spelingTussenTandwielen + spelingTotBovensteLager + spelingTotOndersteLager # m
print(f"Afstand tussen de lagers: {AfstandTussenLagers:.3f} mm")


krachtOpAs_Xas = krachtOpTandenwiel * math.cos(math.radians(hoek_ingrijping)) #N
krachtOpAs_Yas = 2 * veerkracht + krachtOpTandenwiel * math.sin(math.radians(hoek_ingrijping)) #N

totaleKrachtOpAs = math.sqrt(krachtOpAs_Xas **2 + krachtOpAs_Yas**2) # N

print("")
print("totale kracht op de as is ", totaleKrachtOpAs, " N")


#het ingrijpingspunt is belangrijk om de maxiamel diameter te bepalen, aangezien deze invloed heeft op de momenten etc.
#Aangezien er 2 ingrijpingspunten zijn gaan we gwn ze beiden onderzoeken en dan zien welke een dikkere minimale diameter vraagt

#het torsie gedeelte is voor elk tandwile gelijk (uitgangspunt torsie niet)
Torsie = krachtOpAs_Xas * diameter_tandenwiel/2 # Nm

#buigmoment is dus wel afhankelijk van tandwiel. we pakken hier dus buigmoment Boven en Onder

#de onderste lager word bezien als nul punt waar de bovenste lager gezien word als 'afstand tussen lagers'
aangrijpingspuntSituatie1 = AfstandTussenLagers - spelingTotBovensteLager - breedteTandwiel/2 #situatie 1 is waar het bovenste tandwiel werking heeft
aangrijpingspuntSituatie2  = spelingTotOndersteLager + breedteTandwiel/2 #situatie 2 is waar het onderste tandwiel werking heeft

krachtBovensteLagerSit1 = aangrijpingspuntSituatie1 * krachtOpAs_Yas / AfstandTussenLagers
krachtBovensteLagerSit2 = aangrijpingspuntSituatie2 * krachtOpAs_Yas / AfstandTussenLagers
print(f"Kracht op bovenste lager - Situatie 1: {krachtBovensteLagerSit1:.2f} N")
print(f"Kracht op bovenste lager - Situatie 2: {krachtBovensteLagerSit2:.2f} N")

krachtOndersteLagerSit1 = krachtOpAs_Yas - krachtBovensteLagerSit1
krachtOndersteLagerSit2 = krachtOpAs_Yas - krachtBovensteLagerSit2




# ===========================
# V(x) en M(x) voor puntlast op simpel opgelegde as
# x in meter, V in N, M in N*m
# ===========================

def bereken_V_en_M(L_m, a_m, P_N, R0_N, interval_m=0.001):
    """
    L_m   : afstand tussen lagers [m]
    a_m   : positie puntlast vanaf linker lager (x=0) [m]
    P_N   : puntlast (verticale kracht op as) [N]
    R0_N  : reactie linker lager (onderste lager, x=0) [N]
    interval_m : discretisatie stap [m]
    """

    # X-as in meters
    X_values = np.arange(0.0, L_m + interval_m, interval_m)

    # 1) V(x) data (stukgewijs constant)
    V_values = []
    for x in X_values:
        if x < a_m:
            V = R0_N
        else:
            V = R0_N - P_N
        V_values.append(V)
    V_values = np.array(V_values)

    # 2) "mooie sprongen" plotdata voor V(x)
    V_plot_x = [0.0, 0.0]         # start op as, sprong omhoog
    V_plot_y = [0.0, R0_N]

    for i in range(len(X_values)):
        V_plot_x.append(float(X_values[i]))
        V_plot_y.append(float(V_values[i]))

    # sprong terug naar 0 op het einde (rechter lager)
    V_plot_x.append(L_m)
    V_plot_y.append(0.0)

    # 3) M(x) via integratie van V(x) (trapeziumregel), units: N*m
    M_values = [0.0]  # M(0)=0
    for i in range(len(X_values) - 1):
        dx = X_values[i+1] - X_values[i]  # m
        dM = 0.5 * (V_values[i] + V_values[i+1]) * dx  # (N)*m = N*m
        M_values.append(M_values[-1] + dM)
    M_values = np.array(M_values)

    return X_values, V_values, V_plot_x, V_plot_y, M_values


# ===========================
# RUN: situatie 1 en 2
# ===========================

# --- Conversies mm -> m ---
L_m  = AfstandTussenLagers / 1000.0
a1_m = aangrijpingspuntSituatie1 / 1000.0
a2_m = aangrijpingspuntSituatie2 / 1000.0

P_N = krachtOpAs_Yas  # verticale puntlast op as [N]

R0_1 = krachtOndersteLagerSit1
R0_2 = krachtOndersteLagerSit2

interval_m = 0.001  # 1 mm


# =========================================================
# ---- Situatie 1 ----
# =========================================================
X1, V1, V1x_plot, V1y_plot, M1 = bereken_V_en_M(L_m, a1_m, P_N, R0_1, interval_m)

M1_max = np.max(np.abs(M1))
index_M1_max = np.argmax(np.abs(M1))
x_M1_max = X1[index_M1_max]

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8), sharex=True)

ax1.plot(V1x_plot, V1y_plot)
ax1.set_title("Situatie 1 - Dwarskracht V(x)")
ax1.set_ylabel("V [N]")
ax1.grid(True)

ax2.plot(X1, M1)
ax2.set_title("Situatie 1 - Buigmoment M(x)")
ax2.set_xlabel("x [m]")
ax2.set_ylabel("M [N·m]")
ax2.grid(True)

plt.tight_layout()
plt.show()

print("\n--- Situatie 1 ---")
print("Maximaal buigmoment |M|max =", M1_max, "N·m")
print("Locatie M_max =", x_M1_max, "m")


# =========================================================
# ---- Situatie 2 ----
# =========================================================
X2, V2, V2x_plot, V2y_plot, M2 = bereken_V_en_M(L_m, a2_m, P_N, R0_2, interval_m)

M2_max = np.max(np.abs(M2))
index_M2_max = np.argmax(np.abs(M2))
x_M2_max = X2[index_M2_max]

fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(10,8), sharex=True)

ax3.plot(V2x_plot, V2y_plot)
ax3.set_title("Situatie 2 - Dwarskracht V(x)")
ax3.set_ylabel("V [N]")
ax3.grid(True)

ax4.plot(X2, M2)
ax4.set_title("Situatie 2 - Buigmoment M(x)")
ax4.set_xlabel("x [m]")
ax4.set_ylabel("M [N·m]")
ax4.grid(True)

plt.tight_layout()
plt.show()

print("\n--- Situatie 2 ---")
print("Maximaal buigmoment |M|max =", M2_max, "N·m")
print("Locatie M_max =", x_M2_max, "m")




# ===========================
# Kritische situatie bepalen
# ===========================

if M1_max >= M2_max:
    situatie_kritisch = 1
    M_buig_kritisch = M1_max
    x_M_kritisch = x_M1_max
else:
    situatie_kritisch = 2
    M_buig_kritisch = M2_max
    x_M_kritisch = x_M2_max

print("\n=== Kritische situatie ===")
print(f"Maximaal buigmoment komt voor in situatie {situatie_kritisch}")
print(f"|M|max = {M_buig_kritisch:.6g} N·m bij x = {x_M_kritisch:.6g} m")

# Vanaf hier kan je in je dimensionering gewoon deze gebruiken:
# M_buig_kritisch  (N·m)
# x_M_kritisch     (m)



#om de minimale diameter tebepalen hebben we eerst M_v nodig deze word volgens formule 11.7 als volgt bepaald

M_v = math.sqrt(M_buig_kritisch**2 + 0.75 * (((sigma_bToelaatbaar * Torsie)/(phi * tau_tToelaatbaar))**2)) #Nm
M_v_mm = M_v * 1000 #Nmm

minimaleDiameter = (((32*M_v_mm)/(math.pi * sigma_bToelaatbaar))**(1/3)) # mm
print("")
print("de minimale diameter die de aandrijfas nodig heeft is", minimaleDiameter, " mm")