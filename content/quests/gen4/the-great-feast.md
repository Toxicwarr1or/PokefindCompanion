---
title: 'The Great Feast'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'The_Great_Feast'
slug: 'the-great-feast'
description: 'Help the Native Americans and the Pilgrims prepare for their feast!'
author: 'KawaiiestEwok_'
source_file: 'the-great-feast.json'
start:
  npc: 'Head Chief Leon'
  town: 'Thanksgiving Island'
  x: 689.0
  "y": 31.0
  z: -1290.0
steps:
  - text: 'Talk to Jim in StrongHaven wheat Fields'
    location:
      kind: 'battle'
      town: 'Thanksgiving Island'
    battles:
      - trainer: 'Hunter Jim'
        x: -128.0
        "y": 38.0
        z: 437.0
        town: 'Thanksgiving Island'
        team:
          - species: 'Dodrio'
            level: 50
  - text: 'Find and defeat 3 Doduo'
    location:
      kind: 'npc'
      x: -104.0
      "y": 38.0
      z: 420.0
      label: 'Doduo1'
      town: 'Thanksgiving Island'
  - text: 'Defeat 2 more Doduo'
    location:
      kind: 'npc'
      x: -103.5
      "y": 39.0
      z: 358.5
      label: 'Doduo2'
      town: 'Thanksgiving Island'
  - text: 'Defeat 1 more Doduo'
    location:
      kind: 'npc'
      x: -16.0
      "y": 36.0
      z: 426.0
      label: 'Doduo3'
      town: 'Thanksgiving Island'
  - text: 'Return to Jim'
    location:
      kind: 'npc'
      x: -128.0
      "y": 38.0
      z: 437.0
      label: 'Hunter Jim'
      town: 'Thanksgiving Island'
  - text: 'Return to Head Chief Leon and Head Chief Marcel'
    location:
      kind: 'npc'
      x: 689.0
      "y": 31.0
      z: -1290.0
      label: 'Head Chief Leon'
      town: 'Thanksgiving Island'
  - text: 'Meet Kyle in Woodburn'
    location:
      kind: 'npc'
      x: 309.5
      "y": 42.0
      z: 695.0
      label: 'Farmer Kyle'
      town: 'Thanksgiving Island'
  - text: 'Find and collect the wheat'
    location:
      kind: 'destination'
      x: 307.0
      "y": 43.0
      z: 738.0
      town: 'Thanksgiving Island'
  - text: 'Find and collect the carrot'
    location:
      kind: 'destination'
      x: 293.1
      "y": 42.0
      z: 696.9
      town: 'Thanksgiving Island'
  - text: 'Find and collect the potato'
    location:
      kind: 'destination'
      x: 372.0
      "y": 42.0
      z: 716.0
      town: 'Thanksgiving Island'
  - text: 'Return to Kyle'
    location:
      kind: 'npc'
      x: 309.5
      "y": 42.0
      z: 695.0
      label: 'Farmer Kyle'
      town: 'Thanksgiving Island'
    rewards:
      - '2500 Coins'
      - '25 Tokens'
      - '3000 Trainer XP'
      - '5× Rare Candy'
      - '5× Turkey'
---
