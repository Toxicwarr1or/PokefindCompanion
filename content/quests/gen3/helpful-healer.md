---
title: 'Helpful Healer'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'HEALBALLQUEST'
slug: 'helpful-healer'
description: 'A little girl is lost, and her Pokemon is injured.'
source_file: 'helpful-healer.json'
start:
  npc: 'Vivian'
  x: 629.5
  "y": 25.0
  z: 274.5
steps:
  - text: 'Take Vivian to the Pokemon Center'
    location:
      kind: 'npc'
      x: 715.5
      "y": 29.9375
      z: 353.5
      label: 'Vivian'
  - text: 'Talk to Vivian in her home by the marketplace'
    location:
      kind: 'npc'
      x: 629.5
      "y": 25.0
      z: 274.5
      label: 'Vivian'
    rewards:
      - '2000 Coins'
      - '5 Tokens'
      - '1500 Trainer XP'
      - '12× Heal Ball'
---
