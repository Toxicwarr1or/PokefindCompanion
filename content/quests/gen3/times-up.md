---
title: 'Time''s Up!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'TIMERBALLQUEST'
slug: 'times-up'
description: 'A researcher is studying certain Pokemon moves.'
source_file: 'times-up.json'
start:
  npc: 'Millah'
  town: 'Sleet City'
  x: 293.5
  "y": 42.0
  z: -875.5
steps:
  - text: 'Talk to Lerson in his house near the PokeMart'
    location:
      kind: 'npc'
      x: 290.5
      "y": 20.0
      z: -1055.5
      label: 'Lytra'
      town: 'Sleet City'
  - text: 'Find Lytra in the Icy Plains'
    location:
      kind: 'npc'
      x: 290.5
      "y": 20.0
      z: -1055.5
      label: 'Lytra'
      town: 'Icy Plains'
  - text: 'Capture a Jynx and bring it to Lytra'
    location:
      kind: 'npc'
      x: 328.5
      "y": 49.0625
      z: -887.5
      label: 'Lerson'
      town: 'Sleet City'
  - text: 'Return the lab equipment to Lerson'
    location:
      kind: 'npc'
      x: 321.5
      "y": 41.0
      z: -897.5
      label: 'Lerson'
      town: 'Sleet City'
  - text: 'Battle Lerson outside of his house'
    location:
      kind: 'battle'
      town: 'Sleet City'
    battles:
      - trainer: 'Lerson'
        x: 321.5
        "y": 41.0
        z: -897.5
        town: 'Sleet City'
        team:
          - species: 'Sneasel'
            level: 37
          - species: 'Sealeo'
            level: 34
          - species: 'Glalie'
            level: 38
          - species: 'Altaria'
            level: 40
    rewards:
      - '5000 Coins'
      - '5 Tokens'
      - '10000 Trainer XP'
      - '12× Timer Ball'
---
