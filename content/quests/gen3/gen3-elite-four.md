---
title: 'The Elite Four'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'gen3_elite_four'
slug: 'gen3-elite-four'
description: 'You arrive at Victor Island to participate in the Pokémon League!'
source_file: 'gen3-elite-four.json'
video_id: 'EDdqMAlGi6o'
video_title: 'PokéFind Elite Four (Elite Four: Generation 3)'
start:
  npc: 'League Official'
  town: 'Victor Island'
  x: 1471.5
  "y": 31.0
  z: 712.5
steps:
  - text: 'Battle Sidney!'
    location:
      kind: 'battle'
      town: 'Victor Island'
    battles:
      - trainer: 'Phoebe'
        x: 1511.5
        "y": 20.0
        z: 839.5
        town: 'Victor Island'
        team:
          - species: 'Armaldo'
            level: 100
          - species: 'Tyranitar'
            level: 100
          - species: 'Aerodactyl'
            level: 100
          - species: 'Blaziken'
            level: 100
          - species: 'Regirock'
            level: 100
  - text: 'Battle Phoebe!'
    location:
      kind: 'battle'
      town: 'Victor Island'
    battles:
      - trainer: 'Glacia'
        x: 1431.5
        "y": 20.0
        z: 839.5
        town: 'Victor Island'
        team:
          - species: 'Lapras'
            level: 100
          - species: 'Ludicolo'
            level: 100
          - species: 'Cloyster'
            level: 100
          - species: 'Sharpedo'
            level: 100
          - species: 'Regice'
            level: 100
  - text: 'Battle Glacia!'
    location:
      kind: 'battle'
      town: 'Victor Island'
    battles:
      - trainer: 'Drake'
        x: 1408.5
        "y": 20.0
        z: 788.5
        town: 'Victor Island'
        team:
          - species: 'Skarmory'
            level: 100
          - species: 'Flygon'
            level: 100
          - species: 'Altaria'
            level: 100
          - species: 'Aggron'
            level: 101
          - species: 'Raikou'
            level: 101
  - text: 'Battle Drake!'
    location:
      kind: 'battle'
      town: 'Victor Island'
    battles:
      - trainer: 'Charlie'
        x: 1471.5
        "y": 82.0
        z: 782.5
        town: 'Victor Island'
        team:
          - species: 'Milotic'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Dragonite'
            level: 101
          - species: 'Metagross'
            level: 102
          - species: 'Salamence'
            level: 102
          - species: 'Latios'
            level: 103
  - text: 'Battle Charlie!'
    location:
      kind: 'npc'
      x: 1471.5
      "y": 82.0
      z: 782.5
      label: 'Charlie'
      town: 'Victor Island'
    rewards:
      - '600000 Trainer XP'
      - '25 Tokens'
      - '100000 Coins'
      - '10× Focus Sash'
      - '15× Rare Candy'
      - '3× Max PP'
      - 'Achievement: pokémon_world_a_new_champion'
---
