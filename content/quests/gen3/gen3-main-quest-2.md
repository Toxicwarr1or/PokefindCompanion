---
title: 'Main Quest 2 - Find Your Fire!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'gen3_main_quest_2'
slug: 'gen3-main-quest-2'
description: 'Ayumu is in need of your help...again. Minoru has taken over a mine and is digging deep!'
source_file: 'gen3-main-quest-2.json'
video_id: 't7PQZG8O2Hk'
video_title: 'PokeFind Find Your Fire (Main Quest 2: Generation 3)'
start:
  npc: 'Ayumu'
  town: 'Rockford Bay'
  x: -1204.5
  "y": 28.0
  z: -543.5
steps:
  - text: 'Beat Edna at the mine entrance'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Edna'
        x: -973.5
        "y": 54.0
        z: -405.5
        town: 'Rockford Bay'
        team:
          - species: 'Nosepass'
            level: 25
  - text: 'Beat Clarence next to Edna'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Clarence'
        x: -973.5
        "y": 54.0
        z: -402.5
        town: 'Rockford Bay'
        team:
          - species: 'Lunatone'
            level: 27
          - species: 'Solrock'
            level: 25
  - text: 'Beat the Cave Creeper in the mine'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Cave Creeper'
        x: -875.5
        "y": 38.0
        z: -417.5
        town: 'Rockford Bay'
        team:
          - species: 'Golbat'
            level: 29
          - species: 'Graveler'
            level: 30
  - text: 'Jump in the hole next to the Cave Creeper'
    location:
      kind: 'npc'
      x: -875.5
      "y": 38.0
      z: -417.5
      label: 'Cave Creeper'
      town: 'Rockford Bay'
  - text: 'Beat Ingrid in the mine'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Ingrid'
        x: -927.5
        "y": 74.0
        z: -341.5
        town: 'Rockford Bay'
        team:
          - species: 'Pupitar'
            level: 31
          - species: 'Camerupt'
            level: 32
  - text: 'Beat foreman bill in the mine'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Foreman Bill'
        x: -922.5
        "y": 27.0
        z: -340.5
        town: 'Rockford Bay'
        team:
          - species: 'Claydol'
            level: 36
          - species: 'Vibrava'
            level: 35
          - species: 'Sudowoodo'
            level: 35
  - text: 'Beat Minoru in the mine'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Minoru'
        x: -852.5
        "y": 18.0
        z: -286.5
        town: 'Rockford Bay'
        team:
          - species: 'Kadabra'
            level: 38
          - species: 'Medicham'
            level: 38
          - species: 'Metang'
            level: 38
    rewards:
      - '40000 Trainer XP'
      - 'Charcoal'
      - '15 Tokens'
---
