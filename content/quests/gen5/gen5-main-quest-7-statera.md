---
title: 'Main Quest 7 - An Experimental Mess'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_7_statera'
slug: 'gen5-main-quest-7-statera'
description: 'Recent developments ask for a serious analysis of the situation. Get ready to test and don''t make a mess...'
author: 'Mmaarten'
source_file: 'gen5-main-quest-7-statera.json'
video_id: 'z20CcpEa_Zo'
video_title: 'An Experimental Mess/Wyvern Badge (Episode 19.1: Main Quest 7 - Statera/Eighth Gym Badge)'
start:
  npc: 'Vidar'
  description: 'H.A.P.P.Y. in Watterson City'
  town: 'Watterson City'
  x: 77.5
  "y": 77.5
  z: 330.4
steps:
  - text: 'Speak with Vidar in his office on the third floor'
    location:
      kind: 'npc'
      x: 77.5
      "y": 77.5
      z: 330.4
      label: 'Vidar'
      town: 'Watterson City'
  - text: 'Get to the Testing Labs on Floor 2'
    location:
      kind: 'destination'
      x: 98.5
      "y": 62.0
      z: 333.5
      label: 'Go to the Testing Labs on Floor 2'
      town: 'Watterson City'
  - text: 'Step into the safety cage in the Testing Lab'
    location:
      kind: 'region'
      x: 97.0
      "y": 63.5
      z: 333.0
      bbox:
        x1: 97.0
        "y1": 63.0
        z1: 333.0
        x2: 97.0
        "y2": 64.0
        z2: 333.0
      town: 'Watterson City'
  - text: 'Meet Vidar in his office on the third floor'
    location:
      kind: 'npc'
      x: 77.5
      "y": 77.5
      z: 330.4
      label: 'Vidar'
      town: 'Watterson City'
  - text: 'Go beat the final gym and become the Elite Four Champion'
    location:
      kind: 'destination'
      x: 1.0
      "y": 101.5
      z: 166.0
      town: 'Watterson City'
  - text: 'Battle Danielle to keep your title of Regional Champion'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: 101.5
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
  - text: 'Return to the Statera Leader in Watterson City'
    location:
      kind: 'npc'
      x: 77.5
      "y": 77.5
      z: 330.4
      label: 'Vidar'
      town: 'Watterson City'
    rewards:
      - '50000 Coins'
      - '35 Tokens'
      - '135000 Trainer XP'
      - 'Light Ball'
      - 'Electirizer'
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
