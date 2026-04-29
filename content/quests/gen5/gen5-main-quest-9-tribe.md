---
title: 'Main Quest 9 - The Consequences of Truth - Sophro'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_9_tribe'
slug: 'gen5-main-quest-9-tribe'
description: 'Some time has passed since the events of The Great War. Trainers and Pokémon are at peace. Can that peace be maintained as a new threat emerges?'
author: 'Toxicwarr1or'
source_file: 'gen5-main-quest-9-tribe.json'
video_id: 'nFHeMiHL5AM'
video_title: 'Main Quest 9 - The Consequences of Truth - Sophro'
start:
  npc: 'Astrid'
  description: 'Talk to Astrid in the Depths of Greenholm''s Temple'
  town: 'Greenholm'
  x: -330.5
  "y": 33.0
  z: 59.5
steps:
  - text: 'Head back to the entrance of the Temple'
    location:
      kind: 'region'
      x: -499.0
      "y": 78.5
      z: 34.0
      bbox:
        x1: -501.0
        "y1": 72.0
        z1: 32.0
        x2: -497.0
        "y2": 85.0
        z2: 36.0
      town: 'Greenholm'
  - text: 'Investigate the commotion in the center of Greenholm.'
    location:
      kind: 'region'
      x: -361.0
      "y": 62.5
      z: -50.0
      bbox:
        x1: -397.0
        "y1": 48.0
        z1: -91.0
        x2: -325.0
        "y2": 77.0
        z2: -9.0
      town: 'Greenholm'
  - text: 'Defeat the Pokémon before they are able to hurt anyone. [Hint: Start with Jellicent]'
    location:
      kind: 'npc'
      x: -340.5
      "y": 48.94
      z: -38.5
      label: 'Jellicent_1'
      town: 'Greenholm'
  - text: 'Find Astrid back at the Greenholm Temple.'
    location:
      kind: 'npc'
      x: -330.5
      "y": 33.0
      z: 59.5
      label: 'Astrid'
      town: 'Greenholm'
  - text: 'Defeat Astrid''s Pokémon'
    location:
      kind: 'npc'
      x: -498.5
      "y": 64.0
      z: 2.5
      label: 'Samurott_1'
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
  - text: 'Go back to Greenholm Temple and talk to Astrid. [Hint: She is outside the temple.]'
    location:
      kind: 'npc'
      x: -498.5
      "y": 64.0
      z: 6.5
      label: 'Astrid'
      town: 'Greenholm'
  - text: 'Wait for Astrid to contact you to continue.'
    location:
      kind: 'npc'
      x: -330.5
      "y": 33.0
      z: 59.5
      label: 'Astrid'
      town: 'Greenholm'
  - text: 'Meet Astrid in Breezelton.'
    location:
      kind: 'npc'
      x: -330.5
      "y": 33.0
      z: 59.5
      label: 'Astrid'
      town: 'Greenholm'
    rewards:
      - '100000 Coins'
      - '200000 Trainer XP'
      - '50 Tokens'
      - 'Choice Band'
      - 'Choice Scarf'
      - 'Choice Specs'
---
