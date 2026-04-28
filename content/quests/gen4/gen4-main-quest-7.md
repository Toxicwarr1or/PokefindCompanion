---
title: 'Main Quest 7 - Time Vortex'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_7'
slug: 'gen4-main-quest-7'
description: 'Team Cosmic Star seems to be moving onto the final phase of their plan. Find the location of their headquarters and stop them once and for all.'
source_file: 'gen4-main-quest-7.json'
video_id: 'MPydDg7_s0M'
video_title: 'End of Main Quest 7 - Sophro'
start:
  npc: 'Officer Ryan'
  town: 'Circuit City'
  x: -347.5
  "y": 26.0
  z: 727.5
steps:
  - text: 'Find the kids near the Pokemon Center'
    location:
      kind: 'region'
      x: -277.5
      "y": 31.0
      z: 874.0
      bbox:
        x1: -279.0
        "y1": 29.0
        z1: 866.0
        x2: -276.0
        "y2": 33.0
        z2: 882.0
      town: 'Circuit City'
  - text: 'Get within hearing range without being seen'
  - text: 'Get out of hearing range'
    location:
      kind: 'region'
      x: -1243.5
      "y": 35.0
      z: -945.0
      bbox:
        x1: -1247.0
        "y1": 33.0
        z1: -950.0
        x2: -1240.0
        "y2": 37.0
        z2: -940.0
      town: 'Circuit City'
  - text: 'Locate and enter the Team Cosmic Star HQ in the volcanic mountain'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: -1242.5
        "y": 34.0
        z: -950.5
        town: 'Circuit City'
        team:
          - species: 'Dusknoir'
            level: 75
          - species: 'Houndoom'
            level: 75
          - species: 'Camerupt'
            level: 75
          - species: 'Rhyperior'
            level: 75
  - text: 'Make your way through the HQ, defeating all Cosmic Star grunts in your path'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: -1246.5
        "y": 50.9375
        z: -1012.5
        town: 'Circuit City'
        team:
          - species: 'Gliscor'
            level: 75
          - species: 'Magmortar'
            level: 75
          - species: 'Toxicroak'
            level: 76
          - species: 'Lickilicky'
            level: 75
      - trainer: 'Cosmic Star Grunt'
        x: -1214.5
        "y": 58.9375
        z: -988.5
        town: 'Circuit City'
        team:
          - species: 'Rampardos'
            level: 76
          - species: 'Snorlax'
            level: 76
          - species: 'Crobat'
            level: 75
          - species: 'Ninetales'
            level: 76
      - trainer: 'Cosmic Star Grunt'
        x: -1265.5
        "y": 63.9375
        z: -977.5
        town: 'Circuit City'
        team:
          - species: 'Bastiodon'
            level: 76
          - species: 'Purugly'
            level: 77
          - species: 'Drifblim'
            level: 75
          - species: 'Tyranitar'
            level: 76
      - trainer: 'Cosmic Star Grunt'
        x: -1287.5
        "y": 67.9375
        z: -1006.5
        town: 'Circuit City'
        team:
          - species: 'Hippowdon'
            level: 76
          - species: 'Machamp'
            level: 77
          - species: 'Probopass'
            level: 77
          - species: 'Toxicroak'
            level: 76
      - trainer: 'Cosmic Star Grunt'
        x: -1246.5
        "y": 71.9375
        z: -1011.5
        town: 'Circuit City'
        team:
          - species: 'Mismagius'
            level: 76
          - species: 'Umbreon'
            level: 77
          - species: 'Skuntank'
            level: 77
          - species: 'Scizor'
            level: 77
      - trainer: 'Cosmic Star Grunt'
        x: -1264.5
        "y": 72.9375
        z: -1056.5
        town: 'Circuit City'
        team:
          - species: 'Lucario'
            level: 77
          - species: 'Electivire'
            level: 77
          - species: 'Gengar'
            level: 78
          - species: 'Armaldo'
            level: 77
      - trainer: 'Cosmic Star Grunt'
        x: -1304.5
        "y": 68.9375
        z: -1034.5
        town: 'Circuit City'
        team:
          - species: 'Metagross'
            level: 77
          - species: 'Flygon'
            level: 78
          - species: 'Mismagius'
            level: 78
          - species: 'Rhyperior'
            level: 77
      - trainer: 'Cosmic Star Grunt'
        x: -1350.5
        "y": 68.9375
        z: -1078.5
        town: 'Circuit City'
        team:
          - species: 'Spiritomb'
            level: 78
          - species: 'Hippowdon'
            level: 78
          - species: 'Luxray'
            level: 77
          - species: 'Medicham'
            level: 78
      - trainer: 'Cosmic Star Grunt'
        x: -1367.5
        "y": 71.9375
        z: -1106.5
        town: 'Circuit City'
        team:
          - species: 'Steelix'
            level: 78
          - species: 'Salamence'
            level: 78
          - species: 'Toxicroak'
            level: 77
          - species: 'Starmie'
            level: 78
      - trainer: 'Karminrot'
        x: -1356.5
        "y": 69.0
        z: -1166.5
        town: 'Circuit City'
        team:
          - species: 'Gallade'
            level: 79
          - species: 'Porygon-Z'
            level: 80
          - species: 'Gliscor'
            level: 80
          - species: 'Drapion'
            level: 79
          - species: 'Tangrowth'
            level: 80
  - text: 'Go to Haru and Sora'
    location:
      kind: 'npc'
      x: -1356.5
      "y": 70.0
      z: -1203.5
      label: 'Haru'
      town: 'Circuit City'
  - text: 'Find a way to free Uxie, Mesprit and Azelf'
  - text: 'Flick the levers one by one to free the Guardians'
    location:
      kind: 'region'
      x: -1350.0
      "y": 71.0
      z: -1181.0
      bbox:
        x1: -1352.0
        "y1": 69.0
        z1: -1183.0
        x2: -1348.0
        "y2": 73.0
        z2: -1179.0
      town: 'Circuit City'
  - text: 'Go to Sora and Haru'
    location:
      kind: 'npc'
      x: -1354.5
      "y": 70.0
      z: -1203.5
      label: 'Sora'
      town: 'Circuit City'
  - text: 'Get to the Giratina before it disappears'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Danielle'
        x: 724.0
        "y": 3.0
        z: 1036.5
        town: 'Circuit City'
        team:
          - species: 'Empoleon'
            level: 78
          - species: 'Togekiss'
            level: 77
          - species: 'Chimecho'
            level: 79
          - species: 'Lopunny'
            level: 78
          - species: 'Blissey'
            level: 79
          - species: 'Roserade'
            level: 80
  - text: 'Explore the area'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Professor Hemlock'
        x: 677.5
        "y": 3.0
        z: 1057.5
        town: 'Circuit City'
        team:
          - species: 'Torterra'
            level: 81
          - species: 'Swampert'
            level: 80
          - species: 'Alakazam'
            level: 81
          - species: 'Togekiss'
            level: 80
  - text: 'Keep exploring the area'
    location:
      kind: 'region'
      x: 698.0
      "y": 5.0
      z: 1057.0
      bbox:
        x1: 696.0
        "y1": 2.0
        z1: 1055.0
        x2: 700.0
        "y2": 8.0
        z2: 1059.0
      town: 'Circuit City'
  - text: 'Follow Uxie'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Strom'
        x: -607.5
        "y": 27.9375
        z: 1032.5
        town: 'Circuit City'
        team:
          - species: 'Magnezone'
            level: 80
          - species: 'Luxray'
            level: 81
          - species: 'Electivire'
            level: 81
          - species: 'Rotom'
            level: 82
  - text: 'Explore the area'
    location:
      kind: 'region'
      x: -608.0
      "y": 29.5
      z: 1064.0
      bbox:
        x1: -610.0
        "y1": 27.0
        z1: 1062.0
        x2: -606.0
        "y2": 32.0
        z2: 1066.0
      town: 'Circuit City'
  - text: 'Follow Mesprit'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Cynthia'
        x: 1063.5
        "y": 2.0
        z: 994.5
        town: 'Circuit City'
        team:
          - species: 'Spiritomb'
            level: 82
          - species: 'Roserade'
            level: 83
          - species: 'Togekiss'
            level: 83
          - species: 'Lucario'
            level: 82
          - species: 'Milotic'
            level: 83
          - species: 'Garchomp'
            level: 84
  - text: 'Explore the area'
    location:
      kind: 'region'
      x: 1075.0
      "y": 5.0
      z: 976.5
      bbox:
        x1: 1073.0
        "y1": 2.0
        z1: 975.0
        x2: 1077.0
        "y2": 8.0
        z2: 978.0
      town: 'Circuit City'
  - text: 'Follow Azelf'
    location:
      kind: 'region'
      x: 1100.0
      "y": 4.5
      z: 978.0
      bbox:
        x1: 1098.0
        "y1": 1.0
        z1: 976.0
        x2: 1102.0
        "y2": 8.0
        z2: 980.0
      town: 'Circuit City'
  - text: 'Explore the area'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Sora'
        x: 1534.5
        "y": 35.0
        z: 1110.5
        town: 'Circuit City'
        team:
          - species: 'Empoleon'
            level: 84
          - species: 'Milotic'
            level: 84
          - species: 'Suicune'
            level: 84
          - species: 'Slowbro'
            level: 85
          - species: 'Kyogre'
            level: 85
  - text: 'Defeat Sora'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Haru'
        x: 1532.5
        "y": 35.0
        z: 1111.5
        town: 'Circuit City'
        team:
          - species: 'Infernape'
            level: 85
          - species: 'Arcanine'
            level: 84
          - species: 'Entei'
            level: 85
          - species: 'Groudon'
            level: 85
          - species: 'Giratina'
            level: 86
  - text: 'Defeat Haru'
    location:
      kind: 'npc'
      x: -1356.5
      "y": 70.0
      z: -1203.5
      label: 'Haru'
      town: 'Circuit City'
  - text: 'Go to Danielle and the Professor'
    location:
      kind: 'npc'
      x: 724.0
      "y": 3.0
      z: 1036.5
      label: 'Danielle'
      town: 'Circuit City'
    rewards:
      - '25000 Coins'
      - '20 Tokens'
      - '250000 Trainer XP'
      - 'Heat_Rock'
---
