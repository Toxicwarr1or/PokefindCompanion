---
title: 'For When The Sun Sets'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'dusk_ball'
slug: 'dusk-ball'
description: 'A rare pokéball has been discovered nearby. Tony seems to know about it!'
source_file: 'dusk-ball.json'
start:
  npc: 'Tony'
  town: 'Sleepy Hollow'
  x: -736.5
  "y": 33.0
  z: 432.5
steps:
  - text: 'Head to the Cave between Safari and Stoneridge'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Tony'
        x: -1217.5
        "y": 42.0
        z: -119.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Poochyena'
            level: 17
          - species: 'Murkrow'
            level: 21
          - species: 'Sneasel'
            level: 24
          - species: 'Sableye'
            level: 28
    rewards:
      - '5000 Trainer XP'
      - '5 Tokens'
      - '10000 Coins'
      - '12× Dusk Ball'
---
