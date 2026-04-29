---
title: 'Quick To Your Feet!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'FASTANDQUICKBALLQUEST'
slug: 'quick-to-your-feet'
description: 'Some friends are looking to have some sporting fun'
source_file: 'quick-to-your-feet.json'
start:
  npc: 'Brayden'
  town: 'Arc City'
  x: -871.5
  "y": 38.0
  z: 599.5
steps:
  - text: 'Find Brayden somewhere near the PokéCenter'
    location:
      kind: 'battle'
      town: 'Arc City'
    battles:
      - trainer: 'Brayden'
        x: -806.5
        "y": 32.0
        z: 653.5
        town: 'Arc City'
        team:
          - species: 'Tauros'
            level: 42
          - species: 'Absol'
            level: 44
          - species: 'Electabuzz'
            level: 45
          - species: 'Sneasel'
            level: 46
          - species: 'Slaking'
            level: 48
  - text: 'Find Mitchell near the docks'
    location:
      kind: 'battle'
      town: 'Arc City'
    battles:
      - trainer: 'Mitchell'
        x: -1083.5
        "y": 20.0
        z: 611.5
        town: 'Arc City'
        team:
          - species: 'Miltank'
            level: 46
          - species: 'Ninetales'
            level: 48
          - species: 'Ninjask'
            level: 49
          - species: 'Linoone'
            level: 52
          - species: 'Jumpluff'
            level: 50
          - species: 'Manectric'
            level: 51
  - text: 'Find Eliza near the gym'
    location:
      kind: 'battle'
      town: 'Arc City'
    battles:
      - trainer: 'Eliza'
        x: -930.5
        "y": 28.0
        z: 676.5
        town: 'Arc City'
        team:
          - species: 'Jolteon'
            level: 53
          - species: 'Crobat'
            level: 55
          - species: 'Houndoom'
            level: 57
          - species: 'Starmie'
            level: 58
          - species: 'Dugtrio'
            level: 50
          - species: 'Swellow'
            level: 51
  - text: 'Talk to Brayden in front of the PokéMart'
    location:
      kind: 'npc'
      x: -871.5
      "y": 38.0
      z: 599.5
      label: 'Brayden'
      town: 'Arc City'
    rewards:
      - '10000 Coins'
      - '10 Tokens'
      - '10000 Trainer XP'
      - '6× Fast Ball'
      - '6× Quick Ball'
---
