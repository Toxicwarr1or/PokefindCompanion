---
title: 'Main Quest 3 - Wash Away'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'gen3_main_quest_3'
slug: 'gen3-main-quest-3'
description: 'There was a strange storm at Lodestar Port. Go and investigate.'
source_file: 'gen3-main-quest-3.json'
video_id: 'sE3Bprl1ogQ'
video_title: 'PokeFind Wash Away (Main Quest 3: Generation 3)'
start:
  npc: 'Birchall'
  town: 'Lodestar Port'
  x: 1119.5
  "y": 21.0
  z: -502.5
steps:
  - text: 'Find Gorin on the docks'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Spider'
        x: 1186.5
        "y": 21.0
        z: -468.5
        town: 'Lodestar Port'
        team:
          - species: 'Armaldo'
            level: 55
          - species: 'Ninjask'
            level: 53
  - text: 'Keep searching the docks and find Spider'
    location:
      kind: 'npc'
      x: 1186.5
      "y": 21.0
      z: -468.5
      label: 'Spider'
      town: 'Lodestar Port'
  - text: 'Find the Wingull Egg near the Lighthouse!'
    location:
      kind: 'npc'
      x: 1186.5
      "y": 21.0
      z: -468.5
      label: 'Spider'
      town: 'Lodestar Port'
  - text: 'Return the egg to Spider!'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Margot'
        x: 1203.5
        "y": 21.0
        z: -471.5
        town: 'Lodestar Port'
        team:
          - species: 'Grumpig'
            level: 57
          - species: 'Lunatone'
            level: 55
          - species: 'Chimecho'
            level: 55
  - text: 'Keep searching the docks and find Margot'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Ethan'
        x: 1222.5
        "y": 24.0
        z: -476.5
        town: 'Lodestar Port'
        team:
          - species: 'Claydol'
            level: 59
          - species: 'Espeon'
            level: 57
          - species: 'Chimecho'
            level: 57
  - text: 'Search the docks again and find Ethan'
    location:
      kind: 'npc'
      x: 1222.5
      "y": 24.0
      z: -476.5
      label: 'Ethan'
      town: 'Lodestar Port'
  - text: 'Give Ethan a Magikarp.'
    location:
      kind: 'npc'
      x: 1222.5
      "y": 24.0
      z: -476.5
      label: 'Ethan'
      town: 'Lodestar Port'
    rewards:
      - '10 Coins'
  - text: 'Enter the boat at the end of the docks'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Sora'
        x: 1277.5
        "y": 22.0
        z: -470.5
        town: 'Lodestar Port'
        team:
          - species: 'Ludicolo'
            level: 60
          - species: 'Milotic'
            level: 58
          - species: 'Gorebyss'
            level: 58
  - text: 'Beat Sora'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Minoru'
        x: 1277.5
        "y": 22.0
        z: -468.5
        town: 'Lodestar Port'
        team:
          - species: 'Kadabra'
            level: 60
          - species: 'Medicham'
            level: 60
          - species: 'Metagross'
            level: 60
  - text: 'Beat Minoru'
    location:
      kind: 'npc'
      x: 1277.5
      "y": 22.0
      z: -468.5
      label: 'Minoru'
      town: 'Lodestar Port'
    rewards:
      - '80000 Trainer XP'
      - 'Mystic Water'
      - '13 Tokens'
      - '20000 Coins'
---
