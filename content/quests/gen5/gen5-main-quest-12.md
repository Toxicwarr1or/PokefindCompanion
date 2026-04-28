---
title: 'Main Quest 12 - Zeinova, Rejoice!'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_12'
slug: 'gen5-main-quest-12'
description: 'The region is on the brink of destruction. With the Power of Therian Landorus, Ghetsis has all but secured his position as ruler of Zeinova. With the capture of Tornadus and Thundurus, you and Danielle have allowed a moment of weakness to strike Ghetsis. The fate of Zeinova rests on its two champions.'
author: 'Toxicwarr1or'
source_file: 'gen5-main-quest-12.json'
video_id: 'IJCpG97GkF0'
video_title: 'Main Quest 12 - Zeinova, Rejoice'
start:
  npc: 'Sailor Jeffrey'
  description: 'Talk to the sailor at Sparkmont Docks.'
  town: 'Sparkmont City'
  x: 1431.5
  "y": 44.0
  z: 425.5
steps:
  - text: 'Locate the entrance of the HQ.)'
    location:
      kind: 'npc'
      x: 846.5
      "y": 78.0
      z: 1087.0
      label: 'Danielle'
  - text: 'Find another way into the Plasma HQ without being spotted. (Hint: Locate the Sewer Pipe)'
    location:
      kind: 'npc'
      x: 991.5
      "y": 43.0
      z: 1078.5
      label: 'Danielle'
  - text: 'Enter the sewer'
    location:
      kind: 'region'
      x: 42.5
      "y": 8.0
      z: -669.5
      bbox:
        x1: 40.0
        "y1": 5.0
        z1: -674.0
        x2: 45.0
        "y2": 11.0
        z2: -665.0
      town: 'Northrun'
  - text: 'Find your way through the sewer. There are two levels to try and escape.'
    location:
      kind: 'region'
      x: 186.0
      "y": 21.5
      z: -664.0
      bbox:
        x1: 181.0
        "y1": 18.0
        z1: -668.0
        x2: 191.0
        "y2": 25.0
        z2: -660.0
      town: 'Northrun'
  - text: 'Find a way past the locked door.'
    location:
      kind: 'region'
      x: 888.0
      "y": 7.5
      z: 1166.0
      bbox:
        x1: 886.0
        "y1": 5.0
        z1: 1164.0
        x2: 890.0
        "y2": 10.0
        z2: 1168.0
  - text: 'Defeat the Plasma Grunts on Floor 1. Grunts remaining: 5'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Plasma Grunt'
        x: 899.5
        "y": 6.0
        z: 1141.5
        team:
          - species: 'Dragonite'
            level: 100
          - species: 'Gengar'
            level: 100
          - species: 'Snorlax'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Chansey'
            level: 100
          - species: 'Arcanine'
            level: 100
  - text: 'Defeat the Plasma Grunts on Floor 1. Grunts remaining: 4'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Plasma Grunt'
        x: 877.5
        "y": 6.0
        z: 1156.5
        team:
          - species: 'Clefable'
            level: 100
          - species: 'Togekiss'
            level: 100
          - species: 'Azumarill'
            level: 100
          - species: 'Snorlax'
            level: 100
          - species: 'Chansey'
            level: 100
          - species: 'Staraptor'
            level: 100
  - text: 'Defeat the Plasma Grunts on Floor 1. Grunts remaining: 3'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Plasma Grunt'
        x: 864.5
        "y": 6.0
        z: 1143.5
        team:
          - species: 'Conkeldurr'
            level: 100
          - species: 'Breloom'
            level: 100
          - species: 'Infernape'
            level: 100
          - species: 'Machamp'
            level: 100
          - species: 'Heracross'
            level: 100
          - species: 'Lucario'
            level: 100
  - text: 'Defeat the Plasma Grunts on Floor 1. Grunts remaining: 2'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Plasma Grunt'
        x: 885.5
        "y": 6.0
        z: 1142.5
        team:
          - species: 'Garchomp'
            level: 100
          - species: 'Rotom'
            level: 100
          - species: 'Ferrothorn'
            level: 100
          - species: 'Volcarona'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Scizor'
            level: 100
  - text: 'Defeat the Plasma Grunts on Floor 1. Grunts remaining: 1'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Plasma Grunt Captain'
        x: 885.5
        "y": 6.0
        z: 1140.5
        team:
          - species: 'Jirachi'
            level: 100
          - species: 'Togekiss'
            level: 101
          - species: 'Hitmontop'
            level: 102
          - species: 'Excadrill'
            level: 103
          - species: 'Garchomp'
            level: 104
          - species: 'Amoonguss'
            level: 105
  - text: 'Inspect the locked door near the Storage Room'
    location:
      kind: 'region'
      x: 888.0
      "y": 7.5
      z: 1166.0
      bbox:
        x1: 886.0
        "y1": 5.0
        z1: 1164.0
        x2: 890.0
        "y2": 10.0
        z2: 1168.0
  - text: 'Follow the puzzle presented at the Locked Door.'
  - text: 'Find the correct chest in the Storage Room and enter the code: 34908.'
  - text: 'Press the button to open the door.'
  - text: 'Continue onto the next locked door and puzzle. (Press the button outside the door to access the puzzle: Ice Breaker)'
  - text: 'Open the door and continue to the next puzzle. (Next puzzle is Mousetraps)'
  - text: 'Continue onto the next locked door and puzzle. (Press the button outside the door to access the puzzle: What''s my password?)'
  - text: 'Continue onto the next locked door and puzzle. (Press the button outside the door to access the puzzle: Plasma Says)'
    location:
      kind: 'npc'
      x: 894.5
      "y": 80.0
      z: 1139.5
      label: 'Plasma Grunt'
  - text: 'Continue onto the next locked door and puzzle. (Press the button outside the door to access the puzzle: Security Levers)'
  - text: 'Continue onto the final locked door and puzzle. (Press the button outside the door to access the puzzle: Lights Out)'
  - text: 'Climb the stairs to access the next part of Team Plasma HQ'
    location:
      kind: 'npc'
      x: 894.5
      "y": 80.0
      z: 1139.5
      label: 'Plasma Grunt'
  - text: 'Investigate the interior of Team Plasma HQ'
    location:
      kind: 'npc'
      x: 894.5
      "y": 80.0
      z: 1139.5
      label: 'Plasma Grunt'
  - text: 'Battle Ghetsis'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Ghetsis'
        x: 424.5
        "y": 126.0
        z: 1681.5
        team:
          - species: 'Hydreigon'
            level: 105
          - species: 'Cofagrigus'
            level: 105
          - species: 'Reuniclus'
            level: 105
          - species: 'Bisharp'
            level: 105
          - species: 'Krookodile'
            level: 105
          - species: 'Eelektross'
            level: 105
          - species: 'Landorus'
            level: 100
          - species: 'Zoroark'
            level: 105
    rewards:
      - 'Pokémon: Landorus (Lv 50)'
      - 'Pokémon: Landorus (Lv 50)'
      - 'Pokémon: Thundurus (Lv 50)'
      - 'Pokémon: Thundurus (Lv 50)'
      - 'Pokémon: Tornadus (Lv 50)'
      - 'Pokémon: Tornadus (Lv 50)'
      - '200000 Coins'
      - '200000 Trainer XP'
      - '150 Tokens'
      - 'reveal_glass'
---
