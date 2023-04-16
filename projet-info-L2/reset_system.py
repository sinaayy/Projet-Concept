from classes import *
from save_read_objects import save_objects

def reset_system():
    p11 = Pompe("P11")
    p12 = Pompe("P12", "arrêt")
    p21 = Pompe("P21")
    p22 = Pompe("P22", "arrêt")
    p31 = Pompe("P31")
    p32 = Pompe("P32", "arrêt")

    t1 = Tank("Tank1", p11, p12)
    t2 = Tank("Tank2", p21, p22)
    t3 = Tank("Tank3", p31, p32)

    m1 = Moteur("M1")
    m2 = Moteur("M2")
    m3 = Moteur("M3")

    vt12 = Vanne_tank(t1, t2, "VT12")
    vt23 = Vanne_tank(t2, t3, "VT23")

    v12 = Vanne_moteur(t1, m2, "V12")
    v23 = Vanne_moteur(t2, m3, "V23")
    v13 = Vanne_moteur(t3, m1, "V13")

    pompes = [p11, p12, p21, p22, p31, p32]
    tanks = [t1, t2, t3]
    moteurs = [m1, m2, m3]
    vannes_tank = [vt12, vt23]
    vannes_moteur = [v12, v23, v13]

    save_objects(pompes, "objects/pompes")
    save_objects(tanks, "objects/tanks")
    save_objects(moteurs, "objects/moteurs")
    save_objects(vannes_tank, "objects/vannes_tank")
    save_objects(vannes_moteur, "objects/vannes_moteur")