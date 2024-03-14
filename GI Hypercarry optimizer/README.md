This is a (limited functionality) party/build optimizer for the game Genshin Impact, focusing on 'hypercarry' compositions - where one character does meaningful damage and others buff them.

GUI is made using PyQt5, the structure is somewhat modular - while this is a singular Jupyter notebook, functional and GUI elements are organized by cells and can be easily exported to be standalone.

Features:
- Build output calculator:
Calculating (relative) damage output for a selected hypercarry character with the current weapon option, including level, refinement level and passive efficiency, artifact selection, substat sums, and relevant artifact options. Provides a breakdown of effective stats after all buffs and conversions.
- Buffer calculator:
In addition to the hypercarry, select up to three support characters, including elemental resonances, and pick relevant specifics of their builds. Answers such questions as "Would Bennett or Kazuha offer more damage here with the builds I have for them?" without requiring uploading full builds. Adjustments made to characters here persist thoughout other functions of the program.
- Build optimizer:
Select what options do you want to optimize - currently includes weapon and artifact main stats - and calculate the option with the highest relevant output.
- Buffer optimizer:
Select what support characters are available, how many to use, and calculate relative damage outputs for different combinations, showing the highest output one. Non-buffer characters providing elemental resonance are considered as always available.
