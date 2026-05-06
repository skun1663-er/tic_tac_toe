# 🎮 Tic-Tac-Toe Game

A modern desktop Tic-Tac-Toe game built using Python and Tkinter with a clean GUI, scoreboard system, and Windows installer support.

---

## ✨ Features

* Interactive GUI board
* Two-player gameplay
* Winner detection
* Tie detection
* Live scoreboard
* Reset game functionality
* Reset scores functionality
* Custom application icon
* Windows installer support

---

## 🛠 Built With

* Python
* Tkinter
* PyInstaller
* Inno Setup

---

## 📦 Downloads

### Recommended

Download and install:

```text
TicTacToeSetup.exe
```

from the GitHub Releases section.

### Portable Version

You can also use:

```text
tic_tac_toe.exe
```

without installation.

---

## 🚀 Running From Source

### 1. Clone Repository

```bash
git clone https://github.com/skun1663-er/tic_tac_toe.git
cd tic_tac_toe
```
password: 1663

### 2. Run the Game

```bash
python tic_tac_toe.py
```

---

## 🔨 Build Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build executable:

```bash
pyinstaller ^
--onefile ^
--windowed ^
--icon=icon.ico ^
--add-data "icon.ico;." ^
--add-data "icon.png;." ^
tic_tac_toe.py
```

Generated executable will appear inside:

```text
dist/
```

---

## 🧰 Build Installer

Use:

* Inno Setup 6

Compile the `.iss` setup script to generate:

```text
TicTacToeSetup.exe
```

---

## 📁 Project Structure

```text
TIC_TAC_TOE/
│
├── tic_tac_toe.py
├── icon.ico
├── icon.png
├── tic_tac_toe.iss
├── README.md
├── .gitignore
│
├── build/
├── dist/
└── installer_output/
```

---

## 🚀 Future Improvements

* AI opponent
* Sound effects
* Dark mode
* Animations
* Difficulty levels
* Online multiplayer

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Developer

Created by skun1663-er
