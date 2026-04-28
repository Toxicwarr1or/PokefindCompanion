---
title: 'Mine Your Business'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'mine_your_business'
slug: 'mine-your-business'
description: 'Talk to Rick near the mines in Pure Harbor Heights'
source_file: 'mine-your-business.json'
video_id: 'qPR9QYE39VQ'
video_title: 'Mine Your Business (Episode 14: Yearn For The Mines)'
start:
  npc: 'Rick'
  town: 'Pure Harbor Heights'
  x: 1017.5
  "y": 66.0
  z: -661.5
steps:
  - text: 'Follow the railway to get into the mines'
    location:
      kind: 'region'
      x: 1021.0
      "y": 64.5
      z: -659.5
      bbox:
        x1: 1019.0
        "y1": 64.0
        z1: -661.0
        x2: 1023.0
        "y2": 65.0
        z2: -658.0
      town: 'Pure Harbor Heights'
  - text: 'Fight the Pokémon around the mines to save Rick Jr.!'
    location:
      kind: 'npc'
      x: 1047.5
      "y": 33.0
      z: -688.5
      label: 'Kabuto'
      town: 'Pure Harbor Heights'
    rewards:
      - '2500 Coins'
      - '20 Tokens'
      - '3000 Trainer XP'
      - 'Magnet'
---
