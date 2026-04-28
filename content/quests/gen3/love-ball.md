---
title: 'Charming!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'love_ball'
slug: 'love-ball'
description: 'A woman seems distressed, what has happened to her niece & nephew?'
source_file: 'love-ball.json'
start:
  npc: 'Danielle'
  x: -925.5
  "y": 23.0
  z: 988.5
steps:
  - text: 'Head West and find Danielle''s Niece and Nephew'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Kristen'
        x: -1044.5
        "y": 22.0
        z: 1002.5
        team:
          - species: 'Gorebyss'
            level: 45
          - species: 'Espeon'
            level: 49
          - species: 'Delcatty'
            level: 51
  - text: 'Beat Kristen'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Christian'
        x: -1044.5
        "y": 22.0
        z: 1005.5
        team:
          - species: 'Huntail'
            level: 46
          - species: 'Umbreon'
            level: 50
          - species: 'Mightyena'
            level: 53
  - text: 'Beat Christian'
    location:
      kind: 'npc'
      x: -1044.5
      "y": 22.0
      z: 1005.5
      label: 'Christian'
    rewards:
      - '10 Tokens'
      - '10000 Trainer XP'
      - '12× Love Ball'
---
