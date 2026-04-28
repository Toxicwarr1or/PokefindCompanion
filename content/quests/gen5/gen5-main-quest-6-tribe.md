---
title: 'Main Quest 6 - A New Family'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_6_tribe'
slug: 'gen5-main-quest-6-tribe'
description: 'New situations can be scary but the tribe has its arms wide open to welcome a new family member. Let''s get to know them!'
author: 'Mmaarten'
source_file: 'gen5-main-quest-6-tribe.json'
video_id: 'vXXbmMVURGc'
video_title: 'A New Family (Episode 17: Main Quest 6 - Sophro)'
start:
  npc: 'Anthony'
  description: 'Anthony in Greenholm'
  town: 'Greenholm'
  x: -333.6
  "y": 48.0
  z: -48.5
steps:
  - text: 'Talk to the members of Sophro'
    location:
      kind: 'destination'
      x: -397.5
      "y": 47.0
      z: -63.5
      label: 'Talk to Greta in Greenholm'
      town: 'Greenholm'
  - text: 'Find Greta''s Purrloin hiding around Greenholm'
    location:
      kind: 'npc'
      x: -428.5
      "y": 48.0
      z: -11.5
      label: 'Purrloin'
      town: 'Greenholm'
  - text: 'Return the Purrloin to Greta'
    location:
      kind: 'destination'
      x: -397.5
      "y": 47.0
      z: -63.5
      label: 'Return to Greta'
      town: 'Greenholm'
  - text: 'See if you can meet another tribe member'
    location:
      kind: 'destination'
      x: -358.5
      "y": 49.1
      z: -75.5
      label: 'Talk to Beth in Greenholm'
      town: 'Greenholm'
  - text: 'Plant some flowers by clicking the sparkling podzol'
    location:
      kind: 'destination'
      x: 1.0
      "y": -363.0
      z: 47.0
      town: 'Everhallow'
  - text: 'Return to the Ancient Temple and find the new sewaddle puzzle'
    location:
      kind: 'destination'
      x: -498.5
      "y": 73.0
      z: 39.5
      label: 'Travel back to the Ancient Temple in Greenholm'
      town: 'Greenholm'
  - text: 'Guide the Sewaddle to the oxeye daisy to unlock the door'
    location:
      kind: 'npc'
      x: -474.5
      "y": 33.0
      z: 59.5
      label: 'Sewaddle'
      town: 'Greenholm'
  - text: 'Travel through the Ancient Temple'
    location:
      kind: 'region'
      x: -425.0
      "y": 37.0
      z: 58.0
      bbox:
        x1: -438.0
        "y1": 30.0
        z1: 38.0
        x2: -412.0
        "y2": 44.0
        z2: 78.0
      town: 'Greenholm'
  - text: 'Prove your worth by battling the first Guardian'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Guardian 1'
        x: -424.5
        "y": 33.0
        z: 52.5
        town: 'Greenholm'
        team:
          - species: 'Jellicent'
            level: 65
          - species: 'Garbodor'
            level: 67
          - species: 'Amoonguss'
            level: 66
          - species: 'Galvantula'
            level: 68
          - species: 'Ferrothorn'
            level: 65
          - species: 'Eelektross'
            level: 68
          - species: 'Lampent'
            level: 66
          - species: 'Beartic'
            level: 62
          - species: 'Accelgor'
            level: 66
          - species: 'Golurk'
            level: 66
          - species: 'Bouffalant'
            level: 68
          - species: 'Braviary'
            level: 68
          - species: 'Alomomola'
            level: 70
          - species: 'Escavalier'
            level: 70
  - text: 'Collect the first key shard'
    location:
      kind: 'destination'
      x: -424.5
      "y": 36.0
      z: 35.5
      town: 'Greenholm'
  - text: 'Battle the second Guardian'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Guardian 2'
        x: -424.5
        "y": 33.0
        z: 66.5
        town: 'Greenholm'
        team:
          - species: 'Jellicent'
            level: 65
          - species: 'Garbodor'
            level: 67
          - species: 'Amoonguss'
            level: 66
          - species: 'Galvantula'
            level: 68
          - species: 'Ferrothorn'
            level: 65
          - species: 'Eelektross'
            level: 68
          - species: 'Lampent'
            level: 66
          - species: 'Beartic'
            level: 62
          - species: 'Accelgor'
            level: 66
          - species: 'Golurk'
            level: 66
          - species: 'Bouffalant'
            level: 68
          - species: 'Braviary'
            level: 68
          - species: 'Alomomola'
            level: 70
          - species: 'Escavalier'
            level: 70
  - text: 'Collect the second key shard'
    location:
      kind: 'destination'
      x: -424.5
      "y": 36.0
      z: 83.5
      town: 'Greenholm'
  - text: 'Proceed to the next room to unlock the door'
    location:
      kind: 'region'
      x: -402.0
      "y": 36.0
      z: 59.0
      bbox:
        x1: -407.0
        "y1": 31.0
        z1: 50.0
        x2: -397.0
        "y2": 41.0
        z2: 68.0
      town: 'Greenholm'
  - text: 'Speak to Astrid at the very end of the Ancient Temple'
    location:
      kind: 'npc'
      x: -330.0
      "y": 33.0
      z: 61.5
      label: 'Astrid'
      town: 'Greenholm'
  - text: 'Protect Zekrom from the Company'
    location:
      kind: 'npc'
      x: -313.5
      "y": 35.3
      z: 59.5
      label: 'Zekrom Master Ball'
      town: 'Greenholm'
  - text: 'Battle Danielle to protect Zekrom and Reshiram'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: -339.0
        "y": 32.0
        z: 59.5
        town: 'Greenholm'
        team:
          - species: 'Emboar'
            level: 70
          - species: 'Haxorus'
            level: 69
          - species: 'Gigalith'
            level: 68
          - species: 'Unfezant'
            level: 68
          - species: 'Simisage'
            level: 70
          - species: 'Liepard'
            level: 69
    rewards:
      - '35000 Coins'
      - '35 Tokens'
      - '40000 Trainer XP'
      - '20× material'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
      - 'Grassy Seed'
      - 'Misty Seed'
      - 'Electric Seed'
      - 'Psychic Seed'
---
