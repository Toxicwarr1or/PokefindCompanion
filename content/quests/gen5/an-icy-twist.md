---
title: 'An Icy Twist'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'an_icy_twist'
slug: 'an-icy-twist'
description: 'Explorer Ivor has made it to Northrun! Speak with him to see if he needs help with his exploration of the region.'
source_file: 'an-icy-twist.json'
start:
  npc: 'Explorer Ivor'
  town: 'Northrun'
  x: 157.5
  "y": 63.0
  z: -701.5
steps:
  - text: 'Race Explorer Ivor to the Icy Stone within 1 minute and 30 seconds'
    location:
      kind: 'npc'
      x: 157.5
      "y": 63.0
      z: -701.5
      label: 'Explorer Ivor'
      town: 'Northrun'
    rewards:
      - '5× Rare Candy'
  - text: 'Battle Explorer Ivor'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Explorer Ivor'
        x: 373.5
        "y": 62.0
        z: -762.5
        town: 'Icy Stone'
        team:
          - species: 'Glaceon'
            level: 100
    rewards:
      - '1500 Coins'
      - '2500 Trainer XP'
      - '15 Tokens'
      - 'Master Ball'
      - 'Ice Stone'
---
