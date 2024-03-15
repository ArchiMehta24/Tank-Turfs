•	The game features a dynamic menu, engaging sound effects, and a quiz mini-game on famous monuments, adding an educational twist. Players can test their knowledge between tank battles. Tank Turfs offers a blend of action and learning in a visually appealing setting.


https://github.com/ArchiMehta24/Tank-Turfs/assets/160386503/6d9ce010-6093-4751-9c9d-967de20bb1b3


To make it linux compatible i created a desktop instance by following steps:
1. Make a .desktop file by running the command : nano ~/Desktop/run_my_game.desktop
   
2. Inside it write the following:
   [Desktop Entry]
  Name=Your_Project_Name
  Exec=/usr/bin/env bash -c 'cd /path/to/your/project && python3 your_script.py'
  Type=Application
  Terminal=false
Save and close the file

3.run this command to make it executable : chmod +x ~/Desktop/run_my_game.desktop
