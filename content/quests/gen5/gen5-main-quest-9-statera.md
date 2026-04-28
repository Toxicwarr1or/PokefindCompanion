---
title: 'Main Quest 9 - The Restoration of Ideals - Statera'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_9_statera'
slug: 'gen5-main-quest-9-statera'
description: 'Some time has passed since the events of The Great War. Trainers and Pokemon are at peace. Can that peace be maintained as a new threat emerges?'
author: 'Toxicwarr1or'
source_file: 'gen5-main-quest-9-statera.json'
video_id: 'rMcCB1xq0sU'
video_title: 'Main Quest 9 - The Restoration of Ideals - Statera'
start:
  npc: 'Lexi'
  description: 'Head over to Watterson and investigate the Static'
  town: 'Watterson City'
  x: 74.5
  "y": 53.0
  z: 300.5
steps:
  - text: 'Walk around Watterson until you start receiving Static from your Pokegear.'
    location:
      kind: 'region'
      x: 71.5
      "y": 66.5
      z: 228.5
      bbox:
        x1: 67.0
        "y1": 51.0
        z1: 211.0
        x2: 76.0
        "y2": 82.0
        z2: 246.0
      town: 'Watterson City'
  - text: 'Track the unknown signal to one of the buildings in Watterson. (Hint: Perhaps it is one you are already familiar with)'
    location:
      kind: 'region'
      x: 70.0
      "y": 61.5
      z: 338.5
      bbox:
        x1: 50.0
        "y1": 53.0
        z1: 325.0
        x2: 90.0
        "y2": 70.0
        z2: 352.0
      town: 'Watterson City'
  - text: 'Head inside the abandoned Statera HQ.'
    location:
      kind: 'region'
      x: 75.0
      "y": 53.0
      z: 337.0
      bbox:
        x1: 71.0
        "y1": 53.0
        z1: 331.0
        x2: 79.0
        "y2": 53.0
        z2: 343.0
      town: 'Watterson City'
  - text: 'Head to the elevator.'
  - text: 'Start the backup generator behind Statera HQ by flipping the lever.'
    location:
      kind: 'destination'
      x: 90.5
      "y": 54.0
      z: 341.5
      town: 'Watterson City'
  - text: 'Go to the lab on Floor 2 in Statera HQ.'
    location:
      kind: 'region'
      x: 99.5
      "y": 64.0
      z: 332.0
      bbox:
        x1: 95.0
        "y1": 62.0
        z1: 329.0
        x2: 104.0
        "y2": 66.0
        z2: 335.0
      town: 'Watterson City'
  - text: 'Find an Ender Chest containing spare circuit boards. (Hint: Follow the stairs to the top)'
  - text: 'Next, locate the Ender Chest that contains a new monitor. (Hint: It is back near the elevator on Floor 2)'
  - text: 'The final Ender Chest contains copper wiring. (Hint: Check the Lobby)'
  - text: 'Return to H.A.P.P.Y''s body in the Lab on Floor 2.'
    location:
      kind: 'npc'
      x: 100.5
      "y": 62.0
      z: 328.5
      label: 'Happy1'
      town: 'Watterson City'
  - text: 'Go to Greenholm to find any information on events transpiring in the world.'
    location:
      kind: 'region'
      x: -435.0
      "y": 43.5
      z: -41.5
      bbox:
        x1: -562.0
        "y1": 0.0
        z1: -106.0
        x2: -308.0
        "y2": 87.0
        z2: 23.0
      town: 'Greenholm'
  - text: 'Battle the two Serperiors.'
    location:
      kind: 'npc'
      x: -387.5
      "y": 65.0
      z: -22.5
      label: 'Serperior_1'
      town: 'Greenholm'
  - text: 'Head into the depths of the Kyurem shrine in Northrun. [Hint: Use the secondary entrance. No need to use the main entrance.]'
    location:
      kind: 'region'
      x: 82.5
      "y": 86.0
      z: -737.0
      bbox:
        x1: -54.0
        "y1": 53.0
        z1: -839.0
        x2: 219.0
        "y2": 119.0
        z2: -635.0
      town: 'Northrun'
  - text: 'Battle Danielle'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: -277.5
        "y": 54.0
        z: -749.5
        town: 'Icy Plains'
        team:
          - species: 'Emboar'
            level: 100
          - species: 'Haxorus'
            level: 100
          - species: 'Gigalith'
            level: 100
          - species: 'Unfezant'
            level: 100
          - species: 'Simisage'
            level: 100
          - species: 'Liepard'
            level: 100
  - text: 'Inspect Kyurem''s resting place.'
    location:
      kind: 'region'
      x: -328.0
      "y": 54.0
      z: -748.0
      bbox:
        x1: -337.0
        "y1": 50.0
        z1: -754.0
        x2: -319.0
        "y2": 58.0
        z2: -742.0
      town: 'Icy Plains'
  - text: 'Hide behind the ice structure.'
    location:
      kind: 'region'
      x: -336.0
      "y": 52.0
      z: -749.0
      bbox:
        x1: -338.0
        "y1": 50.0
        z1: -752.0
        x2: -334.0
        "y2": 54.0
        z2: -746.0
      town: 'Icy Plains'
  - text: 'Confront the newcomer.'
    location:
      kind: 'npc'
      x: -321.5
      "y": 50.0
      z: -749.5
      label: 'Grunt'
      town: 'Icy Plains'
  - text: 'Pursue the Grunt.'
    location:
      kind: 'npc'
      x: -293.5
      "y": 49.0
      z: -748.5
      label: 'Grunt'
      town: 'Icy Plains'
  - text: 'Meet with Danielle.'
    location:
      kind: 'npc'
      x: -273.5
      "y": 54.0
      z: -749.5
      label: 'Danielle'
      town: 'Icy Plains'
  - text: 'Inspect the scrap from Danielle.'
    location:
      kind: 'npc'
      x: -276.5
      "y": 54.0
      z: -754.5
      label: 'Danielle'
      town: 'Icy Plains'
  - text: 'Go back to the Statera Facility in Watterson and talk to H.A.P.P.Y. [Hint: He is in the lobby.]'
    location:
      kind: 'npc'
      x: 79.5
      "y": 53.0
      z: 341.5
      label: 'H.A.P.P.Y.'
      town: 'Watterson City'
  - text: 'Wait for H.A.P.P.Y. to contact you to continue.'
  - text: 'Meet Happy in Breezelton.'
    location:
      kind: 'region'
      x: 994.0
      "y": 54.0
      z: 276.5
      bbox:
        x1: 979.0
        "y1": 43.0
        z1: 264.0
        x2: 1009.0
        "y2": 65.0
        z2: 289.0
      town: 'Breezelton Village'
    rewards:
      - '100000 Coins'
      - '200000 Trainer XP'
      - '50 Tokens'
      - 'Choice Band'
      - 'Choice Scarf'
      - 'Choice Specs'
---
