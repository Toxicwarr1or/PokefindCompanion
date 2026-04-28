---
title: 'Flying High'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'fly'
slug: 'fly'
description: 'While battling a trainer called Martha, she shows you a unique move and is willing to share where she acquired it.'
source_file: 'fly.json'
start:
  npc: 'Martha'
  x: 736.5
  "y": 31.0
  z: 287.5
steps:
  - text: 'Talk to Mahayla'
    location:
      kind: 'npc'
      x: 847.5
      "y": 175.0
      z: 272.5
      label: 'Kierson'
  - text: 'Talk to Kierson and Zaiden'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Kierson'
        x: 847.5
        "y": 175.0
        z: 272.5
        team:
          - species: 'Gligar'
            level: 100
          - species: 'Pidgeot'
            level: 100
          - species: 'Ninjask'
            level: 100
          - species: 'Gyarados'
            level: 100
          - species: 'Dragonite'
            level: 100
          - species: 'Lugia'
            level: 100
  - text: 'Battle Kierson and Zaiden'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Zaiden'
        x: 847.5
        "y": 175.0
        z: 274.5
        team:
          - species: 'Swellow'
            level: 100
          - species: 'Skarmory'
            level: 100
          - species: 'Aerodactyl'
            level: 100
          - species: 'Mantine'
            level: 100
          - species: 'Salamence'
            level: 100
          - species: 'Ho-Oh'
            level: 100
  - text: 'Talk to Mahayla'
    location:
      kind: 'npc'
      x: 838.5
      "y": 81.0
      z: 305.5
      label: 'Mahayla'
    rewards:
      - '2500 Trainer XP'
      - '25000 Coins'
      - '5 Tokens'
---
