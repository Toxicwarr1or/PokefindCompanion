---
title: 'Main Quest 11 - ...Together We Fall'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_11'
slug: 'gen5-main-quest-11'
description: 'Team Plasma''s plan continues to gain traction. Ghetsis has recovered the artifact known as the Reveal Glass, as well as the Force of Nature Landorus. There is still time. The two remaining Forces elude them. Perhaps you can find them and turn the tides, but you can''t go in unprepared. This isn''t the first power struggle the region has faced.'
author: 'Toxicwarr1or'
source_file: 'gen5-main-quest-11.json'
video_id: 'IT2UOq83bdA'
video_title: 'Main Quest 11 - ...Together We Fall'
start:
  npc: 'Astrid'
  description: 'Talk to Astrid and H.A.P.P.Y. outside Voltaris Pokecenter.'
  town: 'Voltaris Island'
  x: 1500.5
  "y": 49.0
  z: 1268.5
steps:
  - text: 'Go to the Observatory/Weather Station on Volatris.'
    location:
      kind: 'region'
      x: 1557.5
      "y": 75.0
      z: 1273.5
      bbox:
        x1: 1538.0
        "y1": 65.0
        z1: 1256.0
        x2: 1577.0
        "y2": 85.0
        z2: 1291.0
      town: 'Voltaris Island'
  - text: 'Stop the Plasma Grunts'
    location:
      kind: 'npc'
      x: 1548.5
      "y": 72.0
      z: 1279.5
      label: 'Paul'
      town: 'Voltaris Island'
  - text: 'Battle the Plasma Grunt'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Paul'
        x: 1548.5
        "y": 72.0
        z: 1279.5
        town: 'Voltaris Island'
        team:
          - species: 'Garchomp'
            level: 95
          - species: 'Scizor'
            level: 95
          - species: 'Eelektross'
            level: 95
          - species: 'Ferrothorn'
            level: 95
          - species: 'Starmie'
            level: 95
          - species: 'Conkeldurr'
            level: 95
          - species: 'Chandelure'
            level: 95
          - species: 'Gliscor'
            level: 95
  - text: 'Check on the scientist'
    location:
      kind: 'npc'
      x: 1545.5
      "y": 72.0
      z: 1279.5
      label: 'Ayda'
      town: 'Voltaris Island'
  - text: 'Find Inventor Jasmine in the building at the center of Sparkmont.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Give Jasmine 64 Poke Balls, 64 Great Balls, 64 Ultra Balls and 1 Heavy Ball.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Give Jasmine 64 Great Balls, 64 Ultra Balls and 1 Heavy Ball.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Give Jasmine 64 Ultra Balls and 1 Heavy Ball.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Give Jasmine 1 Heavy Ball.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Wait a minute for Jasmine to conclude her experiment.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Return to Jasmine.'
    location:
      kind: 'npc'
      x: 1497.5
      "y": 87.0
      z: 766.5
      label: 'Jasmine'
      town: 'Sparkmont City'
  - text: 'Head back to the Weather Station on Voltaris to talk to Ayda.'
    location:
      kind: 'npc'
      x: 1545.5
      "y": 72.0
      z: 1279.5
      label: 'Ayda'
      town: 'Voltaris Island'
  - text: 'Search the Tree of Life on Voltaris.'
    location:
      kind: 'npc'
      x: 1401.5
      "y": 96.5
      z: 1253.5
      label: 'tornadus1'
      town: 'Voltaris Island'
  - text: 'Battle Tornadus.'
    location:
      kind: 'npc'
      x: 1401.5
      "y": 96.5
      z: 1253.5
      label: 'tornadus1'
      town: 'Voltaris Island'
  - text: 'Follow Tornadus further up the tree and battle.'
    location:
      kind: 'npc'
      x: 1393.5
      "y": 113.5
      z: 1253.5
      label: 'tornadus2'
      town: 'Voltaris Island'
  - text: 'Follow Tornadus further up the tree and battle for a third time.'
    location:
      kind: 'npc'
      x: 1380.5
      "y": 128.5
      z: 1248.5
      label: 'tornadus3'
      town: 'Voltaris Island'
  - text: 'Follow Tornadus further up the tree and battle one final time.'
    location:
      kind: 'npc'
      x: 1327.5
      "y": 140.5
      z: 1234.5
      label: 'tornadus4'
      town: 'Voltaris Island'
  - text: 'Battle Thundurus.'
    location:
      kind: 'npc'
      x: 1401.5
      "y": 96.5
      z: 1253.5
      label: 'thundurus1'
      town: 'Voltaris Island'
  - text: 'Follow Thundurus further up the tree and battle.'
    location:
      kind: 'npc'
      x: 1393.5
      "y": 113.5
      z: 1253.5
      label: 'thundurus2'
      town: 'Voltaris Island'
  - text: 'Follow Thundurus further up the tree and battle for a third time.'
    location:
      kind: 'npc'
      x: 1380.5
      "y": 128.5
      z: 1248.5
      label: 'thundurus3'
      town: 'Voltaris Island'
  - text: 'Follow Thundurus further up the tree and battle one final time.'
    location:
      kind: 'npc'
      x: 1327.5
      "y": 140.5
      z: 1234.5
      label: 'thundurus4'
      town: 'Voltaris Island'
  - text: 'Head to the Weather Station one final time and meet Danielle.'
    location:
      kind: 'npc'
      x: 1547.5
      "y": 72.0
      z: 1277.5
      label: 'Danielle'
      town: 'Voltaris Island'
    rewards:
      - '100000 Coins'
      - '200000 Trainer XP'
      - '50 Tokens'
---
