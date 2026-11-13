# Gestion de rendez-vous

Application Django permettant de gérer des clients et leurs rendez-vous.

## Installation locale

Prérequis : Python 3 et Git.

Linux / macOS :

```bash
git clone https://github.com/thetika434/gestion-de-rendez-vous.git
cd gestion-de-rendez-vous
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell :

```powershell
git clone https://github.com/thetika434/gestion-de-rendez-vous.git
cd gestion-de-rendez-vous
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Après avoir copié `.env.example`, renseignez `SECRET_KEY` dans `.env` avec une
clé locale. Vous pouvez en générer une avec :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Initialisez la base SQLite et lancez les vérifications :

```bash
python manage.py migrate
python manage.py check
python manage.py test
```

Démarrez ensuite le serveur local :

```bash
python manage.py runserver
```

La liste des rendez-vous est disponible à <http://127.0.0.1:8000/> et la liste
des clients à <http://127.0.0.1:8000/clients/>.

## Tests

Les tests automatisés du projet s’exécutent avec `python manage.py test`.
