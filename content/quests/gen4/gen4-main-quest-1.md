---
title: 'Main Quest 1 - The Time is now!'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_1'
slug: 'gen4-main-quest-1'
description: 'Professor Hemlock told you about another scientist who lives in Findville Cape. Pay him a visit and listen to what he has to say.'
source_file: 'gen4-main-quest-1.json'
video_id: '1Rv7moTOBmA'
video_title: 'PokeFind Shadow Quest 1'
start:
  npc: 'Isaac'
  x: 916.5
  "y": 72.0
  z: 1016.5
steps:
  - text: 'Battle Danielle'
    location:
      kind: 'npc'
      x: 927.0
      "y": 72.0
      z: 1009.5
      label: 'Danielle'
  - text: 'Go to the lab and find Isaac''s computer'
    location:
      kind: 'npc'
      x: 916.5
      "y": 72.0
      z: 1016.5
      label: 'Isaac'
  - text: 'Return to Isaac'
    location:
      kind: 'npc'
      x: 916.5
      "y": 72.0
      z: 1016.5
      label: 'Isaac'
  - text: 'Find the Clock'
    location:
      kind: 'destination'
      x: 916.5
      "y": 64.5
      z: 1007.5
  - text: 'Chase the pachirisu and retrieve the clock'
    location:
      kind: 'region'
      x: 916.0
      "y": 54.5
      z: 956.5
      bbox:
        x1: 913.0
        "y1": 52.0
        z1: 952.0
        x2: 919.0
        "y2": 57.0
        z2: 961.0
  - text: 'Pick up the Clock the Pachirisu dropped'
    location:
      kind: 'destination'
      x: 956.5
      "y": 52.0
      z: 1029.5
  - text: 'Return to Isaac'
    location:
      kind: 'npc'
      x: 916.5
      "y": 72.0
      z: 1016.5
      label: 'Isaac'
  - text: 'Look for Senex near the docks'
    location:
      kind: 'npc'
      x: 961.5
      "y": 29.0
      z: 847.5
      label: 'Senex'
  - text: 'Return to Isaac'
    location:
      kind: 'npc'
      x: 916.5
      "y": 72.0
      z: 1016.5
      label: 'Isaac'
    rewards:
      - '5000 Coins'
      - '10 Tokens'
      - '2500 Trainer XP'
---
