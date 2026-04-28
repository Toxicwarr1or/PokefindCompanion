---
title: 'Battle at Baywharf'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_battle_of_baywharf'
slug: 'gen5-battle-of-baywharf'
description: 'It is an exciting day in Zeinova. After much exploration and effort to unite the region, a new island has been discovered. Head down to the Findale docks to begin.'
author: 'Toxicwarr1or'
source_file: 'gen5_battle_of_baywharf.json'
start:
  npc: 'Captain Benny'
  description: 'Speak to Benny at Findale Docks.'
  town: 'Findale Harbor'
  x: 565.5
  "y": 44.0
  z: 473.5
steps:
  - text: 'Use your boat and follow the sea lantern ocean path to get to Baywharf. (use the command ''/boats'' to use the boat.)'
    location:
      kind: 'region'
      x: 122.0
      "y": 61.5
      z: 1002.5
      bbox:
        x1: 88.0
        "y1": 36.0
        z1: 984.0
        x2: 156.0
        "y2": 87.0
        z2: 1021.0
      town: 'Baywharf Cove'
  - text: 'Continue forward and locate the source of the explosions.'
    location:
      kind: 'region'
      x: 214.0
      "y": 87.0
      z: 1136.0
      bbox:
        x1: 162.0
        "y1": 38.0
        z1: 1089.0
        x2: 266.0
        "y2": 136.0
        z2: 1183.0
      town: 'Baywharf Cove'
  - text: 'Make your way onto the ship.'
    location:
      kind: 'region'
      x: 201.0
      "y": 56.0
      z: 1147.5
      bbox:
        x1: 197.0
        "y1": 53.0
        z1: 1141.0
        x2: 205.0
        "y2": 59.0
        z2: 1154.0
      town: 'Baywharf Cove'
  - text: 'Find somebody in charge.'
    location:
      kind: 'region'
      x: 211.5
      "y": 56.0
      z: 1152.0
      bbox:
        x1: 205.0
        "y1": 53.0
        z1: 1141.0
        x2: 218.0
        "y2": 59.0
        z2: 1163.0
      town: 'Baywharf Cove'
  - text: 'Battle Deck Cadet Lou.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Deck Cadet Lou'
        x: 211.5
        "y": 54.0
        z: 1150.5
        town: 'Baywharf Cove'
        team:
          - species: 'Pikachu'
            level: 10
          - species: 'Dratini'
            level: 10
          - species: 'Snorlax'
            level: 10
  - text: 'Locate Engineer Jack.'
    location:
      kind: 'npc'
      x: 225.5
      "y": 49.0
      z: 1150.5
      label: 'Engineer Jack'
      town: 'Baywharf Cove'
  - text: 'Battle Engineer Jack.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Engineer Jack'
        x: 225.5
        "y": 49.0
        z: 1150.5
        town: 'Baywharf Cove'
        team:
          - species: 'Gligar'
            level: 15
          - species: 'Larvitar'
            level: 15
          - species: 'Houndour'
            level: 15
          - species: 'Flaaffy'
            level: 15
  - text: 'Locate First Mate Diego.'
    location:
      kind: 'npc'
      x: 252.5
      "y": 49.0
      z: 1154.5
      label: 'First Mate Diego'
      town: 'Baywharf Cove'
  - text: 'Battle First Mate Diego.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'First Mate Diego'
        x: 252.5
        "y": 49.0
        z: 1154.5
        town: 'Baywharf Cove'
        team:
          - species: 'Kirlia'
            level: 20
          - species: 'Metang'
            level: 20
          - species: 'Wailmer'
            level: 20
          - species: 'Milotic'
            level: 20
          - species: 'Lileep'
            level: 20
  - text: 'Locate the Captain near Baywharf''s PokeMart.'
    location:
      kind: 'npc'
      x: 328.5
      "y": 46.0
      z: 1236.5
      label: 'Captain Annabelle'
      town: 'Baywharf Cove'
  - text: 'Battle Captain Annabelle.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Captain Annabelle'
        x: 328.5
        "y": 46.0
        z: 1236.5
        town: 'Baywharf Cove'
        team:
          - species: 'Kyoto Dragonite'
            level: 25
          - species: 'Jataro Houndoom'
            level: 25
          - species: 'Haikou Slaking'
            level: 25
          - species: 'Shiloh Infernape'
            level: 25
          - species: 'Zeinova Darmanitan'
            level: 25
          - species: 'Roserade'
            level: 25
    rewards:
      - '25 Tokens'
      - '10000 Trainer XP'
      - '50000 Coins'
---
