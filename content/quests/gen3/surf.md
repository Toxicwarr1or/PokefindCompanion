---
title: 'Surf''s Up'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'surf'
slug: 'surf'
description: 'Journey across Haikou, battle new foes and uncover hidden secrets as you search for the Surf HM.'
source_file: 'surf.json'
start:
  npc: 'Old Man'
  town: 'Findview Port'
  x: -181.5
  "y": 23.0
  z: 620.5
steps:
  - text: 'Head to Wavemeet Bay and look for clues to the identity of this mysterious man.'
    location:
      kind: 'npc'
      x: -1003.5
      "y": 22.0
      z: 1045.5
      label: 'Terry'
      town: 'Wavemeet Bay'
  - text: 'Keep looking for clues.'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Terry'
        x: -1003.5
        "y": 22.0
        z: 1045.5
        town: 'Findview Port'
        team:
          - species: 'Luvdisc'
            level: 75
          - species: 'Sharpedo'
            level: 76
          - species: 'Whiscash'
            level: 76
          - species: 'Lanturn'
            level: 77
  - text: 'Head to Lodestar Port, and find the mysterious trainer.'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Samson'
        x: 998.5
        "y": 21.0
        z: -507.5
        town: 'Lodestar Port'
        team:
          - species: 'Slowbro'
            level: 80
          - species: 'Cloyster'
            level: 82
          - species: 'Azumarill'
            level: 82
          - species: 'Jynx'
            level: 83
          - species: 'Shiftry'
            level: 84
  - text: 'Keep searching for clues to the reveal the identity of the mysterious trainer.'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Olivia'
        x: 1132.5
        "y": 21.0
        z: -503.5
        town: 'Findview Port'
        team:
          - species: 'Gyarados'
            level: 85
          - species: 'Ludicolo'
            level: 87
          - species: 'Sneasel'
            level: 88
          - species: 'Piloswine'
            level: 89
          - species: 'Starmie'
            level: 92
          - species: 'Bellossom'
            level: 95
  - text: 'Find the hidden island and confront the mysterious trainer.'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Archie'
        x: 1395.5
        "y": 21.0
        z: -181.5
        town: 'Findview Port'
        team:
          - species: 'Glalie'
            level: 100
          - species: 'Crawdaunt'
            level: 100
          - species: 'Lapras'
            level: 100
          - species: 'Milotic'
            level: 100
          - species: 'Wailord'
            level: 100
          - species: 'Swampert'
            level: 100
    rewards:
      - '5000 Trainer XP'
      - '10000 Coins'
      - '10 Tokens'
---
