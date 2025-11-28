# Space Shooter Santa - Galactic Justice Platform

## Overview
What started as a simple shooter is now a full arcade platform featuring multiple game modes, procedural art, layered scene management, and production-ready build tooling. Everything ships as a native Windows experience powered by Python + Pygame and packaged through PyInstaller.

## Game Modes
- **Space Shooter (Arcade)** – Classic keyboard-driven bullet-hell with wave escalation, power-ups, and particle FX.
- **Android Legacy Shooter** – Pointer-based controls with auto-fire to simulate mobile gameplay.
- **Dog Hunt Patrol** – Top-down treat-chasing mini-game starring Santa’s cyber dog against rogue robo-critters.

## Controls
- **Arcade Shooter**: Arrow Keys to move, `Space` to fire, `Esc` to back out.
- **Android Shooter**: Move the mouse (touch analog) and hold left-click to steer; firing is automatic.
- **Dog Hunt**: Arrow Keys move the dog in 8 directions; collect treats, avoid critters, `Esc` to exit.

## Tech Highlights
- Modular package layout under `src/` (`core`, `entities`, `scenes`, `utils`).
- Scene/state manager with plug-and-play scenes (`menu`, `mode_select`, `settings`, multiple game scenes).
- Procedural AssetManager that sketches every sprite at runtime for zero external dependencies.
- Wave system, layered sprite rendering, particle systems, configurable settings persisted to `config/settings.json`.

## Build & Run
```bash
pip install -r requirements.txt
python main.py              # run from source
./build.bat                 # create dist/SpaceShooterSanta.exe
```

## Credits
Designed and engineered by the GitHub Copilot strike team.
