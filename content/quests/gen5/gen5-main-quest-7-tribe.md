---
title: 'Main Quest 7 - Making Friends'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_7_tribe'
slug: 'gen5-main-quest-7-tribe'
description: 'Friends, allies, non-enemies, ... when everything is on the line, it is all the same. Time to create some new bonds and create unity.'
author: 'Mmaarten'
source_file: 'gen5-main-quest-7-tribe.json'
video_id: 'PWKSzwSJCXY'
video_title: 'Making Friends (Episode 19: Main Quest 7 - Sophro)'
start:
  npc: 'Astrid'
  description: 'Temple near Greenholm'
  town: 'Sandgate'
  x: -1086.5
  "y": 29.0
  z: 184.5
steps:
  - text: 'Head to the medium sized Ancient Pyramid in Sandgate'
    location:
      kind: 'destination'
      x: -1107.5
      "y": 49.0
      z: 202.5
      label: 'Head to the medium Ancient Pyramid in Sandgate'
      town: 'Sandgate'
  - text: 'Inspect the walls for clues'
  - text: 'Look around the Sandgate gym for clues to the password (Hint > Look up)'
    location:
      kind: 'destination'
      x: -980.5
      "y": 73.0
      z: 172.5
      town: 'Sandgate'
  - text: 'Look around for more clues (Hint > Near a garage)'
    location:
      kind: 'destination'
      x: -1089.5
      "y": 49.0
      z: 166.5
      town: 'Sandgate'
  - text: 'Look for the final piece of information (Hint > Diggy, diggy, hole!)'
    location:
      kind: 'destination'
      x: -1061.5
      "y": 36.0
      z: 246.5
      town: 'Sandgate'
  - text: 'Go back to the Ancient Pyramid'
    location:
      kind: 'npc'
      x: 106.5
      "y": 57.0
      z: -191.5
      label: 'Need to get back to Danielle?'
      town: 'Pokemon League'
  - text: 'Answer the secret word in chat! ''/secretword'' (Clues > ''-ro'' ''So-'' & ''-ph-'')'
  - text: 'Explore the pyramid and find Astrid'
    location:
      kind: 'npc'
      x: -1086.5
      "y": 29.0
      z: 184.5
      label: 'Astrid'
      town: 'Sandgate'
  - text: 'Battle Astrid'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Astrid'
        x: -1086.5
        "y": 29.0
        z: 184.5
        town: 'Sandgate'
        team:
          - species: 'Samurott'
            level: 78
          - species: 'Musharna'
            level: 79
          - species: 'Mandibuzz'
            level: 80
          - species: 'Lilligant'
            level: 70
          - species: 'Jellicent'
            level: 79
          - species: 'Gothitelle'
            level: 80
  - text: 'Exit the Ancient Pyramid with the Ancient Tribe Leader to prepare for the war'
    location:
      kind: 'region'
      x: -1124.0
      "y": 52.0
      z: 202.0
      bbox:
        x1: -1125.0
        "y1": 49.0
        z1: 201.0
        x2: -1123.0
        "y2": 55.0
        z2: 203.0
      town: 'Sandgate'
  - text: 'Beat the final gym and become the Regional Champion by completing Elite Four'
    location:
      kind: 'destination'
      x: 104.5
      "y": 169.9
      z: -283.9
      town: 'Pokemon League'
  - text: 'Defeat Danielle to become the Regional Champion'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: 107.5
        "y": 166.0
        z: -290.5
        town: 'Pokemon League'
        team:
          - species: 'Emboar'
            level: 80
          - species: 'Haxorus'
            level: 77
          - species: 'Gigalith'
            level: 78
          - species: 'Unfezant'
            level: 78
          - species: 'Simisage'
            level: 80
          - species: 'Liepard'
            level: 79
  - text: 'Return to Astrid at the Ancient Pyramid'
    location:
      kind: 'destination'
      x: -1116.5
      "y": 49.0
      z: 203.6
      label: 'Return to Astrid at the Ancient Pyramid'
      town: 'Sandgate'
    rewards:
      - '50000 Coins'
      - '35 Tokens'
      - '135000 Trainer XP'
      - 'Silver Powder'
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
