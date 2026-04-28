---
title: 'On Another Level!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'level_ball'
slug: 'level-ball'
description: 'There has been a break in at the Observatory!'
source_file: 'level-ball.json'
start:
  npc: 'Izzy'
  x: 1464.5
  "y": 28.0
  z: -485.5
steps:
  - text: 'Head to the Casino'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Karsen'
        x: 759.5
        "y": 43.0
        z: -512.5
        team:
          - species: 'Swampert'
            level: 39
          - species: 'Sharpedo'
            level: 42
          - species: 'Whiscash'
            level: 44
          - species: 'Crawdaunt'
            level: 46
  - text: 'Battle Karsen!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Laura'
        x: 759.5
        "y": 43.0
        z: -515.5
        team:
          - species: 'Delcatty'
            level: 45
          - species: 'Medicham'
            level: 47
          - species: 'Gardevoir'
            level: 48
          - species: 'Milotic'
            level: 50
          - species: 'Chimecho'
            level: 51
  - text: 'Battle Laura!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Matthew'
        x: 759.5
        "y": 43.0
        z: -518.5
        team:
          - species: 'Claydol'
            level: 47
          - species: 'Armaldo'
            level: 50
          - species: 'Relicanth'
            level: 51
          - species: 'Cradily'
            level: 52
  - text: 'Battle Matthew!'
    location:
      kind: 'npc'
      x: 1464.5
      "y": 28.0
      z: -485.5
      label: 'Izzy'
  - text: 'Go back to the Observatory and speak to Izzy!'
    location:
      kind: 'npc'
      x: 1464.5
      "y": 28.0
      z: -485.5
      label: 'Izzy'
    rewards:
      - '30000 Trainer XP'
      - '10 Tokens'
      - '5× Rare Candy'
      - '12× Level Ball'
---
