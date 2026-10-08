TEAMS = {
    1: "Barcelona",
    2: "Real Madrid",
    3: "Man United",
    4: "Chelsea",
    5: "PSG",
    6: "Juventus",
}


ROSTERS = {
    1: [  # Barcelona
        "Lionel Messi", "Neymar", "Ousmane Dembele", "Dani Alves",
        "Zlatan Ibrahimovic", "Arthur", "Miralem Pjanic", "Arturo Vidal",
        "Joao Cancelo", "Cesc Fabregas", "Marcos Alonso", "Joao Felix",
        "Pedro", "Pierre-Emerick Aubameyang", "Andreas Christensen",
        "Samuel Eto'o", "Gerard Pique", "Alexis Sanchez", "Memphis Depay",
        "Marcus Rashford",
    ],
    2: [  # Real Madrid
        "Kylian Mbappe", "Sergio Ramos", "Achraf Hakimi", "Keylor Navas",
        "David Beckham", "Angel Di Maria", "Eden Hazard", "Thibaut Courtois",
        "Mateo Kovacic", "Antonio Rudiger", "Arjen Robben",
        "Kepa Arrizabalaga", "Cristiano Ronaldo", "Gonzalo Higuain",
        "Alvaro Morata", "Sami Khedira", "Fabio Cannavaro", "Raphael Varane",
        "Casemiro",
    ],
    3: [  # Man United
        "Zlatan Ibrahimovic", "David Beckham", "Angel Di Maria",
        "Cristiano Ronaldo", "Edinson Cavani", "Ander Herrera",
        "Raphael Varane", "Casemiro", "Romelu Lukaku", "Nemanja Matic",
        "Juan Mata", "Radamel Falcao", "Mason Mount", "Paul Pogba",
        "Patrice Evra", "Gerard Pique", "Alexis Sanchez", "Memphis Depay",
        "Marcus Rashford",
    ],
    4: [  # Chelsea
        "Cesc Fabregas", "Marcos Alonso", "Joao Felix", "Pedro",
        "Pierre-Emerick Aubameyang", "Andreas Christensen", "Samuel Eto'o",
        "Thiago Silva", "David Luiz", "Eden Hazard", "Thibaut Courtois",
        "Mateo Kovacic", "Antonio Rudiger", "Arjen Robben",
        "Kepa Arrizabalaga", "Gonzalo Higuain", "Alvaro Morata",
        "Romelu Lukaku", "Nemanja Matic", "Juan Mata", "Radamel Falcao",
        "Mason Mount", "Juan Cuadrado", "Adrian Mutu",
    ],
    5: [  # PSG
         "Lionel Messi", "Neymar", "Ousmane Dembele", "Dani Alves",
        "Zlatan Ibrahimovic", "Kylian Mbappe", "Sergio Ramos",
        "Achraf Hakimi", "Keylor Navas", "David Beckham", "Angel Di Maria",
        "Thiago Silva", "David Luiz", "Edinson Cavani", "Ander Herrera",
        "Adrien Rabiot", "Blaise Matuidi", "Gianluigi Buffon", "Moise Kean",
    ],
    6: [  # Juventus
        "Dani Alves", "Zlatan Ibrahimovic", "Arthur", "Miralem Pjanic",
        "Arturo Vidal", "Joao Cancelo", "Cristiano Ronaldo",
        "Gonzalo Higuain", "Alvaro Morata", "Sami Khedira",
        "Fabio Cannavaro", "Angel Di Maria", "Paul Pogba", "Patrice Evra",
        "Juan Cuadrado", "Adrian Mutu", "Adrien Rabiot", "Blaise Matuidi",
        "Gianluigi Buffon", "Moise Kean",
    ],
}


def clean(text):
    return " ".join(text.split()).lower()


#для каждой команды множество имён в очищенном виде
SETS = {team: {clean(p) for p in players} 
        for team, players in ROSTERS.items()}


def check_player(text, team_a, team_b, used):
    name = clean(text)
    if name in SETS[team_a] and name in SETS[team_b]:
        if name in used:
            return "used", name
        return "ok", name
    return "no", None


#for i in range(1, 7):
    #for j in range(1, 7):
        #if i != j:
            #print(f'{i} x {j} : {sorted(SETS[i] & SETS[j])}')