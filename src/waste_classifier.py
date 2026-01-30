"""
Smart Bin SI - Module de Classification des Déchets
Gère la base de données et la communication avec l'Arduino
Peut être utilisé en mode autonome OU importé par yolo_detector.py
"""

import serial
import sqlite3
import time
import sys

# ============================================
# CONFIGURATION
# ============================================

# Configuration du port série (vérifier avec 'ls /dev/ttyACM*')
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 1

# Configuration de la base de données
DB_NAME = 'data/waste_items.db'

# Couleurs de bacs disponibles
VALID_BINS = ["yellow", "green", "brown"]

# Durée du mouvement de tri (secondes)
SORTING_DURATION = 10


# ============================================
# VARIABLES GLOBALES (Connexions Partagées)
# ============================================

# Ces variables seront initialisées une seule fois
_serial_connection = None
_db_connection = None
_db_cursor = None


# ============================================
# CONNEXION ARDUINO
# ============================================

def init_serial_connection():
    """
    Initialise la connexion avec l'Arduino
    Retourne: objet serial ou None si échec
    """
    global _serial_connection
    
    # Si déjà initialisé, retourner la connexion existante
    if _serial_connection is not None:
        return _serial_connection
    
    try:
        _serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
        time.sleep(2)  # Attendre l'initialisation de l'Arduino
        print("✓ Succès : Connecté à l'Arduino")
        return _serial_connection
    except Exception as e:
        print(f"⚠ Note : Mode simulation (Arduino non détecté sur {SERIAL_PORT})")
        print(f"   Erreur : {e}")
        _serial_connection = None
        return None


def get_serial_connection():
    """
    Obtenir la connexion série (l'initialise si nécessaire)
    Retourne: objet serial ou None
    """
    global _serial_connection
    if _serial_connection is None:
        return init_serial_connection()
    return _serial_connection


# ============================================
# GESTION DE LA BASE DE DONNÉES
# ============================================

def init_database():
    """
    Initialise la base de données SQLite avec les tables requises
    Retourne: objets connection et cursor
    """
    global _db_connection, _db_cursor
    
    # Si déjà initialisé, retourner les objets existants
    if _db_connection is not None and _db_cursor is not None:
        return _db_connection, _db_cursor
    
    _db_connection = sqlite3.connect(DB_NAME, check_same_thread=False)
    _db_cursor = _db_connection.cursor()
    
    # Créer la table principale de classification
    _db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS waste_classification (
            item_name TEXT PRIMARY KEY,
            bin_color TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usage_count INTEGER DEFAULT 1
        )
    ''')
    
    _db_connection.commit()
    print(f"✓ Base de données initialisée : {DB_NAME}")
    return _db_connection, _db_cursor


def get_database():
    """
    Obtenir la connexion à la base de données (l'initialise si nécessaire)
    Retourne: (connection, cursor)
    """
    global _db_connection, _db_cursor
    if _db_connection is None or _db_cursor is None:
        return init_database()
    return _db_connection, _db_cursor


def get_bin_color(item_name):
    """
    Cherche la couleur du bac pour un objet en base de données
    Retourne uniquement si trouvé, None sinon
    
    Args:
        item_name: Nom de l'objet
    
    Retourne:
        str: Couleur du bac (yellow/green/brown) ou None si pas trouvé
    """
    connection, cursor = get_database()
    
    # Chercher dans la base de données
    cursor.execute(
        "SELECT bin_color FROM waste_classification WHERE item_name = ?",
        (item_name.lower(),)
    )
    result = cursor.fetchone()
    
    if result:
        # Objet trouvé - incrémenter le compteur
        bin_color = result[0]
        cursor.execute(
            "UPDATE waste_classification SET usage_count = usage_count + 1 WHERE item_name = ?",
            (item_name.lower(),)
        )
        connection.commit()
        return bin_color
    
    return None


def save_to_database(item_name, bin_color):
    """
    Sauvegarde un nouvel objet dans la base de données
    
    Args:
        item_name: Nom de l'objet
        bin_color: Couleur du bac (yellow/green/brown)
    
    Retourne:
        bool: True si sauvegarde réussie
    """
    if bin_color not in VALID_BINS:
        print(f"✗ Erreur : Couleur invalide '{bin_color}'")
        return False
    
    connection, cursor = get_database()
    
    try:
        cursor.execute(
            "INSERT INTO waste_classification (item_name, bin_color) VALUES (?, ?)",
            (item_name.lower(), bin_color)
        )
        connection.commit()
        print(f"✓ Sauvegardé : {item_name} → bac {bin_color}")
        return True
    except sqlite3.IntegrityError:
        # L'objet existe déjà, mettre à jour
        cursor.execute(
            "UPDATE waste_classification SET bin_color = ? WHERE item_name = ?",
            (bin_color, item_name.lower())
        )
        connection.commit()
        print(f"✓ Mis à jour : {item_name} → bac {bin_color}")
        return True


def ask_user_for_bin(item_name):
    """
    Demande à l'utilisateur d'assigner une couleur de bac
    
    Args:
        item_name: Nom de l'objet
    
    Retourne:
        str: Couleur du bac (yellow/green/brown) ou None si ignoré
    """
    print(f"\n[NOUVEL OBJET DÉTECTÉ : '{item_name}']")
    print("Dans quel bac doit aller cet objet ?")
    print("  - yellow  (recyclable : plastique, carton, métal)")
    print("  - green   (organique : déchets alimentaires, biodégradable)")
    print("  - brown   (déchets généraux : non recyclable)")
    
    while True:
        user_choice = input("Entrer la couleur du bac (yellow/green/brown) ou 'skip' : ").strip().lower()
        
        if user_choice == 'skip':
            print("⊘ Classification ignorée")
            return None
        
        if user_choice in VALID_BINS:
            return user_choice
        
        print(f"✗ Erreur : Veuillez choisir 'yellow', 'green' ou 'brown'")


# ============================================
# CONTRÔLE MATÉRIEL
# ============================================

def send_sorting_command(bin_color):
    """
    Envoie une commande de tri à l'Arduino et attend la fin
    
    Args:
        bin_color: Couleur du bac cible (yellow/green/brown)
    
    Retourne:
        bool: True si envoi réussi
    """
    serial_conn = get_serial_connection()
    
    if serial_conn:
        try:
            # Envoyer la commande via série
            command = f"{bin_color}\n"
            serial_conn.write(command.encode())
            print(f"→ Commande envoyée à l'Arduino : {bin_color}")
            
            # Attendre la fin du mouvement de tri
            print(f"⏳ Attente de la fin du tri ({SORTING_DURATION}s)...")
            time.sleep(SORTING_DURATION)
            print("✓ Tri terminé")
            return True
            
        except Exception as e:
            print(f"✗ Erreur série : {e}")
            return False
    else:
        # Mode simulation
        print(f"[SIMULATION] L'Arduino trierait vers le bac {bin_color}")
        time.sleep(1)  # Court délai pour la simulation
        return True


# ============================================
# FONCTION PRINCIPALE DE CLASSIFICATION
# ============================================

def classify_and_sort(item_name, ask_if_unknown=True, auto_mode=False):
    """
    Fonction principale : classifie un objet et lance le tri
    Cette fonction est appelée par le mode manuel ET par YOLO
    
    Args:
        item_name: Nom de l'objet à trier
        ask_if_unknown: Si True, demande à l'utilisateur pour les objets inconnus
        auto_mode: Si True, mode silencieux (pour YOLO)
    
    Retourne:
        str: Couleur du bac utilisé, ou None si échec
    """
    if not auto_mode:
        print(f"\n🔍 Traitement : '{item_name}'")
    
    # Étape 1 : Chercher en base de données
    bin_color = get_bin_color(item_name)
    
    if bin_color:
        # Objet connu
        if not auto_mode:
            print(f"✓ Trouvé en base : {item_name} → bac {bin_color}")
    else:
        # Objet inconnu
        if not auto_mode:
            print(f"⚠ Objet inconnu : {item_name}")
        
        if ask_if_unknown:
            # Demander à l'utilisateur
            bin_color = ask_user_for_bin(item_name)
            
            if bin_color is None:
                return None  # Utilisateur a ignoré
            
            # Sauvegarder en base
            save_to_database(item_name, bin_color)
        else:
            # En mode auto sans demande, on ne peut pas trier
            if not auto_mode:
                print("⊘ Classification ignorée (mode auto sans confirmation)")
            return None
    
    # Étape 2 : Envoyer la commande de tri
    if not auto_mode:
        print(f"🎯 Action de tri : {item_name} → bac {bin_color}")
    
    success = send_sorting_command(bin_color)
    
    if success:
        return bin_color
    return None


# ============================================
# STATISTIQUES
# ============================================

def show_database_stats():
    """
    Affiche les statistiques de la base de données
    """
    connection, cursor = get_database()
    
    print("\n" + "="*50)
    print("📊 STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*50)
    
    # Total d'objets
    cursor.execute("SELECT COUNT(*) FROM waste_classification")
    total_items = cursor.fetchone()[0]
    print(f"Total d'objets appris : {total_items}")
    
    if total_items == 0:
        print("\nAucun objet en base de données.")
        print("="*50)
        return
    
    # Répartition par bac
    for bin_color in VALID_BINS:
        cursor.execute(
            "SELECT COUNT(*), SUM(usage_count) FROM waste_classification WHERE bin_color = ?",
            (bin_color,)
        )
        count, total_usage = cursor.fetchone()
        total_usage = total_usage or 0
        print(f"  Bac {bin_color:8} : {count:3} objets ({total_usage:4} utilisations)")
    
    # Objets les plus triés
    print("\nTop 5 des objets les plus triés :")
    cursor.execute(
        "SELECT item_name, bin_color, usage_count FROM waste_classification ORDER BY usage_count DESC LIMIT 5"
    )
    results = cursor.fetchall()
    
    if results:
        for idx, (item, color, count) in enumerate(results, 1):
            print(f"  {idx}. {item:20} → {color:6} ({count} fois)")
    
    print("="*50)


def list_all_items():
    """
    Liste tous les objets en base de données
    """
    connection, cursor = get_database()
    
    cursor.execute("SELECT item_name, bin_color, usage_count FROM waste_classification ORDER BY item_name")
    results = cursor.fetchall()
    
    if not results:
        print("\nAucun objet en base de données.")
        return
    
    print("\n" + "="*60)
    print("📋 LISTE DE TOUS LES OBJETS")
    print("="*60)
    print(f"{'Objet':<30} {'Bac':<10} {'Utilisations':<15}")
    print("-"*60)
    
    for item, color, count in results:
        print(f"{item:<30} {color:<10} {count:<15}")
    
    print("="*60)


# ============================================
# NETTOYAGE
# ============================================

def cleanup():
    """
    Ferme proprement toutes les connexions
    """
    global _serial_connection, _db_connection
    
    print("\n🔌 Fermeture des connexions...")
    
    if _serial_connection:
        _serial_connection.close()
        print("  ✓ Connexion série fermée")
    
    if _db_connection:
        _db_connection.close()
        print("  ✓ Connexion base de données fermée")
    
    print("\n✓ Arrêt système complet\n")


# ============================================
# MODE AUTONOME (Interface en Ligne de Commande)
# ============================================

def interactive_mode():
    """
    Mode interactif pour utilisation manuelle
    """
    print("\n" + "="*50)
    print("🤖 SMART BIN SI - SYSTÈME DE CONTRÔLE MANUEL")
    print("="*50)
    print("Entrez les noms d'objets pour simuler une détection")
    print("\nCommandes disponibles :")
    print("  [nom objet] - Trier un objet")
    print("  stats       - Voir les statistiques")
    print("  list        - Lister tous les objets")
    print("  quit        - Quitter")
    print("="*50 + "\n")
    
    # Initialiser les connexions
    init_serial_connection()
    init_database()
    
    try:
        # Boucle de contrôle principale
        while True:
            # Obtenir l'entrée utilisateur
            user_input = input("\nObjet détecté > ").strip()
            
            # Gérer les commandes spéciales
            if user_input.lower() == 'quit':
                print("\n👋 Arrêt du système...")
                break
            
            if user_input.lower() == 'stats':
                show_database_stats()
                continue
            
            if user_input.lower() == 'list':
                list_all_items()
                continue
            
            if not user_input:
                continue
            
            # Traiter la classification de l'objet
            classify_and_sort(user_input, ask_if_unknown=True, auto_mode=False)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Programme interrompu par l'utilisateur")
    
    finally:
        cleanup()


# ============================================
# POINT D'ENTRÉE (Si lancé directement)
# ============================================

if __name__ == "__main__":
    interactive_mode()