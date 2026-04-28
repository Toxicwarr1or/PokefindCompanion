---
title: 'Message in a Bottle'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'message_in_a_bottle_2'
slug: 'message-in-a-bottle-2'
description: 'Maybe you should try fishing around a bit...'
author: 'eicanfly'
source_file: 'message-in-a-bottle-2.json'
start:
  npc: 'Avery'
  town: 'Baremaw'
  x: -819.5
  "y": 49.0
  z: -270.5
steps:
  - text: 'Head to Baremaw'
    location:
      kind: 'region'
      x: -849.5
      "y": 76.5
      z: -288.0
      bbox:
        x1: -973.0
        "y1": 3.0
        z1: -382.0
        x2: -726.0
        "y2": 150.0
        z2: -194.0
      town: 'Baremaw'
  - text: 'Look around Baremaw and ask a local for help'
    location:
      kind: 'npc'
      x: -819.5
      "y": 49.0
      z: -270.5
      label: 'Avery'
      town: 'Baremaw'
  - text: 'Catch a weedle and bring it to Avery'
    location:
      kind: 'npc'
      x: -819.5
      "y": 49.0
      z: -270.5
      label: 'Avery'
      town: 'Baremaw'
  - text: 'Catch a second weedle and bring it to Avery'
    location:
      kind: 'npc'
      x: -819.5
      "y": 49.0
      z: -270.5
      label: 'Avery'
      town: 'Baremaw'
  - text: 'Catch a third weedle and bring it to Avery'
    location:
      kind: 'npc'
      x: -819.5
      "y": 49.0
      z: -270.5
      label: 'Avery'
      town: 'Baremaw'
  - text: 'Speak to Phoenix near the Baremaw pokemart'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Phoenix'
        x: -584.5
        "y": 57.9
        z: -471.5
        town: 'Baremaw'
        team:
          - species: 'Scolipede'
            level: 80
          - species: 'Garbodor'
            level: 80
          - species: 'Amoonguss'
            level: 85
          - species: 'Skuntank'
            level: 85
          - species: 'Swalot'
            level: 80
          - species: 'Leavanny'
            level: 80
          - species: 'Escavalier'
            level: 85
          - species: 'Accelgor'
            level: 85
          - species: 'Volcarona'
            level: 80
          - species: 'Bisharp'
            level: 85
  - text: 'Speak to Mateo near the Baremaw gym'
    location:
      kind: 'npc'
      x: -849.5
      "y": 75.5
      z: -428.5
      label: 'Mateo'
      town: 'Baremaw'
  - text: 'Find the six evolution stones around Baremaw'
  - text: 'Return to Mateo'
    location:
      kind: 'npc'
      x: -849.5
      "y": 75.5
      z: -428.5
      label: 'Mateo'
      town: 'Baremaw'
  - text: 'Speak to another local near the Pokécenter'
    location:
      kind: 'npc'
      x: -826.5
      "y": 48.0
      z: -271.5
      label: 'Amber'
      town: 'Baremaw'
  - text: 'Chase Amber'
    location:
      kind: 'npc'
      x: -863.5
      "y": 46.0
      z: -335.5
      label: 'Amber'
      town: 'Baremaw'
  - text: 'Continue chasing Amber'
    location:
      kind: 'npc'
      x: -815.5
      "y": 44.0
      z: -388.5
      label: 'Amber'
      town: 'Baremaw'
  - text: 'Continue chasing Amber'
    location:
      kind: 'npc'
      x: -753.5
      "y": 47.0
      z: -456.5
      label: 'Amber'
      town: 'Baremaw'
  - text: 'Speak to another local on the docks'
    location:
      kind: 'npc'
      x: -829.5
      "y": 44.0
      z: -245.5
      label: 'Lane'
      town: 'Baremaw'
  - text: 'Speak to Sydney on the island next to Baremaw'
    location:
      kind: 'npc'
      x: -749.5
      "y": 43.0
      z: -195.5
      label: 'Sydney'
      town: 'Baremaw'
  - text: 'Battle Sydney'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Sydney'
        x: -749.5
        "y": 43.0
        z: -195.5
        town: 'Baremaw'
        team:
          - species: 'Scolipede'
            level: 90
          - species: 'Garbodor'
            level: 90
          - species: 'Amoonguss'
            level: 95
          - species: 'Skuntank'
            level: 95
          - species: 'Swalot'
            level: 90
          - species: 'Leavanny'
            level: 90
          - species: 'Escavalier'
            level: 95
          - species: 'Accelgor'
            level: 95
          - species: 'Volcarona'
            level: 90
          - species: 'Bisharp'
            level: 95
  - text: 'Find Katherine at Sandgate'
    location:
      kind: 'npc'
      x: -1111.5
      "y": 48.0
      z: 132.5
      label: 'Katherine'
      town: 'Sandgate'
  - text: 'Meet Katherine at the grave in Everhallow'
    location:
      kind: 'npc'
      x: 30.5
      "y": 35.0
      z: -47.5
      label: 'Katherine'
      town: 'Everhallow'
  - text: 'Fight the Cofagrigus'
    location:
      kind: 'npc'
      x: 27.5
      "y": 35.0
      z: -48.5
      label: 'cofagrigus_one'
      town: 'Everhallow'
    rewards:
      - '25000 Coins'
      - '30 Tokens'
      - '30000 Trainer XP'
      - 'Ghost Gem'
      - 'Reaper Cloth'
      - 'Fire Stone'
---
