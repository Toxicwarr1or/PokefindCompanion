---
title: 'Bitter Rivals Part 3'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'bitter3'
slug: 'bitter3'
description: 'As you are leaving Findview Port you are reunited with Sarah and Casey but they have a new friend. Who is this new Trainer?'
source_file: 'bitter3.json'
video_id: 'Dk3Q2K7PJUM'
video_title: 'PokéFind Bitter Rivals Part 1 - Part 3 (Bitter Rivals: Generation 3)'
start:
  npc: 'Lincoln'
  town: 'Findview Port'
  x: -436.5
  "y": 33.0
  z: 514.5
steps:
  - text: 'Battle Lincoln!'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Sarah'
        x: -435.5
        "y": 33.0
        z: 512.5
        town: 'Findview Port'
        team:
          - species: 'Treecko'
            level: 9
          - species: 'Taillow'
            level: 9
  - text: 'Battle Sarah!'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Casey'
        x: -434.5
        "y": 33.0
        z: 510.5
        town: 'Findview Port'
        team:
          - species: 'Torchic'
            level: 15
          - species: 'Skitty'
            level: 11
  - text: 'Battle Casey!'
    location:
      kind: 'npc'
      x: -434.5
      "y": 33.0
      z: 510.5
      label: 'Casey'
      town: 'Findview Port'
    rewards:
      - '7500 Trainer XP'
      - '2500 Coins'
      - '2 Tokens'
---
