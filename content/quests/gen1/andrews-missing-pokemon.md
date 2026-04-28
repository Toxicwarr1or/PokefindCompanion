---
title: 'Andrew''s Missing Pokémon'
date: 2026-04-28
layout: questguide
gen: 1
quest_key: 'andrews_missing_pokemon'
slug: 'andrews-missing-pokemon'
description: 'A trainer at Finderia Town has lost their Pokémon! Find and help them locate the mysterious missing Pokémon.'
author: 'GrumpyJupe'
source_file: 'andrews-missing-pokemon.json'
start:
  npc: 'Andrew'
  town: 'Finderia Town'
  x: -531.9
  "y": 96.0
  z: 574.3
steps:
  - text: 'Find Andrew''s Pidgey in a big tree at spawn.'
    location:
      kind: 'npc'
      x: -484.5
      "y": 100.0
      z: 570.6
      label: 'Andrew''s Pidgey'
      town: 'Finderia Town'
  - text: 'Find the mysterious person who took Andrew''s Rattata near the Pokémon Center.'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Mysterious Person'
        x: -448.3
        "y": 96.0
        z: 552.5
        town: 'Finderia Town'
        team:
          - species: 'Rattata'
            level: 15
  - text: 'Find Andrew''s Jigglypuff somewhere high up near the Pokémon Center at spawn.'
    location:
      kind: 'npc'
      x: -447.5
      "y": 106.0
      z: 597.3
      label: 'Andrew''s Jigglypuff'
      town: 'Finderia Town'
  - text: 'Talk to Andrew.'
    location:
      kind: 'npc'
      x: -531.9
      "y": 96.0
      z: 574.3
      label: 'Andrew'
      town: 'Finderia Town'
    rewards:
      - '300 Coins'
      - '2 Tokens'
      - '500 Trainer XP'
---
