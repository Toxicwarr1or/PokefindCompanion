---
title: 'The Mysterious Pokémon'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'THE_MYSTERIOUS_POKÉMON'
slug: 'the-mysterious-pokemon'
description: 'Detective Pikachu has caught rumour of a Mysterious Pokémon!'
source_file: 'the-mysterious-pokemon.json'
start:
  npc: 'Mysterious Person'
  town: 'Rockford Bay'
  x: -1311.5
  "y": 49.0
  z: -467.5
steps:
  - text: 'Talk to Detective Pikachu in front of the Springdale library'
    location:
      kind: 'region'
      x: -723.0
      "y": 36.0
      z: 705.5
      bbox:
        x1: -726.0
        "y1": 34.0
        z1: 700.0
        x2: -720.0
        "y2": 38.0
        z2: 711.0
      town: 'Rockford Bay'
  - text: 'Follow Pikachu inside the library'
  - text: 'Help Pikachu find the valuable information by searching the bookshelves'
  - text: 'Continue searching the bookshelves for valuable information'
    location:
      kind: 'destination'
      x: -723.5
      "y": 35.35
      z: 718.5
      town: 'Rockford Bay'
  - text: 'Exit the library'
  - text: 'Search Stoneridge and Rockford for the mysterious person or object'
    location:
      kind: 'npc'
      x: -1311.5
      "y": 49.0
      z: -467.5
      label: 'Mysterious Person'
      town: 'Rockford Bay'
  - text: 'Find the Baltoy in Rockford Bay'
    location:
      kind: 'destination'
      x: -1214.5
      "y": 48.0
      z: -607.5
      town: 'Rockford Bay'
  - text: 'Pick up the clock'
  - text: 'Return to Yellow'
    location:
      kind: 'npc'
      x: -1164.5
      "y": 43.0
      z: 350.5
      label: 'Yellow'
      town: 'Rockford Bay'
  - text: 'Search the windmill for a clue on where to go next'
  - text: 'Go to Occult and find the second person'
    location:
      kind: 'npc'
      x: -1311.5
      "y": 49.0
      z: -467.5
      label: 'Mysterious Person'
      town: 'Rockford Bay'
  - text: 'Find Pink''s Trinket on Occult Island'
    location:
      kind: 'npc'
      x: -1166.5
      "y": 43.0
      z: 350.5
      label: 'Pink'
      town: 'Occult Island'
  - text: 'Return to Pink'
    location:
      kind: 'npc'
      x: -1166.5
      "y": 43.0
      z: 350.5
      label: 'Pink'
      town: 'Rockford Bay'
  - text: 'Find the third person at the location described in the hint:\n"Find the third in a cave, near the meeting spot for waves"'
    location:
      kind: 'npc'
      x: -1311.5
      "y": 49.0
      z: -467.5
      label: 'Mysterious Person'
      town: 'Rockford Bay'
  - text: 'Give Blue 6 Revives'
    location:
      kind: 'battle'
      town: 'Rockford Bay'
    battles:
      - trainer: 'Mysterious Person'
        x: -1062.5
        "y": 24.0
        z: 1135.5
        town: 'Rockford Bay'
        team:
          - species: 'Metagross'
            level: 100
          - species: 'Heracross'
            level: 100
          - species: 'Slowbro'
            level: 100
          - species: 'Rapidash'
            level: 100
          - species: 'Jolteon'
            level: 100
          - species: 'Clefable'
            level: 100
  - text: 'Exit the cave in Wavemeet Bay'
  - text: 'Find the Place described in the three hints'
  - text: 'Summon the Moon for Yellow, Pink and Blue with the move Moonlight'
    location:
      kind: 'npc'
      x: -1164.5
      "y": 43.0
      z: 350.5
      label: 'Yellow'
      town: 'Rockford Bay'
  - text: 'Go closer to Cresselia'
  - text: 'Defeat Cresselia'
    location:
      kind: 'destination'
      x: -723.5
      "y": 34.0
      z: 708.5
      town: 'Rockford Bay'
    rewards:
      - 'Lunar_Wing'
  - text: 'Exit the library'
    rewards:
      - '20000 Coins'
      - '25 Tokens'
      - '25000 Trainer XP'
      - 'Ability_Capsule'
---
