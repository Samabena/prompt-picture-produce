# Assistant Cuisine IA

Une application web intelligente qui te dit quoi cuisiner avec ce que tu as sous la main !

## Fonctionnalités principales
- Saisie d'un prompt (ingrédients, envies, etc.)
- Upload d'une image (par exemple, photo de ton frigo ou de tes ingrédients)
- L'IA (spécialisée cuisine) te propose des idées de recettes ou de plats
- Si la question n'est pas liée à la cuisine, l'IA explique son rôle et s'excuse

## Fichiers importants
- `index.html` : le frontend (formulaire, upload, affichage de la réponse IA)
- `main.py` : le backend FastAPI (reçoit le prompt/l'image, appelle l'API OpenAI, renvoie la réponse)
- `requirements.txt` : dépendances Python pour le backend

## Prérequis
- Python 3.8+
- Node.js et npm (si tu veux modifier le frontend avec Vite, sinon pas nécessaire)
- Une clé API OpenAI compatible GPT-4o (voir https://platform.openai.com/)

## Installation et lancement en local

1. **Clone le projet**
```bash
git clone <URL_DU_REPO>
cd prompt-picture-produce
```

2. **Installe les dépendances Python**
```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

3. **Configure ta clé OpenAI**
- Ouvre `main.py`
- Remplace `YOUR_API_KEY` par ta clé OpenAI :
  ```python
  OPENAI_API_KEY = "sk-..."
  ```

4. **Lance le backend**
```bash
python main.py
```
- Le serveur sera accessible sur http://localhost:8000

5. **Utilise l'application**
- Ouvre http://localhost:8000 dans ton navigateur
- Saisis un prompt (ex: "j'ai des œufs, du riz et du poulet")
- (Optionnel) Upload une image de tes ingrédients
- Clique sur "Envoyer" et découvre ce que tu peux cuisiner !

## Notes importantes
- L'IA ne répond qu'aux questions liées à la cuisine.
- Les images uploadées sont temporairement sauvegardées dans le dossier `uploads/`.
- Pour la production, pense à restreindre les origines CORS dans `main.py`.
- Si tu veux personnaliser l'IA, modifie le message système dans `main.py`.

## Dépendances principales
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pillow](https://python-pillow.org/) (pour la gestion d'images)
- [OpenAI API](https://platform.openai.com/docs/)

---

**Bon appétit et amuse-toi bien avec ton assistant cuisine IA !**
