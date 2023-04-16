import streamlit as st

from classes import *
from users_gestion import *
from save_read_objects import save_objects, read_objects
from reset_system import reset_system
from exercices_pilote import config_exercice


st.title("Simulateur de système de carburant")

## Partie inscription

sidebar = st.sidebar
sidebar.header("Inscription")

new_nom = sidebar.text_input("Nom")
new_prenom = sidebar.text_input("Prénom")
new_id = sidebar.text_input("Identifiant", key=1)
new_mdp = sidebar.text_input("Mot de passe", key=1)

inscription = sidebar.button("Add user")

infos_user = [new_nom, new_prenom, new_id, new_mdp]

if inscription and id_dispo(new_id) and all(infos_user):
    add_user(*infos_user)
    sidebar.markdown("Votre identifiants ont été enregistrés avec succès.")



st.header("User")

identification = st.checkbox("S'identifier")
score = read_score()
in_exercise = False

## Partie connexion

if identification:
    col1, col2 = st.columns(2)

    id = col1.text_input("Identifiant", key=2)
    mdp = col2.text_input("Mot de passe", key=2)

        
    user = find_user(id, mdp)
    if not user.empty:
        st.write("*Meilleurs scores*")
        st.write(find_scores_user(id))
        in_exercise = True

        button = st.button("Commencer l'exercice")

        if button:
            config_exercice()
            score = 10
            save_score(score)

else:
    button = st.button("Commencer entrainement")
    if button:
        reset_system()



### Récupération de la configuration du système

pompes = read_objects("objects/pompes")
tanks = read_objects("objects/tanks")
moteurs = read_objects("objects/moteurs")
vannes_tank = read_objects("objects/vannes_tank")
vannes_moteur = read_objects("objects/vannes_moteur")

p11, p12, p21, p22, p31, p32 = pompes
t1, t2, t3 = tanks
m1, m2, m3 = moteurs
vt12, vt23 = vannes_tank
v12, v23, v13 = vannes_moteur

t1.first_pompe, t1.second_pompe = p11, p12
t2.first_pompe, t2.second_pompe = p21, p22
t3.first_pompe, t3.second_pompe = p31, p32

vt12.first_tank, vt12.second_tank = t1, t2
vt23.first_tank, vt23.second_tank = t2, t3

v12.tank, v12.moteur = t1, m2
v23.tank, v23.moteur = t2, m3
v13.tank, v13.moteur = t3, m1



st.header("Tableau de bord")

col1, _, col2 = st.columns(3)
vt12_click = col1.button("VT12")
vt23_click = col2.button("VT23")

col1, col2, col3 = st.columns(3)
p12_click = col1.button("P12", key=1)
p22_click = col2.button("P22", key=1)
p32_click = col3.button("P32", key=1)

col1, col2, col3 = st.columns(3)
v12_click = col1.button("V12")
v13_click = col2.button("V13")
v23_click = col3.button("V23")


vannes_tank_buttons = [vt12_click, vt23_click]
vannes_moteur_button = [v12_click, v23_click, v13_click]
second_pompes_button = [p12_click, p22_click, p32_click]

if in_exercise:
    solution_exercice = {"second_pompes_index":[0], "vannes_tank_index":[1], "vannes_moteur_index":[0]}
    good = False

for i in range(len(vannes_tank_buttons)):
    if vannes_tank_buttons[i]:
        vannes_tank[i].changer_etat()
        if in_exercise and "second_pompes_index" in solution_exercice and (i not in solution_exercice["second_pompes_index"]):
            score -= 1
            good = True

for i in range(len(vannes_moteur_button)):
    if vannes_moteur_button[i]:
        vannes_moteur[i].changer_etat()
        if in_exercise and "vannes_moteur_index" in solution_exercice and (i not in solution_exercice["vannes_moteur_index"]) and not good:
            score -= 1
            good = True

second_pompes = [pompe for pompe in pompes if pompe.name[-1] == "2"]
for i in range(len(second_pompes_button)):
    if second_pompes_button[i]:
        second_pompes[i].changer_etat()
        if in_exercise and "vannes_tank_index" in solution_exercice and (i not in solution_exercice["vannes_tank_index"]) and not good:
            score -= 1

if in_exercise:
    save_score(score)


st.subheader("Créer un problème")

st.markdown("**Panne/dépanne les pompes**")
col1, col2, col3 = st.columns(3)

p11_click = col1.button("P11")
p21_click = col2.button("P21")
p31_click = col3.button("P31")

p12_click = col1.button("P12", key=2)
p22_click = col2.button("P22", key=2)
p32_click = col3.button("P32", key=2)

st.markdown("**Vider/Remplir les réservoirs**")
col1, col2, col3 = st.columns(3)

t1_click = col1.button("Tank1")
t2_click = col2.button("Tank2")
t3_click = col3.button("Tank3")


pompes_buttons = [p11_click, p12_click, p21_click, p22_click, p31_click, p32_click]
tanks_buttons = [t1_click, t2_click, t3_click]

for i in range(len(pompes_buttons)):
    if pompes_buttons[i]:
        pompes[i].panne_depanne()

for i in range(len(tanks_buttons)):
    if tanks_buttons[i]:
        tanks[i].remplir_vider()


st.header("Etat du système")

col1, col2 = st.columns(2)

col1.markdown("**Etat des pompes :**")
col1.markdown(f"{p11} - {p12}")
col1.markdown(f"{p21} - {p22}")
col1.markdown(f"{p31} - {p32}")

col2.markdown("**Etat des réservoirs :**")
col2.markdown(t1)
col2.markdown(t2)
col2.markdown(t3)

col1, col2 = st.columns(2)

col1.markdown("**Etat des vannes de moteur :**")
col1.markdown(v12)
col1.markdown(v23)
col1.markdown(v13)

col2.markdown("**Etat des vannes de réservoir :**")
col2.markdown(vt12)
col2.markdown(vt23)


st.markdown("**Etat des moteurs :**")

def alimentation_moteur(m, primary_tank, secondary_tank, vanne):
    if not primary_tank.is_empty() and (primary_tank.is_first_pompe_working() or primary_tank.is_second_pompe_working()):
        st.markdown(f"{m.name} est alimenté par {primary_tank.name}.")
        m.alimente()
    else:
        if not vanne.is_open():
            if not secondary_tank.is_empty() and (secondary_tank.is_first_pompe_working() and secondary_tank.is_second_pompe_working()):
                st.markdown(f"{m.name} est alimenté par {secondary_tank.name}")
                m.alimente()
            else:
                st.markdown(f"{m.name} n'est pas alimenté.")
                m.non_alimente()
        else:
            st.markdown(f"{m.name} n'est pas alimenté.")
            m.non_alimente()
    

alimentation_moteur(m1, t1, t3, v13)
alimentation_moteur(m2, t2, t1, v12)
alimentation_moteur(m3, t3, t2, v23)

if in_exercise:
    st.markdown(f"**Score : {score}/10**")

if all(moteur.is_alimente() for moteur in moteurs):
    st.markdown("**Le système fonctionne correctement.**")
    if in_exercise:
        add_score(id, score)
        st.markdown(f"Fin de l'entrainement {user['Nom']} {user['Prénom']}, le score est de {score}")
else:
    st.markdown("**Le système ne fonctionne pas correctement.**")
    if in_exercise and not score:
        st.markdown(f"Fin de l'entrainement {user['Nom']} {user['Prénom']}, le score est de {score}")
        



save_objects(pompes, "objects/pompes")
save_objects(tanks, "objects/tanks")
save_objects(moteurs, "objects/moteurs")
save_objects(vannes_tank, "objects/vannes_tank")
save_objects(vannes_moteur, "objects/vannes_moteur")