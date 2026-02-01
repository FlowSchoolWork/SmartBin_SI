# 📊 Interface Web Admin - Smart Bin SI

> **Tableau de bord complet pour superviser et gérer votre système Smart Bin SI en temps réel.**

**Dernière mise à jour** : Février 2026

---

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Lancement](#lancement)
4. [Interface Utilisateur](#interface-utilisateur)
5. [Fonctionnalités Principales](#fonctionnalités-principales)
6. [API REST](#api-rest)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Vue d'Ensemble

L'interface web admin est un **dashboard complet** permettant de :

✅ **Superviser** le système en temps réel (CPU, RAM, GPU)  
✅ **Gérer** les bacs de tri (vider, voir le remplissage)  
✅ **Consulter** l'historique complet des détections  
✅ **Surveiller** les erreurs et faux positifs  
✅ **Configurer** les paramètres du système  
✅ **Archiver** les données et les logs  
✅ **Lancer/arrêter** les scripts en arrière-plan  

### Caractéristiques

- 📱 **Interface Responsive** : fonctionne sur desktop, tablette, mobile
- 🔄 **Temps Réel** : mise à jour automatique des données
- 📊 **Graphiques** : visualisation des statistiques
- 🔐 **Légère** : pas de base de données supplémentaire
- ⚡ **Rapide** : chargement < 1 sec

---

## 📦 Installation

### Prérequis

- **Python 3.7+**
- **pip** installé
- **Flask** pour l'application web
- **psutil** pour le monitoring système (optionnel mais recommandé)
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)

### Étape 1 : Accéder au Répertoire

```bash
cd z:\SI\SIpoubelle\admin_interface
# Ou
cd ~/SmartBin_SI/admin_interface
```

### Étape 2 : Installer les Dépendances

```bash
# Installer Flask
pip install Flask

# Installer psutil pour le monitoring
pip install psutil

# (Optionnel) GPU monitoring NVIDIA
pip install nvidia-ml-py3
```

**Ou installer tout en une seule commande** :

```bash
pip install Flask psutil nvidia-ml-py3
```

### Étape 3 : Configuration (Optionnel)

Les fichiers de configuration se trouvent dans `static/config.js`.

---

## 🚀 Lancement

### Démarrer l'Application

```bash
# Méthode 1 : Lancement simple
python app.py

# Méthode 2 : Avec logs en fichier
python app.py > logs/admin.log 2>&1

# Méthode 3 : En arrière-plan (Linux/macOS)
nohup python app.py > logs/admin.log 2>&1 &

# Méthode 4 : Mode debug (développement)
python app.py --debug
```

### Affichage au Lancement

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Accès à l'Interface

**Depuis la même machine** :
```
http://localhost:5000
ou
http://127.0.0.1:5000
```

**Depuis un autre ordinateur du réseau** :
```
# Trouver votre IP locale
ipconfig  # Windows
ifconfig  # Linux/macOS

# Puis accéder à :
http://192.168.1.X:5000
```

---

## 🎨 Interface Utilisateur

### 1. Accueil (Dashboard Principal)

```
┌─────────────────────────────────────────┐
│           SMART BIN - ADMIN             │
├─────────────────────────────────────────┤
│                                         │
│  📊 SYSTÈME (Temps réel)                │
│  ├─ CPU : 45% (4 cores @ 2.4 GHz)     │
│  ├─ RAM : 3.2 / 8 GB (40%)            │
│  ├─ DISQUE : 125 / 500 GB (25%)       │
│  ├─ UPTIME : 7j 14h 32m               │
│  └─ GPU : NVIDIA RTX2060, 52°C        │
│                                         │
│  🔌 ÉQUIPEMENTS                        │
│  ├─ Caméra : ✅ Connectée             │
│  └─ Arduino : ✅ Connecté (COM3)      │
│                                         │
│  🗑️  BACS                              │
│  ├─ Jaune (Recyclage)   : 65% ████     │
│  ├─ Vert (Compost)      : 32% ██       │
│  └─ Marron (Reste)      : 78% █████    │
│                                         │
└─────────────────────────────────────────┘
```

### 2. Gestion des Bacs

```
┌─────────────────────────────────────────┐
│         GESTION DES BACS                │
├─────────────────────────────────────────┤
│                                         │
│  BAC JAUNE (Recyclage)                  │
│  ├─ Remplissage    : 65%               │
│  ├─ Items          : 145               │
│  ├─ Dernière vidange : 2026-02-01      │
│  ├─ Capacité       : 10 L              │
│  └─ [VIDER]  [RÉINITIALISER]           │
│                                         │
│  BAC VERT (Compost)                     │
│  ├─ Remplissage    : 32%               │
│  ├─ Items          : 87                │
│  ├─ Dernière vidange : 2026-01-30      │
│  ├─ Capacité       : 10 L              │
│  └─ [VIDER]  [RÉINITIALISER]           │
│                                         │
│  BAC MARRON (Reste)                     │
│  ├─ Remplissage    : 78%               │
│  ├─ Items          : 203               │
│  ├─ Dernière vidange : 2026-01-28      │
│  ├─ Capacité       : 10 L              │
│  └─ [VIDER]  [RÉINITIALISER]           │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Historique des Détections

```
┌─────────────────────────────────────────┐
│     DERNIÈRES DÉTECTIONS                │
├─────────────────────────────────────────┤
│                                         │
│ Heure      | Objet          | Bac    │ │
│─────────────────────────────────────────│
│ 11:42:15   | plastic_bottle | yellow │ │
│ 11:40:33   | banana         | green  │ │
│ 11:38:22   | cardboard_box  | yellow │ │
│ 11:36:45   | glass_jar      | yellow │ │
│ 11:34:10   | food_waste     | green  │ │
│                                         │
│ [← Précédent]  [Suivant →]              │
│ Page 1 de 287                           │
│                                         │
└─────────────────────────────────────────┘
```

### 4. Graphiques et Statistiques

```
Tri par Bac (Dernier mois)
  Jaune  : ▓▓▓▓▓▓▓▓░░ 65% (1523 objets)
  Vert   : ▓▓▓░░░░░░ 32% (745 objets)
  Marron : ▓▓▓▓▓▓▓░░ 56% (1289 objets)

Objets Détectés (Top 10)
  plastic_bottle     : 287 fois
  cardboard          : 156 fois
  banana_peel        : 134 fois
  glass_jar          : 98 fois
  ...
```

### 5. Paramètres

```
┌─────────────────────────────────────────┐
│       PARAMÈTRES DE CONFIG              │
├─────────────────────────────────────────┤
│                                         │
│ Mode Apprentissage      : [ON]  [OFF]   │
│ Sauvegarde Images       : [ON]  [OFF]   │
│ Afficher L'interface    : [ON]  [OFF]   │
│ Seuil Confiance YOLO    : [0.6]  +-     │
│                                         │
│ Port Arduino            : [COM3]        │
│ Caméra Source           : [0]           │
│ Vitesse Baudrate        : [9600]        │
│                                         │
│ [SAUVEGARDER]  [ANNULER]  [RESET]      │
│                                         │
└─────────────────────────────────────────┘
```

---

## ⚙️ Fonctionnalités Principales

### 1. Dashboard Système

**Affichage en temps réel :**
- CPU : usage %, nombre de cores, fréquence
- RAM : GB utilisés, pourcentage
- DISQUE : espace libre, pourcentage
- UPTIME : temps depuis le démarrage
- GPU NVIDIA : modèle, température, VRAM utilisation

**Mise à jour** : Automatique chaque 2 secondes

### 2. Gestion des Bacs

**Actions disponibles :**
- 🗑️ Vider un bac → Reset remplissage à 0%
- 📊 Consulter l'état → Affiche détails
- ⚡ Vidage d'urgence → Immédiat

**Données affichées :**
- Pourcentage de remplissage
- Nombre d'items comptabilisés
- Dernière vidange (date/heure)
- Capacité maximale en litres

### 3. Historique des Détections

**Informations par détection :**
- ⏰ Timestamp précis
- 📦 Nom de l'objet
- 🎯 Bac de destination
- 📈 Confiance YOLO

**Filtres disponibles :**
- Par date/plage
- Par bac
- Par objet
- Par confiance min

**Exports :**
- CSV pour Excel
- JSON pour API externe
- PDF pour rapport

### 4. Gestion des Erreurs

**Suivi des faux positifs :**
- Affiche les détections rejetées
- Permet d'enregistrer les corrections
- Images attachées pour réentraînement

### 5. Configuration Temps Réel

**Édition directe des paramètres :**
- Seuil de confiance YOLO
- Mode apprentissage ON/OFF
- Sauvegarde images ON/OFF
- Port Arduino
- Caméra source
- Vitesse baudrate

⚠️ **Important** : Les changements s'appliquent immédiatement

### 6. Logs et Diagnostiques

**Consultables via l'interface :**
- Logs système (data/logs/system.log)
- Logs erreurs (data/logs/errors.log)
- Logs détections (data/logs/detections.log)

**Téléchargement :**
- Logs complets
- Filtrage par date
- Recherche par mot-clé

---

## 🔌 API REST

### Points de Terminaison (Endpoints)

#### GET /api/status
**Récupère l'état du système**

```json
{
  "cpu": { "usage": 45, "cores": 4, "freq": 2.4 },
  "ram": { "used": 3.2, "total": 8, "percent": 40 },
  "disk": { "free": 125, "total": 500, "percent": 25 },
  "uptime": "7d 14h 32m",
  "gpu": { "model": "RTX2060", "temp": 52, "vram": 60 },
  "camera": true,
  "arduino": true
}
```

#### GET /api/bins
**État de tous les bacs**

```json
{
  "yellow": {
    "fill_level": 65,
    "item_count": 145,
    "last_emptied": "2026-02-01",
    "capacity": 10
  },
  "green": { ... },
  "brown": { ... }
}
```

#### GET /api/detections
**Historique des détections**

```json
[
  {
    "timestamp": "2026-02-01 11:42:15",
    "item": "plastic_bottle",
    "bin": "yellow",
    "confidence": 0.92
  },
  ...
]
```

#### POST /api/bins/empty/{color}
**Vider un bac**

```bash
curl -X POST http://localhost:5000/api/bins/empty/yellow
```

#### GET /api/settings
**Récupère la configuration**

```json
{
  "learning_mode": true,
  "save_images": true,
  "confidence_threshold": 0.6,
  "arduino_port": "COM3"
}
```

#### POST /api/settings
**Modifie la configuration**

```bash
curl -X POST http://localhost:5000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"confidence_threshold": 0.7}'
```

---

## 🔧 Troubleshooting

### Problème : Port 5000 déjà utilisé

**Symptôme** :
```
OSError: [Errno 48] Address already in use
```

**Solution** :

```bash
# Option 1 : Utiliser un autre port
python app.py --port 5001

# Option 2 : Tuer le processus existant
# Windows :
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Linux/macOS :
lsof -i :5000
kill -9 [PID]
```

### Problème : Connexion refusée

**Symptôme** :
```
refused to connect
ERR_CONNECTION_REFUSED
```

**Cause** : Application n'est pas lancée

**Solution** :
```bash
# Vérifier que l'app est bien lancée
python app.py

# Vérifier que vous accédez au bon port
http://localhost:5000  ✓
http://localhost:5001  ✗
```

### Problème : Les données ne se mettent pas à jour

**Symptôme** :
```
Interface statique, pas de changement
```

**Cause** : JavaScript désactivé ou erreur réseau

**Solution** :
1. Vérifier que JavaScript est activé (F12 → Console)
2. Vérifier que la base de données n'est pas verrouillée
3. Redémarrer l'application

### Problème : GPU not detected

**Symptôme** :
```
GPU: N/A ou Not Available
```

**Solution** :

```bash
# Installer les drivers NVIDIA
# Puis installer :
pip install nvidia-ml-py3

# Redémarrer l'app
python app.py
```

---

## 📊 Exemples d'Utilisation

### Cas 1 : Supervision d'une Session de Tri

```
1. Ouvrir http://localhost:5000
2. Observer le dashboard
3. Voir les détections en direct
4. Vérifier que les bacs se remplissent correctement
5. Analyser les statistiques à la fin
```

### Cas 2 : Maintenance Préventive

```
1. Chaque semaine, consulter l'interface
2. Vider les bacs si > 70% de remplissage
3. Vérifier les performances (CPU, GPU)
4. Télécharger les logs pour analyse
```

### Cas 3 : Analyser un Faux Positif

```
1. Consulter l'historique des détections
2. Trouver la détection erronée
3. Noter l'image et l'heure
4. Intégrer cette donnée au réentraînement
```

---

## 📞 Support

**Problème** : Voir [docs/DEPANNAGE.md](../docs/DEPANNAGE.md)  
**Améliorations** : Ouvrir une issue GitHub  
**Questions** : Consulter la [documentation principale](../README.md)

---

**Version** : 1.0  
**Dernière mise à jour** : Février 2026


## 📊 APIs Disponibles

### Informations Système
```
GET /api/system/info
```
Retourne : hostname, OS, uptime, CPU%, RAM (GB et %), Disque (GB et %)

### Informations GPU
```
GET /api/gpu/info
```
Retourne : Nom GPU, Température °C, VRAM utilisée (GB), % utilisation

### Gestion des Scripts
```
GET /api/processes
```
Liste des processus Python en cours

```
GET /api/scripts/run/<script_name>
```
Lance un script (ex: test_app.py, run_auto.sh)

```
GET /api/scripts/stop/<script_name>
```
Arrête un script en cours d'exécution

### Configuration
```
GET /api/config/read
```
Récupère le contenu du config.py

```
POST /api/config/save
```
Enregistre les modifications du config.py
Body: `{"content": "# configuration content"}`

### Équipements (Placeholders)
```
GET /api/camera/status
```
État de la caméra

```
GET /api/arduino/status
```
État d'Arduino

## 🎨 Interface

La page d'accueil affiche :
- **Barre latérale** : Navigation entre les 5 sections
- **En-tête** : Statut du système + Bouton arrêt d'urgence
- **Dashboard** :
  - Grille d'état des équipements (Caméra, Arduino, GPU, Système)
  - Informations système détaillées (CPU, RAM, Disque, Uptime)
  - Console de gestion des scripts
  - Visualisation des niveaux des bacs
  - Tableau des détections YOLO
  - Section erreurs avec corrections IA
  - Éditeur de configuration

## 🛠️ Fonctionnalités Implémentées

### Arrêt d'Urgence
- ✅ Arrête tous les scripts lancés
- ✅ Confirmation avant exécution

### Gestion des Scripts
- ✅ Lance les scripts (test_app.py, test_hardware.py, run_auto.sh, run_manual.sh)
- ✅ Arrête les scripts en cours
- ✅ Console avec logs horodatés

### Mise à Jour en Temps Réel
- ✅ Infos système toutes les 5 secondes
- ✅ Infos GPU toutes les 3 secondes

### Config.py
- ✅ Lecture du fichier config.py
- ✅ Édition dans l'interface
- ✅ Enregistrement des modifications

## 🎮 Navigation

Menu principal :
- 🏠 **Accueil** - Dashboard complet
- 📦 **Gestion des Bacs** - Vue détaillée des 3 bacs
- 📋 **Détections** - Historique YOLO
- ⚠️ **Erreurs** - Signalements utilisateurs et corrections
- ⚙️ **Paramètres** - Configuration et maintenance

## 🔐 Notes de Sécurité

⚠️ **Attention** : Cette version est sans authentification
Avant la production :
- Ajouter un système de login
- Implémenter HTTPS
- Ajouter des contrôles d'accès
- Sécuriser l'API

## 📞 Prochaines Étapes

1. ✅ Interface UI complète
2. ⏳ Backend Flask avec API
3. ⏳ Base de données (SQLite ou autre)
4. ⏳ Intégration Arduino/ESP32
5. ⏳ Système d'authentification
6. ⏳ Déploiement en production

## 💡 Aide

En cas de problème :
1. Vérifiez que Flask est installé : `pip list | grep Flask`
2. Vérifiez le port 5000 n'est pas utilisé : `netstat -ano | findstr :5000`
3. Changez le port dans app.py si nécessaire
4. Consultez la console pour les erreurs

---

**Développé pour SmartBin - Janvier 2026**
