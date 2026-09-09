<p align="center">
  <img src="probox_logo.png" width="140" alt="ProBox logo">
</p>

<h1 align="center">ProBox</h1>

<p align="center">
  A Windows system toolbox — seven everyday tools in one clean app.
</p>

<p align="center">
  🇫🇷 <a href="README.fr.md">Version française</a>
</p>

---

## What is it?

ProBox groups the little tools Windows should have shipped with, in one modern dark app (CustomTkinter) with a card-based home screen. Pick a module, do the job, done.

<img width="1074" height="900" alt="probox" src="https://github.com/user-attachments/assets/14e687a8-4016-4341-b5ae-735761539ada" />




## Modules

- 🚀 **Startup** — see everything that launches when Windows boots. Enable/disable items (same official mechanism as Task Manager, fully reversible) or delete entries.
- 📡 **Network** — real-time bandwidth, the list of every app connected to the internet and where to, plus a **diagnostics window**: connection/DNS/IP tests and a "Repair my connection" button (flush DNS, renew IP, Winsock reset).
- 🗂 **Duplicates** — find duplicate files by CONTENT (renamed copies are caught too). Folder or whole-drive scan, progressive results biggest-first, stop anytime and keep what's found, image previews on hover, recycle-bin deletion.
- 🧹 **Tidy up** — sort the mess in your Downloads folder by type. Analyze first, nothing moves without approval, undoable.
- 📶 **Wi-Fi** — every Wi-Fi network saved on the PC with its password (the same data Windows shows in its settings, just 100x more convenient). Hidden by default, one button to reveal, one to copy.
- 🧽 **Cleanup** — free disk space: temp files, browser caches, thumbnail cache, recycle bin, Windows Update leftovers. Analyze first with per-category sizes and a detailed view of what would be removed.
- 💾 **Disk space** — a pocket TreeSize: heaviest folders (browsable), largest files, right-click actions, and a basic drive-health check.

Plus: a live **PC status card** on the home screen (CPU · RAM · disk), an **action history** of everything ProBox changed on the system, bilingual interface (English/French, auto-detected, 🌐 button), update notifications, and a fully modern CustomTkinter interface (rounded everything, smooth hovers) since v2.0.

## Installation

### Regular users (recommended)

Download `ProBox.exe` from the [Releases](../../releases) page and run it. Nothing to install.

> **SmartScreen note**: on first launch, Windows may warn about an unsigned executable — normal for a small independent project. Click *More info* then *Run anyway*. The full source code is readable in this repository.

> **Tip**: run ProBox as administrator to manage machine-level startup items and reveal Wi-Fi passwords on some configurations.

### From source

```
pip install psutil pillow customtkinter
python probox.py
```

(`psutil` powers the Network module, `pillow` enables image previews in Duplicates, `customtkinter` renders the modern interface.)

### Build the exe yourself

```
pip install pyinstaller psutil pillow customtkinter
pyinstaller --onefile --noconsole --collect-all customtkinter --icon probox.ico --add-data "probox.ico;." --name ProBox probox.py
```

## Requirements

- Windows 10 / 11

## License

MIT — do whatever you want with it, a mention is appreciated.

---

<p align="center">
  Developed by <a href="https://github.com/karkarofff">Karkarofff</a> — also check out <a href="https://github.com/karkarofff/prokill">ProKill</a> and <a href="https://github.com/karkarofff/prograb">ProGrab</a>
</p>
