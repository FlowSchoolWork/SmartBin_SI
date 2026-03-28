# 🤖 Smart Bin SI - Système Intelligent de Tri des Déchets

> **Poubelle autonome utilisant l'Intelligence Artificielle (YOLOv8) pour le tri automatique et intelligent des déchets. Combinaison de vision par ordinateur, machine learning et électronique embarquée.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Arduino](https://img.shields.io/badge/Arduino-Uno-00979D.svg)
![YOLO](https://img.shields.io/badge/YOLO-v8-yellow.svg)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 📚 Table des Matières

1. [Présentation rapide](#-présentation-rapide)
2. [Installation](#-installation)
3. [Utilisation](#-utilisation)
4. [Documentation](#-documentation)
5. [Support](#-support)

---

## 🎯 Présentation Rapide

### Qu'est-ce que Smart Bin SI ?

Smart Bin SI est un **système de tri automatique de déchets** qui utilise l'intelligence artificielle pour trier correctement les déchets dans les bons bacs. Le système combine : 

- **📷 Vision par ordinateur** : détecte les objets via une caméra
- **🧠 Apprentissage automatique** : apprend de chaque nouvelle détection
- **💾 Intelligence persistante** : mémorise les classifications dans une base de données
- **🤖 Automatisation complète** : tri automatisé via servomoteurs Arduino

### ✨ Fonctionnalités principales

✅ **Détection en temps réel** des déchets via caméra  
✅ **Classification intelligente** en 4 catégories :
- 🟡 **Jaune** : Emballages (plastique, métal, carton) et papiers
- 🟢 **Vert** : Verre (bouteilles, bocaux, pots)
- 🟤 **Marron** : Biodéchets (végétaux, déchets alimentaires)
- ⚫ **Noir** : Ordures ménagères résiduelles

✅ **Apprentissage continu** : valide les détections et les enregistre  
✅ **Base de données intelligente** : mémorise toutes les classifications  
✅ **Deux modes d'opération** :
- Mode automatique (détection par caméra + YOLO)
- Mode manuel (saisie texte sans caméra)

✅ **Tableau de bord web** : suivi en temps réel des détections et de l'état du système  
✅ **Apprentissage incrémental** : améliore le modèle YOLO avec vos données

---

## 🚀 Installation

Pour plus de détails sur l'installation, consultez la [documentation d'installation complète](docs/setup/INSTALLATION.md).

---

## 💻 Utilisation

Pour plus de détails sur l'utilisation, consultez la [documentation d'utilisation](docs/usage/UTILISATION.md).

---

## 📖 Documentation

| Document | Contenu |
|----------|---------|
| [docs/setup/INSTALLATION.md](docs/setup/INSTALLATION.md) | Installation complète avec prérequis |
| [docs/setup/CONFIGURATION.md](docs/setup/CONFIGURATION.md) | Configuration avancée du système |
| [docs/usage/UTILISATION.md](docs/usage/UTILISATION.md) | Guide d'utilisation des modes |
| [docs/technical/ARCHITECTURE.md](docs/technical/ARCHITECTURE.md) | Architecture technique détaillée |
| [docs/technical/APPENTISSAGE.md](docs/technical/APPENTISSAGE.md) | Système d'apprentissage et d'amélioration |
| [docs/technical/ENTRAINEMENT_IA.md](docs/technical/ENTRAINEMENT_IA.md) | Réentraînement du modèle YOLO |
| [docs/technical/DEPANNAGE.md](docs/technical/DEPANNAGE.md) | Troubleshooting et solutions |

---

## 🆘 Support

Pour plus de détails sur le support, consultez la [FAQ complète](docs/technical/DEPANNAGE.md).

---

## 📊 Structure du Projet

```
SmartBin_SI/
├── src/                          # Code Python principal
│   ├── config.py                # Configuration centralisée
│   ├── yolo_detector.py         # Détection YOLO
│   ├── waste_classifier.py      # Gestion base de données
│   └── models/
│       └── best.pt              # Modèle YOLO entraîné
│
├── admin_interface/             # Tableau de bord web
│   ├── app.py                   # Application Flask
│   ├── requirements.txt          # Dépendances admin
│   └── static/
│       ├── index.html
│       ├── script.js
│       └── style.css
│
├── arduino/                     # Code Arduino
│   ├── smart_bin_controller.ino
│   └── wokwi-project.txt        # Simulation Wokwi
│
├── docs/                        # Documentation organisée
│   ├── setup/
│   │   ├── INSTALLATION.md
│   │   └── CONFIGURATION.md
│   ├── usage/
│   │   ├── UTILISATION.md
│   │   └── QUICK_START.md
│   └── technical/
│       ├── ARCHITECTURE.md
│       ├── APPENTISSAGE.md
│       ├── ENTRAINEMENT_IA.md
│       └── DEPANNAGE.md
│
├── data/                        # Données du système
│   ├── waste_items.db           # Base SQLite
│   ├── training_images/         # Images pour apprentissage
│   └── logs/                    # Fichiers journaux
│
└── requirements.txt             # Dépendances principales
```

---

## 🎓 Apprentissage et Amélioration

Smart Bin SI utilise un système d'apprentissage continu :

1. **Détection** : YOLO propose une classification
2. **Validation** : L'utilisateur confirme ou rejette
3. **Enregistrement** : Les données sont sauvegardées
4. **Apprentissage** : Réentraînement du modèle avec les nouvelles données

Cela permet au système de s'améliorer progressivement !

---

## 📄 Licence

Ce projet est sous licence Creative Commons Attribution-NonCommercial (CC BY-NC). Interdiction d'usage commercial - voir [LICENSE](LICENSE) pour les détails.

---

## 👥 Contributeurs

- **Auteur Principal** : Équipe SmartBin (FlowCreativeStudio"Florian"; Cyrille; Valentin)
- **Contributions** : Améliorations bienvenues via Pull Requests

---

## 📞 Contact & Ressources

- **Problèmes** : Ouvrir une [Issue GitHub](https://github.com/sayfox8/SmartBin_SI/issues)
- **Documentation** : Voir le dossier [docs/](docs/)

---

**Dernière mise à jour** : Février 2026  
**Version** : 9.0 - Documentation Complète