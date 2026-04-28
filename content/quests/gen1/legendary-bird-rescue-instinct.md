---
title: 'Legendary Bird Rescue'
date: 2026-04-28
layout: questguide
gen: 1
quest_key: 'legendary_bird_rescue_instinct'
slug: 'legendary-bird-rescue-instinct'
description: 'Team Rocket has kidnapped your team''s Zapdos! Talk to your Professor Hemlock in Amp City to start the rescue!'
author: 'Lillian890 and CapnMerica'
source_file: 'legendary-bird-rescue-instinct.json'
start:
  npc: 'Professor Hemlock'
  town: 'Amp City'
  x: 801.5
  "y": 82.0
  z: 287.5
steps:
  - text: 'Talk to Spark in the team base in Amp City!'
    location:
      kind: 'npc'
      x: 932.5
      "y": 97.5
      z: 379.5
      label: 'Spark'
      town: 'Amp City'
  - text: 'Battle the first Team Rocket Member on a mystical beach!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: 963.5
        "y": 64.0
        z: -858.5
        town: 'Amp City'
        team:
          - species: 'Raticate'
            level: 100
          - species: 'Golbat'
            level: 100
  - text: 'Battle the second Team Rocket Member somewhere filled with smog!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: 1325.5
        "y": 68.0
        z: -531.5
        town: 'Amp City'
        team:
          - species: 'Tauros'
            level: 100
          - species: 'Slowbro'
            level: 100
          - species: 'Vileplume'
            level: 100
  - text: 'Battle the third Team Rocket Member somewhere near a farm!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: 666.5
        "y": 70.0
        z: 943.5
        town: 'Amp City'
        team:
          - species: 'Sandslash'
            level: 100
          - species: 'Golem'
            level: 100
          - species: 'Marowak'
            level: 100
  - text: 'Battle the fourth Team Rocket Member where you can see the planes take off!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: -496.5
        "y": 84.0
        z: 1270.5
        town: 'Amp City'
        team:
          - species: 'Hypno'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Jynx'
            level: 100
  - text: 'Battle the fifth Team Rocket Member near a lagoon!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: -962.5
        "y": 66.0
        z: -8.5
        town: 'Amp City'
        team:
          - species: 'Weezing'
            level: 100
          - species: 'Arbok'
            level: 100
          - species: 'Nidoking'
            level: 100
          - species: 'Nidoqueen'
            level: 100
          - species: 'Muk'
            level: 100
  - text: 'Talk to Spark in Amp City to see if he can solve the puzzle!'
    location:
      kind: 'npc'
      x: 932.5
      "y": 97.5
      z: 379.5
      label: 'Spark'
      town: 'Amp City'
  - text: 'Talk to Lavender in Finderia Town!'
    location:
      kind: 'npc'
      x: -493.5
      "y": 96.5
      z: 562.5
      label: 'Lavender'
      town: 'Finderia Town'
  - text: 'Break the wall with a Fighting Type Pokémon to get into Team Rocket''s Headquarters!'
    location:
      kind: 'npc'
      x: 963.5
      "y": 64.0
      z: -858.5
      label: 'Team Rocket Member'
      town: 'Amp City'
  - text: 'Defeat the Team Rocket Members around the Headquarters!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: -99.5
        "y": 37.0
        z: -1761.5
        town: 'Amp City'
        team:
          - species: 'Dodrio'
            level: 100
          - species: 'Golbat'
            level: 100
          - species: 'Jynx'
            level: 100
          - species: 'Weezing'
            level: 100
          - species: 'Electrode'
            level: 100
      - trainer: 'Team Rocket Member'
        x: 92.5
        "y": 37.0
        z: -1761.5
        town: 'Amp City'
        team:
          - species: 'Machamp'
            level: 100
          - species: 'Hypno'
            level: 100
          - species: 'Raticate'
            level: 100
          - species: 'Sandslash'
            level: 100
          - species: 'Parasect'
            level: 100
  - text: 'Find the two keys at the end of the parkour to open the next door!'
    location:
      kind: 'destination'
      x: -3.5
      "y": 54.0
      z: -1821.5
      town: 'Amp City'
  - text: 'Use the keys by clicking the dispenser at the door!'
    location:
      kind: 'region'
      x: 25.0
      "y": 41.0
      z: -1899.0
      bbox:
        x1: 21.0
        "y1": 37.0
        z1: -1899.0
        x2: 29.0
        "y2": 45.0
        z2: -1899.0
      town: 'Amp City'
  - text: 'Battle the remaining Team Rocket Members as you make your way through their Headquarters!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Team Rocket Member'
        x: 30.5
        "y": 37.0
        z: -2030.5
        town: 'Amp City'
        team:
          - species: 'Tentacruel'
            level: 100
          - species: 'Lickitung'
            level: 100
          - species: 'Hitmonchan'
            level: 100
          - species: 'Dewgong'
            level: 100
          - species: 'Onix'
            level: 100
      - trainer: 'Team Rocket Member'
        x: -70.5
        "y": 37.0
        z: -2025.5
        town: 'Amp City'
        team:
          - species: 'Wigglytuff'
            level: 100
          - species: 'Fearow'
            level: 100
          - species: 'Beedrill'
            level: 100
          - species: 'Poliwrath'
            level: 100
          - species: 'Magneton'
            level: 100
          - species: 'Rhydon'
            level: 100
      - trainer: 'Team Rocket Member'
        x: 121.5
        "y": 37.0
        z: -2025.5
        town: 'Amp City'
        team:
          - species: 'Omastar'
            level: 100
          - species: 'Aerodactyl'
            level: 100
          - species: 'Kabutops'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Cloyster'
            level: 100
          - species: 'Muk'
            level: 100
  - text: 'Confront Jessie and James!'
    location:
      kind: 'npc'
      x: 26.5
      "y": 72.0
      z: -2150.5
      label: 'Jessie'
      town: 'Amp City'
  - text: 'Find a way to get back up to Jessie and James.'
    location:
      kind: 'npc'
      x: 78.5
      "y": 6.0
      z: -2675.5
      label: 'Jessie'
      town: 'Amp City'
  - text: 'Beat Jessie in a battle!'
    location:
      kind: 'battle'
      town: 'Amp City'
    battles:
      - trainer: 'Jessie'
        x: 78.5
        "y": 6.0
        z: -2675.5
        town: 'Amp City'
        team:
          - species: 'Arbok'
            level: 100
          - species: 'Meowth'
            level: 100
          - species: 'Weezing'
            level: 100
          - species: 'Machamp'
            level: 100
          - species: 'Gengar'
            level: 100
          - species: 'Gyarados'
            level: 100
  - text: 'Free the Zapdos by clicking the lock!'
    location:
      kind: 'npc'
      x: 78.5
      "y": 10.0
      z: -2657.5
      label: 'Zapdos'
      town: 'Amp City'
  - text: 'Return to Spark with the good news!'
    location:
      kind: 'npc'
      x: 932.5
      "y": 97.5
      z: 379.5
      label: 'Spark'
      town: 'Amp City'
    rewards:
      - '260000 Coins'
      - '60 Tokens'
      - '15× Rare Candy'
      - 'Choice Specs'
      - '3× Lucky Egg'
  - text: 'Head outside and find the Zapdos!'
    location:
      kind: 'npc'
      x: 78.5
      "y": 10.0
      z: -2657.5
      label: 'Zapdos'
      town: 'Amp City'
---
