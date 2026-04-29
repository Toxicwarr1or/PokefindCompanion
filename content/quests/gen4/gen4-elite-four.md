---
title: 'Elite Four'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'gen4_elite_four'
slug: 'gen4-elite-four'
description: 'Your ultimate challenge is before you, the Elite Four awaits!'
source_file: 'gen4-elite-four.json'
video_id: 'IOa1_se8GYE'
video_title: 'PokéFind Elite Four (E4: Generation 4)'
start:
  npc: 'Cletus'
  x: 1534.0
  "y": 33.0
  z: 691.5
steps:
  - text: 'Battle Elite Four member Aaron'
    location:
      kind: 'npc'
      x: 1541.5
      "y": 6.0
      z: 691.5
      label: 'Cletus'
  - text: 'Talk to Cletus'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Bertha'
        x: 1569.5
        "y": 45.0
        z: 691.4
        team:
          - species: 'Golem'
            level: 100
          - species: 'Whiscash'
            level: 100
          - species: 'Gliscor'
            level: 100
          - species: 'Rhyperior'
            level: 100
          - species: 'Hippowdon'
            level: 100
          - species: 'Gastrodon'
            level: 100
  - text: 'Battle Elite Four member Bertha'
    location:
      kind: 'npc'
      x: 1541.5
      "y": 45.0
      z: 691.5
      label: 'Cletus'
  - text: 'Talk to Cletus'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Flint'
        x: 1568.5
        "y": 62.0
        z: 691.4
        team:
          - species: 'Camerupt'
            level: 100
          - species: 'Flareon'
            level: 100
          - species: 'Houndoom'
            level: 100
          - species: 'Rapidash'
            level: 100
          - species: 'Arcanine'
            level: 100
          - species: 'Infernape'
            level: 100
  - text: 'Battle Elite Four member Flint'
    location:
      kind: 'npc'
      x: 1537.5
      "y": 62.0
      z: 691.5
      label: 'Cletus'
  - text: 'Talk to Cletus'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Lucian'
        x: 1545.6
        "y": 83.0
        z: 691.5
        team:
          - species: 'Bronzong'
            level: 100
          - species: 'Grumpig'
            level: 100
          - species: 'Espeon'
            level: 100
          - species: 'Gallade'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Claydol'
            level: 100
  - text: 'Battle Elite Four member Lucian'
    location:
      kind: 'npc'
      x: 1545.6
      "y": 83.0
      z: 691.5
      label: 'Lucian'
  - text: 'Take the portal at the end of the arena to the Champions arena'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Cynthia'
        x: 1546.5
        "y": 110.0
        z: 691.5
        team:
          - species: 'Spiritomb'
            level: 100
          - species: 'Roserade'
            level: 100
          - species: 'Togekiss'
            level: 100
          - species: 'Lucario'
            level: 100
          - species: 'Milotic'
            level: 100
          - species: 'Garchomp'
            level: 100
  - text: 'Battle Elite Four Champion Cynthia'
    location:
      kind: 'npc'
      x: 1546.5
      "y": 110.0
      z: 691.5
      label: 'Cynthia'
    rewards:
      - '500000 Trainer XP'
      - '150000 Coins'
      - '50 Tokens'
      - '25× Rare_Candy'
      - '3× Max_PP'
      - 'Ability_Capsule'
      - 'Leftovers'
---
