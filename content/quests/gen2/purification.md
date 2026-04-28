---
title: 'Purification Quest'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'purification'
slug: 'purification'
description: 'Michael made friends with a Professor who claims he can purify Shadow Pokémon. Could this be the end of Cipher''s shadow plans?'
source_file: 'purification.json'
start:
  npc: 'Michael'
  town: 'Sundye City'
  x: 375.5
  "y": 69.0
  z: -579.5
steps:
  - text: 'Head over to Professor Batraz''s Purification Lab in Sundye City'
    location:
      kind: 'region'
      x: 259.0
      "y": 68.0
      z: -712.0
      bbox:
        x1: 256.0
        "y1": 66.0
        z1: -716.0
        x2: 262.0
        "y2": 70.0
        z2: -708.0
      town: 'Sundye City'
  - text: 'Find Jeptha in Sundye City''s Port'
    location:
      kind: 'battle'
      town: 'Sundye City'
    battles:
      - trainer: 'Jeptha'
        x: 259.5
        "y": 66.0
        z: -708.5
        town: 'Sundye City'
        team:
          - species: 'Absol'
            level: 85
  - text: 'Head back to Professor Batraz''s Purification Lab in Sundye City'
  - text: 'Talk to Professor Batraz to find out more about his research'
    location:
      kind: 'battle'
      town: 'Sundye City'
    battles:
      - trainer: 'Jeptha'
        x: 407.5
        "y": 76.0
        z: -711.5
        town: 'Sundye City'
        team:
          - species: 'Charizard'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Tyranitar'
            level: 100
          - species: 'Scizor'
            level: 100
          - species: 'Dragonite'
            level: 100
    rewards:
      - 'Pokémon: Houndoom (Lv 50)'
  - text: 'Give Professor Batraz your Shadow Houndoom with Max Happiness'
    rewards:
      - '50000 Trainer XP'
      - '100000 Coins'
      - '50 Tokens'
---
