import pandas as pd

def id_dispo(id):
    users = pd.read_csv("users.csv")
    return id not in users["id"]


def add_user(nom, prenom, id, mdp):
    users = pd.read_csv("users.csv")

    new_user = {"Nom":nom, "Prénom":prenom, "id":id, "mdp":mdp}
    new_user = pd.DataFrame([new_user])

    users = pd.concat([users, new_user])
    users.to_csv("users.csv", index=False)


def find_user(id, mdp):
    users = pd.read_csv("users.csv")
    user = users[(users["id"] == id) & (users["mdp"] == mdp)]
    if not user.empty:
        user = user.iloc[0]
    return user


def find_scores_user(id):
    scores = pd.read_csv("scores.csv")
    user_scores = scores[scores["id"] == id]
    return user_scores.head()


def add_score(id, score):
    scores = pd.read_csv("scores.csv")

    new_score = {"id":id, "score":score}
    new_score = pd.DataFrame([new_score])

    scores = pd.concat([scores, new_score])
    scores.sort_values(by="score", ascending=False, inplace=True)
    scores.to_csv("scores.csv", index=False)

def save_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def read_score():
    with open("score.txt", "r") as file:
        return int(file.read())