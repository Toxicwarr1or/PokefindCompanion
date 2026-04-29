---
title: 'Bitter Rivals Part 4'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'bitter4'
slug: 'bitter4'
description: 'After passing through the Safari zone, you encounter your new friends, or are they your rivals?'
source_file: 'bitter4.json'
video_id: 'Ys_V7LncrQo'
video_title: 'PokéFind Bitter Rivals Part 4 (Bitter Rivals: Generation 3)'
start:
  npc: 'Lincoln'
  x: -1184.5
  "y": 48.0
  z: -26.5
steps:
  - text: 'Battle Lincoln!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Sarah'
        x: -1184.5
        "y": 48.0
        z: -20.5
        team:
          - species: 'Grovyle'
            level: 18
          - species: 'Taillow'
            level: 17
          - species: 'Electrike'
            level: 14
  - text: 'Battle Sarah!'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Casey'
        x: -1184.5
        "y": 48.0
        z: -23.5
        team:
          - species: 'Combusken'
            level: 19
          - species: 'Skitty'
            level: 16
          - species: 'Surskit'
            level: 15
  - text: 'Battle Casey!'
    location:
      kind: 'npc'
      x: -1184.5
      "y": 48.0
      z: -23.5
      label: 'Casey'
    rewards:
      - '10000 Trainer XP'
      - '4000 Coins'
      - '5 Tokens'
      - '3× Pp Up'
---
