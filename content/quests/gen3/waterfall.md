---
title: 'When It Rains It Pours'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'waterfall'
slug: 'waterfall'
description: 'While exploring Lodestar Port you discover a new water-type move that holds unbelievable strength. Can you prove your worth and be granted access to a Families secret that has only been shared with a select few for centuries?'
source_file: 'waterfall.json'
video_id: 'OmFuL5T4O5k'
video_title: 'PokeFind When It Rains It Pours (HM Quest: Generation 3)'
start:
  npc: 'Charlotte'
  town: 'Lodestar Port'
  x: 1171.5
  "y": 21.0
  z: -485.5
steps:
  - text: 'Find Adam in Misty Falls'
    location:
      kind: 'npc'
      x: -739.5
      "y": 34.0
      z: -388.5
      label: 'Adam'
      town: 'Misty Falls'
  - text: 'Catch a Walrein and give it to Adam.'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Adam'
        x: -725.5
        "y": 47.0
        z: -227.5
        town: 'Lodestar Port'
        team:
          - species: 'Walrein'
            level: 44
  - text: 'Find Adam near the Waterfall'
    location:
      kind: 'battle'
      town: 'Lodestar Port'
    battles:
      - trainer: 'Sam'
        x: -737.5
        "y": 34.0
        z: -388.5
        town: 'Lodestar Port'
        team:
          - species: 'Blastoise'
            level: 100
          - species: 'Cloyster'
            level: 100
          - species: 'Wailord'
            level: 100
          - species: 'Omastar'
            level: 100
      - trainer: 'Adam'
        x: -739.5
        "y": 34.0
        z: -388.5
        town: 'Lodestar Port'
        team:
          - species: 'Milotic'
            level: 100
          - species: 'Sharpedo'
            level: 100
          - species: 'Kabutops'
            level: 100
          - species: 'Azumarill'
            level: 100
          - species: 'Swampert'
            level: 100
          - species: 'Gyarados'
            level: 100
    rewards:
      - '25000 Trainer XP'
      - '50000 Coins'
---
