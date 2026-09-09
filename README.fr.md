<p align="center">
  <img src="probox_logo.png" width="140" alt="Logo ProBox">
</p>

<h1 align="center">ProBox</h1>

<p align="center">
  Une boîte à outils système pour Windows — sept outils du quotidien dans une seule app propre.
</p>

<p align="center">
  🇬🇧 <a href="README.md">English version</a>
</p>

---

## C'est quoi ?

ProBox regroupe les petits outils que Windows aurait dû livrer d'origine, dans une seule app moderne et sombre (CustomTkinter) avec un accueil à cartes. Tu choisis un module, tu fais le boulot, terminé.

<img width="1200" height="929" alt="accueil app" src="https://github.com/user-attachments/assets/c112080f-1658-45d1-9013-3c3116f23d4a" />


## Modules

- 🚀 **Démarrage** — voir tout ce qui se lance à l'ouverture de Windows. Activer/désactiver (même mécanisme officiel que le Gestionnaire des tâches, réversible) ou supprimer des entrées.
- 📡 **Réseau** — débit en temps réel, la liste des applications connectées à internet et vers où, plus une **fenêtre de diagnostic** : tests connexion/DNS/IP et un bouton « Réparer ma connexion » (vidage DNS, renouvellement IP, reset Winsock).
- 🗂 **Doublons** — trouve les fichiers en double par CONTENU (les copies renommées aussi). Scan d'un dossier ou d'un disque entier, résultats progressifs les plus gros d'abord, arrêt possible en gardant les trouvailles, aperçu des images au survol, suppression via la corbeille.
- 🧹 **Rangement** — trie le bazar du dossier Téléchargements par type. Analyse d'abord, rien ne bouge sans accord, annulable.
- 📶 **Wi-Fi** — tous les réseaux Wi-Fi enregistrés sur le PC avec leur mot de passe (les mêmes données que Windows affiche dans ses paramètres, en 100 fois plus pratique). Masqués par défaut, un bouton pour révéler, un pour copier.
- 🧽 **Nettoyage** — libère de l'espace : fichiers temporaires, caches navigateurs, cache des miniatures, corbeille, restes de Windows Update. Analyse d'abord avec les tailles par catégorie et le détail de ce qui serait supprimé.
- 💾 **Espace disque** — un TreeSize de poche : dossiers les plus lourds (navigables), plus gros fichiers, actions au clic droit, et un contrôle basique de la santé des disques.

Et aussi : une **carte État du PC** en temps réel sur l'accueil (CPU · RAM · disque), un **historique des actions** de tout ce que ProBox a modifié sur le système, l'interface bilingue (français/anglais, détection auto, bouton 🌐), les notifications de mise à jour, et une interface entièrement modernisée en CustomTkinter (coins arrondis, survols fluides) depuis la v2.0.

## Installation

### Utilisateur (recommandé)

Téléchargez `ProBox.exe` depuis la page [Releases](../../releases) et lancez-le. Rien à installer.

> **Note SmartScreen** : au premier lancement, Windows peut avertir d'un exécutable non signé, c'est normal pour un petit projet indépendant. Cliquez sur *Informations complémentaires* puis *Exécuter quand même*. Le code source est entièrement lisible dans ce dépôt.

> **Astuce** : lancez ProBox en administrateur pour gérer les éléments de démarrage « machine » et révéler les mots de passe Wi-Fi sur certaines configurations.

### Depuis les sources

```
pip install psutil pillow customtkinter
python probox.py
```

(`psutil` fait tourner le module Réseau, `pillow` active les aperçus d'images dans Doublons, `customtkinter` affiche l'interface moderne.)

### Compiler soi-même l'exe

```
pip install pyinstaller psutil pillow customtkinter
pyinstaller --onefile --noconsole --collect-all customtkinter --icon probox.ico --add-data "probox.ico;." --name ProBox probox.py
```

## Prérequis

- Windows 10 / 11

## Licence

MIT — faites-en ce que vous voulez, une mention est appréciée.

---

<p align="center">
  Développé par <a href="https://github.com/karkarofff">Karkarofff</a> — jetez aussi un œil à <a href="https://github.com/karkarofff/prokill">ProKill</a> et <a href="https://github.com/karkarofff/prograb">ProGrab</a>
</p>
