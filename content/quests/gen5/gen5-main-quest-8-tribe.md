---
title: 'Main Quest 8 - The Great War - Sophro'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_8_tribe'
slug: 'gen5-main-quest-8-tribe'
description: 'It all comes down to this. Now is your time to shine!'
author: 'Mmaarten'
source_file: 'gen5-main-quest-8-tribe.json'
video_id: 'y7f7x_xD1YU'
video_title: 'The Great War (Episode 20: Main Quest 8 - Sophro)'
start:
  npc: 'Astrid'
  description: 'Talk to Astrid at the temple near Greenholm'
  town: 'Greenholm'
  x: -500.5
  "y": 64.5
  z: 18.5
steps:
  - text: 'Head to Northrun and enter the Shrine for Kyurem'
    location:
      kind: 'destination'
      x: -78.5
      "y": 60.0
      z: -751.5
      label: 'Head to Northrun and enter the Shrine for Kyurem'
      town: 'Icy Plains'
  - text: 'Follow the path to the top'
    location:
      kind: 'region'
      x: -158.0
      "y": 86.5
      z: -773.0
      bbox:
        x1: -164.0
        "y1": 83.0
        z1: -780.0
        x2: -152.0
        "y2": 90.0
        z2: -766.0
      town: 'Icy Plains'
  - text: 'Navigate through the maze of ice'
    location:
      kind: 'region'
      x: -154.5
      "y": 100.5
      z: -751.0
      bbox:
        x1: -157.0
        "y1": 98.0
        z1: -756.0
        x2: -152.0
        "y2": 103.0
        z2: -746.0
      town: 'Icy Plains'
  - text: 'Beat the second maze in less than 60 seconds'
    location:
      kind: 'region'
      x: -149.0
      "y": 75.0
      z: -728.5
      bbox:
        x1: -149.0
        "y1": 74.0
        z1: -729.0
        x2: -149.0
        "y2": 76.0
        z2: -728.0
      town: 'Icy Plains'
  - text: 'Navigate through the maze of illusions'
    location:
      kind: 'region'
      x: -240.0
      "y": 51.0
      z: -803.5
      bbox:
        x1: -240.0
        "y1": 50.0
        z1: -804.0
        x2: -240.0
        "y2": 52.0
        z2: -803.0
      town: 'Icy Plains'
  - text: 'Pick up the Master Ball'
    location:
      kind: 'npc'
      x: -329.5
      "y": 52.0
      z: -749.5
      label: 'Kyurem Master Ball'
      town: 'Icy Plains'
  - text: 'Follow the path out of the Shrine (There''s a hidden path to the right of the ice mazes)'
    location:
      kind: 'region'
      x: -56.5
      "y": 57.0
      z: -691.0
      bbox:
        x1: -59.0
        "y1": 53.0
        z1: -695.0
        x2: -54.0
        "y2": 61.0
        z2: -687.0
      town: 'Icy Plains'
  - text: 'Battle the Statera members'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Statera Member'
        x: -26.5
        "y": 55.9
        z: -750.5
        town: 'Northrun'
        team:
          - species: 'Jellicent'
            level: 85
          - species: 'Garbodor'
            level: 87
          - species: 'Amoonguss'
            level: 88
          - species: 'Galvantula'
            level: 88
          - species: 'Ferrothorn'
            level: 85
          - species: 'Eelektross'
            level: 88
          - species: 'Lampent'
            level: 86
          - species: 'Beartic'
            level: 82
          - species: 'Accelgor'
            level: 90
          - species: 'Golurk'
            level: 87
          - species: 'Bouffalant'
            level: 88
          - species: 'Braviary'
            level: 88
          - species: 'Alomomola'
            level: 90
          - species: 'Escavalier'
            level: 90
      - trainer: 'Statera Member'
        x: -20.5
        "y": 56.0
        z: -726.5
        town: 'Icy Plains'
        team:
          - species: 'Jellicent'
            level: 85
          - species: 'Garbodor'
            level: 87
          - species: 'Amoonguss'
            level: 88
          - species: 'Galvantula'
            level: 88
          - species: 'Ferrothorn'
            level: 85
          - species: 'Eelektross'
            level: 88
          - species: 'Lampent'
            level: 86
          - species: 'Beartic'
            level: 82
          - species: 'Accelgor'
            level: 90
          - species: 'Golurk'
            level: 87
          - species: 'Bouffalant'
            level: 88
          - species: 'Braviary'
            level: 88
          - species: 'Alomomola'
            level: 90
          - species: 'Escavalier'
            level: 90
  - text: 'Battle the Statera Leader'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Vidar'
        x: -41.5
        "y": 55.0
        z: -752.5
        town: 'Icy Plains'
        team:
          - species: 'Serperior'
            level: 88
          - species: 'Druddigon'
            level: 89
          - species: 'Braviary'
            level: 90
          - species: 'Hydreigon'
            level: 90
          - species: 'Jellicent'
            level: 89
          - species: 'Reuniclus'
            level: 90
  - text: 'Battle Danielle'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: -42.5
        "y": 55.0
        z: -747.5
        town: 'Icy Plains'
        team:
          - species: 'Emboar'
            level: 90
          - species: 'Haxorus'
            level: 87
          - species: 'Gigalith'
            level: 88
          - species: 'Unfezant'
            level: 88
          - species: 'Simisage'
            level: 90
          - species: 'Liepard'
            level: 89
  - text: 'Visit Professor Hemlock at his lab'
    location:
      kind: 'npc'
      x: 638.5
      "y": 49.0
      z: 441.5
      label: 'Professor Hemlock'
      town: 'Findale Harbor'
    rewards:
      - '75000 Coins'
      - '255000 Trainer XP'
      - '45 Tokens'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
      - 'Choice Band'
      - 'Choice Scarf'
      - 'Choice Specs'
---
