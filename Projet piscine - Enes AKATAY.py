import os
from datetime import datetime

commande = ''

param = {
    'bdd': [(1, 3, 10, '2025-01-01'), (2, 1, 13, '2025-01-02'), (3, 2, 6, '2025-01-03'), (3, 1, 8, '2025-01-04')],
    'nages': [(1, "Brasse"), (2, "Dos"), (3, "Crawl")],
    'nageurs': [(1, "Pierre"), (2, "Paul"), (3, "Léa")]
}

def reset(param):
    '''réinitialise la bdd'''
    param.clear()
    param['bdd'] = []
    param['nages'] = []
    param['nageurs'] = []

def get_str_from_num_in_list(num, liste):
    """Return str from num into liste"""
    for elt in liste:
        if elt[0] == num:
            return elt[1]
    return "unknown"

def cmd_individu(param):
    """Ajoute un nouveau nageur"""
    prénom = input("Prénom du nouveau nageur ? ")
    id = len(param['nageurs']) + 1
    param['nageurs'].append((id, prénom))
    print(param['nageurs'])

def cmd_nouvelle_nage(param):
    """Ajoute une nouvelle nage au logiciel"""
    nage = input("Quelle nage enregistrer ? ")
    id = len(param['nages']) + 1
    param['nages'].append((id, nage))
    print(param['nages'])

def cmd_ajout(param):
    """Ajoute un évènement à la liste"""
    for elt in param['nageurs']:
        print(f"{elt[0]:5} : {elt[1]}")
    a = int(input("Nageur n° ? "))
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    b = int(input("Nage n° ? "))
    c = int(input("Combien de longueurs ? "))
    date_str = input("Date de l'événement (AAAA-MM-JJ) ? ")
    try:
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("La date est invalide. Format attendu : YYYY-MM-DD")
        return
    
    param['bdd'].append((a, b, c, event_date))
    print("Ajout validé !")

def cmd_liste(param):
    """Affiche toutes les performances des nageurs"""
    print("\nPrénom      |  nage   |  longueur |   Date")
    print("------------------------------------------")
    for elt in param['bdd']:
        nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
        nage = get_str_from_num_in_list(elt[1], param['nages'])
        print(f" {nageur:11}| {nage:8}|  {elt[2]}  |{elt[3]}")
    
    if param['bdd']:
        longueurs = [elt[2] for elt in param['bdd']]
        max_performance = max(longueurs)
        min_performance = min(longueurs)
        average_performance = sum(longueurs) / len(longueurs)
        print(f"\nMax performance: {max_performance} Longueur")
        print(f"Min performance: {min_performance} Longueur")
        print(f"Moyenne: {average_performance:.2f} Longueur")

def cmd_nageur(param):
    """Affiche toutes les performances d'un nageur avec statistiques"""
    for elt in param['nageurs']:
        print(f"{elt[0]:5} : {elt[1]}")
    tmp = int(input("Quel numéro de nageur ? "))
    print(f"\nPerformances de {get_str_from_num_in_list(tmp, param['nageurs'])}")
    print("  nage   |  longueur |   Date")
    print("-----------------------------")
    
    performances = [elt for elt in param['bdd'] if elt[0] == tmp]
    for elt in performances:
        nage = get_str_from_num_in_list(elt[1], param['nages'])
        print(f" {nage:8}|  {elt[2]}     | {elt[3]}")
    
    if performances:
        longueurs = [elt[2] for elt in performances]
        max_performance = max(longueurs)
        min_performance = min(longueurs)
        average_performance = sum(longueurs) / len(longueurs)
        print(f"\nMax performance: {max_performance} Longueur")
        print(f"Min performance: {min_performance} Longueur")
        print(f"Moyenne: {average_performance:.2f} Longueur")

def cmd_nage(param):
    """Affiche toutes les performances suivant une nage donnée avec statistiques"""
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    tmp = int(input("Quel numéro de nage ? "))
    print(f"\nPerformances pour la nage {get_str_from_num_in_list(tmp, param['nages'])}")
    print(" Nageur     |  longueur |   Date")
    print("------------------------------")
    
    performances = [elt for elt in param['bdd'] if elt[1] == tmp]
    for elt in performances:
        nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
        print(f" {nageur:11}|  {elt[2]}     | {elt[3]}")
    
    if performances:
        longueurs = [elt[2] for elt in performances]
        max_performance = max(longueurs)
        min_performance = min(longueurs)
        average_performance = sum(longueurs) / len(longueurs)
        print(f"\nMax performance: {max_performance} Longueur")
        print(f"Min performance: {min_performance} Longueur")
        print(f"Moyenne: {average_performance:.2f} Longueur")

def cmd_exit(param):
    tmp = input("En êtes-vous sûr ? (o)ui/(n)on ")
    if tmp == 'o':
        cmd_save(param, 'save.backup')
        return False
    else:
        return True

def cmd_save(param, filename='save.csv'):
    '''sauvegarde complète de la BDD'''
    fichier = open(filename, 'w')
    fichier.write('@ nageurs\n')
    for elt in param['nageurs']:
        fichier.write(str(elt[0]) + ',' + str(elt[1]) + "\n")
    fichier.write('@ nages\n')
    for elt in param['nages']:
        fichier.write(str(elt[0]) + ',' + str(elt[1]) + "\n")
    fichier.write('@ bdd\n')
    for elt in param['bdd']:
        fichier.write(f"{elt[0]},{elt[1]},{elt[2]},{elt[3]}\n")
    fichier.close()

def cmd_load(param, filename='save.csv'):
    '''chargement complet la BDD avec réinitialisation'''
    reset(param)
    key = ''
    fichier = open(filename, 'r')
    for line in fichier:
        line.strip()
        if line[-1] == '\n':
            line = line[:-1]
        if line[0] == '#':
            continue
        if line[0] == '@':
            key = line[2:]
            continue
        if key == '':
            continue
        tmp = line.split(',')
        if key == 'bdd':
            tmp[0] = int(tmp[0])
            tmp[1] = int(tmp[1])
            tmp[2] = int(tmp[2])
            tmp[3] = datetime.strptime(tmp[3], '%Y-%m-%d').date()
        if key == 'nages' or key == 'nageurs':
            tmp[0] = int(tmp[0])
        param[key].append(tuple(tmp))
    fichier.close()

def get_cmd():
    '''Traitement de la commande d'entrée'''
    msg = input("\nSaisissez un chiffre pour réaliser une action. \n1 -> ajouter une performance. \n2 -> ajouter un individu. \n3 -> ajouter une nouvelle nage. \n4 -> lister toutes les performances \n5 -> lister les performances d'un nageur. \n6 -> lister tous les nageurs pratiquant une nage. \n7 -> sauvegarder les données utilisateurs. \n8 -> charger les données utilisateurs. \n0 -> quitter le logiciel. \nQue voulez-vous faire ? ")
    msg = msg.lower()
    return msg

# Programme principal
isAlive = True
if os.path.exists('save.backup'):
    cmd_load(param, 'save.backup')
while isAlive:
    commande = get_cmd()

    if commande == '1':
        cmd_ajout(param)
        continue
    if commande == '2':
        cmd_individu(param)
        continue

    if commande == '3':
        cmd_nouvelle_nage(param)
        continue

    if commande == '4':
        cmd_liste(param)
        continue

    if commande == '5':
        cmd_nageur(param)
        continue

    if commande == '6':
        cmd_nage(param)
        continue

    if commande == '7':
        cmd_save(param)
        continue

    if commande == '8':
        cmd_load(param)
        continue

    if commande == '9':
        isAlive = cmd_exit(param)
        continue

    print(f"Commande {commande} inconnue, veuillez réessayer")