---
title: 'Lets Go Fishing!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'DIVEBALLQUEST'
slug: 'dive-ball'
description: 'Nothing like a relaxing day of fishing!'
source_file: 'dive-ball.json'
start:
  npc: 'Miranda'
  x: -1434.5
  "y": 24.0625
  z: 215.5
steps:
  - text: 'Find Miranda down at the water'
    location:
      kind: 'npc'
      x: -1458.5
      "y": 20.0
      z: 225.5
      label: 'Miranda'
  - text: 'Catch a Magikarp and give it to Miranda'
    location:
      kind: 'npc'
      x: -1458.5
      "y": 20.0
      z: 225.5
      label: 'Miranda'
  - text: 'Catch a Marill and give it to Miranda'
    location:
      kind: 'npc'
      x: -1458.5
      "y": 20.0
      z: 225.5
      label: 'Miranda'
  - text: 'Catch a Poliwag and give it to Miranda'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Miranda'
        x: -1458.5
        "y": 20.0
        z: 210.5
        team:
          - species: 'Lombre'
            level: 20
          - species: 'Pelipper'
            level: 22
          - species: 'Carvanha'
            level: 23
          - species: 'Wailmer'
            level: 26
          - species: 'Luvdisc'
            level: 31
    rewards:
      - '5000 Coins'
      - '5 Tokens'
      - '7500 Trainer XP'
      - '12× Dive Ball'
      - 'Water Stone'
---
