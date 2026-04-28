---
title: 'A Medical Emergency'
date: 2026-04-28
layout: questguide
gen: 1
quest_key: 'a_medical_emergency'
slug: 'a-medical-emergency'
description: 'Team Rocket has stolen the medical supplies at the Wyvern Pokemon Center. It is up to you to infiltrate Team Rocket''s warehouse and return the medical supplies to the Pokemon Center.'
author: 'bunstop, lego121212, luk_aszek'
source_file: 'a-medical-emergency.json'
start:
  npc: 'Nurse Iris'
  town: 'Finderia Town'
  x: -456.0
  "y": 97.0
  z: 548.0
steps:
  - text: 'Follow Nurse Iris'
    location:
      kind: 'npc'
      x: -456.0
      "y": 97.0
      z: 548.0
      label: 'Nurse Iris'
      town: 'Finderia Town'
  - text: 'Talk to Nurse Iris'
    location:
      kind: 'npc'
      x: 822.0
      "y": 77.0
      z: -599.0
      label: 'Nurse Iris'
      town: 'Finderia Town'
  - text: 'Follow the gravel path and see where it leads'
    location:
      kind: 'region'
      x: 693.5
      "y": 67.5
      z: -631.0
      bbox:
        x1: 683.0
        "y1": 63.0
        z1: -639.0
        x2: 704.0
        "y2": 72.0
        z2: -623.0
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Grunt!'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 686.0
        "y": 66.0
        z: -628.0
        town: 'Finderia Town'
        team:
          - species: 'Persian'
            level: 62
          - species: 'Machamp'
            level: 63
          - species: 'Raichu'
            level: 65
          - species: 'Sandslash'
            level: 62
  - text: 'Explore the warehouse and make sure there are no more Team Rocket Grunts'
    location:
      kind: 'npc'
      x: 686.0
      "y": 66.0
      z: -628.0
      label: 'Team Rocket Grunt'
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Grunt!'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 679.0
        "y": 69.0
        z: -594.0
        town: 'Finderia Town'
        team:
          - species: 'Flareon'
            level: 71
          - species: 'Dewgong'
            level: 72
          - species: 'Aerodactyl'
            level: 74
          - species: 'Electabuzz'
            level: 76
          - species: 'Rhydon'
            level: 77
  - text: 'Find the entrance to the storage room'
    location:
      kind: 'region'
      x: 635.0
      "y": 70.0
      z: -579.5
      bbox:
        x1: 634.0
        "y1": 69.0
        z1: -580.0
        x2: 636.0
        "y2": 71.0
        z2: -579.0
      town: 'Finderia Town'
  - text: 'Find the alternate entrance to the storage room'
    location:
      kind: 'region'
      x: 646.0
      "y": 70.5
      z: -609.0
      bbox:
        x1: 646.0
        "y1": 69.0
        z1: -610.0
        x2: 646.0
        "y2": 72.0
        z2: -608.0
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Grunt!'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 640.0
        "y": 69.0
        z: -609.0
        town: 'Finderia Town'
        team:
          - species: 'Kabutops'
            level: 75
          - species: 'Vaporeon'
            level: 77
          - species: 'Golbat'
            level: 78
          - species: 'Ninetales'
            level: 79
          - species: 'Chansey'
            level: 80
  - text: 'Enter the storage room'
    location:
      kind: 'region'
      x: 631.0
      "y": 73.5
      z: -602.5
      bbox:
        x1: 631.0
        "y1": 69.0
        z1: -604.0
        x2: 631.0
        "y2": 78.0
        z2: -601.0
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Grunt!'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 623.0
        "y": 69.0
        z: -603.0
        town: 'Finderia Town'
        team:
          - species: 'Cloyster'
            level: 80
          - species: 'Kangaskhan'
            level: 82
          - species: 'Golem'
            level: 84
          - species: 'Gengar'
            level: 86
          - species: 'Arbok'
            level: 89
  - text: 'Find the Supply Box in the storage room'
    location:
      kind: 'destination'
      x: 602.5
      "y": 69.0
      z: -550.5
      town: 'Finderia Town'
  - text: 'Exit the warehouse'
    location:
      kind: 'region'
      x: 656.5
      "y": 71.0
      z: -595.0
      bbox:
        x1: 656.0
        "y1": 69.0
        z1: -595.0
        x2: 657.0
        "y2": 73.0
        z2: -595.0
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Officer!'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Officer'
        x: 656.0
        "y": 69.0
        z: -593.0
        town: 'Finderia Town'
        team:
          - species: 'Onix'
            level: 100
          - species: 'Jolteon'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Nidoking'
            level: 100
          - species: 'Snorlax'
            level: 100
          - species: 'Dragonite'
            level: 100
  - text: 'Talk to Nurse Iris at the Wyvern Village Pokemon Center'
    location:
      kind: 'npc'
      x: 833.0
      "y": 77.0
      z: -613.0
      label: 'Nurse Iris'
      town: 'Wyvern Village'
    rewards:
      - 'Black Sludge'
  - text: 'Talk to Officer Jenny in Finderia Town'
    location:
      kind: 'npc'
      x: -478.0
      "y": 83.0
      z: 574.0
      label: 'Officer Jenny'
      town: 'Finderia Town'
    rewards:
      - '25000 Coins'
      - '25 Tokens'
      - '10000 Trainer XP'
---
