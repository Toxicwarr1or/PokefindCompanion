---
title: 'Main Quest 4 - An Ancient Encounter'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_4'
slug: 'gen5-main-quest-4'
description: 'Statera has a special mission for you and Danielle. Something about... the past?'
author: 'Mmaarten'
source_file: 'gen5-main-quest-4.json'
video_id: 'fmyB9VUxShM'
video_title: 'Complete Magma Puzzle Guide (Main Quest 4: An Ancient Encounter)'
start:
  npc: 'Agent Ty'
  description: 'H.A.P.P.Y. in Watterson City'
  town: 'Watterson City'
  x: 76.3
  "y": 77.0
  z: 341.1
steps:
  - text: 'Provide H.A.P.P.Y. with the password to enter the headquarters (Use /youranswer) HINT> Company Name'
  - text: 'Talk to Agent Ty on the third floor'
    location:
      kind: 'npc'
      x: 76.3
      "y": 77.0
      z: 341.1
      label: 'Agent Ty'
      town: 'Watterson City'
  - text: 'Head over to Redgrove and find the secret entrance to their base by the Volcano'
    location:
      kind: 'destination'
      x: -790.5
      "y": 51.0
      z: 772.5
      label: 'Head to the Redgrove secret entrance by the volcano'
      town: 'Redgrove'
  - text: 'Solve the magma puzzle inside the volcano'
    location:
      kind: 'destination'
      x: -789.5
      "y": 51.0
      z: 732.5
      town: 'Redgrove'
  - text: 'Enter the cave and find the Ancient Tribe Elders'
    location:
      kind: 'region'
      x: -791.0
      "y": 52.5
      z: 724.5
      bbox:
        x1: -794.0
        "y1": 50.0
        z1: 724.0
        x2: -788.0
        "y2": 55.0
        z2: 725.0
      town: 'Redgrove'
  - text: 'Battle the first Sophro Elder across the parkour'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Anthony'
        x: -804.5
        "y": 12.0
        z: 650.5
        town: 'Redgrove'
        team:
          - species: 'Jellicent'
            level: 45
          - species: 'Garbodor'
            level: 47
          - species: 'Amoonguss'
            level: 46
          - species: 'Galvantula'
            level: 48
          - species: 'Ferrothorn'
            level: 45
          - species: 'Eelektross'
            level: 48
          - species: 'Lampent'
            level: 46
          - species: 'Beartic'
            level: 42
          - species: 'Accelgor'
            level: 46
          - species: 'Golurk'
            level: 46
          - species: 'Bouffalant'
            level: 47
          - species: 'Braviary'
            level: 48
          - species: 'Alomomola'
            level: 45
          - species: 'Escavalier'
            level: 48
  - text: 'Head to the next room'
    location:
      kind: 'region'
      x: -851.0
      "y": 29.5
      z: 689.0
      bbox:
        x1: -851.0
        "y1": 28.0
        z1: 686.0
        x2: -851.0
        "y2": 31.0
        z2: 692.0
      town: 'Redgrove'
  - text: 'Defeat the second Tribe Elder'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Fatih'
        x: -865.8
        "y": 28.0
        z: 683.4
        town: 'Redgrove'
        team:
          - species: 'Jellicent'
            level: 45
          - species: 'Garbodor'
            level: 47
          - species: 'Amoonguss'
            level: 46
          - species: 'Galvantula'
            level: 48
          - species: 'Ferrothorn'
            level: 45
          - species: 'Eelektross'
            level: 48
          - species: 'Lampent'
            level: 46
          - species: 'Beartic'
            level: 42
          - species: 'Accelgor'
            level: 46
          - species: 'Golurk'
            level: 46
          - species: 'Bouffalant'
            level: 47
          - species: 'Braviary'
            level: 48
          - species: 'Alomomola'
            level: 45
          - species: 'Escavalier'
            level: 48
  - text: 'Head to the next room and battle the third Sophro Elder'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Beth'
        x: -891.5
        "y": 20.0
        z: 667.5
        town: 'Redgrove'
        team:
          - species: 'Jellicent'
            level: 45
          - species: 'Garbodor'
            level: 47
          - species: 'Amoonguss'
            level: 46
          - species: 'Galvantula'
            level: 48
          - species: 'Ferrothorn'
            level: 45
          - species: 'Eelektross'
            level: 48
          - species: 'Lampent'
            level: 46
          - species: 'Beartic'
            level: 42
          - species: 'Accelgor'
            level: 46
          - species: 'Golurk'
            level: 46
          - species: 'Bouffalant'
            level: 47
          - species: 'Braviary'
            level: 48
          - species: 'Alomomola'
            level: 45
          - species: 'Escavalier'
            level: 48
  - text: 'Head to the next room and battle the fourth Sophro Elder'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Greta'
        x: -849.4
        "y": 14.0
        z: 815.5
        town: 'Redgrove'
        team:
          - species: 'Jellicent'
            level: 45
          - species: 'Garbodor'
            level: 47
          - species: 'Amoonguss'
            level: 46
          - species: 'Galvantula'
            level: 48
          - species: 'Ferrothorn'
            level: 45
          - species: 'Eelektross'
            level: 48
          - species: 'Lampent'
            level: 46
          - species: 'Beartic'
            level: 42
          - species: 'Accelgor'
            level: 46
          - species: 'Golurk'
            level: 46
          - species: 'Bouffalant'
            level: 47
          - species: 'Braviary'
            level: 48
          - species: 'Alomomola'
            level: 45
          - species: 'Escavalier'
            level: 48
  - text: 'Head to the next room and battle the Ancient Tribe Leader'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Astrid'
        x: -847.5
        "y": 13.0
        z: 887.5
        town: 'Redgrove'
        team:
          - species: 'Samurott'
            level: 48
          - species: 'Musharna'
            level: 49
          - species: 'Mandibuzz'
            level: 50
          - species: 'Lilligant'
            level: 50
          - species: 'Jellicent'
            level: 49
          - species: 'Gothitelle'
            level: 50
  - text: 'Return to Agent Ty with this new information'
    location:
      kind: 'destination'
      x: 76.3
      "y": 77.0
      z: 341.5
      label: 'Return to Agent Ty'
      town: 'Watterson City'
    rewards:
      - '25000 Coins'
      - '25 Tokens'
      - '25000 Trainer XP'
      - '10× material'
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
