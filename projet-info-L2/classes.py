class Pompe:

    def __init__(self, name, etat="marche"):
        self.name = name
        self.etat = etat
    
    def __str__(self):
        return f"{self.name} : {self.etat}"

    def changer_etat(self):
        self.etat = "marche" if self.etat == "arrêt" else "arrêt"

    def panne_depanne(self):
        if self.name[-1] == "1":
            self.etat = "panne" if self.etat != "panne" else "marche"
        else:
            self.etat = "panne" if self.etat != "panne" else "arrêt"


class Tank:

    def __init__(self, name, first_pompe, second_pompe, etat="plein"):
        self.name = name
        self.etat = etat
        self.first_pompe = first_pompe
        self.second_pompe = second_pompe

    def __str__(self):
        return f"{self.name} : {self.etat}"

    def is_empty(self):
        return self.etat == "vide"
    
    def remplir_vider(self):
        self.etat = "plein" if self.etat != "plein" else "vide"

    def is_first_pompe_working(self):
        return self.first_pompe.etat == "marche"

    def is_second_pompe_working(self):
        return self.second_pompe.etat == "marche"

    def is_first_pompe_good(self):
        return self.first_pompe.etat != "panne"

    def is_second_pompe_good(self):
        return self.second_pompe.etat != "panne"

    def change_first_pompe_state(self):
        self.first_pompe.changer_etat() 

    def change_second_pompe_state(self):
        self.second_pompe.changer_etat() 



class Moteur:

    def __init__(self, name, etat="alimenté"):
        self.name = name
        self.etat = etat

    def __str__(self):
        return f"{self.name} : {self.etat}"

    def is_alimente(self):
        return self.etat == "alimenté"
    
    def alimente(self):
        self.etat = "alimenté"

    def non_alimente(self):
        self.etat = "non alimenté"


class Vanne:

    def __init__(self, name, etat="ouverte"):
        self.name = name
        self.etat = etat

    def __str__(self):
        return f"{self.name} : {self.etat}"

    def changer_etat(self):
        self.etat = "ouverte" if self.etat == "fermée" else "fermée" 
    
    def is_open(self):
        return self.etat == "ouverte"



class Vanne_tank(Vanne):

    def __init__(self, first_tank, second_tank, name, etat="ouverte"):
        super().__init__(name, etat)
        self.first_tank = first_tank
        self.second_tank = second_tank

    def changer_etat(self):
        super().changer_etat()
        if self.first_tank.is_empty() and not self.second_tank.is_empty():
            self.first_tank.remplir_vider()
        elif self.second_tank.is_empty() and not self.first_tank.is_empty():
            self.second_tank.remplir_vider()


class Vanne_moteur(Vanne):

    def __init__(self, tank, moteur, name, etat="ouverte"):
        super().__init__(name, etat)
        self.tank = tank
        self.moteur = moteur

