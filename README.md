# IUT Orsay - Portail de Gestion des Stages

Ce projet est une application web réalisée avec Django, permettant la mise en relation entre entreprises et étudiants de l'IUT. Il inclut un tableau de bord statistique pour l'administration et un workflow complet de validation des offres.

# Installation et Lancement

# 1. Installation des dépendances
```bash
pip install -r requirements.txt

# 2. Préparation de la base de données
python manage.py makemigrations
python manage.py migrate

# 3. Lancement du serveur
python manage.py runserver
Accédez au site via : http://127.0.0.1:8000/


# Comptes de Démonstration (Logs de création)
# Voici les comptes générés automatiquement pour la démonstration :

# Administrateur
admin créé : admin (MDP: admin)

# Professeur
1 Professeur créé (Login: prof_stage / MDP: profpassword)

# Élèves
Élève créé : eleve1 (MDP: eleve1password)
Élève créé : eleve2 (MDP: eleve2password)
Élève créé : eleve3 (MDP: eleve3password)
Élève créé : eleve4 (MDP: eleve4password)
Élève créé : eleve5 (MDP: eleve5password)
Élève créé : eleve6 (MDP: eleve6password)
Élève créé : eleve7 (MDP: eleve7password)
Élève créé : eleve8 (MDP: eleve8password)
Élève créé : eleve9 (MDP: eleve9password)
Élève créé : eleve10 (MDP: eleve10password)
Élève créé : eleve11 (MDP: eleve11password)

# Détails des Rôles et Accès
1. Administrateur (Superuser)
Accès : Gestion complète, Tableau de bord statistique, Changement de statut forcé.
Login : admin
Mot de passe : admin
URL Dashboard : http://127.0.0.1:8000/dashboard/

# 2. Responsable des Stages (Professeur)
Accès : Validation et refus des offres en attente.
Login : prof_stage
Mot de passe : profpassword
URL Validation : http://127.0.0.1:8000/pending/

# 3. Entreprises (Non connectées)
Accès : Dépôt d'offre uniquement.
Compte : Pas de compte nécessaire.
URL Dépôt : http://127.0.0.1:8000/Create/