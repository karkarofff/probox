#!/usr/bin/env python3
# ProBox v2.0 (CustomTkinter) - boîte à outils système Windows / Windows system toolbox
# Requis / requires : pip install psutil pillow  (pillow optionnel : preview images)
# Exe : pyinstaller --onefile --noconsole --icon probox.ico --add-data "probox.ico;." --name ProBox probox.py

import os
import sys
import json
import time
import string
import threading
import subprocess
import webbrowser
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import customtkinter as ctk
except ImportError:
    print("customtkinter manquant. ->  pip install customtkinter")
    sys.exit(1)

APP_NAME = "ProBox"
APP_VERSION = "2.0.0"
AUTHOR = "Karkarofff"
AUTHOR_URL = "https://github.com/karkarofff"
# Fichier JSON hébergé : {"version": "0.8.0", "url": "https://..."}
UPDATE_URL = ("https://raw.githubusercontent.com/karkarofff/probox/"
              "main/version.json")

# ---------- Palette ----------
BG      = "#15161b"
BG2     = "#1e1f26"
BG3     = "#2a2b34"
FG      = "#eceef2"
FG_DIM  = "#9a9ba6"
ACCENT  = "#e05555"

MOD_COLORS = {
    "startup": ("#1c2f26", "#22392e", "#4fbf78"),
    "network": ("#1b2637", "#213047", "#4f9cf0"),
    "dupes":   ("#261f3a", "#2e2648", "#9a6cf0"),
    "tidy":    ("#33291c", "#3e3222", "#f0b64f"),
    "wifi":    ("#1b3134", "#213c3f", "#4fd0c7"),
    "clean":   ("#331f27", "#3e2630", "#f06a8a"),
    "disk":    ("#2b3119", "#343c20", "#b8d34f"),
}

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")),
                          APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ---------- Traductions (français = langue source, clé = texte FR) ----------
EN = {
 "Ouvrir": "Open",
 "Accueil": "Home",
 "← Accueil": "← Home",
 "Bonjour": "Good morning",
 "Bonsoir": "Good evening",
 "{h} ! Choisis un module pour commencer.":
     "{h}! Pick a module to get started.",
 "développé par": "developed by",
 "Clique pour ouvrir la page de {a}.\nClic droit : vérifier les mises à jour.":
     "Click to open {a}'s page.\nRight-click: check for updates.",
 "Basculer l'interface en anglais": "Switch interface to French",
 "Mise à jour disponible": "Update available",
 "Une nouvelle version de {app} est dispo !\n\nTa version : {cur}\nDernière version : {new}\n\nOuvrir la page de téléchargement ?":
     "A new version of {app} is available!\n\nYour version: {cur}\nLatest version: {new}\n\nOpen the download page?",
 "Mise à jour": "Update",
 "Tu as déjà la dernière version ({v}).":
     "You already have the latest version ({v}).",
 "Impossible de vérifier les mises à jour\n(pas de connexion ou fichier de version introuvable).":
     "Could not check for updates\n(no connection or version file not found).",
 "⟳ Rafraîchir": "⟳ Refresh",
 "Confirmation": "Confirmation",
 "Emplacement introuvable.": "Location not found.",
 # ----- modules (titres / descriptions cartes) -----
 "Démarrage": "Startup",
 "Voir et contrôler tout ce qui se lance à l'ouverture de Windows.":
     "See and control everything that launches when Windows starts.",
 "Réseau": "Network",
 "Quelle application utilise ta connexion, combien, et vers où.":
     "Which app is using your connection, how much, and where to.",
 "Doublons": "Duplicates",
 "Trouver les fichiers en double par contenu, pas juste par nom.":
     "Find duplicate files by content, not just by name.",
 "Rangement": "Tidy up",
 "Trier automatiquement le bazar du dossier Téléchargements.":
     "Automatically sort the mess in your Downloads folder.",
 # ----- démarrage -----
 "Tout ce qui se lance à l'ouverture de Windows. Désactive ce qui ralentit ton PC, sans le désinstaller.":
     "Everything that launches when Windows starts. Disable what slows down your PC, without uninstalling anything.",
 "Nom": "Name",
 "État": "State",
 "Source": "Source",
 "Commande / fichier": "Command / file",
 "Activé": "Enabled",
 "Désactivé": "Disabled",
 "{n} éléments, {on} activés": "{n} items, {on} enabled",
 "Activer / Désactiver": "Enable / Disable",
 "Active ou désactive l'élément sélectionné au démarrage.\nDésactiver ne désinstalle rien : le programme reste sur le PC, il ne se lancera juste plus tout seul.":
     "Enables or disables the selected startup item.\nDisabling uninstalls nothing: the program stays on the PC, it just won't launch by itself anymore.",
 "Supprimer l'entrée": "Delete entry",
 "Supprime définitivement l'entrée de démarrage (le programme lui-même n'est pas désinstallé).\nPréfère Désactiver si tu n'es pas sûr.":
     "Permanently deletes the startup entry (the program itself is not uninstalled).\nPrefer Disable if you're not sure.",
 "📁 Ouvrir l'emplacement": "📁 Open location",
 "Ouvre le dossier du programme concerné.": "Opens the program's folder.",
 "Registre (utilisateur)": "Registry (user)",
 "Registre (machine)": "Registry (machine)",
 "Dossier Démarrage (utilisateur)": "Startup folder (user)",
 "Dossier Démarrage (machine)": "Startup folder (machine)",
 "Accès refusé : cet élément appartient à la machine.\nRelance {app} en administrateur pour le modifier.":
     "Access denied: this item belongs to the machine.\nRestart {app} as administrator to change it.",
 "Accès refusé : cet élément appartient à la machine.\nRelance {app} en administrateur pour le supprimer.":
     "Access denied: this item belongs to the machine.\nRestart {app} as administrator to delete it.",
 "Impossible de modifier : {e}": "Could not change: {e}",
 "Impossible de supprimer : {e}": "Could not delete: {e}",
 "Supprimer définitivement « {n} » du démarrage ?\n\nLe programme n'est pas désinstallé, seule son entrée de démarrage disparaît.\nSi tu n'es pas sûr, utilise plutôt Désactiver.":
     "Permanently remove \u201c{n}\u201d from startup?\n\nThe program is not uninstalled, only its startup entry disappears.\nIf unsure, use Disable instead.",
 "Ouvre l'explorateur avec le fichier déjà sélectionné dedans.":
     "Opens Explorer with the file already selected in it.",
 # ----- réseau -----
 "Débit global en temps réel, et liste des applications connectées à internet : combien de connexions, et vers où.":
     "Real-time global bandwidth, and the list of apps connected to the internet: how many connections, and where to.",
 "téléchargement": "download",
 "envoi": "upload",
 "Application": "Application",
 "Connexions": "Connections",
 "En écoute": "Listening",
 "Connecté vers": "Connected to",
 "☠ Tuer le process": "☠ Kill process",
 "Tue de force l'application sélectionnée.\nSa connexion s'arrête immédiatement.":
     "Force-kills the selected application.\nIts connection stops immediately.",
 "Double-clic : détail des connexions": "Double-click: connection details",
 "Tuer de force « {n} » (PID {p}) ?": "Force-kill \u201c{n}\u201d (PID {p})?",
 "Impossible : {e}": "Failed: {e}",
 "psutil requis": "psutil required",
 "(aucune connexion ou accès refusé)": "(no connections or access denied)",
 "{n} - connexions": "{n} - connections",
 # ----- doublons -----
 "Trouve les fichiers en double dans un dossier, par CONTENU (deux fichiers identiques sont détectés même renommés). La suppression envoie à la corbeille, donc récupérable.":
     "Finds duplicate files in a folder, by CONTENT (two identical files are detected even if renamed). Deleting sends to the recycle bin, so it's recoverable.",
 "📁 Choisir un dossier": "📁 Pick a folder",
 "💽 Disque entier": "💽 Whole drive",
 "Scanner un disque complet (C:, D:, ...).\nAttention : sur un gros disque, le scan peut prendre de longues minutes.":
     "Scan a whole drive (C:, D:, ...).\nWarning: on a big drive, the scan can take long minutes.",
 "Aucun dossier choisi": "No folder selected",
 "Lancer le scan": "Start scan",
 "■ Stop (garde les résultats)": "■ Stop (keeps results)",
 "Ignorer les fichiers < 1 Mo": "Ignore files < 1 MB",
 "Accélère beaucoup le scan en ignorant les petits fichiers,\nqui sont rarement ceux qui prennent de la place.":
     "Greatly speeds up the scan by ignoring small files,\nwhich are rarely the ones taking up space.",
 "Ignorer les dossiers système": "Ignore system folders",
 "Ignore Windows, Program Files, la corbeille, etc.\nRecommandé : ces dossiers contiennent des doublons NORMAUX qu'il ne faut pas toucher.":
     "Ignores Windows, Program Files, the recycle bin, etc.\nRecommended: these folders contain NORMAL duplicates that must not be touched.",
 "Fichier": "File",
 "Taille": "Size",
 "Emplacement": "Location",
 "✔ Tout sélectionner sauf 1 par groupe": "✔ Select all but 1 per group",
 "Sélectionne automatiquement toutes les copies SAUF la plus ancienne de chaque groupe.\nIl te reste juste à cliquer sur Corbeille.":
     "Automatically selects every copy EXCEPT the oldest of each group.\nAll that's left is clicking the Recycle bin button.",
 "🗑 Mettre la sélection à la corbeille": "🗑 Send selection to recycle bin",
 "Envoie les fichiers sélectionnés à la corbeille Windows.\nRécupérables tant que tu ne vides pas la corbeille.":
     "Sends the selected files to the Windows recycle bin.\nRecoverable as long as you don't empty the bin.",
 "🖼 Ouvrir le fichier": "🖼 Open file",
 "Ouvre le fichier sélectionné avec son application par défaut.\nAstuce : double-clic sur une ligne fait pareil.":
     "Opens the selected file with its default application.\nTip: double-clicking a row does the same.",
 "Choisis un disque à scanner": "Pick a drive to scan",
 "Disque {l}:": "Drive {l}:",
 "{free} libres sur {total}": "{free} free of {total}",
 "Scan d'un disque complet : ça peut prendre de longues minutes. Le bouton ■ arrête en gardant les résultats déjà trouvés.":
     "Scanning a whole drive: it can take long minutes. The ■ button stops while keeping the results already found.",
 "Dossier à scanner": "Folder to scan",
 "Dossier introuvable.": "Folder not found.",
 "Parcours... {n} fichiers vus": "Walking... {n} files seen",
 "Analyse du contenu... {d}/{t}": "Analyzing content... {d}/{t}",
 "  |  {n} groupes trouvés": "  |  {n} groups found",
 "{name}  ({n} copies)": "{name}  ({n} copies)",
 "Scan arrêté — résultats conservés : ": "Scan stopped — results kept: ",
 "Terminé : ": "Done: ",
 "{p}{n} groupes de doublons, {w} récupérables":
     "{p}{n} duplicate groups, {w} recoverable",
 "Scan arrêté.": "Scan stopped.",
 "Aucun doublon trouvé. 🎉": "No duplicates found. 🎉",
 "Envoyer {n} fichier(s) à la corbeille ?\n({s} récupérés)\n\nIls resteront récupérables dans la corbeille Windows.":
     "Send {n} file(s) to the recycle bin?\n({s} recovered)\n\nThey will remain recoverable in the Windows recycle bin.",
 "{n} fichier(s) envoyés à la corbeille, {s} récupérés":
     "{n} file(s) sent to the recycle bin, {s} recovered",
 "L'envoi à la corbeille a échoué.": "Sending to the recycle bin failed.",
 # ----- rangement -----
 "Trie les fichiers en vrac d'un dossier (Téléchargements par défaut) dans des sous-dossiers par type : Images, Vidéos, Documents... Analyse d'abord, rien ne bouge sans ton accord, et le dernier rangement est annulable.":
     "Sorts loose files in a folder (Downloads by default) into subfolders by type: Images, Videos, Documents... Analyze first, nothing moves without your approval, and the last tidy-up can be undone.",
 "Images": "Images",
 "Vidéos": "Videos",
 "Musique": "Music",
 "Documents": "Documents",
 "Archives": "Archives",
 "Programmes": "Programs",
 "Autres": "Others",
 "📁 Changer de dossier": "📁 Change folder",
 "🧹 Ranger": "🧹 Tidy up",
 "Déplace les fichiers selon le plan affiché ci-dessous.\nActif après une analyse.":
     "Moves the files according to the plan shown below.\nActive after an analysis.",
 "🔍 Analyser": "🔍 Analyze",
 "Montre ce qui serait déplacé et où.\nRIEN ne bouge à cette étape.":
     "Shows what would be moved and where.\nNOTHING moves at this step.",
 "Sous-dossiers par année": "Subfolders by year",
 "Range aussi par année de modification :\nImages/2025, Images/2026, etc.":
     "Also sorts by modification year:\nImages/2025, Images/2026, etc.",
 "Catégorie": "Category",
 "Destination": "Destination",
 "↩ Annuler le dernier rangement": "↩ Undo last tidy-up",
 "Remet à leur place d'origine les fichiers déplacés lors du DERNIER rangement.":
     "Puts the files moved during the LAST tidy-up back where they came from.",
 "Dossier à ranger": "Folder to tidy",
 "{n} fichiers à ranger dans {c} catégories. Vérifie le plan puis clique sur Ranger.":
     "{n} files to sort into {c} categories. Check the plan then click Tidy up.",
 "Rien à ranger : aucun fichier en vrac dans ce dossier. 🎉":
     "Nothing to tidy: no loose files in this folder. 🎉",
 "Déplacer {n} fichiers selon le plan affiché ?\n\nAnnulable ensuite avec le bouton ↩.":
     "Move {n} files according to the displayed plan?\n\nUndoable afterwards with the ↩ button.",
 "{n} fichiers rangés": "{n} files tidied",
 ", {e} échecs (fichiers utilisés ?)": ", {e} failures (files in use?)",
 "Aucun rangement à annuler.": "No tidy-up to undo.",
 "Remettre {n} fichiers à leur emplacement d'origine ?":
     "Put {n} files back to their original location?",
 "{n} fichiers remis en place": "{n} files put back",
 ", {e} introuvables ou bloqués": ", {e} missing or locked",
 # ----- wifi -----
 "Wi-Fi": "Wi-Fi",
 "Retrouver les mots de passe des réseaux Wi-Fi enregistrés sur ce PC.":
     "Recover the passwords of the Wi-Fi networks saved on this PC.",
 "Tous les réseaux Wi-Fi que ce PC connaît, avec leur mot de passe enregistré. Pratique quand on te demande « c'est quoi le code du wifi ? ».":
     "Every Wi-Fi network this PC knows, with its saved password. Handy when someone asks \u201cwhat's the wifi password?\u201d.",
 "Sécurité": "Security",
 "Mot de passe": "Password",
 "👁 Afficher les mots de passe": "👁 Show passwords",
 "🙈 Masquer les mots de passe": "🙈 Hide passwords",
 "Affiche ou masque les mots de passe dans la liste.":
     "Shows or hides the passwords in the list.",
 "📋 Copier le mot de passe": "📋 Copy password",
 "Copie le mot de passe du réseau sélectionné dans le presse-papier.":
     "Copies the selected network's password to the clipboard.",
 "(réseau ouvert)": "(open network)",
 "Mot de passe copié : {n}": "Password copied: {n}",
 "{n} réseaux enregistrés": "{n} saved networks",
 "Aucun réseau ou mots de passe invisibles ? Relance {app} en administrateur.":
     "No networks or passwords hidden? Restart {app} as administrator.",
 # ----- nettoyage -----
 "Nettoyage": "Cleanup",
 "Libérer de l'espace : fichiers temporaires, caches, corbeille.":
     "Free up space: temporary files, caches, recycle bin.",
 "Libère de l'espace disque en supprimant ce qui ne sert plus : fichiers temporaires, caches, corbeille. Analyse d'abord pour voir ce qui est récupérable, rien n'est supprimé sans ton accord.":
     "Frees up disk space by removing what's no longer needed: temporary files, caches, recycle bin. Analyze first to see what's recoverable, nothing is deleted without your approval.",
 "Fichiers temporaires (utilisateur)": "Temporary files (user)",
 "Fichiers temporaires Windows": "Windows temporary files",
 "Corbeille": "Recycle bin",
 "Caches des navigateurs": "Browser caches",
 "Cache des miniatures": "Thumbnail cache",
 "Restes de Windows Update": "Windows Update leftovers",
 "🧹 Nettoyer la sélection": "🧹 Clean selection",
 "Supprime définitivement le contenu des catégories cochées.\nActif après une analyse.":
     "Permanently deletes the content of the checked categories.\nActive after an analysis.",
 "Calcule la taille récupérable de chaque catégorie.\nRIEN n'est supprimé à cette étape.":
     "Computes the recoverable size of each category.\nNOTHING is deleted at this step.",
 "Analyse de {c}...": "Analyzing {c}...",
 "{s} récupérables au total. Coche ce que tu veux nettoyer.":
     "{s} recoverable in total. Check what you want to clean.",
 "Nettoyer les catégories cochées ?\n\nLes fichiers seront définitivement supprimés (la corbeille, elle, sera simplement vidée). Les fichiers en cours d'utilisation seront ignorés.":
     "Clean the checked categories?\n\nFiles will be permanently deleted (the recycle bin itself will simply be emptied). Files currently in use will be skipped.",
 "Nettoyage... {c}": "Cleaning... {c}",
 "Nettoyage terminé : {s} libérés.": "Cleanup done: {s} freed.",
 "Astuce : ferme les navigateurs avant de nettoyer leurs caches, et lance {app} en admin pour les catégories Windows.":
     "Tip: close your browsers before cleaning their caches, and run {app} as admin for the Windows categories.",
 # ----- historique -----
 "📜 Historique": "📜 History",
 "Historique des actions": "Action history",
 "Tout ce que {app} a modifié sur ce PC, pour garder l'esprit tranquille.":
     "Everything {app} changed on this PC, for peace of mind.",
 "Vider l'historique": "Clear history",
 "(aucune action pour l'instant)": "(no actions yet)",
 "Nettoyage : {s} libérés ({c})": "Cleanup: {s} freed ({c})",
 "Doublons : {n} fichier(s) envoyés à la corbeille ({s})":
     "Duplicates: {n} file(s) sent to recycle bin ({s})",
 "Rangement : {n} fichiers déplacés": "Tidy up: {n} files moved",
 "Rangement annulé : {n} fichiers remis en place":
     "Tidy up undone: {n} files put back",
 "Démarrage : « {n} » activé": "Startup: \u201c{n}\u201d enabled",
 "Démarrage : « {n} » désactivé": "Startup: \u201c{n}\u201d disabled",
 "Démarrage : entrée « {n} » supprimée":
     "Startup: entry \u201c{n}\u201d deleted",
 "Réseau : process « {n} » tué": "Network: process \u201c{n}\u201d killed",
 "Voir le détail de ce qui sera nettoyé.":
     "See exactly what would be cleaned.",
 "Détail — {c}": "Details — {c}",
 "Les {n} plus gros éléments de cette catégorie :":
     "The {n} largest items in this category:",
 "Ouvre la corbeille Windows pour voir son contenu.":
     "Open the Windows recycle bin to see its content.",
 "🗑 Ouvrir la corbeille": "🗑 Open recycle bin",
 # ----- espace disque -----
 "Espace disque": "Disk space",
 "Trouver ce qui remplit ton disque : plus gros dossiers et fichiers.":
     "Find what fills your drive: largest folders and files.",
 "Analyse un disque ou un dossier et montre où part la place : les dossiers les plus lourds (navigables) et les plus gros fichiers. Pratique pour répondre à « pourquoi mon disque est plein ? ».":
     "Analyzes a drive or folder and shows where the space goes: the heaviest folders (browsable) and the largest files. Handy to answer \u201cwhy is my drive full?\u201d.",
 "📂 Dossiers": "📂 Folders",
 "📄 Plus gros fichiers": "📄 Largest files",
 "Santé des disques : OK": "Drive health: OK",
 "Santé des disques à surveiller : {d}": "Drive health needs attention: {d}",
 "Terminé : {d} dossiers et {f} fichiers analysés.":
     "Done: {d} folders and {f} files analyzed.",
 "Scan arrêté — résultats partiels.": "Scan stopped — partial results.",
 "🗑 Mettre à la corbeille": "🗑 Send to recycle bin",
 "Envoie le fichier sélectionné (vue Fichiers) à la corbeille Windows.":
     "Sends the selected file (Files view) to the Windows recycle bin.",
 "Envoyer « {n} » à la corbeille ?\n({s})":
     "Send \u201c{n}\u201d to the recycle bin?\n({s})",
 "Espace disque : « {n} » envoyé à la corbeille ({s})":
     "Disk space: \u201c{n}\u201d sent to recycle bin ({s})",
 # ----- diagnostic réseau -----
 "🩺 Diagnostic": "🩺 Diagnostics",
 "Diagnostic réseau": "Network diagnostics",
 "Teste la connexion et répare les problèmes réseau courants.":
     "Tests the connection and fixes common network problems.",
 "Connexion à internet": "Internet connection",
 "Résolution DNS": "DNS resolution",
 "IP locale": "Local IP",
 "IP publique": "Public IP",
 "▶ Relancer les tests": "▶ Run tests again",
 "🔧 Réparer ma connexion": "🔧 Repair my connection",
 "Vide le cache DNS, renouvelle l'adresse IP et réinitialise Winsock.\nLa connexion peut se couper quelques secondes.":
     "Flushes the DNS cache, renews the IP address and resets Winsock.\nThe connection may drop for a few seconds.",
 "Réparer la connexion ?\n\nOpérations : vidage du cache DNS, renouvellement de l'adresse IP, réinitialisation Winsock.\nLa connexion peut se couper quelques secondes pendant l'opération.":
     "Repair the connection?\n\nOperations: flush DNS cache, renew IP address, reset Winsock.\nThe connection may drop for a few seconds during the process.",
 "Vidage du cache DNS": "Flushing DNS cache",
 "Renouvellement de l'adresse IP": "Renewing IP address",
 "Réinitialisation Winsock": "Resetting Winsock",
 "échec (admin requis ?)": "failed (admin needed?)",
 "Un redémarrage du PC est conseillé pour finaliser la réinitialisation Winsock.":
     "Restarting the PC is recommended to finalize the Winsock reset.",
 "Réseau : réparation effectuée ({s})":
     "Network: repair performed ({s})",
 "hors ligne ?": "offline?",
 # ----- état du PC -----
 "Ton PC fonctionne normalement": "Your PC is running normally",
 "Ton PC est très sollicité en ce moment":
     "Your PC is under heavy load right now",
 "Ton disque système est presque plein":
     "Your system drive is almost full",
 "CPU {c}% · RAM {r}% · Disque {d}% ({free} libres)":
     "CPU {c}% · RAM {r}% · Disk {d}% ({free} free)",
}


def detect_lang():
    cfg = load_config()
    if cfg.get("lang") in ("fr", "en"):
        return cfg["lang"]
    if sys.platform == "win32":
        try:
            import ctypes
            lid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if lid & 0x3FF == 0x0C:
                return "fr"
        except Exception:
            pass
    else:
        try:
            import locale
            if (locale.getlocale()[0] or "").lower().startswith("fr"):
                return "fr"
        except Exception:
            pass
    return "en"


LANG = detect_lang()


def t(text):
    """Traduit un texte FR vers la langue courante."""
    if LANG == "en":
        return EN.get(text, text)
    return text


def set_lang(lang):
    global LANG
    LANG = lang
    cfg = load_config()
    cfg["lang"] = lang
    save_config(cfg)


def fmt_size(n):
    units = ("o", "Ko", "Mo", "Go") if LANG == "fr" else \
            ("B", "KB", "MB", "GB")
    for i, unit in enumerate(units):
        if n < 1024 or i == 3:
            return f"{n:.1f} {unit}" if i else f"{int(n)} {unit}"
        n /= 1024


def fmt_speed(bps):
    mo = "Mo/s" if LANG == "fr" else "MB/s"
    ko = "Ko/s" if LANG == "fr" else "KB/s"
    o = "o/s" if LANG == "fr" else "B/s"
    if bps >= 1024 * 1024:
        return f"{bps / (1024 * 1024):.1f} {mo}"
    if bps >= 1024:
        return f"{bps / 1024:.0f} {ko}"
    return f"{bps:.0f} {o}"


def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def setup_window(win):
    try:
        win.iconbitmap(resource_path("probox.ico"))
    except Exception:
        pass
    if sys.platform == "win32":
        try:
            import ctypes
            win.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
            value = ctypes.c_int(1)
            for attr in (20, 19):
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, attr, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass


def open_in_explorer(path):
    if os.path.exists(path):
        subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])


def log_action(msg):
    """Journalise une action système dans la config (300 dernières)."""
    cfg = load_config()
    hist = cfg.get("history", [])
    hist.append({"t": time.strftime("%d/%m %H:%M"), "msg": msg})
    cfg["history"] = hist[-300:]
    save_config(cfg)


def show_history(parent):
    win = tk.Toplevel(parent)
    win.title(t("Historique des actions"))
    win.configure(bg=BG)
    win.geometry("560x480")
    setup_window(win)
    ttk.Label(win, text=t("Tout ce que {app} a modifié sur ce PC, pour "
                          "garder l'esprit tranquille."
                          ).format(app=APP_NAME),
              style="Dim.TLabel", wraplength=520,
              padding=(12, 10, 12, 4)).pack(anchor="w")
    lb = tk.Listbox(win, bg=BG2, fg=FG, selectbackground="#3d3e49",
                    highlightthickness=0, relief="flat",
                    font=("Segoe UI", 10))
    lb.pack(fill="both", expand=True, padx=10, pady=4)
    hist = load_config().get("history", [])
    if hist:
        for h in reversed(hist):
            lb.insert("end", f'  {h["t"]}   {h["msg"]}')
    else:
        lb.insert("end", "  " + t("(aucune action pour l'instant)"))
    fr = ttk.Frame(win, padding=10)
    fr.pack(fill="x")

    def clear():
        cfg = load_config()
        cfg["history"] = []
        save_config(cfg)
        lb.delete(0, "end")
        lb.insert("end", "  " + t("(aucune action pour l'instant)"))
    PBButton(fr, text=t("Vider l'historique"), style="Soft.TButton",
               command=clear).pack(side="right")


class Tooltip:
    def __init__(self, widget, text, delay=450):
        self.widget, self.text, self.delay = widget, text, delay
        self.tip, self._job = None, None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _=None):
        self._job = self.widget.after(self.delay, self._show)

    def _show(self):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        tk.Label(self.tip, text=self.text, justify="left", wraplength=340,
                 bg="#0d0e12", fg=FG, relief="solid", borderwidth=1,
                 font=("Segoe UI", 9), padx=8, pady=6).pack()

    def _hide(self, _=None):
        if self._job:
            self.widget.after_cancel(self._job)
            self._job = None
        if self.tip:
            self.tip.destroy()
            self.tip = None


def round_rect(canvas, x1, y1, x2, y2, r, **kw):
    pts = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2,
           x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    return canvas.create_polygon(pts, smooth=True, **kw)


class Check(tk.Frame):
    """Case à cocher dessinée sur mesure : coins arrondis, couleur
    d'accent du module, coche blanche."""

    def __init__(self, parent, text, variable=None, command=None,
                 accent="#4f9cf0", bg=BG):
        super().__init__(parent, bg=bg)
        self.var = variable if variable is not None \
            else tk.BooleanVar(value=False)
        self.command = command
        self.accent = accent
        self._hover = False
        self.cv = tk.Canvas(self, width=20, height=20, bg=bg,
                            highlightthickness=0)
        self.cv.pack(side="left")
        self.lbl = tk.Label(self, text=text, bg=bg, fg=FG,
                            font=("Segoe UI", 10))
        self.lbl.pack(side="left", padx=(7, 0))
        for w in (self, self.cv, self.lbl):
            w.bind("<Button-1>", self._toggle)
            w.bind("<Enter>", self._enter)
            w.bind("<Leave>", self._leave)
            w.configure(cursor="hand2")
        self.var.trace_add("write", lambda *_: self._draw())
        self._draw()

    def _enter(self, _=None):
        self._hover = True
        self._draw()

    def _leave(self, _=None):
        self._hover = False
        self._draw()

    def _toggle(self, _=None):
        self.var.set(not self.var.get())
        if self.command:
            self.command()

    def _draw(self):
        self.cv.delete("all")
        checked = self.var.get()
        if checked:
            fill = outline = self.accent
        else:
            fill = BG3
            outline = "#5a5b68" if self._hover else "#42434f"
        round_rect(self.cv, 2, 2, 18, 18, 6, fill=fill, outline=outline)
        if checked:
            self.cv.create_line(6, 10, 9, 13, 14, 6, fill="#ffffff",
                                width=2, capstyle="round",
                                joinstyle="round")


BTN_STYLES = {
    "Kill.TButton": (ACCENT, "#c9414f", "#ffffff"),
    "Soft.TButton": (BG3, "#3a3b47", FG),
    "Blue.TButton": ("#4f9cf0", "#3f86d6", "#ffffff"),
    "Green.TButton": ("#4fbf78", "#41a566", "#ffffff"),
}


class PBScroll(ctk.CTkScrollbar):
    """Scrollbar fine CustomTkinter, compatible avec l'API ttk."""

    def __init__(self, parent, orient="vertical", command=None, **kw):
        kw.setdefault("bg_color", BG2)
        super().__init__(parent, orientation=orient, command=command,
                         width=14 if orient == "vertical" else None,
                         height=14 if orient == "horizontal" else None,
                         fg_color="transparent", button_color="#3a3b47",
                         button_hover_color="#4a4b57", **kw)


class PBButton(ctk.CTkButton):
    """Bouton CustomTkinter compatible avec l'API ttk utilisée partout."""

    def __init__(self, parent, text="", style="Soft.TButton",
                 command=None, **kw):
        fg, hov, txt = BTN_STYLES.get(style, BTN_STYLES["Soft.TButton"])
        kw.setdefault("width", max(64, int(len(text) * 7.2) + 30))
        super().__init__(parent, text=text, command=command,
                         fg_color=fg, hover_color=hov, text_color=txt,
                         corner_radius=10, height=32,
                         font=("Segoe UI", 12), **kw)

    def configure(self, **kw):
        style = kw.pop("style", None)
        if style:
            fg, hov, txt = BTN_STYLES.get(style,
                                          BTN_STYLES["Soft.TButton"])
            kw.update(fg_color=fg, hover_color=hov, text_color=txt)
        return super().configure(**kw)


class ScrollFrame(ttk.Frame):
    """Zone défilante verticale (barre + molette)."""

    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.sb = PBScroll(self, orient="vertical",
                                command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self._win = self.canvas.create_window((0, 0), window=self.inner,
                                              anchor="nw")
        self.canvas.configure(yscrollcommand=self.sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.sb.pack(side="right", fill="y")
        self.inner.bind("<Configure>", self._update_region)
        self.canvas.bind("<Configure>", self._update_region)

    def _update_region(self, _=None):
        w = self.canvas.winfo_width()
        self.canvas.itemconfigure(self._win, width=w)
        # la zone de défilement ne descend jamais sous la hauteur visible :
        # si tout tient à l'écran, aucun scroll possible, pas de vide
        h = max(self.inner.winfo_reqheight(), self.canvas.winfo_height())
        self.canvas.configure(scrollregion=(0, 0, w, h))

    def _wheel(self, e):
        try:
            if (self.canvas.winfo_exists()
                    and self.inner.winfo_reqheight()
                    > self.canvas.winfo_height()):
                self.canvas.yview_scroll(int(-e.delta / 120), "units")
        except tk.TclError:
            pass

    def enable_wheel(self):
        try:
            self.canvas.bind_all("<MouseWheel>", self._wheel)
        except tk.TclError:
            pass

    def disable_wheel(self):
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except tk.TclError:
            pass


class ModuleCard(tk.Canvas):
    W, H, R = 310, 210, 18

    def __init__(self, parent, icon, title, desc, colors, command):
        super().__init__(parent, width=self.W, height=self.H,
                         bg=BG, highlightthickness=0)
        self.tint, self.hover, self.acc = colors
        self.command = command
        self._draw(icon, title, desc)
        self.bind("<Enter>", lambda e: self._set_bg(self.hover))
        self.bind("<Leave>", lambda e: self._set_bg(self.tint))
        self.bind("<Button-1>", lambda e: self.command())
        self.configure(cursor="hand2")

    def _draw(self, icon, title, desc):
        self.card = round_rect(self, 2, 2, self.W-2, self.H-2, self.R,
                               fill=self.tint, outline=self.hover)
        cx = self.W // 2
        self.create_text(cx, 46, text=icon, font=("Segoe UI Emoji", 30),
                         fill=self.acc)
        self.create_text(cx, 94, text=title, fill=FG,
                         font=("Segoe UI", 15, "bold"))
        self.create_text(cx, 132, text=desc, fill=FG_DIM, width=self.W-60,
                         justify="center", font=("Segoe UI", 9))
        bw, bh = 150, 34
        self.btn = round_rect(self, cx-bw//2, self.H-2-14-bh,
                              cx+bw//2, self.H-2-14, 10, fill=self.acc)
        self.btn_txt = self.create_text(cx, self.H-2-14-bh//2,
                                        text=t("Ouvrir"),
                                        fill="#101216",
                                        font=("Segoe UI", 10, "bold"))

    def _set_bg(self, color):
        self.itemconfigure(self.card, fill=color)


# ======================================================================
#  MODULE : Démarrage
# ======================================================================
class StartupModule(ttk.Frame):
    RUN_APPROVED = (r"Software\Microsoft\Windows\CurrentVersion\Explorer"
                    r"\StartupApproved\Run")
    FOLDER_APPROVED = (r"Software\Microsoft\Windows\CurrentVersion\Explorer"
                       r"\StartupApproved\StartupFolder")

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["startup"][2]
        self._items = []
        self._build()
        self.refresh()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="🚀", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Démarrage"),
                  font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        PBButton(head, text=t("⟳ Rafraîchir"), style="Soft.TButton",
                   command=self.refresh).pack(side="right")
        ttk.Label(self, text=t("Tout ce qui se lance à l'ouverture de "
                               "Windows. Désactive ce qui ralentit ton PC, "
                               "sans le désinstaller."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 10), wraplength=760).pack(fill="x")

        cols = ("name", "state", "source", "command")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                 selectmode="browse")
        for c, txt, w in (("name", t("Nom"), 200), ("state", t("État"), 90),
                          ("source", t("Source"), 170),
                          ("command", t("Commande / fichier"), 430)):
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))
        self.tree.tag_configure("off", foreground=FG_DIM)
        self.tree.tag_configure("on", foreground=FG)

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        b1 = PBButton(bar, text=t("Activer / Désactiver"),
                        style="Blue.TButton", command=self.toggle)
        b1.pack(side="left")
        Tooltip(b1, t("Active ou désactive l'élément sélectionné au "
                      "démarrage.\nDésactiver ne désinstalle rien : le "
                      "programme reste sur le PC, il ne se lancera juste "
                      "plus tout seul."))
        b2 = PBButton(bar, text=t("Supprimer l'entrée"),
                        style="Kill.TButton", command=self.delete)
        b2.pack(side="left", padx=6)
        Tooltip(b2, t("Supprime définitivement l'entrée de démarrage (le "
                      "programme lui-même n'est pas désinstallé).\nPréfère "
                      "Désactiver si tu n'es pas sûr."))
        b3 = PBButton(bar, text=t("📁 Ouvrir l'emplacement"),
                        style="Soft.TButton", command=self.open_location)
        b3.pack(side="left")
        Tooltip(b3, t("Ouvre l'explorateur avec le fichier déjà "
                      "sélectionné dedans."))
        self.count_lbl = ttk.Label(bar, text="", style="Dim.TLabel")
        self.count_lbl.pack(side="right")

    def refresh(self):
        self._items = []
        self.tree.delete(*self.tree.get_children())
        if sys.platform == "win32":
            self._read_registry()
            self._read_folders()
        for it in self._items:
            state = t("Activé") if it["enabled"] else t("Désactivé")
            self.tree.insert("", "end", values=(
                it["name"], state, t(it["source"]), it["command"]),
                tags=("on" if it["enabled"] else "off",))
        n_on = sum(1 for i in self._items if i["enabled"])
        self.count_lbl.configure(
            text=t("{n} éléments, {on} activés").format(
                n=len(self._items), on=n_on))

    def _approved_state(self, root, subkey, name):
        try:
            import winreg
            with winreg.OpenKey(root, subkey) as k:
                val, _ = winreg.QueryValueEx(k, name)
            return not (val and val[0] & 0x01 == 0x01 and val[0] != 0x02)
        except Exception:
            return True

    def _read_registry(self):
        import winreg
        sources = [
            (winreg.HKEY_CURRENT_USER, "Registre (utilisateur)"),
            (winreg.HKEY_LOCAL_MACHINE, "Registre (machine)"),
        ]
        for root, label in sources:
            try:
                with winreg.OpenKey(
                        root,
                        r"Software\Microsoft\Windows\CurrentVersion\Run") as k:
                    i = 0
                    while True:
                        try:
                            name, cmd, _ = winreg.EnumValue(k, i)
                        except OSError:
                            break
                        i += 1
                        self._items.append({
                            "name": name, "command": cmd, "source": label,
                            "kind": "reg", "root": root,
                            "enabled": self._approved_state(
                                root, self.RUN_APPROVED, name),
                        })
            except Exception:
                continue

    def _startup_folders(self):
        out = []
        appdata = os.environ.get("APPDATA")
        if appdata:
            out.append((os.path.join(
                appdata, r"Microsoft\Windows\Start Menu\Programs\Startup"),
                "Dossier Démarrage (utilisateur)"))
        progdata = os.environ.get("PROGRAMDATA")
        if progdata:
            out.append((os.path.join(
                progdata, r"Microsoft\Windows\Start Menu\Programs\StartUp"),
                "Dossier Démarrage (machine)"))
        return out

    def _read_folders(self):
        import winreg
        for folder, label in self._startup_folders():
            if not os.path.isdir(folder):
                continue
            for f in os.listdir(folder):
                if f.lower() == "desktop.ini":
                    continue
                self._items.append({
                    "name": f, "command": os.path.join(folder, f),
                    "source": label, "kind": "folder",
                    "root": winreg.HKEY_CURRENT_USER,
                    "enabled": self._approved_state(
                        winreg.HKEY_CURRENT_USER, self.FOLDER_APPROVED, f),
                })

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        idx = self.tree.index(sel[0])
        return self._items[idx] if idx < len(self._items) else None

    def toggle(self):
        it = self._selected()
        if not it:
            return
        import winreg
        subkey = self.RUN_APPROVED if it["kind"] == "reg" \
            else self.FOLDER_APPROVED
        new_enabled = not it["enabled"]
        data = (b"\x02" if new_enabled else b"\x03") + b"\x00" * 11
        try:
            with winreg.CreateKeyEx(it["root"], subkey, 0,
                                    winreg.KEY_SET_VALUE) as k:
                winreg.SetValueEx(k, it["name"], 0, winreg.REG_BINARY, data)
            log_action(t("Démarrage : « {n} » activé" if new_enabled
                         else "Démarrage : « {n} » désactivé"
                         ).format(n=it["name"]))
            self.refresh()
        except PermissionError:
            messagebox.showwarning(
                APP_NAME,
                t("Accès refusé : cet élément appartient à la machine.\n"
                  "Relance {app} en administrateur pour le modifier."
                  ).format(app=APP_NAME))
        except Exception as e:
            messagebox.showwarning(
                APP_NAME, t("Impossible de modifier : {e}").format(e=e))

    def delete(self):
        it = self._selected()
        if not it:
            return
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Supprimer définitivement « {n} » du démarrage ?\n\nLe "
                  "programme n'est pas désinstallé, seule son entrée de "
                  "démarrage disparaît.\nSi tu n'es pas sûr, utilise plutôt "
                  "Désactiver.").format(n=it["name"])):
            return
        import winreg
        try:
            if it["kind"] == "reg":
                with winreg.OpenKey(
                        it["root"],
                        r"Software\Microsoft\Windows\CurrentVersion\Run",
                        0, winreg.KEY_SET_VALUE) as k:
                    winreg.DeleteValue(k, it["name"])
                cfg = load_config()
                cfg.setdefault("startup_backup", []).append(
                    {"name": it["name"], "command": it["command"]})
                save_config(cfg)
            else:
                os.remove(it["command"])
            log_action(t("Démarrage : entrée « {n} » supprimée"
                         ).format(n=it["name"]))
            self.refresh()
        except PermissionError:
            messagebox.showwarning(
                APP_NAME,
                t("Accès refusé : cet élément appartient à la machine.\n"
                  "Relance {app} en administrateur pour le supprimer."
                  ).format(app=APP_NAME))
        except Exception as e:
            messagebox.showwarning(
                APP_NAME, t("Impossible de supprimer : {e}").format(e=e))

    def open_location(self):
        it = self._selected()
        if not it:
            return
        path = it["command"]
        if it["kind"] == "reg":
            path = path.strip()
            if path.startswith('"'):
                path = path[1:].split('"', 1)[0]
            else:
                path = path.split(" ", 1)[0]
        if os.path.exists(path):
            open_in_explorer(path)
        else:
            messagebox.showinfo(APP_NAME, t("Emplacement introuvable."))


# ======================================================================
#  MODULE : Réseau
# ======================================================================
class NetworkModule(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["network"][2]
        self._last_io = None
        self._last_t = None
        self._rows = []
        self._alive = True
        self._build()
        self._tick()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="📡", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Réseau"), font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        db = PBButton(head, text=t("🩺 Diagnostic"), style="Blue.TButton",
                        command=self.show_diagnostic)
        db.pack(side="right")
        Tooltip(db, t("Teste la connexion et répare les problèmes réseau "
                      "courants."))
        ttk.Label(self, text=t("Débit global en temps réel, et liste des "
                               "applications connectées à internet : "
                               "combien de connexions, et vers où."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 8), wraplength=760).pack(fill="x")

        speed = tk.Frame(self, bg=BG2)
        speed.pack(fill="x", padx=16, pady=(0, 8))
        self.dl_lbl = tk.Label(speed, text="↓ --", bg=BG2, fg=self.acc,
                               font=("Segoe UI", 16, "bold"))
        self.dl_lbl.pack(side="left", padx=(16, 6), pady=10)
        tk.Label(speed, text=t("téléchargement"), bg=BG2, fg=FG_DIM
                 ).pack(side="left")
        self.ul_lbl = tk.Label(speed, text="↑ --", bg=BG2, fg="#f0b64f",
                               font=("Segoe UI", 16, "bold"))
        self.ul_lbl.pack(side="left", padx=(28, 6))
        tk.Label(speed, text=t("envoi"), bg=BG2, fg=FG_DIM).pack(side="left")

        cols = ("name", "pid", "estab", "listen", "remotes")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                 selectmode="browse")
        for c, txt, w in (("name", t("Application"), 190),
                          ("pid", "PID", 70),
                          ("estab", t("Connexions"), 90),
                          ("listen", t("En écoute"), 80),
                          ("remotes", t("Connecté vers"), 420)):
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))
        self.tree.bind("<Double-1>", lambda e: self.show_details())

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        b1 = PBButton(bar, text=t("☠ Tuer le process"),
                        style="Kill.TButton",
                        command=self.kill_selected)
        b1.pack(side="left")
        Tooltip(b1, t("Tue de force l'application sélectionnée.\nSa "
                      "connexion s'arrête immédiatement."))
        b2 = PBButton(bar, text=t("📁 Ouvrir l'emplacement"),
                        style="Soft.TButton", command=self.open_location)
        b2.pack(side="left", padx=6)
        Tooltip(b2, t("Ouvre l'explorateur avec le fichier déjà "
                      "sélectionné dedans."))
        ttk.Label(bar, text=t("Double-clic : détail des connexions"),
                  style="Dim.TLabel").pack(side="right")

    def destroy(self):
        self._alive = False
        super().destroy()

    def _tick(self):
        if not self._alive:
            return
        try:
            import psutil
        except ImportError:
            self.dl_lbl.configure(text=t("psutil requis"))
            return

        def worker():
            io = psutil.net_io_counters()
            now = time.time()
            dl = ul = 0.0
            if self._last_io and now > self._last_t:
                dt = now - self._last_t
                dl = (io.bytes_recv - self._last_io.bytes_recv) / dt
                ul = (io.bytes_sent - self._last_io.bytes_sent) / dt
            self._last_io, self._last_t = io, now

            per_pid = {}
            try:
                conns = psutil.net_connections(kind="inet")
            except Exception:
                conns = []
            for c in conns:
                if not c.pid:
                    continue
                d = per_pid.setdefault(c.pid, {"estab": 0, "listen": 0,
                                               "remotes": []})
                if c.status == "ESTABLISHED":
                    d["estab"] += 1
                    if c.raddr:
                        d["remotes"].append(f"{c.raddr.ip}:{c.raddr.port}")
                elif c.status == "LISTEN":
                    d["listen"] += 1
            rows = []
            for pid, d in per_pid.items():
                try:
                    p = psutil.Process(pid)
                    name, exe = p.name(), (p.exe() or "")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    name, exe = f"PID {pid}", ""
                uniq = list(dict.fromkeys(d["remotes"]))
                rows.append({"name": name, "pid": pid, "exe": exe,
                             "estab": d["estab"], "listen": d["listen"],
                             "remotes": ", ".join(uniq[:4])
                             + (" …" if len(uniq) > 4 else "")})
            rows.sort(key=lambda r: r["estab"], reverse=True)

            def apply():
                if not self._alive:
                    return
                self.dl_lbl.configure(text=f"↓ {fmt_speed(dl)}")
                self.ul_lbl.configure(text=f"↑ {fmt_speed(ul)}")
                sel_pid = None
                if self.tree.selection():
                    sel_pid = int(self.tree.item(self.tree.selection()[0],
                                                 "values")[1])
                self._rows = rows
                self.tree.delete(*self.tree.get_children())
                for r in rows:
                    iid = self.tree.insert("", "end", values=(
                        r["name"], r["pid"], r["estab"], r["listen"],
                        r["remotes"]))
                    if r["pid"] == sel_pid:
                        self.tree.selection_add(iid)
            self.after(0, apply)
        threading.Thread(target=worker, daemon=True).start()
        self.after(2000, self._tick)

    # ---------- diagnostic ----------
    def show_diagnostic(self):
        win = tk.Toplevel(self)
        win.title(t("Diagnostic réseau"))
        win.configure(bg=BG)
        win.geometry("540x480")
        setup_window(win)

        tests = [("net", t("Connexion à internet")),
                 ("dns", t("Résolution DNS")),
                 ("lip", t("IP locale")),
                 ("pip", t("IP publique"))]
        labels = {}
        box = ttk.Frame(win, padding=(16, 14, 16, 4))
        box.pack(fill="x")
        for key, name in tests:
            row = ctk.CTkFrame(box, fg_color=BG2, corner_radius=10)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=name, bg=BG2, fg=FG,
                     font=("Segoe UI", 10)).pack(side="left",
                                                 padx=12, pady=8)
            lbl = tk.Label(row, text="⏳", bg=BG2, fg=FG_DIM,
                           font=("Segoe UI", 10, "bold"))
            lbl.pack(side="right", padx=12)
            labels[key] = lbl

        rb = PBButton(box, text=t("▶ Relancer les tests"),
                        style="Soft.TButton",
                        command=lambda: self._run_tests(win, labels))
        rb.pack(anchor="e", pady=(8, 0))

        fix = ttk.Frame(win, padding=(16, 10, 16, 8))
        fix.pack(fill="both", expand=True)
        fix_out = tk.Label(fix, text="", bg=BG, fg=FG_DIM,
                           font=("Segoe UI", 10), justify="left",
                           anchor="nw")
        fb = PBButton(fix, text=t("🔧 Réparer ma connexion"),
                        style="Kill.TButton",
                        command=lambda: self._repair(win, fix_out, labels))
        fb.pack(anchor="w")
        Tooltip(fb, t("Vide le cache DNS, renouvelle l'adresse IP et "
                      "réinitialise Winsock.\nLa connexion peut se couper "
                      "quelques secondes."))
        fix_out.pack(fill="both", expand=True, pady=(10, 0))

        self._run_tests(win, labels)

    def _set_test(self, win, lbl, txt, ok):
        def apply():
            if win.winfo_exists():
                lbl.configure(text=txt,
                              fg="#4fbf78" if ok else "#e05555")
        self.after(0, apply)

    def _run_tests(self, win, labels):
        for l in labels.values():
            l.configure(text="⏳", fg=FG_DIM)

        def worker():
            import socket
            times = []
            for _ in range(3):
                try:
                    t0 = time.time()
                    s = socket.create_connection(("1.1.1.1", 443),
                                                 timeout=3)
                    s.close()
                    times.append((time.time() - t0) * 1000)
                except OSError:
                    pass
            if times:
                self._set_test(win, labels["net"],
                               f"✅ {sum(times) / len(times):.0f} ms", True)
            else:
                self._set_test(win, labels["net"],
                               "❌ " + t("hors ligne ?"), False)
            try:
                t0 = time.time()
                socket.getaddrinfo("google.com", 443)
                self._set_test(win, labels["dns"],
                               f"✅ {(time.time() - t0) * 1000:.0f} ms",
                               True)
            except OSError:
                self._set_test(win, labels["dns"], "❌", False)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                self._set_test(win, labels["lip"], f"✅ {ip}", True)
            except OSError:
                self._set_test(win, labels["lip"], "❌", False)
            try:
                req = urllib.request.Request(
                    "https://api.ipify.org",
                    headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"})
                with urllib.request.urlopen(req, timeout=6) as r:
                    ip = r.read().decode().strip()
                self._set_test(win, labels["pip"], f"✅ {ip}", True)
            except Exception:
                self._set_test(win, labels["pip"], "❌", False)
        threading.Thread(target=worker, daemon=True).start()

    def _repair(self, win, out_lbl, labels):
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Réparer la connexion ?\n\nOpérations : vidage du cache "
                  "DNS, renouvellement de l'adresse IP, réinitialisation "
                  "Winsock.\nLa connexion peut se couper quelques "
                  "secondes pendant l'opération."), parent=win):
            return

        steps = [(t("Vidage du cache DNS"), ["ipconfig", "/flushdns"]),
                 (t("Renouvellement de l'adresse IP"),
                  ["ipconfig", "/renew"]),
                 (t("Réinitialisation Winsock"),
                  ["netsh", "winsock", "reset"])]

        def worker():
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            lines, done = [], []
            winsock_ok = False
            for i, (name, cmd) in enumerate(steps):
                lines.append(f"⏳ {name}...")
                self._set_out(win, out_lbl, lines)
                try:
                    r = subprocess.run(cmd, capture_output=True,
                                       timeout=90, creationflags=flags)
                    ok = r.returncode == 0
                except Exception:
                    ok = False
                if ok:
                    lines[-1] = f"✅ {name}"
                    done.append(name)
                    if i == 2:
                        winsock_ok = True
                else:
                    lines[-1] = f"❌ {name} — " + t("échec (admin requis ?)")
                self._set_out(win, out_lbl, lines)
            if winsock_ok:
                lines.append("")
                lines.append("ℹ " + t("Un redémarrage du PC est conseillé "
                                      "pour finaliser la réinitialisation "
                                      "Winsock."))
                self._set_out(win, out_lbl, lines)
            if done:
                log_action(t("Réseau : réparation effectuée ({s})"
                             ).format(s=", ".join(done)))
            time.sleep(2)
            if win.winfo_exists():
                self.after(0, lambda: self._run_tests(win, labels))
        threading.Thread(target=worker, daemon=True).start()

    def _set_out(self, win, lbl, lines):
        def apply():
            if win.winfo_exists():
                lbl.configure(text="\n".join(lines))
        self.after(0, apply)

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        pid = int(self.tree.item(sel[0], "values")[1])
        return next((r for r in self._rows if r["pid"] == pid), None)

    def kill_selected(self):
        it = self._selected()
        if not it:
            return
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Tuer de force « {n} » (PID {p}) ?").format(
                    n=it["name"], p=it["pid"])):
            return
        try:
            import psutil
            psutil.Process(it["pid"]).kill()
            log_action(t("Réseau : process « {n} » tué"
                         ).format(n=it["name"]))
        except Exception as e:
            messagebox.showwarning(APP_NAME,
                                   t("Impossible : {e}").format(e=e))

    def open_location(self):
        it = self._selected()
        if not it:
            return
        if it["exe"] and os.path.exists(it["exe"]):
            open_in_explorer(it["exe"])
        else:
            messagebox.showinfo(APP_NAME, t("Emplacement introuvable."))

    def show_details(self):
        it = self._selected()
        if not it:
            return
        try:
            import psutil
            proc = psutil.Process(it["pid"])
            conns = proc.net_connections(kind="inet") \
                if hasattr(proc, "net_connections") \
                else proc.connections(kind="inet")
        except Exception:
            conns = []
        win = tk.Toplevel(self)
        win.title(t("{n} - connexions").format(n=it["name"]))
        win.configure(bg=BG)
        win.geometry("640x460")
        setup_window(win)
        txt = tk.Text(win, bg=BG2, fg=FG, relief="flat",
                      font=("Consolas", 10), wrap="none", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=8, pady=8)
        lines = [f"{it['name']} (PID {it['pid']})", ""]
        for c in conns:
            l = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "?"
            r = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "-"
            lines.append(f"{c.status:<14} {l:<24} ->  {r}")
        if len(lines) == 2:
            lines.append(t("(aucune connexion ou accès refusé)"))
        txt.insert("1.0", "\n".join(lines))
        txt.configure(state="disabled")


# ======================================================================
#  MODULE : Doublons
# ======================================================================
def send_to_trash(paths):
    import ctypes
    from ctypes import wintypes

    class SHFILEOPSTRUCTW(ctypes.Structure):
        _fields_ = [("hwnd", wintypes.HWND),
                    ("wFunc", ctypes.c_uint),
                    ("pFrom", ctypes.c_wchar_p),
                    ("pTo", ctypes.c_wchar_p),
                    ("fFlags", ctypes.c_ushort),
                    ("fAnyOperationsAborted", wintypes.BOOL),
                    ("hNameMappings", ctypes.c_void_p),
                    ("lpszProgressTitle", ctypes.c_wchar_p)]

    FO_DELETE, FOF_ALLOWUNDO = 3, 0x40
    FOF_NOCONFIRMATION, FOF_SILENT = 0x10, 0x4
    src = "\0".join(paths) + "\0\0"
    op = SHFILEOPSTRUCTW(None, FO_DELETE, src, None,
                         FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT,
                         False, None, None)
    return ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op)) == 0


IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".ico"}


class ImagePreview:
    def __init__(self, tree, get_path):
        self.tree, self.get_path = tree, get_path
        self.tip, self.iid, self._job, self._photo = None, None, None, None
        tree.bind("<Motion>", self._motion, add="+")
        tree.bind("<Leave>", self._hide, add="+")
        tree.bind("<ButtonPress>", self._hide, add="+")

    def _motion(self, e):
        iid = self.tree.identify_row(e.y)
        if iid == self.iid:
            return
        self.iid = iid
        self._hide()
        path = self.get_path(iid) if iid else None
        if path and os.path.splitext(path)[1].lower() in IMG_EXTS:
            self._job = self.tree.after(
                350, lambda: self._show(path, e.x_root, e.y_root))

    def _show(self, path, x, y):
        try:
            from PIL import Image, ImageTk
        except ImportError:
            return
        try:
            img = Image.open(path)
            img.thumbnail((280, 280))
            self._photo = ImageTk.PhotoImage(img)
        except Exception:
            return
        self.tip = tk.Toplevel(self.tree)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x + 18}+{y + 12}")
        tk.Label(self.tip, image=self._photo, bg="#0d0e12", bd=1,
                 relief="solid").pack()

    def _hide(self, _=None):
        if self._job:
            self.tree.after_cancel(self._job)
            self._job = None
        if self.tip:
            self.tip.destroy()
            self.tip = None


class DupesModule(ttk.Frame):
    SYS_DIRS = {"windows", "program files", "program files (x86)",
                "programdata", "$recycle.bin", "system volume information",
                "recovery", "perflogs", "$windows.~bt", "$windows.~ws"}

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["dupes"][2]
        self.folder = None
        self._scanning = False
        self._cancel = False
        self._paths = {}
        self._n_groups, self._wasted = 0, 0
        self._build()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="🗂", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Doublons"), font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        ttk.Label(self, text=t("Trouve les fichiers en double dans un "
                               "dossier, par CONTENU (deux fichiers "
                               "identiques sont détectés même renommés). "
                               "La suppression envoie à la corbeille, donc "
                               "récupérable."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 8), wraplength=780).pack(fill="x")

        ctrl = ttk.Frame(self, padding=(16, 0, 16, 6))
        ctrl.pack(fill="x")
        PBButton(ctrl, text=t("📁 Choisir un dossier"),
                   style="Soft.TButton",
                   command=self.pick_folder).pack(side="left")
        bd = PBButton(ctrl, text=t("💽 Disque entier"),
                        style="Soft.TButton", command=self.pick_drive)
        bd.pack(side="left", padx=6)
        self.drive_btn = bd
        Tooltip(bd, t("Scanner un disque complet (C:, D:, ...).\nAttention "
                      ": sur un gros disque, le scan peut prendre de "
                      "longues minutes."))
        self.folder_lbl = ttk.Label(ctrl, text=t("Aucun dossier choisi"),
                                    style="Dim.TLabel", padding=(10, 0))
        self.folder_lbl.pack(side="left")
        self.scan_btn = PBButton(ctrl, text=t("Lancer le scan"),
                                   style="Blue.TButton", command=self.scan)
        self.scan_btn.pack(side="right")
        self.min_size = tk.BooleanVar(value=True)
        cb = Check(ctrl, t("Ignorer les fichiers < 1 Mo"),
                   variable=self.min_size, accent=self.acc)
        cb.pack(side="right", padx=10)
        Tooltip(cb.lbl, t("Accélère beaucoup le scan en ignorant les petits "
                          "fichiers,\nqui sont rarement ceux qui prennent "
                          "de la place."))
        self.skip_sys = tk.BooleanVar(value=True)
        cb2 = Check(ctrl, t("Ignorer les dossiers système"),
                    variable=self.skip_sys, accent=self.acc)
        cb2.pack(side="right", padx=4)
        Tooltip(cb2.lbl, t("Ignore Windows, Program Files, la corbeille, "
                           "etc.\nRecommandé : ces dossiers contiennent "
                           "des doublons NORMAUX qu'il ne faut pas "
                           "toucher."))

        self.status_lbl = ttk.Label(self, text="", style="Dim.TLabel",
                                    padding=(18, 0, 16, 4))
        self.status_lbl.pack(fill="x")

        self.tree = ttk.Treeview(self, columns=("size", "path"),
                                 show="tree headings", selectmode="extended")
        self.tree.heading("#0", text=t("Fichier"))
        self.tree.column("#0", width=280, anchor="w")
        self.tree.heading("size", text=t("Taille"))
        self.tree.column("size", width=90, anchor="w")
        self.tree.heading("path", text=t("Emplacement"))
        self.tree.column("path", width=440, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        b1 = PBButton(bar, text=t("✔ Tout sélectionner sauf 1 par groupe"),
                        style="Soft.TButton", command=self.auto_select)
        b1.pack(side="left")
        Tooltip(b1, t("Sélectionne automatiquement toutes les copies SAUF "
                      "la plus ancienne de chaque groupe.\nIl te reste "
                      "juste à cliquer sur Corbeille."))
        b2 = PBButton(bar, text=t("🗑 Mettre la sélection à la corbeille"),
                        style="Kill.TButton", command=self.trash_selected)
        b2.pack(side="left", padx=6)
        Tooltip(b2, t("Envoie les fichiers sélectionnés à la corbeille "
                      "Windows.\nRécupérables tant que tu ne vides pas la "
                      "corbeille."))
        b3 = PBButton(bar, text=t("🖼 Ouvrir le fichier"),
                        style="Soft.TButton", command=self.open_file)
        b3.pack(side="left")
        Tooltip(b3, t("Ouvre le fichier sélectionné avec son application "
                      "par défaut.\nAstuce : double-clic sur une ligne "
                      "fait pareil."))
        b4 = PBButton(bar, text=t("📁 Ouvrir l'emplacement"),
                        style="Soft.TButton", command=self.open_location)
        b4.pack(side="left", padx=6)
        Tooltip(b4, t("Ouvre l'explorateur avec le fichier déjà "
                      "sélectionné dedans."))
        self.tree.bind("<Double-1>", self._dblclick)
        ImagePreview(self.tree, lambda iid: self._paths.get(iid))

    def _dblclick(self, e):
        iid = self.tree.identify_row(e.y)
        if iid in self._paths:
            self.open_file()
            return "break"

    def open_file(self):
        sel = self.tree.selection()
        if sel and sel[0] in self._paths:
            path = self._paths[sel[0]]
            if os.path.exists(path):
                os.startfile(path)

    # ---------- scan ----------
    def pick_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(title=t("Dossier à scanner"))
        if folder:
            self.folder = folder
            self.folder_lbl.configure(text=folder)

    def pick_drive(self):
        import shutil
        pop = tk.Toplevel(self)
        pop.overrideredirect(True)
        x = self.drive_btn.winfo_rootx()
        y = self.drive_btn.winfo_rooty() + self.drive_btn.winfo_height() + 4
        pop.geometry(f"+{x}+{y}")
        frame = tk.Frame(pop, bg=BG2, highlightthickness=1,
                         highlightbackground=BG3)
        frame.pack()
        tk.Label(frame, text=t("Choisis un disque à scanner"), bg=BG2,
                 fg=FG_DIM, font=("Segoe UI", 9), anchor="w",
                 padx=14, pady=6).pack(fill="x")

        def choose(root):
            pop.destroy()
            self._set_drive(root)

        for l in string.ascii_uppercase:
            root = f"{l}:\\"
            if not os.path.exists(root):
                continue
            try:
                u = shutil.disk_usage(root)
                info = t("{free} libres sur {total}").format(
                    free=fmt_size(u.free), total=fmt_size(u.total))
            except OSError:
                info = ""
            lbl = tk.Label(frame,
                           text=f"💽  {t('Disque {l}:').format(l=l)}"
                                f"      {info}",
                           bg=BG2, fg=FG, font=("Segoe UI", 11),
                           anchor="w", padx=14, pady=9, cursor="hand2")
            lbl.pack(fill="x")
            lbl.bind("<Enter>", lambda e: e.widget.configure(bg=BG3))
            lbl.bind("<Leave>", lambda e: e.widget.configure(bg=BG2))
            lbl.bind("<Button-1>", lambda e, r=root: choose(r))

        pop.bind("<FocusOut>", lambda e: pop.destroy())
        pop.bind("<Escape>", lambda e: pop.destroy())
        pop.focus_force()

    def _set_drive(self, root):
        self.folder = root
        self.folder_lbl.configure(text=root)
        self.status_lbl.configure(
            text=t("Scan d'un disque complet : ça peut prendre de longues "
                   "minutes. Le bouton ■ arrête en gardant les résultats "
                   "déjà trouvés."))

    def scan(self):
        if self._scanning:
            self._cancel = True
            return
        if not self.folder:
            self.pick_folder()
            if not self.folder:
                return
        self._scanning, self._cancel = True, False
        self._n_groups, self._wasted = 0, 0
        self.scan_btn.configure(text=t("■ Stop (garde les résultats)"))
        self.tree.delete(*self.tree.get_children())
        self._paths.clear()
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _status(self, txt):
        self.after(0, lambda: self.status_lbl.configure(text=txt))

    def _digest(self, path, quick):
        import hashlib
        h = hashlib.sha1()
        try:
            with open(path, "rb") as fh:
                if quick:
                    h.update(fh.read(65536))
                else:
                    for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                        if self._cancel:
                            return None
                        h.update(chunk)
        except OSError:
            return None
        return h.hexdigest()

    def _scan_worker(self):
        min_bytes = 1024 * 1024 if self.min_size.get() else 1
        skip_sys = self.skip_sys.get()
        by_size, n = {}, 0
        for root, dirs, files in os.walk(self.folder):
            if skip_sys:
                dirs[:] = [d for d in dirs
                           if d.lower() not in self.SYS_DIRS]
            if self._cancel:
                return self._scan_done(stopped=True)
            for f in files:
                path = os.path.join(root, f)
                try:
                    sz = os.path.getsize(path)
                except OSError:
                    continue
                if sz >= min_bytes:
                    by_size.setdefault(sz, []).append(path)
                n += 1
                if n % 500 == 0:
                    self._status(t("Parcours... {n} fichiers vus"
                                   ).format(n=n))
                    if self._cancel:
                        return self._scan_done(stopped=True)

        items = sorted(((s, p) for s, p in by_size.items() if len(p) > 1),
                       key=lambda x: -x[0])
        total = sum(len(p) for _, p in items)
        done = 0
        for size, paths in items:
            if self._cancel:
                return self._scan_done(stopped=True)
            quick = {}
            for p in paths:
                done += 1
                status = t("Analyse du contenu... {d}/{t}").format(
                    d=done, t=total)
                if self._n_groups:
                    status += t("  |  {n} groupes trouvés").format(
                        n=self._n_groups)
                self._status(status)
                d = self._digest(p, quick=True)
                if d:
                    quick.setdefault(d, []).append(p)
            for sub in quick.values():
                if len(sub) < 2:
                    continue
                full = {}
                for p in sub:
                    if self._cancel:
                        return self._scan_done(stopped=True)
                    d = self._digest(p, quick=False)
                    if d:
                        full.setdefault(d, []).append(p)
                for same in full.values():
                    if len(same) > 1:
                        self.after(0, lambda s=size, pp=list(same):
                                   self._add_group(s, pp))
        self._scan_done(stopped=False)

    def _add_group(self, size, paths):
        self._n_groups += 1
        self._wasted += size * (len(paths) - 1)
        name = os.path.basename(paths[0])
        parent = self.tree.insert(
            "", "end",
            text=t("{name}  ({n} copies)").format(name=name, n=len(paths)),
            values=(fmt_size(size), ""), open=True)
        for p in paths:
            iid = self.tree.insert(parent, "end",
                                   text=os.path.basename(p),
                                   values=(fmt_size(size),
                                           os.path.dirname(p)))
            self._paths[iid] = p

    def _final_status(self, stopped):
        if self._n_groups:
            prefix = t("Scan arrêté — résultats conservés : ") if stopped \
                else t("Terminé : ")
            self.status_lbl.configure(
                text=t("{p}{n} groupes de doublons, {w} récupérables"
                       ).format(p=prefix, n=self._n_groups,
                                w=fmt_size(self._wasted)))
        else:
            self.status_lbl.configure(
                text=t("Scan arrêté.") if stopped
                else t("Aucun doublon trouvé. 🎉"))

    def _scan_done(self, stopped=False):
        self._scanning = False
        self.after(0, lambda: (
            self.scan_btn.configure(text=t("Lancer le scan")),
            self._final_status(stopped)))

    # ---------- actions ----------
    def auto_select(self):
        self.tree.selection_remove(*self.tree.selection())
        for parent in self.tree.get_children():
            children = self.tree.get_children(parent)
            if len(children) < 2:
                continue
            def mtime(iid):
                try:
                    return os.path.getmtime(self._paths[iid])
                except OSError:
                    return 0
            keep = min(children, key=mtime)
            for c in children:
                if c != keep:
                    self.tree.selection_add(c)

    def trash_selected(self):
        paths = [self._paths[i] for i in self.tree.selection()
                 if i in self._paths]
        if not paths:
            return
        total = 0
        for p in paths:
            try:
                total += os.path.getsize(p)
            except OSError:
                pass
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Envoyer {n} fichier(s) à la corbeille ?\n({s} récupérés)"
                  "\n\nIls resteront récupérables dans la corbeille "
                  "Windows.").format(n=len(paths), s=fmt_size(total))):
            return
        if send_to_trash(paths):
            for i in list(self.tree.selection()):
                if i in self._paths:
                    parent = self.tree.parent(i)
                    self.tree.delete(i)
                    del self._paths[i]
                    if len(self.tree.get_children(parent)) < 2:
                        for c in self.tree.get_children(parent):
                            self._paths.pop(c, None)
                        self.tree.delete(parent)
            self.status_lbl.configure(
                text=t("{n} fichier(s) envoyés à la corbeille, {s} "
                       "récupérés").format(n=len(paths), s=fmt_size(total)))
            log_action(t("Doublons : {n} fichier(s) envoyés à la corbeille "
                         "({s})").format(n=len(paths), s=fmt_size(total)))
        else:
            messagebox.showwarning(
                APP_NAME, t("L'envoi à la corbeille a échoué."))

    def open_location(self):
        sel = self.tree.selection()
        if not sel or sel[0] not in self._paths:
            return
        open_in_explorer(self._paths[sel[0]])


# ======================================================================
#  MODULE : Rangement
# ======================================================================
class TidyModule(ttk.Frame):
    CATEGORIES = {
        "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                   ".svg", ".ico", ".heic", ".tiff"},
        "Vidéos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",
                   ".webm", ".m4v"},
        "Musique": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac",
                    ".wma", ".opus"},
        "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                      ".pptx", ".odt", ".ods", ".txt", ".rtf", ".csv",
                      ".md", ".epub"},
        "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".iso"},
        "Programmes": {".exe", ".msi", ".msix", ".apk", ".bat", ".cmd"},
    }

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["tidy"][2]
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self._plan = []
        self._build()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="🧹", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Rangement"), font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        ttk.Label(self, text=t("Trie les fichiers en vrac d'un dossier "
                               "(Téléchargements par défaut) dans des "
                               "sous-dossiers par type : Images, Vidéos, "
                               "Documents... Analyse d'abord, rien ne "
                               "bouge sans ton accord, et le dernier "
                               "rangement est annulable."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 8), wraplength=780).pack(fill="x")

        ctrl = ttk.Frame(self, padding=(16, 0, 16, 6))
        ctrl.pack(fill="x")
        PBButton(ctrl, text=t("📁 Changer de dossier"),
                   style="Soft.TButton",
                   command=self.pick_folder).pack(side="left")
        self.folder_lbl = ttk.Label(ctrl, text=self.folder,
                                    style="Dim.TLabel", padding=(10, 0))
        self.folder_lbl.pack(side="left")
        self.tidy_btn = PBButton(ctrl, text=t("🧹 Ranger"),
                                   style="Green.TButton", command=self.tidy,
                                   state="disabled")
        self.tidy_btn.pack(side="right")
        Tooltip(self.tidy_btn, t("Déplace les fichiers selon le plan "
                                 "affiché ci-dessous.\nActif après une "
                                 "analyse."))
        ab = PBButton(ctrl, text=t("🔍 Analyser"), style="Blue.TButton",
                        command=self.analyse)
        ab.pack(side="right", padx=6)
        Tooltip(ab, t("Montre ce qui serait déplacé et où.\nRIEN ne bouge "
                      "à cette étape."))
        self.by_year = tk.BooleanVar(value=False)
        cb = Check(ctrl, t("Sous-dossiers par année"),
                   variable=self.by_year, accent=self.acc)
        cb.pack(side="right", padx=10)
        Tooltip(cb.lbl, t("Range aussi par année de modification :\n"
                          "Images/2025, Images/2026, etc."))

        self.status_lbl = ttk.Label(self, text="", style="Dim.TLabel",
                                    padding=(18, 0, 16, 4))
        self.status_lbl.pack(fill="x")

        self.tree = ttk.Treeview(self, columns=("cat", "dest"),
                                 show="tree headings", selectmode="browse")
        self.tree.heading("#0", text=t("Fichier"))
        self.tree.column("#0", width=300, anchor="w")
        self.tree.heading("cat", text=t("Catégorie"))
        self.tree.column("cat", width=110, anchor="w")
        self.tree.heading("dest", text=t("Destination"))
        self.tree.column("dest", width=400, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        ub = PBButton(bar, text=t("↩ Annuler le dernier rangement"),
                        style="Soft.TButton", command=self.undo)
        ub.pack(side="left")
        Tooltip(ub, t("Remet à leur place d'origine les fichiers déplacés "
                      "lors du DERNIER rangement."))

    def pick_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(title=t("Dossier à ranger"),
                                         initialdir=self.folder)
        if folder:
            self.folder = folder
            self.folder_lbl.configure(text=folder)
            self._plan = []
            self.tree.delete(*self.tree.get_children())
            self.tidy_btn.configure(state="disabled")

    def _category(self, ext):
        for cat, exts in self.CATEGORIES.items():
            if ext in exts:
                return cat
        return "Autres"

    def analyse(self):
        self.tree.delete(*self.tree.get_children())
        self._plan = []
        if not os.path.isdir(self.folder):
            self.status_lbl.configure(text=t("Dossier introuvable."))
            return
        for f in sorted(os.listdir(self.folder), key=str.lower):
            src = os.path.join(self.folder, f)
            if not os.path.isfile(src):
                continue
            ext = os.path.splitext(f)[1].lower()
            cat = self._category(ext)
            sub = t(cat)
            if self.by_year.get():
                try:
                    year = time.localtime(os.path.getmtime(src)).tm_year
                    sub = os.path.join(t(cat), str(year))
                except OSError:
                    pass
            dest = os.path.join(self.folder, sub, f)
            self._plan.append((src, cat, dest))
        nodes = {}
        for src, cat, dest in self._plan:
            if cat not in nodes:
                nodes[cat] = self.tree.insert("", "end",
                                              text=f"📂 {t(cat)}",
                                              values=("", ""), open=True)
            self.tree.insert(nodes[cat], "end",
                             text=os.path.basename(src),
                             values=(t(cat), os.path.dirname(dest)))
        if self._plan:
            self.status_lbl.configure(
                text=t("{n} fichiers à ranger dans {c} catégories. Vérifie "
                       "le plan puis clique sur Ranger.").format(
                    n=len(self._plan), c=len(nodes)))
            self.tidy_btn.configure(state="normal")
        else:
            self.status_lbl.configure(
                text=t("Rien à ranger : aucun fichier en vrac dans ce "
                       "dossier. 🎉"))
            self.tidy_btn.configure(state="disabled")

    def _unique(self, dest):
        if not os.path.exists(dest):
            return dest
        base, ext = os.path.splitext(dest)
        i = 2
        while os.path.exists(f"{base} ({i}){ext}"):
            i += 1
        return f"{base} ({i}){ext}"

    def tidy(self):
        if not self._plan:
            return
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Déplacer {n} fichiers selon le plan affiché ?\n\n"
                  "Annulable ensuite avec le bouton ↩.").format(
                    n=len(self._plan))):
            return
        import shutil
        journal, errs = [], 0
        for src, cat, dest in self._plan:
            try:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                final = self._unique(dest)
                shutil.move(src, final)
                journal.append({"from": final, "to": src})
            except OSError:
                errs += 1
        cfg = load_config()
        cfg["tidy_last"] = journal
        save_config(cfg)
        self._plan = []
        self.tree.delete(*self.tree.get_children())
        self.tidy_btn.configure(state="disabled")
        log_action(t("Rangement : {n} fichiers déplacés"
                     ).format(n=len(journal)))
        msg = t("{n} fichiers rangés").format(n=len(journal))
        if errs:
            msg += t(", {e} échecs (fichiers utilisés ?)").format(e=errs)
        self.status_lbl.configure(text=msg + ".")

    def undo(self):
        cfg = load_config()
        journal = cfg.get("tidy_last") or []
        if not journal:
            messagebox.showinfo(APP_NAME, t("Aucun rangement à annuler."))
            return
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Remettre {n} fichiers à leur emplacement d'origine ?"
                  ).format(n=len(journal))):
            return
        import shutil
        back, errs = 0, 0
        for mv in journal:
            try:
                if os.path.exists(mv["from"]):
                    os.makedirs(os.path.dirname(mv["to"]), exist_ok=True)
                    shutil.move(mv["from"], self._unique(mv["to"]))
                    back += 1
                else:
                    errs += 1
            except OSError:
                errs += 1
        cfg["tidy_last"] = []
        save_config(cfg)
        log_action(t("Rangement annulé : {n} fichiers remis en place"
                     ).format(n=back))
        msg = t("{n} fichiers remis en place").format(n=back)
        if errs:
            msg += t(", {e} introuvables ou bloqués").format(e=errs)
        self.status_lbl.configure(text=msg + ".")
        for cat in list(self.CATEGORIES) + ["Autres"]:
            for name in (cat, t(cat)):
                p = os.path.join(self.folder, name)
                try:
                    for root, dirs, files in os.walk(p, topdown=False):
                        if not dirs and not files:
                            os.rmdir(root)
                except OSError:
                    pass


# ======================================================================
#  MODULE : Nettoyage
# ======================================================================
def recycle_bin_info():
    """(taille en octets, nombre d'éléments) de la corbeille."""
    import ctypes

    class SHQUERYRBINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("i64Size", ctypes.c_longlong),
                    ("i64NumItems", ctypes.c_longlong)]

    info = SHQUERYRBINFO()
    info.cbSize = ctypes.sizeof(info)
    try:
        ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
        return info.i64Size, info.i64NumItems
    except Exception:
        return 0, 0


def empty_recycle_bin():
    import ctypes
    # 1=no confirm, 2=no progress ui, 4=no sound
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        return True
    except Exception:
        return False


class CleanModule(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["clean"][2]
        self._sizes = {}
        self._working = False
        self._build()

    CATS = ["usertemp", "wintemp", "bin", "browsers", "thumbs", "update"]
    CAT_LABELS = {
        "usertemp": "Fichiers temporaires (utilisateur)",
        "wintemp": "Fichiers temporaires Windows",
        "bin": "Corbeille",
        "browsers": "Caches des navigateurs",
        "thumbs": "Cache des miniatures",
        "update": "Restes de Windows Update",
    }

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="🧽", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Nettoyage"), font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        self.clean_btn = PBButton(head, text=t("🧹 Nettoyer la sélection"),
                                    style="Kill.TButton", command=self.clean,
                                    state="disabled")
        self.clean_btn.pack(side="right")
        Tooltip(self.clean_btn,
                t("Supprime définitivement le contenu des catégories "
                  "cochées.\nActif après une analyse."))
        ab = PBButton(head, text=t("🔍 Analyser"), style="Blue.TButton",
                        command=self.analyse)
        ab.pack(side="right", padx=6)
        Tooltip(ab, t("Calcule la taille récupérable de chaque catégorie.\n"
                      "RIEN n'est supprimé à cette étape."))
        ttk.Label(self, text=t("Libère de l'espace disque en supprimant ce "
                               "qui ne sert plus : fichiers temporaires, "
                               "caches, corbeille. Analyse d'abord pour "
                               "voir ce qui est récupérable, rien n'est "
                               "supprimé sans ton accord."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 8), wraplength=780).pack(fill="x")

        self.rows = {}
        box = ttk.Frame(self, padding=(16, 0))
        box.pack(fill="x")
        for key in self.CATS:
            row = ctk.CTkFrame(box, fg_color=BG2, corner_radius=10)
            row.pack(fill="x", pady=3)
            var = tk.BooleanVar(value=True)
            cb = Check(row, t(self.CAT_LABELS[key]), variable=var,
                       accent=self.acc, bg=BG2)
            cb.pack(side="left", padx=12, pady=8)
            size_lbl = tk.Label(row, text="—", bg=BG2, fg=FG_DIM,
                                font=("Segoe UI", 10, "bold"))
            size_lbl.pack(side="right", padx=14)
            det = tk.Label(row, text="🔎", bg=BG2, fg=FG_DIM,
                           cursor="hand2", font=("Segoe UI Emoji", 11))
            det.pack(side="right", padx=4)
            det.bind("<Button-1>",
                     lambda e, k=key: self.show_details(k))
            Tooltip(det, t("Voir le détail de ce qui sera nettoyé."))
            self.rows[key] = {"var": var, "lbl": size_lbl, "det": det}

        self.status_lbl = ttk.Label(
            self,
            text=t("Astuce : ferme les navigateurs avant de nettoyer "
                   "leurs caches, et lance {app} en admin pour les "
                   "catégories Windows.").format(app=APP_NAME),
            style="Dim.TLabel", padding=(18, 8, 16, 4), wraplength=780)
        self.status_lbl.pack(fill="x", anchor="w")

    # ---------- chemins ----------
    def _cat_paths(self, key):
        import glob
        import tempfile
        env = os.environ.get
        winroot = env("SystemRoot", r"C:\Windows")
        la = env("LOCALAPPDATA", "")
        if key == "usertemp":
            return [tempfile.gettempdir()]
        if key == "wintemp":
            return [os.path.join(winroot, "Temp")]
        if key == "update":
            return [os.path.join(winroot, "SoftwareDistribution",
                                 "Download")]
        if key == "browsers":
            out = []
            for pat in (r"Google\Chrome\User Data\*\Cache",
                        r"Google\Chrome\User Data\*\Code Cache",
                        r"Microsoft\Edge\User Data\*\Cache",
                        r"Microsoft\Edge\User Data\*\Code Cache",
                        r"BraveSoftware\Brave-Browser\User Data\*\Cache",
                        r"BraveSoftware\Brave-Browser\User Data\*"
                        r"\Code Cache",
                        r"Mozilla\Firefox\Profiles\*\cache2"):
                out += glob.glob(os.path.join(la, pat))
            return [p for p in out if os.path.isdir(p)]
        return []

    def _thumb_files(self):
        import glob
        la = os.environ.get("LOCALAPPDATA", "")
        base = os.path.join(la, r"Microsoft\Windows\Explorer")
        return (glob.glob(os.path.join(base, "thumbcache_*.db"))
                + glob.glob(os.path.join(base, "iconcache_*.db")))

    @staticmethod
    def _dir_size_collect(folder, bucket):
        total = 0
        for root, dirs, files in os.walk(folder):
            for f in files:
                p = os.path.join(root, f)
                try:
                    s = os.path.getsize(p)
                except OSError:
                    continue
                total += s
                bucket.append((s, p))
        return total

    # ---------- analyse ----------
    def analyse(self):
        if self._working:
            return
        self._working = True
        self._details = {}
        self.clean_btn.configure(state="disabled")

        def worker():
            total = 0
            for key in self.CATS:
                self._set_status(t("Analyse de {c}...").format(
                    c=t(self.CAT_LABELS[key])))
                bucket = []
                if key == "bin":
                    size, _ = recycle_bin_info()
                elif key == "thumbs":
                    size = 0
                    for f in self._thumb_files():
                        try:
                            s = os.path.getsize(f)
                            size += s
                            bucket.append((s, f))
                        except OSError:
                            pass
                else:
                    size = 0
                    for p in self._cat_paths(key):
                        size += self._dir_size_collect(p, bucket)
                        bucket.sort(key=lambda x: -x[0])
                        del bucket[500:]
                bucket.sort(key=lambda x: -x[0])
                self._details[key] = bucket[:200]
                self._sizes[key] = size
                total += size
                self.after(0, lambda k=key, s=size: (
                    self.rows[k]["lbl"].configure(
                        text=fmt_size(s), fg=FG if s else FG_DIM),
                    self.rows[k]["det"].configure(
                        fg=self.acc if s else FG_DIM)))
            self._working = False
            self.after(0, lambda: (
                self.clean_btn.configure(state="normal"),
                self.status_lbl.configure(
                    text=t("{s} récupérables au total. Coche ce que tu "
                           "veux nettoyer.").format(s=fmt_size(total)))))
        threading.Thread(target=worker, daemon=True).start()

    def show_details(self, key):
        if key == "bin":
            win = tk.Toplevel(self)
            win.title(t("Détail — {c}").format(c=t(self.CAT_LABELS[key])))
            win.configure(bg=BG)
            win.geometry("400x160")
            setup_window(win)
            ttk.Label(win, text=t("Ouvre la corbeille Windows pour voir "
                                  "son contenu."),
                      padding=(16, 16), wraplength=360).pack(anchor="w")
            PBButton(win, text=t("🗑 Ouvrir la corbeille"),
                       style="Blue.TButton",
                       command=lambda: os.startfile(
                           "shell:RecycleBinFolder")).pack(pady=8)
            return
        items = getattr(self, "_details", {}).get(key)
        if not items:
            return
        win = tk.Toplevel(self)
        win.title(t("Détail — {c}").format(c=t(self.CAT_LABELS[key])))
        win.configure(bg=BG)
        win.geometry("780x520")
        setup_window(win)
        ttk.Label(win, text=t("Les {n} plus gros éléments de cette "
                              "catégorie :").format(n=len(items)),
                  style="Dim.TLabel", padding=(12, 10, 12, 4)
                  ).pack(anchor="w")
        tree = ttk.Treeview(win, columns=("size", "path"), show="headings")
        tree.heading("size", text=t("Taille"))
        tree.column("size", width=90, anchor="w")
        tree.heading("path", text=t("Emplacement"))
        tree.column("path", width=630, anchor="w")
        tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        sb = PBScroll(tree, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        for s, p in items:
            tree.insert("", "end", values=(fmt_size(s), p))

    @staticmethod
    def _delete_contents(folder):
        freed = 0
        for root, dirs, files in os.walk(folder, topdown=False):
            for f in files:
                p = os.path.join(root, f)
                try:
                    s = os.path.getsize(p)
                    os.remove(p)
                    freed += s
                except OSError:
                    pass
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except OSError:
                    pass
        return freed

    def _set_status(self, txt):
        self.after(0, lambda: self.status_lbl.configure(text=txt))

    # ---------- nettoyage ----------
    def clean(self):
        if self._working:
            return
        checked = [k for k in self.CATS if self.rows[k]["var"].get()]
        if not checked:
            return
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Nettoyer les catégories cochées ?\n\nLes fichiers "
                  "seront définitivement supprimés (la corbeille, elle, "
                  "sera simplement vidée). Les fichiers en cours "
                  "d'utilisation seront ignorés.")):
            return
        self._working = True
        self.clean_btn.configure(state="disabled")

        def worker():
            freed = 0
            for key in checked:
                self._set_status(t("Nettoyage... {c}").format(
                    c=t(self.CAT_LABELS[key])))
                if key == "bin":
                    before, _ = recycle_bin_info()
                    empty_recycle_bin()
                    after, _ = recycle_bin_info()
                    freed += max(0, before - after)
                elif key == "thumbs":
                    for f in self._thumb_files():
                        try:
                            s = os.path.getsize(f)
                            os.remove(f)
                            freed += s
                        except OSError:
                            pass
                else:
                    for p in self._cat_paths(key):
                        freed += self._delete_contents(p)
                self.after(0, lambda k=key:
                           self.rows[k]["lbl"].configure(text="—",
                                                         fg=FG_DIM))
            self._working = False
            names = ", ".join(t(self.CAT_LABELS[k]) for k in checked)
            log_action(t("Nettoyage : {s} libérés ({c})").format(
                s=fmt_size(freed), c=names))
            self.after(0, lambda: self.status_lbl.configure(
                text=t("Nettoyage terminé : {s} libérés.").format(
                    s=fmt_size(freed))))
        threading.Thread(target=worker, daemon=True).start()


# ======================================================================
#  MODULE : Espace disque
# ======================================================================
class DiskModule(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["disk"][2]
        self.folder = os.environ.get("SystemDrive", "C:") + "\\"
        self._scanning = False
        self._cancel = False
        self._dir_sizes = {}
        self._big_files = []
        self._paths = {}          # iid -> chemin (les deux vues)
        self._view = "folders"
        self._counts = (0, 0)
        self._build()
        self._smart_check()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="💾", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Espace disque"),
                  font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        self.scan_btn = PBButton(head, text=t("Lancer le scan"),
                                   style="Blue.TButton", command=self.scan)
        self.scan_btn.pack(side="right")
        ttk.Label(self, text=t("Analyse un disque ou un dossier et montre "
                               "où part la place : les dossiers les plus "
                               "lourds (navigables) et les plus gros "
                               "fichiers. Pratique pour répondre à "
                               "« pourquoi mon disque est plein ? »."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 6), wraplength=780).pack(fill="x")

        ctrl = ttk.Frame(self, padding=(16, 0, 16, 4))
        ctrl.pack(fill="x")
        PBButton(ctrl, text=t("📁 Choisir un dossier"),
                   style="Soft.TButton",
                   command=self.pick_folder).pack(side="left")
        bd = PBButton(ctrl, text=t("💽 Disque entier"),
                        style="Soft.TButton", command=self.pick_drive)
        bd.pack(side="left", padx=6)
        self.drive_btn = bd
        self.folder_lbl = ttk.Label(ctrl, text=self.folder,
                                    style="Dim.TLabel", padding=(10, 0))
        self.folder_lbl.pack(side="left")
        self.files_tab = PBButton(ctrl, text=t("📄 Plus gros fichiers"),
                                    style="Soft.TButton",
                                    command=lambda: self._switch("files"))
        self.files_tab.pack(side="right")
        self.folders_tab = PBButton(ctrl, text=t("📂 Dossiers"),
                                      style="Blue.TButton",
                                      command=lambda:
                                      self._switch("folders"))
        self.folders_tab.pack(side="right", padx=6)

        self.status_lbl = ttk.Label(self, text="", style="Dim.TLabel",
                                    padding=(18, 0, 16, 2))
        self.status_lbl.pack(fill="x")
        self.smart_lbl = ttk.Label(self, text="", style="Dim.TLabel",
                                   padding=(18, 0, 16, 4))
        self.smart_lbl.pack(fill="x")

        self.tree = ttk.Treeview(self, columns=("size", "path"),
                                 show="tree headings", selectmode="browse")
        self.tree.heading("#0", text=t("Nom"))
        self.tree.column("#0", width=300, anchor="w")
        self.tree.heading("size", text=t("Taille"))
        self.tree.column("size", width=100, anchor="w")
        self.tree.heading("path", text=t("Emplacement"))
        self.tree.column("path", width=420, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))
        self.tree.bind("<<TreeviewOpen>>", self._on_open)
        self.tree.bind("<Button-3>", self._popup)
        self.tree.bind("<Double-1>", self._dblclick)

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        b1 = PBButton(bar, text=t("📁 Ouvrir l'emplacement"),
                        style="Soft.TButton", command=self.open_location)
        b1.pack(side="left")
        Tooltip(b1, t("Ouvre l'explorateur avec le fichier déjà "
                      "sélectionné dedans."))
        b2 = PBButton(bar, text=t("🗑 Mettre à la corbeille"),
                        style="Kill.TButton", command=self.trash_selected)
        b2.pack(side="left", padx=6)
        Tooltip(b2, t("Envoie le fichier sélectionné (vue Fichiers) à la "
                      "corbeille Windows."))

    # ---------- santé disques ----------
    def _smart_check(self):
        if sys.platform != "win32":
            return

        def worker():
            try:
                flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                out = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "Get-PhysicalDisk | ForEach-Object { "
                     "$_.FriendlyName + '|' + $_.HealthStatus }"],
                    capture_output=True, text=True, timeout=15,
                    creationflags=flags).stdout
                disks = [l.split("|") for l in out.splitlines()
                         if "|" in l]
                if not disks:
                    return
                bad = [f"{n} ({h})" for n, h in disks
                       if h.strip().lower() != "healthy"]
                if bad:
                    txt, color = t("Santé des disques à surveiller : {d}"
                                   ).format(d=", ".join(bad)), "#f0b64f"
                else:
                    txt, color = t("Santé des disques : OK"), "#4fbf78"
                self.after(0, lambda: self.smart_lbl.configure(
                    text="💚 " + txt if not bad else "⚠ " + txt,
                    foreground=color))
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()

    # ---------- sélection cible ----------
    def pick_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(title=t("Dossier à scanner"))
        if folder:
            self.folder = folder
            self.folder_lbl.configure(text=folder)

    def pick_drive(self):
        import shutil
        pop = tk.Toplevel(self)
        pop.overrideredirect(True)
        x = self.drive_btn.winfo_rootx()
        y = self.drive_btn.winfo_rooty() + self.drive_btn.winfo_height() + 4
        pop.geometry(f"+{x}+{y}")
        frame = tk.Frame(pop, bg=BG2, highlightthickness=1,
                         highlightbackground=BG3)
        frame.pack()
        tk.Label(frame, text=t("Choisis un disque à scanner"), bg=BG2,
                 fg=FG_DIM, font=("Segoe UI", 9), anchor="w",
                 padx=14, pady=6).pack(fill="x")

        def choose(root):
            pop.destroy()
            self.folder = root
            self.folder_lbl.configure(text=root)

        for l in string.ascii_uppercase:
            root = f"{l}:\\"
            if not os.path.exists(root):
                continue
            try:
                u = shutil.disk_usage(root)
                info = t("{free} libres sur {total}").format(
                    free=fmt_size(u.free), total=fmt_size(u.total))
            except OSError:
                info = ""
            lbl = tk.Label(frame,
                           text=f"💽  {t('Disque {l}:').format(l=l)}"
                                f"      {info}",
                           bg=BG2, fg=FG, font=("Segoe UI", 11),
                           anchor="w", padx=14, pady=9, cursor="hand2")
            lbl.pack(fill="x")
            lbl.bind("<Enter>", lambda e: e.widget.configure(bg=BG3))
            lbl.bind("<Leave>", lambda e: e.widget.configure(bg=BG2))
            lbl.bind("<Button-1>", lambda e, r=root: choose(r))
        pop.bind("<FocusOut>", lambda e: pop.destroy())
        pop.bind("<Escape>", lambda e: pop.destroy())
        pop.focus_force()

    # ---------- scan ----------
    def scan(self):
        if self._scanning:
            self._cancel = True
            return
        self._scanning, self._cancel = True, False
        self.scan_btn.configure(text=t("■ Stop (garde les résultats)"))
        self._dir_sizes, self._big_files = {}, []
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        target = os.path.normpath(self.folder)
        skip = {"$recycle.bin", "system volume information"}
        dir_local = {}
        big, n_files, n_dirs = [], 0, 0
        stopped = False
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d.lower() not in skip]
            n_dirs += 1
            if self._cancel:
                stopped = True
                break
            local = 0
            for f in files:
                p = os.path.join(root, f)
                try:
                    s = os.path.getsize(p)
                except OSError:
                    continue
                local += s
                n_files += 1
                big.append((s, p))
                if len(big) > 3000:
                    big.sort(key=lambda x: -x[0])
                    del big[300:]
                if n_files % 2000 == 0:
                    self.after(0, lambda n=n_files:
                               self.status_lbl.configure(
                                   text=t("Parcours... {n} fichiers vus"
                                          ).format(n=n)))
            dir_local[root] = dir_local.get(root, 0) + local

        # propager les tailles aux dossiers parents
        sizes = dict(dir_local)
        for path in sorted(dir_local, key=len, reverse=True):
            parent = os.path.dirname(path)
            if len(parent) >= len(target) and parent != path:
                sizes[parent] = sizes.get(parent, 0) + sizes[path]
        big.sort(key=lambda x: -x[0])
        self._dir_sizes = sizes
        self._big_files = big[:200]
        self._counts = (n_dirs, n_files)
        self._scanning = False
        self.after(0, lambda: (
            self.scan_btn.configure(text=t("Lancer le scan")),
            self.status_lbl.configure(
                text=t("Scan arrêté — résultats partiels.") if stopped
                else t("Terminé : {d} dossiers et {f} fichiers analysés."
                       ).format(d=n_dirs, f=n_files)),
            self._fill()))

    # ---------- affichage ----------
    def _switch(self, view):
        self._view = view
        self.folders_tab.configure(
            style="Blue.TButton" if view == "folders" else "Soft.TButton")
        self.files_tab.configure(
            style="Blue.TButton" if view == "files" else "Soft.TButton")
        self._fill()

    def _children_of(self, folder):
        out = []
        try:
            for name in os.listdir(folder):
                p = os.path.join(folder, name)
                if os.path.isdir(p) and p in self._dir_sizes:
                    out.append((self._dir_sizes[p], name, p))
        except OSError:
            pass
        out.sort(key=lambda x: -x[0])
        return out

    def _insert_dir(self, parent_iid, size, name, path):
        iid = self.tree.insert(parent_iid, "end", text=f"📂 {name}",
                               values=(fmt_size(size),
                                       os.path.dirname(path)))
        self._paths[iid] = path
        if self._children_of(path):
            self.tree.insert(iid, "end", text="...")   # enfant factice
        return iid

    def _on_open(self, _):
        iid = self.tree.focus()
        path = self._paths.get(iid)
        if not path:
            return
        kids = self.tree.get_children(iid)
        if len(kids) == 1 and self.tree.item(kids[0], "text") == "...":
            self.tree.delete(kids[0])
            for size, name, p in self._children_of(path):
                self._insert_dir(iid, size, name, p)

    def _fill(self):
        self.tree.delete(*self.tree.get_children())
        self._paths.clear()
        if self._view == "folders":
            target = os.path.normpath(self.folder)
            for size, name, p in self._children_of(target):
                self._insert_dir("", size, name, p)
        else:
            for s, p in self._big_files:
                iid = self.tree.insert("", "end",
                                       text=os.path.basename(p),
                                       values=(fmt_size(s),
                                               os.path.dirname(p)))
                self._paths[iid] = p

    # ---------- actions ----------
    def _popup(self, event):
        iid = self.tree.identify_row(event.y)
        if not iid or iid not in self._paths:
            return
        self.tree.selection_set(iid)
        path = self._paths[iid]
        menu = tk.Menu(self, tearoff=0, bg=BG3, fg=FG,
                       activebackground="#3d3e49",
                       activeforeground="#ffffff")
        menu.add_command(label=t("📁 Ouvrir l'emplacement"),
                         command=self.open_location)
        if os.path.isfile(path):
            menu.add_command(label=t("🖼 Ouvrir le fichier"),
                             command=self.open_file)
            menu.add_separator()
            menu.add_command(label=t("🗑 Mettre à la corbeille"),
                             command=self.trash_selected)
        menu.tk_popup(event.x_root, event.y_root)

    def _dblclick(self, event):
        iid = self.tree.identify_row(event.y)
        path = self._paths.get(iid)
        if path and os.path.isfile(path):
            os.startfile(path)
            return "break"

    def open_file(self):
        sel = self.tree.selection()
        if sel and sel[0] in self._paths:
            path = self._paths[sel[0]]
            if os.path.isfile(path):
                os.startfile(path)

    def open_location(self):
        sel = self.tree.selection()
        if sel and sel[0] in self._paths:
            open_in_explorer(self._paths[sel[0]])

    def trash_selected(self):
        sel = self.tree.selection()
        if not sel or sel[0] not in self._paths:
            return
        path = self._paths[sel[0]]
        if not os.path.isfile(path):
            return   # on ne met pas des dossiers entiers à la corbeille
        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0
        if not messagebox.askyesno(
                t("Confirmation"),
                t("Envoyer « {n} » à la corbeille ?\n({s})").format(
                    n=os.path.basename(path), s=fmt_size(size))):
            return
        if send_to_trash([path]):
            log_action(t("Espace disque : « {n} » envoyé à la corbeille "
                         "({s})").format(n=os.path.basename(path),
                                         s=fmt_size(size)))
            self.tree.delete(sel[0])
            del self._paths[sel[0]]
        else:
            messagebox.showwarning(
                APP_NAME, t("L'envoi à la corbeille a échoué."))


# ======================================================================
#  MODULE : Wi-Fi
# ======================================================================
class WifiModule(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.acc = MOD_COLORS["wifi"][2]
        self._profiles = []
        self._show = False
        self._build()
        self.refresh()

    def _build(self):
        head = ttk.Frame(self, padding=(16, 14, 16, 2))
        head.pack(fill="x")
        PBButton(head, text=t("← Accueil"), style="Soft.TButton",
                   command=lambda: self.app.show("home")
                   ).pack(side="left", padx=(0, 12))
        tk.Label(head, text="📶", bg=BG, fg=self.acc,
                 font=("Segoe UI Emoji", 18)).pack(side="left")
        ttk.Label(head, text=t("Wi-Fi"), font=("Segoe UI", 17, "bold"),
                  padding=(8, 0)).pack(side="left")
        PBButton(head, text=t("⟳ Rafraîchir"), style="Soft.TButton",
                   command=self.refresh).pack(side="right")
        ttk.Label(self, text=t("Tous les réseaux Wi-Fi que ce PC connaît, "
                               "avec leur mot de passe enregistré. Pratique "
                               "quand on te demande « c'est quoi le code du "
                               "wifi ? »."),
                  style="Dim.TLabel",
                  padding=(18, 2, 16, 10), wraplength=760).pack(fill="x")

        cols = ("ssid", "auth", "key")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                 selectmode="browse")
        for c, txt, w in (("ssid", t("Réseau"), 260),
                          ("auth", t("Sécurité"), 140),
                          ("key", t("Mot de passe"), 320)):
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 4))

        sb = PBScroll(self.tree, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        bar = ttk.Frame(self, padding=(16, 6, 16, 12))
        bar.pack(fill="x")
        self.show_btn = PBButton(bar,
                                   text=t("👁 Afficher les mots de passe"),
                                   style="Blue.TButton",
                                   command=self.toggle_show)
        self.show_btn.pack(side="left")
        Tooltip(self.show_btn,
                t("Affiche ou masque les mots de passe dans la liste."))
        b2 = PBButton(bar, text=t("📋 Copier le mot de passe"),
                        style="Soft.TButton", command=self.copy_key)
        b2.pack(side="left", padx=6)
        Tooltip(b2, t("Copie le mot de passe du réseau sélectionné dans "
                      "le presse-papier."))
        self.count_lbl = ttk.Label(bar, text="", style="Dim.TLabel")
        self.count_lbl.pack(side="right")

    def refresh(self):
        import tempfile
        import glob
        import shutil
        import xml.etree.ElementTree as ET
        self._profiles = []
        if sys.platform == "win32":
            tmp = tempfile.mkdtemp(prefix="probox_wifi_")
            try:
                flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                subprocess.run(
                    ["netsh", "wlan", "export", "profile", "key=clear",
                     f"folder={tmp}"],
                    capture_output=True, creationflags=flags)
                ns = {"w": "http://www.microsoft.com/networking/WLAN/"
                           "profile/v1"}
                for f in glob.glob(os.path.join(tmp, "*.xml")):
                    try:
                        root = ET.parse(f).getroot()
                        name = root.findtext("w:name", namespaces=ns) or "?"
                        auth = root.findtext(".//w:authentication",
                                             namespaces=ns) or "?"
                        key = root.findtext(".//w:keyMaterial",
                                            namespaces=ns) or ""
                        self._profiles.append(
                            {"name": name, "auth": auth, "key": key})
                    except ET.ParseError:
                        continue
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        self._profiles.sort(key=lambda p: p["name"].lower())
        self._fill()

    def _fill(self):
        self.tree.delete(*self.tree.get_children())
        for p in self._profiles:
            if not p["key"]:
                shown = t("(réseau ouvert)")
            elif self._show:
                shown = p["key"]
            else:
                shown = "•" * 10
            self.tree.insert("", "end",
                             values=(p["name"], p["auth"], shown))
        txt = t("{n} réseaux enregistrés").format(n=len(self._profiles))
        if not self._profiles or not any(p["key"] for p in self._profiles):
            txt = t("Aucun réseau ou mots de passe invisibles ? Relance "
                    "{app} en administrateur.").format(app=APP_NAME)
        self.count_lbl.configure(text=txt)

    def toggle_show(self):
        self._show = not self._show
        self.show_btn.configure(
            text=t("🙈 Masquer les mots de passe") if self._show
            else t("👁 Afficher les mots de passe"))
        self._fill()

    def copy_key(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        if idx >= len(self._profiles):
            return
        p = self._profiles[idx]
        if p["key"]:
            self.clipboard_clear()
            self.clipboard_append(p["key"])
            self.count_lbl.configure(
                text=t("Mot de passe copié : {n}").format(n=p["name"]))


# ======================================================================
#  PAGE D'ACCUEIL
# ======================================================================
MODULES = [
    ("startup", "🚀", "Démarrage",
     "Voir et contrôler tout ce qui se lance à l'ouverture de Windows."),
    ("network", "📡", "Réseau",
     "Quelle application utilise ta connexion, combien, et vers où."),
    ("dupes", "🗂", "Doublons",
     "Trouver les fichiers en double par contenu, pas juste par nom."),
    ("tidy", "🧹", "Rangement",
     "Trier automatiquement le bazar du dossier Téléchargements."),
    ("wifi", "📶", "Wi-Fi",
     "Retrouver les mots de passe des réseaux Wi-Fi enregistrés sur ce PC."),
    ("clean", "🧽", "Nettoyage",
     "Libérer de l'espace : fichiers temporaires, caches, corbeille."),
    ("disk", "💾", "Espace disque",
     "Trouver ce qui remplit ton disque : plus gros dossiers et fichiers."),
]


class HomePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        brand = ctk.CTkFrame(self, fg_color="transparent")
        brand.pack(fill="x", padx=24, pady=(18, 0))
        ctk.CTkLabel(brand, text="🧰", font=("Segoe UI Emoji", 26)
                     ).pack(side="left")
        ctk.CTkLabel(brand, text=APP_NAME,
                     font=("Segoe UI", 24, "bold")).pack(side="left",
                                                         padx=(10, 4))
        ctk.CTkLabel(brand, text=f"v{APP_VERSION}", text_color=FG_DIM,
                     font=("Segoe UI", 12)).pack(side="left",
                                                 pady=(10, 0))
        lb = ctk.CTkButton(brand,
                           text="🌐 EN" if LANG == "fr" else "🌐 FR",
                           width=76, height=32, corner_radius=10,
                           fg_color=BG3, hover_color="#333540",
                           text_color=FG, font=("Segoe UI", 12),
                           command=app.switch_lang)
        lb.pack(side="right")
        hb = ctk.CTkButton(brand, text=t("📜 Historique"),
                           width=110, height=32, corner_radius=10,
                           fg_color=BG3, hover_color="#333540",
                           text_color=FG, font=("Segoe UI", 12),
                           command=lambda: show_history(app))
        hb.pack(side="right", padx=8)

        h = time.localtime().tm_hour
        hello = t("Bonjour") if 5 <= h < 18 else t("Bonsoir")
        ctk.CTkLabel(self,
                     text=t("{h} ! Choisis un module pour commencer."
                            ).format(h=hello),
                     text_color=FG_DIM, font=("Segoe UI", 12),
                     anchor="w").pack(fill="x", padx=26, pady=(6, 8))

        # carte état du PC (temps réel)
        state = ctk.CTkFrame(self, fg_color=BG2, corner_radius=14)
        state.pack(fill="x", padx=24, pady=(0, 12))
        self._dot = ctk.CTkLabel(state, text="●", text_color=FG_DIM,
                                 font=("Segoe UI", 16), width=20)
        self._dot.pack(side="left", padx=(16, 10), pady=12)
        col = ctk.CTkFrame(state, fg_color="transparent")
        col.pack(side="left", pady=10)
        self._state_lbl = ctk.CTkLabel(col, text="…", text_color=FG,
                                       font=("Segoe UI", 12, "bold"),
                                       anchor="w")
        self._state_lbl.pack(anchor="w")
        self._state_sub = ctk.CTkLabel(col, text="", text_color=FG_DIM,
                                       font=("Segoe UI", 10), anchor="w")
        self._state_sub.pack(anchor="w")
        self._tick_state()

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=16, pady=4)
        for i, (key, icon, title, desc) in enumerate(MODULES):
            card = ModuleCard(grid, icon, t(title), t(desc),
                              MOD_COLORS[key],
                              command=lambda k=key: app.show(k))
            card.grid(row=i // 3, column=i % 3, padx=8, pady=10)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        credit = ctk.CTkLabel(self, text=f"{APP_NAME} v{APP_VERSION} — "
                                         f"{t('développé par')} {AUTHOR}",
                              text_color=FG_DIM, font=("Segoe UI", 10),
                              cursor="hand2", anchor="e")
        credit.pack(fill="x", padx=24, pady=(4, 12))
        credit.bind("<Button-1>", lambda e: webbrowser.open(AUTHOR_URL))
        credit.bind("<Button-3>",
                    lambda e: app.check_updates(silent=False))

    def enable_wheel(self):
        pass

    def disable_wheel(self):
        pass

    def _tick_state(self):
        if not self.winfo_exists():
            return
        try:
            import psutil
        except ImportError:
            return
        import shutil

        def worker():
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                drive = os.environ.get("SystemDrive", "C:") + "\\"
                u = shutil.disk_usage(drive)
                disk = u.used * 100 / u.total
                free = u.free
            except Exception:
                return
            if cpu > 90 or ram > 90:
                txt, color = t("Ton PC est très sollicité en ce moment"), \
                    "#f0b64f"
            elif disk > 90:
                txt, color = t("Ton disque système est presque plein"), \
                    "#f0b64f"
            else:
                txt, color = t("Ton PC fonctionne normalement"), "#4fbf78"
            sub = t("CPU {c}% · RAM {r}% · Disque {d}% ({free} libres)"
                    ).format(c=round(cpu), r=round(ram), d=round(disk),
                             free=fmt_size(free))

            def apply():
                if self.winfo_exists():
                    self._dot.configure(text_color=color)
                    self._state_lbl.configure(text=txt)
                    self._state_sub.configure(text=sub)
            try:
                self.after(0, apply)
            except tk.TclError:
                pass
        threading.Thread(target=worker, daemon=True).start()
        try:
            self.after(2000, self._tick_state)
        except tk.TclError:
            pass


# ======================================================================
#  APPLICATION
# ======================================================================
class ProBox(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG)
        self.title(APP_NAME)
        self.geometry("1080x680")
        self.minsize(760, 430)
        self.configure(bg=BG)
        self._style()
        self._build()
        setup_window(self)
        self.show("home")
        self.after(1500, lambda: self.check_updates(silent=True))

    def switch_lang(self):
        set_lang("en" if LANG == "fr" else "fr")
        for w in self.winfo_children():
            w.destroy()
        self._pages = {}
        self._build()
        self.show("home")

    def check_updates(self, silent=True):
        def worker():
            try:
                req = urllib.request.Request(
                    UPDATE_URL,
                    headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"})
                with urllib.request.urlopen(req, timeout=6) as r:
                    data = json.load(r)
                latest = str(data.get("version") or "").lstrip("vV")
                url = data.get("url") or AUTHOR_URL
                if not latest:
                    raise ValueError("no version")
                def as_tuple(v):
                    return tuple(int(x) for x in v.split(".") if x.isdigit())
                if as_tuple(latest) > as_tuple(APP_VERSION):
                    def ask():
                        if messagebox.askyesno(
                                t("Mise à jour disponible"),
                                t("Une nouvelle version de {app} est dispo "
                                  "!\n\nTa version : {cur}\nDernière "
                                  "version : {new}\n\nOuvrir la page de "
                                  "téléchargement ?").format(
                                    app=APP_NAME, cur=APP_VERSION,
                                    new=latest)):
                            webbrowser.open(url)
                    self.after(0, ask)
                elif not silent:
                    self.after(0, lambda: messagebox.showinfo(
                        t("Mise à jour"),
                        t("Tu as déjà la dernière version ({v})."
                          ).format(v=APP_VERSION)))
            except Exception:
                if not silent:
                    self.after(0, lambda: messagebox.showinfo(
                        t("Mise à jour"),
                        t("Impossible de vérifier les mises à jour\n(pas "
                          "de connexion ou fichier de version "
                          "introuvable).")))
        threading.Thread(target=worker, daemon=True).start()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=BG, foreground=FG, fieldbackground=BG2,
                    font=("Segoe UI", 10))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG)
        s.configure("Dim.TLabel", foreground=FG_DIM)
        s.configure("TCheckbutton", background=BG, foreground=FG,
                    indicatorbackground=BG2, indicatorforeground="#ffffff")
        s.map("TCheckbutton",
              background=[("active", BG)],
              foreground=[("active", FG)],
              indicatorbackground=[("selected", "#4f9cf0"),
                                   ("pressed", "#4f9cf0"),
                                   ("active", BG3)])
        s.configure("Row.TCheckbutton", background=BG2, foreground=FG,
                    indicatorbackground=BG3, indicatorforeground="#ffffff")
        s.map("Row.TCheckbutton",
              background=[("active", BG2)],
              foreground=[("active", FG)],
              indicatorbackground=[("selected", "#4f9cf0"),
                                   ("pressed", "#4f9cf0"),
                                   ("active", BG3)])
        s.configure("Treeview", background=BG2, fieldbackground=BG2,
                    foreground=FG, rowheight=26, bordercolor=BG,
                    lightcolor=BG, darkcolor=BG)
        s.configure("Treeview.Heading", background=BG3, foreground=FG,
                    relief="flat", font=("Segoe UI", 10, "bold"))
        s.map("Treeview.Heading", background=[("active", "#353640")])
        s.map("Treeview", background=[("selected", "#3d3e49")],
              foreground=[("selected", "#ffffff")])
        s.configure("Vertical.TScrollbar", background=BG3, troughcolor=BG,
                    bordercolor=BG, arrowcolor=FG_DIM,
                    lightcolor=BG3, darkcolor=BG3)
        s.map("Vertical.TScrollbar",
              background=[("active", "#353640"), ("pressed", "#3d3e49")],
              arrowcolor=[("active", FG), ("pressed", FG)])
        s.configure("Horizontal.TScrollbar", background=BG3, troughcolor=BG,
                    bordercolor=BG, arrowcolor=FG_DIM,
                    lightcolor=BG3, darkcolor=BG3)
        s.map("Horizontal.TScrollbar",
              background=[("active", "#353640"), ("pressed", "#3d3e49")],
              arrowcolor=[("active", FG), ("pressed", FG)])
        for name, bg, fg in (("Kill.TButton", ACCENT, "#ffffff"),
                             ("Soft.TButton", BG3, FG),
                             ("Blue.TButton", "#4f9cf0", "#ffffff"),
                             ("Green.TButton", "#4fbf78", "#ffffff")):
            s.configure(name, background=bg, foreground=fg, bordercolor=bg,
                        focusthickness=0, padding=(10, 6))
            s.map(name, background=[("active", bg), ("pressed", bg)])

    def _build(self):
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(fill="both", expand=True)
        self._pages = {}

    def show(self, key):
        for p in self._pages.values():
            p.pack_forget()
        if key not in self._pages:
            if key == "home":
                page = HomePage(self.content, self)
            elif key == "startup":
                page = StartupModule(self.content, self)
            elif key == "network":
                page = NetworkModule(self.content, self)
            elif key == "dupes":
                page = DupesModule(self.content, self)
            elif key == "wifi":
                page = WifiModule(self.content, self)
            elif key == "clean":
                page = CleanModule(self.content, self)
            elif key == "disk":
                page = DiskModule(self.content, self)
            else:
                page = TidyModule(self.content, self)
            self._pages[key] = page
        self._pages[key].pack(fill="both", expand=True)
        home = self._pages.get("home")
        if home:
            if key == "home":
                home.enable_wheel()
            else:
                home.disable_wheel()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ProBox().mainloop()
