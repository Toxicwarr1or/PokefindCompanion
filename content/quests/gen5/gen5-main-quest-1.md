---
title: 'Main Quest 1 - A Myth Or A Lie?'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_1'
slug: 'gen5-main-quest-1'
description: 'The Professor heard a rumour about Pokémon behaviour. Will it be worth it to verify the rumour or is it a waste of your time?'
author: 'Mmaarten'
source_file: 'gen5-main-quest-1.json'
video_id: 'BEzZVzX_3OE'
video_title: 'A Myth or a Lie? (Episode 2: Main Quest 1)'
start:
  npc: 'Thomas'
  description: 'Talk to Thomas on the Bridge to Breezelton village'
  town: 'Findale Harbor'
  x: 784.5
  "y": 59.0
  z: 442.5
steps:
  - text: 'Cross the bridge to the next island'
    location:
      kind: 'region'
      x: 895.5
      "y": 50.5
      z: 348.0
      bbox:
        x1: 880.0
        "y1": 1.0
        z1: 320.0
        x2: 911.0
        "y2": 100.0
        z2: 376.0
      town: 'Breezelton Village'
  - text: 'Find the cave near Breezelton Village'
    location:
      kind: 'destination'
      x: 984.2
      "y": 65.0
      z: 66.5
      label: 'Find the cave near Breezelton Village'
      town: 'Breezelton Village'
  - text: 'Battle the wild Pokémon'
    location:
      kind: 'npc'
      x: 977.0
      "y": 64.0
      z: 63.1
      label: 'pokemon1'
      town: 'Breezelton Village'
  - text: 'Continue through the cave and fight the remaining guardian Pokémon'
    location:
      kind: 'npc'
      x: 942.1
      "y": 50.0
      z: 52.2
      label: 'pokemon2'
  - text: 'Continue deeper into the cave'
    location:
      kind: 'region'
      x: 1018.0
      "y": 32.0
      z: 61.0
      bbox:
        x1: 1010.0
        "y1": 26.0
        z1: 50.0
        x2: 1026.0
        "y2": 38.0
        z2: 72.0
      town: 'Bridgerun'
  - text: 'Battle the Old Man'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Old Man'
        x: 1019.5
        "y": 28.0
        z: 63.5
        town: 'Bridgerun'
        team:
          - species: 'Ducklett'
            level: 12
          - species: 'Munna'
            level: 13
          - species: 'Audino'
            level: 15
  - text: 'Talk to Professor Hemlock near the map in Bridgerun'
    location:
      kind: 'destination'
      x: 1131.5
      "y": 51.0
      z: 63.5
      label: 'Talk to Professor Hemlock near the map in Bridgerun'
      town: 'Bridgerun'
    rewards:
      - '10000 Coins'
      - '3500 Trainer XP'
      - '25 Tokens'
      - 'Silk Scarf'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
---
