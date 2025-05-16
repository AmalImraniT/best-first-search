# 🎯 Best-First Search Visualizer [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

<div align="center">
  <img src="https://img.shields.io/badge/Algorithm-Visualization-important" alt="Header">
  <br>
  <em>Explorez visuellement le parcours d'un graphe avec l'algorithme Best-First Search !</em>
</div>

---

## 🌟 Fonctionnalités

<div align="center">
  
| **Interface**          | **Fonctionnalité**           | **Technologie**       |
|------------------------|------------------------------|-----------------------|
| 🎨 Interface graphique | Visualisation interactive    | Matplotlib/Tkinter    |
| 📁 Gestion de fichiers | Import/Export JSON           | Custom JSON Parser    |
| 🚀 Exécution en direct | Animation pas-à-pas          | NetworkX Algorithm    |
| 📊 Analyse de données  | Sauvegarde des résultats     | Pandas/Numpy          |

</div>

---

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- Pip package manager

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/elarbi-allam/best_first_search_project.git
cd best_first_search_project

# Installer les dépendances
pip install -r requirements.txt
```

> **Note** : Pour Python 3.12+, exécutez d'abord :
> ```bash
> pip install setuptools && pip install --upgrade pip setuptools wheel
> ```

---

## 🖥️ Utilisation

```bash
python main.py
```

### 🖲️ Interface Utilisateur


| Bouton                  | Fonctionnalité                          |
|-------------------------|-----------------------------------------|
| 🎯 **Exécuter BFS**     | Lance la recherche en temps réel        |
| 📽️ **Créer Animation** | Génère un GIF étape par étape           |
| 💾 **Sauvegarder**      | Exporte les données au format JSON      |

**Légende** :
- Icônes cliquables avec effets hover
- Zone de visualisation centrale interactive
- Panneau latéral pour paramètres avancés

## 🧠 Algorithme

### Workflow Principal
1. **🎯 Initialisation**
   Création d'une file de priorité basée sur les valeurs heuristiques

2. **🔍 Exploration**
   Sélection itérative du nœud le plus prometteur

3. **✅ Vérification**
   Test de la condition d'arrêt (nœud final atteint)

4. **🔄 Propagation**
   Mise à jour des voisins et répétition du processus

```python
def best_first_search(graph, start, goal):
    # Initialisation de la file de priorité
    open_list = PriorityQueue()
    open_list.put((heuristic(start), start))
    visited = {start: None}

    # Exploration des nœuds
    while not open_list.empty():
        current = open_list.get()[1]

        # Vérification du but
        if current == goal:
            break

        # Propagation aux voisins
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                priority = heuristic(neighbor)
                open_list.put((priority, neighbor))
                visited[neighbor] = current

    # Reconstruction du chemin
    return reconstruct_path(visited, goal)
```

## 📂 Structure du Projet

```plaintext
best-first-search-visualizer/
├── core/
│   ├── algorithms.py    # Implémentation BFS
│   ├── graph_manager.py # Gestion des graphes
│   └── visualizer.py    # Système de rendu
├── data/
│   ├── examples/        # Graphes pré-configurés
│   └── exports/         # Résultats d'exécution
└── docs/
    └── tutorial.md      # Guide approfondi
```

## 🧪 Exemples

---

### Graphe Simple (A → G)
```json
{
    "nodes": [
        {"id": "A", "heuristic": 7},
        {"id": "G", "heuristic": 0}
    ],
    "edges": [
        {"from": "A", "to": "G", "weight": 1}
    ]
}
```

**Résultat Attendu** :
➤ `Chemin optimal : A → G`
➤ `Coût total : 1`

## 🤝 Contribution

<div align="center">

| Type de Contribution       | Instructions                      | Lien                      |
|---------------------------|-----------------------------------|--------------------------|
| 🐛 **Rapport de bug**      | Utiliser le template d'issue      | [Ouvrir une issue]()      |
| 💡 **Nouvelle fonction**   | Discuter dans les discussions     | [Démarrer discussion]()   |
| 📚 **Amélioration docs**   | Soumettre une Pull Request        | [Voir le guide]()         |
| 🎨 **Design UI**           | Proposer des maquettes Figma      | [Partager design]()       |

</div>

**Processus :**
1. Forker le dépôt
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commiter vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

```text
MIT License
```

<div align="center">


</div>
