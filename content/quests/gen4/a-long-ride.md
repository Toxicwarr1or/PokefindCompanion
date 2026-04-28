---
title: 'A Long Ride'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'a_long_ride'
slug: 'a-long-ride'
description: 'Help Eive find his missing gold!'
author: 'Eivets500'
source_file: 'a-long-ride.json'
start:
  npc: 'Noah'
  x: 699.5
  "y": 37.0
  z: 542.0
steps:
  - text: 'Find the 1st Gold piece for Noah.'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
  - text: 'Find The 2nd gold piece for Noah.'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
  - text: 'Find the 3rd Gold piece for Noah.'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
  - text: 'Find the 4th Gold piece for Noah.'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
  - text: 'Find the 5th Gold piece for Noah.'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
  - text: 'Go talk to Noah'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Jean'
        x: 725.5
        "y": 39.0
        z: 501.0
        team:
          - species: 'Lumineon'
            level: 45
          - species: 'Mantyke'
            level: 49
          - species: 'Bibarel'
            level: 52
  - text: 'Take the Gold back to Noah'
    location:
      kind: 'npc'
      x: 699.5
      "y": 37.0
      z: 542.0
      label: 'Noah'
    rewards:
      - '15000 Coins'
      - '10 Tokens'
      - '10000 Trainer XP'
      - 'Water_Stone'
---
