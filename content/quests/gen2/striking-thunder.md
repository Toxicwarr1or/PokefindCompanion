---
title: 'Striking Thunder'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'striking_thunder'
slug: 'striking-thunder'
description: 'It''s time to check in on Eusine and his research. I wonder what crazy adventure will unfold this time!'
source_file: 'striking-thunder.json'
start:
  npc: 'Eusine'
  town: 'Windfall Town'
  x: 565.5
  "y": 64.0
  z: 404.5
steps:
  - text: 'Go outside and investigate the roar'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get back to Cassidy and Butch?'
      town: 'Windfall Town'
  - text: 'Have a Pyschic Pokémon heal Suicune'
    location:
      kind: 'npc'
      x: 551.5
      "y": 70.0
      z: 410.5
      label: 'Suicune'
      town: 'Windfall Town'
  - text: 'Go inside and talk to Eusine'
    location:
      kind: 'npc'
      x: 564.5
      "y": 71.0
      z: 404.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Talk to Yosanda in Cruxirt Port'
    location:
      kind: 'npc'
      x: -548.5
      "y": 68.0
      z: 319.5
      label: 'Yosanda'
      town: 'Cruxirt Port'
  - text: 'Chase after Yosanda'
    location:
      kind: 'npc'
      x: -548.5
      "y": 68.0
      z: 319.5
      label: 'Yosanda'
      town: 'Windfall Town'
  - text: 'Keep chasing after Yosanda'
    location:
      kind: 'npc'
      x: -548.5
      "y": 68.0
      z: 319.5
      label: 'Yosanda'
      town: 'Windfall Town'
  - text: 'Continue to chase after Yosanda'
    location:
      kind: 'npc'
      x: -548.5
      "y": 68.0
      z: 319.5
      label: 'Yosanda'
      town: 'Windfall Town'
  - text: 'Follow Yosanda into her house'
    location:
      kind: 'npc'
      x: -548.5
      "y": 68.0
      z: 319.5
      label: 'Yosanda'
      town: 'Windfall Town'
  - text: 'Find another way into the house'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Talk to Yosanda'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Yosanda'
        x: -536.5
        "y": 68.0
        z: 326.5
        town: 'Windfall Town'
        team:
          - species: 'Tentacruel'
            level: 100
          - species: 'Magneton'
            level: 100
          - species: 'Crobat'
            level: 100
          - species: 'Steelix'
            level: 100
          - species: 'Nidoking'
            level: 100
          - species: 'Jataro_Typhlosion'
            level: 100
  - text: 'Talk to Eusine at his lab'
    location:
      kind: 'npc'
      x: 564.5
      "y": 71.0
      z: 404.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Find Eusine in Fog City near the Umbreon map'
    location:
      kind: 'npc'
      x: 565.5
      "y": 64.0
      z: 404.5
      label: 'Eusine'
      town: 'Fog City'
  - text: 'Check out the Game Corner in Fog City'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Fog City'
  - text: 'Find someone to talk to in the Game Corner'
    location:
      kind: 'npc'
      x: 141.5
      "y": 79.0
      z: 1263.5
      label: 'Shady Guy'
      town: 'Windfall Town'
  - text: 'Head upstairs to check it out'
    location:
      kind: 'region'
      x: 132.5
      "y": 87.0
      z: 1253.0
      bbox:
        x1: 131.0
        "y1": 86.0
        z1: 1251.0
        x2: 134.0
        "y2": 88.0
        z2: 1255.0
      town: 'Windfall Town'
  - text: 'Head downstairs and try out the different slot machines'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Shady Guy'
        x: 134.5
        "y": 79.0
        z: 1263.5
        town: 'Windfall Town'
        team:
          - species: 'Arbok'
            level: 100
          - species: 'Machamp'
            level: 100
          - species: 'Golbat'
            level: 100
          - species: 'Ariados'
            level: 100
          - species: 'Golem'
            level: 100
          - species: 'Scizor'
            level: 100
  - text: 'Use your key card to take the elevator'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 168.5
        "y": 60.0
        z: 1237.5
        town: 'Windfall Town'
        team:
          - species: 'Forretress'
            level: 100
          - species: 'Umbreon'
            level: 100
          - species: 'Crobat'
            level: 100
          - species: 'Qwilfish'
            level: 100
          - species: 'Murkrow'
            level: 100
          - species: 'Muk'
            level: 100
  - text: 'Find a way to disable the blockades'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 161.5
        "y": 60.0
        z: 1230.5
        town: 'Windfall Town'
        team:
          - species: 'Beedrill'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Nidoking'
            level: 100
          - species: 'Nidoqueen'
            level: 100
          - species: 'Vileplume'
            level: 100
          - species: 'Lapras'
            level: 100
  - text: 'Find the lever to disable the blockade'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Search the newly unblocked area'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Find the hidden switch in the supply room (Make sure to click blocks as well!)'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Explore the area more'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Scientist'
        x: 165.5
        "y": 60.0
        z: 1249.5
        town: 'Windfall Town'
        team:
          - species: 'Magneton'
            level: 100
          - species: 'Ampharos'
            level: 100
          - species: 'Electrode'
            level: 100
          - species: 'Raichu'
            level: 100
          - species: 'Scizor'
            level: 100
          - species: 'Alolan_Raichu'
            level: 100
  - text: 'Check out the computers in the room'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Go explore the area'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Worker'
        x: 173.5
        "y": 60.0
        z: 1276.5
        town: 'Windfall Town'
        team:
          - species: 'Sudowoodo'
            level: 100
          - species: 'Hitmonchan'
            level: 100
          - species: 'Electrode'
            level: 100
          - species: 'Hitmontop'
            level: 100
          - species: 'Kangaskhan'
            level: 100
          - species: 'Heracross'
            level: 100
      - trainer: 'Team Rocket Scientist'
        x: 176.5
        "y": 60.0
        z: 1276.5
        town: 'Windfall Town'
        team:
          - species: 'Donphan'
            level: 100
          - species: 'Magneton'
            level: 100
          - species: 'Omastar'
            level: 100
          - species: 'Muk'
            level: 100
          - species: 'Kabutops'
            level: 100
          - species: 'Aerodactyl'
            level: 100
  - text: 'Search the area for the blockade switch'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Explore the area some more'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Look around the library and talk to the Team Rocket Admin'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Admin'
        x: 172.5
        "y": 60.0
        z: 1305.5
        town: 'Windfall Town'
        team:
          - species: 'Forretress'
            level: 100
          - species: 'Alolan_Persian'
            level: 100
          - species: 'Kyoto_Gengar'
            level: 100
          - species: 'Alolan_Muk'
            level: 100
          - species: 'Clefable'
            level: 100
          - species: 'Dragonite'
            level: 100
  - text: 'Use the key card in the elevator in the library to proceed down'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Explore the area'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Make your way across the toxic waste'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Jump into the bubbling pipe'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Make your way across the toxic waste'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Find Eusine in the prison'
    location:
      kind: 'npc'
      x: 565.5
      "y": 64.0
      z: 404.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Battle the Team Rocket Grunts'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 192.5
        "y": 34.0
        z: 1360.5
        town: 'Windfall Town'
        team:
          - species: 'Blissey'
            level: 100
          - species: 'Espeon'
            level: 100
          - species: 'Pidgeot'
            level: 100
          - species: 'Scizor'
            level: 100
          - species: 'Azumarill'
            level: 100
          - species: 'Tyranitar'
            level: 100
      - trainer: 'Team Rocket Grunt'
        x: 192.5
        "y": 34.0
        z: 1373.5
        town: 'Windfall Town'
        team:
          - species: 'Arbok'
            level: 100
          - species: 'Miltank'
            level: 100
          - species: 'Gallade'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Typhlosion'
            level: 100
          - species: 'Gengar'
            level: 100
  - text: 'Talk to Eusine'
    location:
      kind: 'npc'
      x: 197.5
      "y": 34.0
      z: 1370.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Grab the key card from the guard''s pocket without waking him up (Don''t step on broken bricks!)'
    location:
      kind: 'npc'
      x: 213.5
      "y": 34.0
      z: 1373.5
      label: 'Team Rocket Grunt'
      town: 'Windfall Town'
  - text: 'Talk to Eusine again'
    location:
      kind: 'npc'
      x: 197.5
      "y": 34.0
      z: 1370.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Continue down into the lower levels using the elevator'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Continue through the teleporting maze'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Battle the Team Rocket Grunts'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Grunt'
        x: 95.5
        "y": 41.0
        z: 1289.5
        town: 'Windfall Town'
        team:
          - species: 'Heracross'
            level: 100
          - species: 'Blissey'
            level: 100
          - species: 'Azumarill'
            level: 100
          - species: 'Togetic'
            level: 100
          - species: 'Gligar'
            level: 100
          - species: 'Kabutops'
            level: 100
      - trainer: 'Team Rocket Grunt'
        x: 96.5
        "y": 41.0
        z: 1292.5
        town: 'Windfall Town'
        team:
          - species: 'Espeon'
            level: 100
          - species: 'Miltank'
            level: 100
          - species: 'Azumarill'
            level: 100
          - species: 'Sunflora'
            level: 100
          - species: 'Ampharos'
            level: 100
          - species: 'Steelix'
            level: 100
      - trainer: 'Team Rocket Grunt'
        x: 99.0
        "y": 41.0
        z: 1292.5
        town: 'Windfall Town'
        team:
          - species: 'Dunsparce'
            level: 100
          - species: 'Umbreon'
            level: 100
          - species: 'Aipom'
            level: 100
          - species: 'Granbull'
            level: 100
          - species: 'Stantler'
            level: 100
          - species: 'Heracross'
            level: 100
      - trainer: 'Team Rocket Grunt'
        x: 101.5
        "y": 41.0
        z: 1292.5
        town: 'Windfall Town'
        team:
          - species: 'Girafarig'
            level: 100
          - species: 'Xatu'
            level: 100
          - species: 'Sneasel'
            level: 100
          - species: 'Donphan'
            level: 100
          - species: 'Lapras'
            level: 100
          - species: 'Starmie'
            level: 100
  - text: 'Confront the Team Rocket Admin'
    location:
      kind: 'npc'
      x: 101.0
      "y": 41.0
      z: 1297.5
      label: 'Team Rocket Admin'
      town: 'Windfall Town'
  - text: 'Battle the Team Rocket Admin'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Team Rocket Admin'
        x: 101.0
        "y": 41.0
        z: 1297.5
        town: 'Windfall Town'
        team:
          - species: 'Feraligatr'
            level: 100
          - species: 'Scizor'
            level: 100
          - species: 'Quagsire'
            level: 100
          - species: 'Heracross'
            level: 100
          - species: 'Piloswine'
            level: 100
          - species: 'Dragonite'
            level: 100
  - text: 'Pick up the key card on the desk'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Continue down to the lower level using the elevator'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Talk to Cassidy and Butch'
    location:
      kind: 'npc'
      x: 234.5
      "y": 25.0
      z: 1232.5
      label: 'Cassidy'
      town: 'Windfall Town'
  - text: 'Battle Cassidy'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Cassidy'
        x: 234.5
        "y": 25.0
        z: 1232.5
        town: 'Windfall Town'
        team:
          - species: 'Typhlosion'
            level: 130
          - species: 'Alakazam'
            level: 100
          - species: 'Tyranitar'
            level: 100
          - species: 'Dragonite'
            level: 100
          - species: 'Ursaring'
            level: 100
          - species: 'Crobat'
            level: 100
  - text: 'Battle Butch'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Butch'
        x: 232.5
        "y": 25.0
        z: 1232.5
        town: 'Windfall Town'
        team:
          - species: 'Golem'
            level: 100
          - species: 'Ampharos'
            level: 100
          - species: 'Meganium'
            level: 100
          - species: 'Poliwrath'
            level: 100
          - species: 'Arcanine'
            level: 100
          - species: 'Xatu'
            level: 100
  - text: 'Free Raikou by using Rock Smash on the machinery'
    location:
      kind: 'npc'
      x: 233.5
      "y": 26.5
      z: 1243.5
      label: 'Raikou'
      town: 'Windfall Town'
  - text: 'Return to Eusine outside his house in Windfall Town'
    location:
      kind: 'npc'
      x: 554.5
      "y": 70.0
      z: 411.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Pick up the piece of the Clear Bell'
    location:
      kind: 'npc'
      x: 186.5
      "y": 34.0
      z: 1366.5
      label: 'Need to get to the end of the teleporting maze?'
      town: 'Windfall Town'
  - text: 'Give the Clear Bell shard to Eusine'
    location:
      kind: 'npc'
      x: 554.5
      "y": 70.0
      z: 411.5
      label: 'Eusine'
      town: 'Windfall Town'
    rewards:
      - '100000 Coins'
      - '50 Tokens'
      - '150000 Trainer XP'
      - '3× Lucky Egg'
      - '10× rare Candy'
      - 'Shed Shell'
---
