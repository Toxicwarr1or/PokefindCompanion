---
title: 'Lighthouse Panic!'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'LIGHTHOUSE_PANIC'
slug: 'lighthouse-panic'
description: 'The Pokémon who keeps the Cruxirt Port Lighthouse running has fallen ill.'
source_file: 'lighthouse-panic.json'
start:
  npc: 'Jerry'
  town: 'Cruxirt Port'
  x: -511.5
  "y": 74.0
  z: 398.5
steps:
  - text: 'Make your way to the top of the lighthouse'
    location:
      kind: 'npc'
      x: -511.5
      "y": 74.0
      z: 398.5
      label: 'Jerry'
      town: 'Cruxirt Port'
  - text: 'Talk to Jerry again'
    location:
      kind: 'battle'
      town: 'Cruxirt Port'
    battles:
      - trainer: 'Jasmine'
        x: -282.5
        "y": 69.0
        z: 645.5
        town: 'Cruxirt Port'
        team:
          - species: 'Skarmory'
            level: 56
          - species: 'Magneton'
            level: 57
          - species: 'Onix'
            level: 58
          - species: 'Forretress'
            level: 60
          - species: 'Steelix'
            level: 62
          - species: 'Ampharos'
            level: 65
  - text: 'Find Jasmine in Altus City'
    location:
      kind: 'npc'
      x: -513.5
      "y": 113.0
      z: 406.5
      label: 'Jasmine'
      town: 'Altus City'
  - text: 'Talk to Jasmine at the top of Cruxirt Lighthouse'
    location:
      kind: 'npc'
      x: 1196.5
      "y": 71.0
      z: 366.5
      label: 'Winston'
      town: 'Cruxirt Port'
  - text: 'Talk to Winston at MooMoo Farms near Mt. Iron'
    location:
      kind: 'npc'
      x: 1196.5
      "y": 71.0
      z: 366.5
      label: 'Winston'
      town: 'Cruxirt Port'
  - text: 'Find the giant white tulip in Draco Valley'
    location:
      kind: 'region'
      x: 21.0
      "y": 90.5
      z: 408.0
      bbox:
        x1: 11.0
        "y1": 76.0
        z1: 394.0
        x2: 31.0
        "y2": 105.0
        z2: 422.0
      town: 'Draco Valley'
  - text: 'Find the giant mushroom near Zephyrus City Gym'
    location:
      kind: 'npc'
      x: -513.5
      "y": 113.0
      z: 406.5
      label: 'Jasmine'
      town: 'Zephyrus City'
  - text: 'Take the ingredients back to Jasmine'
    location:
      kind: 'npc'
      x: -282.5
      "y": 69.0
      z: 645.5
      label: 'Jasmine'
      town: 'Cruxirt Port'
    rewards:
      - '20000 Coins'
      - '25 Tokens'
      - '25000 Trainer XP'
      - 'Magnet'
      - '24× tm24'
---
