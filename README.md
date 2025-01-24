Groupe :
Nathaniel Josse et Raphaël Roscian

Commandes pour lancer le programme :
```bash
pip install -r requirements.txt

python fetch_and_store.py

python main.py
```

Les endpoints de l'API sont :
- Liste des collections : http://127.0.0.1:8000/
- Stats d'une collection : http://127.0.0.1:8000/[collection]/stats
  <br>Exemple :
  <br>http://127.0.0.1:8000/bruxelles_arbres_remarquables/stats
- Résultats d'une recherche dans une collection : http://127.0.0.1:8000/bruxelles_arbres_remarquables/search?field=[field]&value=[value]
  <br>Exemple :
  <br>http://127.0.0.1:8000/bruxelles_arbres_remarquables/search?field=nom_fr&value=Araucaria%20du%20Chili

Collections disponibles :
- Arbres remarquables de Bruxelles : `bruxelles_arbres_remarquables`
- Parcours BD de Bruxelles : `bruxelles_parcours_bd`
- Musées de Bruxelles : `musees-a-bruxelles`
- Parcs et Jardins de Bruxelles : `bruxelles_parcs_et_jardins`
- Streetart de Bruxelles : `streetart`