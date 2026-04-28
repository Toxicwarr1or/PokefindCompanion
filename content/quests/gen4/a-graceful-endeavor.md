---
title: 'A Graceful Endeavor'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'A_GRACEFUL_ENDEAVOR'
slug: 'a-graceful-endeavor'
description: 'A young girl needs your help growing a special flower.'
source_file: 'a-graceful-endeavor.json'
start:
  npc: 'Grace'
  x: 24.5
  "y": 26.0
  z: 690.5
steps:
  - text: 'Show Grace a Grass Type Pokémon'
    location:
      kind: 'npc'
      x: 24.5
      "y": 26.0
      z: 690.5
      label: 'Grace'
  - text: 'Stand on the boulder and have your Pokémon till the ground'
  - text: 'Go talk to Grace'
    location:
      kind: 'npc'
      x: 24.5
      "y": 26.0
      z: 690.5
      label: 'Grace'
  - text: 'Stand on the boulder and have use your Water Type Pokémon'
  - text: 'Talk to Grace'
    location:
      kind: 'npc'
      x: 24.5
      "y": 26.0
      z: 690.5
      label: 'Grace'
  - text: 'Follow Grace and speak with her'
    location:
      kind: 'npc'
      x: 30.5
      "y": 26.0
      z: 666.5
      label: 'Grace'
  - text: 'Talk to Grace and battle her Shaymin'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Grace'
        x: 30.5
        "y": 26.0
        z: 666.5
        team:
          - species: 'Shaymin'
            level: 50
    rewards:
      - '10000 Coins'
      - '15 Tokens'
      - '20000 Trainer XP'
      - 'Miracle Seed'
---
