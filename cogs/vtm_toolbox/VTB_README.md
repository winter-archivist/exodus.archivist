### Common VTB Terminology
* VTM = Vampire: The Masquerade [The TTRPG system this Cog/"Toolbox" is designed to assist with]
* VTB = Vampire ToolBox [The Cog/"Toolbox" itself]

---
### Note
You should understand VTM mechanics if you intend on modifying any of the code, some parts will make ZERO sense without 
understanding some of the math/systems involved in VTM. Additionally, quite a bit of this bot is written for my 
chronicle specifically; An example of this is can be found in the Discipline section of the bot, specifically in its 
lack of support for many disciplines.
---
### VTB File Structure
Tree Characters:`║ ═ ╠ ╚`
```
vtm_toolbox
║
╠═ /vtb_characters  # All Stored Character Info
║  ║
║  ╠═ /USER_ID_1  # Example User
║  ║  ║
║  ║  ╠═ /NAME_ONE  # Example Char 1
║  ║  ║  ║
║  ║  ║  ╠═ /roll
║  ║  ║  ║  ║
║  ║  ║  ║  ╚═ info.json
║  ║  ║  ║
║  ║  ║  ╠═ /skills
║  ║  ║  ║  ║
║  ║  ║  ║  ╠═ mental.json
║  ║  ║  ║  ╠═ physical.json
║  ║  ║  ║  ╚═ social.json
║  ║  ║  ║
║  ║  ║  ╠═ attributes.json
║  ║  ║  ╠═ disciplines.json
║  ║  ║  ╠═ health.json
║  ║  ║  ╠═ humanity.json
║  ║  ║  ╠═ misc.json
║  ║  ║  ╚═ willpower.json
║  ║  ║
║  ║  ╚═ /NAME_TWO  # etc...
║  ╚═ /USER_ID_2  # etc...
║
╠═ /vtb_cm
║  ║
║  ╠═ /sections
║  ║  ║
║  ║  ╠═ /options
║  ║  ║  ║
║  ║  ║  ╚═ vtb_roller_options.py
║  ║  ║
║  ║  ╠═ vtb_roller.py
║  ║  ╚═ vtb_tracker.py
║  ║
║  ╠═ vtb_character_manager.py
║  ╚═ vtb_pages.py
║
╠═ vampireToolboxCog.py
╚═ VTB_README.md
```


---