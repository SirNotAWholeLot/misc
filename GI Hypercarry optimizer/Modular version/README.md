<div class="alert alert-block alert-info"><b>Genshin Impact buff optimization thingy</b></div>

General idea of this thing is this: main widget assembles the party out of the hypercarry and buffer widgets. Those widgets handle whatever internal calculations for the members.
Main widget asks hypercarry to calculate their 'solo' stats, ask buffers to calculate their buffs, adds the buffs, asks hypercarry to apply conversions, and calculates the damage output.
Optimizers should assemble either relevant buffers or relevant artifacts and call the 'calculate everything' function.
As such, either the calculator should be separate, or the optimizers should be parts of the main widget. The former seems to be a better option.

<b>To do</b>:
- DONE Rework hypercarry class stats
- DONE Add specific hypercarries such as Raiden, Hu Tao, Itto and make separate hypercarry widget
- DONE Add Chevreuse as a buffer (HP scale + VV)
- DONE Add VV as a buffer (with average gained value being ~25%)
- DONE Rework buffer class to allow better constellation tracking maybe
- DONE Add input validator for numerical fields, or change them for QSpinBox
- DONE Redo talent selectors for QSpinBox
- DONE Inheritance for character widgets
- DONE Redo the whole thing as 'party composition' class containing a HC and buffers to allow resonances to be smoother
- DONE Add Zhongli as a buffer
- DONE Add resonances and a resonator
- DONE Implement cycling resonator's elements for the buffer optimizer
- DONE Add frames for the pretty
- DONE Make the calculator and optimisers into their proper widgets
- DONE Add weapons as separate widgets
- DONE Add relevancy lists for buffers and resonances
- Add more weapons: Homa
- Add more characters: Xiao, Faruzan, Ayato
- Rework weapon-character link -> use weakref instead of a full parent reference
- DONE Rework how character/weapon widget work -> universal widget class, list of fields to display in an entity
- Rework hypercarry stat keys for uniformity, including elements