![0_banner](https://github.com/user-attachments/assets/ff8c098e-a8b8-414c-9717-8b60a99b7a65)
> Thine earthmother comes unto thee, gifts abound.  
> Don thou life of earth, for a great many victory ye shall have.  
> — The Druid  

### A daily task completer for the browser fantasy RPG, Tagoria.

Auto-completes daily tasks including quests, plunders, & farming. Forever.

**FEATURES**::
- Quests - accepts, attempts, & turns-in quests by going to quest location and plundering.
- Plundering - plunders chosen location when out of Quest Points with remaining Action Points.
- Farming - farms for 24 hrs when out of Action Points until points reset at new day. Collects wages every 8 hrs.
- Skiller (WIP) - increase attributes on levelup, buys skillpoints with extra amber above threshold.
- Amber Preserver (WIP) - can set max amber carrying threshold if saving for weapons/armour/enchantments. Avoids carrying a large stealable sum by spending excess on skillpoints through Skiller.


**REQUIREMENTS**::
- Firefox
- Geckodriver - put exe in same folder as 'TagoriaDailies.exe' - [link](https://github.com/mozilla/geckodriver/releases "GitHub")


**INSTRUCTIONS**::
1. (Optional but Recommended to increase speed & reduce bandwidth) Download Firefox extensions 'uBlock' & 'NoScript' (right-click "Add to Firefox" -> "Save Link As"). Rename files to 'ublock_origin.xpi' & 'noscript.xpi' and put them in the same folder as 'TagoriaDailies.exe'.
2. Enter credentials & edit preferences in 'config.yml'.
3. Confirm character is not currently taking an action, and has turned-in any quest. Logout.
4. Start 'TagoriaDailies.exe'.
5. Sit back & relax (or leave it running on a raspberry pi and forget about it for months 😅)

Notes:
- If using extensions, the action timers won't show by default. Open 'NoScript' in top right corner, trust 'tagoria.net', untrust every other URL.
- If you encounter an error - logout, close browser, check instructions, restart script.


**DEVELOPMENT**::

Code is far from ideal, and is not hardened or self-healing if an error occurs.

Dependencies required for dev --
- Firefox
- Python 3
- Selenium 4
- Splinter 0.21


Made with ❤️ by foxton_
