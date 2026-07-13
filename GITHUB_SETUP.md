# GitHub Setup

Use this folder as the source repo for NT Performance Hub. The clean split is:

- Laptop: edit, test, commit, and push.
- Performance PC: pull updates, keep local config, and run the show server.

## First-Time Laptop Setup

Create a private GitHub repository named `nt-performance-hub`. This prepared folder already has Git initialized, so run these commands from this folder:

```powershell
git add .
git commit -m "Initial NT Performance Hub app"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USER/nt-performance-hub.git
git push -u origin main
```

If Git reports `dubious ownership` because the folder was created by the Codex sandbox, run this once with the real folder path:

```powershell
git config --global --add safe.directory "C:/Users/ryant/Documents/Codex/NT Performance Hub"
```

## First-Time Performance PC Setup

Clone the private repo onto the performance PC:

```powershell
git clone https://github.com/YOUR-GITHUB-USER/nt-performance-hub.git "NT Performance Hub"
cd "NT Performance Hub"
.\Install NT Performance Hub.bat
```

Create the local config on that machine:

```powershell
copy .\config\app_config.example.json .\config\app_config.json
```

Then edit `config/app_config.json` for that room and machine.

## Normal Update Flow

On the laptop:

```powershell
git status
git add .
git commit -m "Describe the change"
git push
```

On the performance PC:

```powershell
.\Update From GitHub.bat
.\Start NT Performance Hub.bat
```

## What Should Not Go To GitHub

The repo should not track machine-local runtime files:

- `.venv/`
- `config/app_config.json`
- `data/*.json`
- `data/current_artwork.jpg`
- `logs/*`
- `server.*.log`
- `.agents/`
- `.codex/`

Keep those local to each machine.