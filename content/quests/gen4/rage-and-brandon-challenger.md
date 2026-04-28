---
title: 'Rage and Brandon Challenger'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'rage_and_brandon_challenger'
slug: 'rage-and-brandon-challenger'
description: 'Make your way through the gym to battle RageElixir and BrandonCrafterMC for some unique rewards!'
source_file: 'rage-and-brandon-challenger.json'
start:
  npc: 'Cletus'
  town: 'Circuit City'
  x: -267.5
  "y": 29.0
  z: 682.5
steps:
  - text: 'Battle Autumn in the next room'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Autumn'
        x: -277.5
        "y": 31.0
        z: 695.5
        town: 'Circuit City'
        team:
          - species: 'Dragonair'
            level: 28
          - species: 'Venomoth'
            level: 29
          - species: 'Rotom'
            level: 29
          - species: 'Metang'
            level: 30
          - species: 'Combusken'
            level: 30
          - species: 'Pidgeotto'
            level: 31
  - text: 'Battle Walter upstairs'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Walter'
        x: -265.9
        "y": 42.0
        z: 697.5
        town: 'Circuit City'
        team:
          - species: 'Pupitar'
            level: 30
          - species: 'Ivysaur'
            level: 31
          - species: 'Growlithe'
            level: 31
          - species: 'Heracross'
            level: 32
          - species: 'Skarmory'
            level: 32
          - species: 'Kadabra'
            level: 33
  - text: 'Battle Fauna in the same room'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Fauna'
        x: -277.5
        "y": 42.0
        z: 695.2
        town: 'Circuit City'
        team:
          - species: 'Gabite'
            level: 32
          - species: 'Marshtomp'
            level: 33
          - species: 'Kirlia'
            level: 33
          - species: 'Flaaffy'
            level: 34
          - species: 'Graveler'
            level: 34
          - species: 'Jolteon'
            level: 35
  - text: 'Battle Oscar upstairs'
    location:
      kind: 'battle'
      town: 'Circuit City'
    battles:
      - trainer: 'Oscar'
        x: -276.5
        "y": 53.0
        z: 698.1
        town: 'Circuit City'
        team:
          - species: 'Vaporeon'
            level: 34
          - species: 'Nidorino'
            level: 35
          - species: 'Scyther'
            level: 35
          - species: 'Shelgon'
            level: 36
          - species: 'Hippowdon'
            level: 36
          - species: 'Torkoal'
            level: 37
  - text: 'Battle BrandonCrafterMC and RageElixir'
    location:
      kind: 'region'
      x: -72.0
      "y": 31.0
      z: 813.0
      bbox:
        x1: -75.0
        "y1": 29.0
        z1: 812.0
        x2: -69.0
        "y2": 33.0
        z2: 814.0
      town: 'Circuit City'
    rewards:
      - '2500 Coins'
      - '3000 Trainer XP'
      - '20 Tokens'
---
