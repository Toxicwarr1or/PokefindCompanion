---
title: 'Power Storm'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_SIDEQUEST'
slug: 'gen4-main-quest-sidequest'
description: 'The Pokemon powering the generators disappeared after an enormous storm.'
source_file: 'gen4-main-quest-sidequest.json'
video_id: '8hetNvzL23w'
video_title: 'PokeFind Power Storm (Main Questline, Generation 4)'
start:
  npc: 'Strom'
  town: 'Circuit City'
  x: -302.5
  "y": 29.5
  z: 663.5
steps:
  - text: 'Look around for suspicious people and retrieve the pokemon that power the generator'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Elise'
        x: -299.5
        "y": 30.0
        z: 713.5
        town: 'Circuit City'
        team:
          - species: 'Pachirisu'
            level: 66
      - trainer: 'Zach'
        x: -392.5
        "y": 30.0
        z: 772.5
        town: 'Circuit City'
        team:
          - species: 'Magnezone'
            level: 66
      - trainer: 'Shana'
        x: -292.5
        "y": 30.0
        z: 809.5
        town: 'Circuit City'
        team:
          - species: 'Luxray'
            level: 66
      - trainer: 'Tase'
        x: -244.5
        "y": 29.0
        z: 596.5
        town: 'Circuit City'
        team:
          - species: 'Electivire'
            level: 67
  - text: 'Return to Strom'
    location:
      kind: 'npc'
      x: -302.5
      "y": 29.5
      z: 663.5
      label: 'Strom'
      town: 'Circuit City'
    rewards:
      - '15000 Coins'
      - '15 Tokens'
      - '25000 Trainer XP'
---
