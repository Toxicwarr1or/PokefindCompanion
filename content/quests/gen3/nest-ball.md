---
title: 'Beginners Luck'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'nest_ball'
slug: 'nest-ball'
description: 'Gabrielle wants to play a game with you!'
source_file: 'nest-ball.json'
start:
  npc: 'Gabrielle'
  town: 'Arc City'
  x: -596.5
  "y": 26.0
  z: 746.5
steps:
  - text: 'Gabrielle is hiding somewhere in Springdale, go find her!'
    location:
      kind: 'npc'
      x: -713.5
      "y": 31.0
      z: 731.5
      label: 'Gabrielle'
      town: 'Arc City'
  - text: 'Gabrielle is hidden, find her. . . again!'
    location:
      kind: 'battle'
      town: 'Arc City'
    battles:
      - trainer: 'Gabrielle'
        x: -762.5
        "y": 33.0
        z: 748.5
        town: 'Arc City'
        team:
          - species: 'Surskit'
            level: 5
          - species: 'Zigzagoon'
            level: 7
          - species: 'Seedot'
            level: 9
  - text: 'Gabrielle has hid away once more, find her for the final time!'
    location:
      kind: 'npc'
      x: -596.5
      "y": 26.0
      z: 746.5
      label: 'Gabrielle'
      town: 'Arc City'
    rewards:
      - '10 Tokens'
      - '10000 Trainer XP'
      - '12× Nest Ball'
---
