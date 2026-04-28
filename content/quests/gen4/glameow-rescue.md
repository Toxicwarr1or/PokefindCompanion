---
title: 'Glameow Rescue'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'glameow_rescue'
slug: 'glameow-rescue'
description: 'Nana Sissy lost her Glameow, help her free it and bring it back to her.'
author: 'MrLenovo'
source_file: 'glameow-rescue.json'
start:
  npc: 'Nana Sissy'
  x: 346.5
  "y": 43.0
  z: 716.5
steps:
  - text: 'Walk around the pathway surrounding the giant tree in the center of Woodburn'
    location:
      kind: 'region'
      x: 323.5
      "y": 51.0
      z: 719.0
      bbox:
        x1: 320.0
        "y1": 50.0
        z1: 714.0
        x2: 327.0
        "y2": 52.0
        z2: 724.0
  - text: 'Get a Flying Type Pokémon, and walk further into the pathway'
    location:
      kind: 'destination'
      x: 315.5
      "y": 85.0
      z: 735.5
  - text: 'Battle your way through guards to save Glameow'
    location:
      kind: 'npc'
      x: 317.5
      "y": 88.0
      z: 723.5
      label: 'ledyba1'
  - text: 'Defeat the leader of Spinarak'
    location:
      kind: 'npc'
      x: 334.5
      "y": 99.0
      z: 715.5
      label: 'spinarak4'
  - text: 'Take Glameow from the tree branch'
    location:
      kind: 'npc'
      x: 337.5
      "y": 100.0
      z: 712.5
      label: 'Glameow'
  - text: 'Bring Glameow back to Nana Sissy'
    location:
      kind: 'npc'
      x: 346.5
      "y": 43.0
      z: 716.5
      label: 'Nana Sissy'
    rewards:
      - '10× Rare Candy'
      - '7500 Coins'
      - '15 Tokens'
      - '25000 Trainer XP'
---
