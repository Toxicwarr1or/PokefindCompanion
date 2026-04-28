---
title: 'Main Quest 10 - United We Stand...'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_10'
slug: 'gen5-main-quest-10'
description: 'Team Plasma has taken root somewhere in Zeinova. In the years following the fall of Statera, the region has expanded. What secrets these new lands hold is up to you to find out.'
author: 'Toxicwarr1or'
source_file: 'gen5-main-quest-10.json'
video_id: '4NRP91WsAQk'
video_title: 'Main Quest 10 - United We Stand Stand...'
start:
  npc: 'Jessica'
  description: 'Talk to Citizen Jessica on the massive bridge leaving Breezelton to the East'
  town: 'Breezelton Village'
  x: 1086.5
  "y": 52.0
  z: 365.5
steps:
  - text: 'Cross the bridge and head to Sparkmont to find another Citizen'
    location:
      kind: 'npc'
      x: 1402.5
      "y": 83.0
      z: 762.5
      label: 'Bobby'
      town: 'Sparkmont City'
  - text: 'Battle Team Plasma Grunt Corven'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Corven'
        x: 1405.5
        "y": 83.0
        z: 761.5
        town: 'Sparkmont City'
        team:
          - species: 'Hydreigon'
            level: 100
          - species: 'Weavile'
            level: 100
          - species: 'Crobat'
            level: 100
          - species: 'Tyranitar'
            level: 100
          - species: 'Bisharp'
            level: 100
          - species: 'Chandelure'
            level: 100
  - text: 'Battle Team Plasma Grunt Brisa'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Brisa'
        x: 1405.5
        "y": 83.0
        z: 763.5
        town: 'Sparkmont City'
        team:
          - species: 'Gengar'
            level: 100
          - species: 'Drapion'
            level: 100
          - species: 'Honchkrow'
            level: 100
          - species: 'Spiritomb'
            level: 100
          - species: 'Armaldo'
            level: 100
          - species: 'Togekiss'
            level: 100
  - text: 'Chat with Bobby'
    location:
      kind: 'npc'
      x: 1402.5
      "y": 83.0
      z: 762.5
      label: 'Bobby'
      town: 'Sparkmont City'
  - text: 'Find Nurse Rosie at the Pokecenter'
    location:
      kind: 'npc'
      x: 1416.5
      "y": 89.0
      z: 867.5
      label: 'Nurse Rosie'
      town: 'Sparkmont City'
  - text: 'Find five pieces of fruit under the palm trees near the border with Voltaris (Hint: Follow the path going past the Pokecenter that leads to stairs down to the edge of the city)'
    location:
      kind: 'destination'
      x: 1436.5
      "y": 54.0
      z: 1046.5
      town: 'Sparkmont City'
    rewards:
      - 'Draco_Plate'
      - 'Meadow_Plate'
      - 'Pixie_Plate'
      - 'Mind_Plate'
      - 'Spooky_Plate'
      - 'Earth_Plate'
      - 'Toxic_Plate'
      - 'Insect_Plate'
      - 'Fist_Plate'
      - 'Splash_Plate'
      - 'Zap_Plate'
      - 'Sky_Plate'
      - 'Flame_Plate'
      - 'Iron_Plate'
      - 'Stone_Plate'
      - 'Dread_Plate'
      - 'Icicle_Plate'
  - text: 'Return the fruit to Nurse Rosie at the Pokecenter'
    location:
      kind: 'npc'
      x: 1416.5
      "y": 89.0
      z: 867.5
      label: 'Nurse Rosie'
      town: 'Sparkmont City'
  - text: 'Check out the Plasma assembly outside the gym in Sparkmont'
    location:
      kind: 'region'
      x: 1646.5
      "y": 99.5
      z: 762.0
      bbox:
        x1: 1625.0
        "y1": 84.0
        z1: 743.0
        x2: 1668.0
        "y2": 115.0
        z2: 781.0
      town: 'Sparkmont City'
  - text: 'Check-in with the citizens of Sparkmont'
    location:
      kind: 'npc'
      x: 1638.5
      "y": 84.0
      z: 764.5
      label: 'Roughneck Tom'
      town: 'Sparkmont City'
  - text: 'Battle N'
    location:
      kind: 'battle'
    battles:
      - trainer: 'N'
        x: 1645.5
        "y": 84.0
        z: 762.5
        town: 'Sparkmont City'
        team:
          - species: 'Zoroark'
            level: 102
          - species: 'Carracosta'
            level: 101
          - species: 'Klinklang'
            level: 100
          - species: 'Sigilyph'
            level: 104
          - species: 'Landorus'
            level: 105
          - species: 'Vanilluxe'
            level: 103
  - text: 'Cross the stepping stones into Voltaris. (Hint: The stepping stones are where you collected the fruit for Nurse Rosie)'
    location:
      kind: 'npc'
      x: 1416.5
      "y": 89.0
      z: 867.5
      label: 'Nurse Rosie'
      town: 'Sparkmont City'
  - text: 'Continue into Voltaris and find Danielle'
    location:
      kind: 'npc'
      x: 1429.0
      "y": 43.0
      z: 1159.5
      label: 'Danielle'
      town: 'Voltaris Island'
  - text: 'Follow Danielle'
    location:
      kind: 'npc'
      x: 1535.0
      "y": 43.0
      z: 1191.5
      label: 'Danielle'
      town: 'Voltaris Island'
  - text: 'Find Danielle at one of the entrances Team Plasma hasn''t blocked off. (Hint: Check the top of the hill where the Grunts are guarding, or the river for a secret entrance)'
    location:
      kind: 'npc'
      x: 1575.5
      "y": 79.0
      z: 1216.5
      label: 'Danielle'
      town: 'Voltaris Island'
  - text: 'Locate a member of Team Plasma in the cave.'
    location:
      kind: 'npc'
      x: 1512.5
      "y": 14.0
      z: 1242.5
      label: 'Ulric'
      town: 'Voltaris Island'
  - text: 'Battle Plasma Grunt Ulric.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Ulric'
        x: 1512.5
        "y": 14.0
        z: 1242.5
        town: 'Voltaris Island'
        team:
          - species: 'Togekiss'
            level: 100
          - species: 'Krookodile'
            level: 100
          - species: 'Volcarona'
            level: 100
          - species: 'Reuniclus'
            level: 100
          - species: 'Chandelure'
            level: 100
          - species: 'Conkeldurr'
            level: 100
  - text: 'Continue through the tunnel.'
    location:
      kind: 'region'
      x: 1504.5
      "y": 13.0
      z: 1240.0
      bbox:
        x1: 1500.0
        "y1": 10.0
        z1: 1236.0
        x2: 1509.0
        "y2": 16.0
        z2: 1244.0
      town: 'Voltaris Island'
  - text: 'Complete the block puzzle in the Voltaris cave.'
    location:
      kind: 'npc'
      x: 1489.5
      "y": 12.0
      z: 1237.5
      label: 'Mirelle'
      town: 'Voltaris Island'
  - text: 'Battle Plasma Grunt Mirelle.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Mirelle'
        x: 1489.5
        "y": 12.0
        z: 1237.5
        town: 'Voltaris Island'
        team:
          - species: 'Whimsicott'
            level: 100
          - species: 'Gallade'
            level: 100
          - species: 'Amoonguss'
            level: 100
          - species: 'Chandelure'
            level: 100
          - species: 'Scrafty'
            level: 100
          - species: 'Togekiss'
            level: 100
  - text: 'Head into the lava chamber.'
    location:
      kind: 'region'
      x: 1479.5
      "y": 17.0
      z: 1234.0
      bbox:
        x1: 1469.0
        "y1": 11.0
        z1: 1224.0
        x2: 1490.0
        "y2": 23.0
        z2: 1244.0
      town: 'Voltaris Island'
    rewards:
      - '125000 Coins'
      - '200000 Trainer XP'
      - '75 Tokens'
---
