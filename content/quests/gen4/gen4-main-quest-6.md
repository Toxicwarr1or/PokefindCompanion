---
title: 'Main Quest 6 - Out of Time'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_6'
slug: 'gen4-main-quest-6'
description: 'Team Cosmic Star has taken over Duskburn. Go to the island and prevent them from capturing Azelf'
source_file: 'gen4-main-quest-6.json'
video_id: 'engEWsMOkMc'
video_title: 'Flood of Destruction (Episode 10: Main Quest 6)'
start:
  npc: 'Isaac'
  town: 'Circuit City'
  x: -545.5
  "y": 26.0
  z: 679.5
steps:
  - text: 'Ascend the stairs to the city'
    location:
      kind: 'region'
      x: -752.0
      "y": 83.5
      z: 710.0
      bbox:
        x1: -760.0
        "y1": 81.0
        z1: 702.0
        x2: -744.0
        "y2": 86.0
        z2: 718.0
      town: 'Circuit City'
  - text: 'Get to the crypt without being seen by Team Cosmic Star'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: -752.5
        "y": 81.0
        z: 713.5
        town: 'Circuit City'
        team:
          - species: 'Dusknoir'
            level: 69
          - species: 'Weavile'
            level: 70
          - species: 'Houndoom'
            level: 70
  - text: 'Defeat the Cosmic Star Grunts in the crypt'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: -715.5
        "y": 44.0
        z: 682.5
        town: 'Circuit City'
        team:
          - species: 'Drifblim'
            level: 70
          - species: 'Skuntank'
            level: 71
          - species: 'Shiftry'
            level: 70
          - species: 'Purugly'
            level: 71
      - trainer: 'Cosmic Star Grunt'
        x: -695.5
        "y": 38.0
        z: 692.5
        town: 'Circuit City'
        team:
          - species: 'Drapion'
            level: 71
          - species: 'Spiritomb'
            level: 72
          - species: 'Umbreon'
            level: 72
      - trainer: 'Cosmic Star Grunt'
        x: -696.5
        "y": 32.0
        z: 720.5
        town: 'Circuit City'
        team:
          - species: 'Sharpedo'
            level: 72
          - species: 'Froslass'
            level: 73
          - species: 'Absol'
            level: 73
          - species: 'Tyranitar'
            level: 72
      - trainer: 'Cosmic Star Grunt'
        x: -731.5
        "y": 23.0
        z: 701.5
        town: 'Circuit City'
        team:
          - species: 'Mightyena'
            level: 73
          - species: 'Gengar'
            level: 73
          - species: 'Rotom'
            level: 72
          - species: 'Mismagius'
            level: 72
  - text: 'Confront general Karminrot'
    location:
      kind: 'npc'
      x: -727.5
      "y": 23.0
      z: 673.5
      label: 'Karminrot'
      town: 'Circuit City'
    rewards:
      - '15000 Coins'
      - '10 Tokens'
      - '120000 Trainer XP'
---
