@echo off
echo Building Space Shooter Santa: Galactic Justice...
python -m PyInstaller --noconsole --onefile --name "SpaceShooterSanta" --add-data "src;src" main.py
echo Build Complete!
echo Executable is in the dist folder.
pause
