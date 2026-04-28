---
title: 'Main Quest 3 - Discovery of Existence'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_3'
slug: 'gen4-main-quest-3'
description: 'Isaac wants to find the hiding spot of a certain pokemon. You find something else instead...'
source_file: 'gen4-main-quest-3.json'
video_id: 'NZnSbXrKFas'
video_title: 'PokeFind Shadow Quest 3'
start:
  npc: 'Isaac'
  x: 409.5
  "y": 51.0
  z: 161.5
steps:
  - text: 'Interview the locals to find Uxie''s hiding spot'
  - text: 'Return to Isaac'
    location:
      kind: 'npc'
      x: 409.5
      "y": 51.0
      z: 161.5
      label: 'Isaac'
  - text: 'Find the hidden cave entrance in the city'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: 319.5
        "y": 83.0
        z: 101.5
        team:
          - species: 'Cloyster'
            level: 20
          - species: 'Snover'
            level: 21
      - trainer: 'Cosmic Star Grunt'
        x: 287.5
        "y": 60.0
        z: 78.5
        team:
          - species: 'Sneasel'
            level: 21
          - species: 'Snover'
            level: 21
  - text: 'Defeat the remaining Cosmic Star Grunts'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: 266.5
        "y": 44.0
        z: 46.5
        team:
          - species: 'Snover'
            level: 22
          - species: 'Jynx'
            level: 22
          - species: 'Delibird'
            level: 22
      - trainer: 'Cosmic Star Grunt'
        x: 290.5
        "y": 31.0
        z: 72.5
        team:
          - species: 'Miltank'
            level: 23
          - species: 'Golbat'
            level: 22
          - species: 'Sealeo'
            level: 22
      - trainer: 'Cosmic Star General'
        x: 311.5
        "y": 30.0
        z: 91.5
        team:
          - species: 'Gallade'
            level: 25
          - species: 'Porygon-Z'
            level: 24
          - species: 'Skorupi'
            level: 24
          - species: 'Tangela'
            level: 25
  - text: 'Defeat the Team Cosmic Star General'
    location:
      kind: 'npc'
      x: 319.5
      "y": 83.0
      z: 101.5
      label: 'Cosmic Star Grunt'
    rewards:
      - '10 Tokens'
      - '24000 Trainer XP'
      - 'Icy_Rock'
---
