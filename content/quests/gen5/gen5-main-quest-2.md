---
title: 'Main Quest 2 - Pokémon On The Loose!'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_2'
slug: 'gen5-main-quest-2'
description: 'The Pokémon in Pure Harbor have gone haywire. A trainer should take a look before things get out of hand...'
author: 'Mmaarten'
source_file: 'gen5-main-quest-2.json'
video_id: 'qpbNpIN_bhg'
video_title: 'Pokemon On The Loose! (Episode 7: Main Quest 2)'
start:
  npc: 'Lewis'
  description: 'Talk to Lewis on the bridge to Pure Harbor'
  town: 'Bridgerun'
  x: 1189.7
  "y": 51.0
  z: -90.6
steps:
  - text: 'Join Lewis for a ride across the bridge.'
    location:
      kind: 'npc'
      x: 1189.7
      "y": 51.0
      z: -90.6
      label: 'Lewis'
      town: 'Bridgerun'
  - text: 'Talk to the citizen that is stuck in their home'
    location:
      kind: 'destination'
      x: 925.5
      "y": 48.0
      z: -559.5
      label: 'Talk to the citizen that is stuck in their home'
      town: 'Pure Harbor'
  - text: 'Investigate the shrine on top of the waterfall'
    location:
      kind: 'destination'
      x: 1103.5
      "y": 77.0
      z: -668.5
      label: 'Investigate the shrine on top of the waterfall'
      town: 'Pure Harbor Heights'
  - text: 'Lead the water to the gate using the barriers (Pull a lever to get started)'
  - text: 'Enter the shrine and explore (Complete the first parkour)'
    location:
      kind: 'region'
      x: 1124.0
      "y": 45.0
      z: -607.0
      bbox:
        x1: 1111.0
        "y1": 40.0
        z1: -616.0
        x2: 1137.0
        "y2": 50.0
        z2: -598.0
      town: 'Pure Harbor Heights'
  - text: 'Battle the wild angry Pokémon'
    location:
      kind: 'npc'
      x: 1131.5
      "y": 43.0
      z: -602.0
      label: 'Shrine_Pokemon1'
      town: 'Pure Harbor Heights'
  - text: 'Complete the second parkour'
    location:
      kind: 'region'
      x: 1058.0
      "y": 24.0
      z: -537.5
      bbox:
        x1: 1057.0
        "y1": 21.0
        z1: -540.0
        x2: 1059.0
        "y2": 27.0
        z2: -535.0
      town: 'Pure Harbor Heights'
  - text: 'Talk to the Spirit in the first room'
  - text: 'Talk to the Spirit in the second room'
  - text: 'Continue into the next room of the shrine'
    location:
      kind: 'region'
      x: 1081.5
      "y": 10.5
      z: -434.5
      bbox:
        x1: 1072.0
        "y1": 1.0
        z1: -447.0
        x2: 1091.0
        "y2": 20.0
        z2: -422.0
      town: 'Pure Harbor Heights'
  - text: 'Battle the Ancient Tribe Member'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Dahli'
        x: 1082.5
        "y": 6.0
        z: -431.5
        town: 'Pure Harbor Heights'
        team:
          - species: 'Purrloin'
            level: 19
          - species: 'Pansear'
            level: 22
          - species: 'Scraggy'
            level: 20
          - species: 'Trubbish'
            level: 23
          - species: 'Sandile'
            level: 25
  - text: 'Call Statera HQ to see what''s going on (/call)'
  - text: 'To exit, type /accept'
    location:
      kind: 'destination'
      x: 1103.5
      "y": 77.0
      z: -665.5
      town: 'Pure Harbor Heights'
  - text: 'Check on the Citizen who was trapped in their house'
    location:
      kind: 'destination'
      x: 925.5
      "y": 48.0
      z: -559.5
      label: 'Check on the Citizen who was trapped in their house'
      town: 'Pure Harbor'
  - text: 'Have a friendly battle with your rival'
    location:
      kind: 'battle'
      x: 928.5
      "y": 47.0
      z: -550.5
      label: 'Have a friendly battle with your rival'
      town: 'Pure Harbor'
    battles:
      - trainer: 'Danielle'
        x: 928.8
        "y": 47.0
        z: -550.2
        town: 'Pure Harbor'
        team:
          - species: 'Liepard'
            level: 25
          - species: 'Pansage'
            level: 26
          - species: 'Tranquill'
            level: 28
          - species: 'Pignite'
            level: 30
    rewards:
      - '15000 Coins'
      - '25 Tokens'
      - '10000 Trainer XP'
      - '5× material'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
---
