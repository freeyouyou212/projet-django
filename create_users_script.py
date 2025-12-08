import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iut_portal.settings')
django.setup()

from django.contrib.auth.models import User

def create_accounts():
    # 1. Création de l'ADMIN (Superuser)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@iut.fr', 'admin123')
        print("✅ Compte ADMIN créé (Login: admin / Pass: admin123)")
    else:
        print("ℹ️ Compte ADMIN existe déjà")

    # 2. Création de l'ENSEIGNANT (Staff mais pas Superuser)
    if not User.objects.filter(username='prof').exists():
        user = User.objects.create_user('prof', 'prof@iut.fr', 'prof123')
        user.is_staff = True  # Donne les droits "Enseignant/Responsable"
        user.is_superuser = False # Pas accès au dashboard admin
        user.save()
        print("✅ Compte ENSEIGNANT créé (Login: prof / Pass: prof123)")
    else:
        print("ℹ️ Compte ENSEIGNANT existe déjà")

    # 3. Création de l'ÉTUDIANT (Lambda)
    if not User.objects.filter(username='etudiant').exists():
        User.objects.create_user('etudiant', 'etu@iut.fr', 'etu123')
        print("✅ Compte ETUDIANT créé (Login: etudiant / Pass: etu123)")
    else:
        print("ℹ️ Compte ETUDIANT existe déjà")

if __name__ == '__main__':
    create_accounts()