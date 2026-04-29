---
title: 'Bitter Rivals Part 5'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'bitter5'
slug: 'bitter5'
description: 'On your way to explore Searing Peak you cross paths with your newly formed rivals, have they finally become a match for you?'
source_file: 'bitter5.json'
video_id: 'rk2WgVrIkg4'
video_title: 'PokéFind Bitter Rivals Part5-8 (Bitter Rivals: Generation 3)'
start:
  npc: 'Lincoln'
  x: -1095.5
  "y": 40.0
  z: -950.5
steps:
  - text: 'Battle Lincoln!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Sarah'
        x: -1089.5
        "y": 40.0
        z: -950.5
        team:
          - species: 'Sceptile'
            level: 40
          - species: 'Swellow'
            level: 39
          - species: 'Cacturne'
            level: 37
          - species: 'Manectric'
            level: 38
  - text: 'Battle Sarah!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Casey'
        x: -1092.5
        "y": 40.0
        z: -950.5
        team:
          - species: 'Blaziken'
            level: 41
          - species: 'Delcatty'
            level: 39
          - species: 'Masquerain'
            level: 38
          - species: 'Mawile'
            level: 37
  - text: 'Battle Casey!'
    location:
      kind: 'npc'
      x: -1092.5
      "y": 40.0
      z: -950.5
      label: 'Casey'
    rewards:
      - '12000 Trainer XP'
      - '4000 Coins'
      - '7 Tokens'
---
