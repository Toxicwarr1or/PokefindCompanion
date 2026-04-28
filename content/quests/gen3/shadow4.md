---
title: 'Shadows Emerging'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'shadow4'
slug: 'shadow4'
description: 'Team Rocket are up to no good! They seem to have a new partner to help take over the Haikou region using Pokémon'
source_file: 'shadow4.json'
start:
  npc: 'Michael'
  town: 'Findview Port'
  x: -365.5
  "y": 36.0
  z: 502.5
steps:
  - text: 'Head to Findview Port to see what Team Rocket is up to'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Captain Kaj'
        x: -152.5
        "y": 24.0
        z: 610.5
        town: 'Findview Port'
        team:
          - species: 'Raticate'
            level: 80
          - species: 'Muk'
            level: 80
          - species: 'Sandslash'
            level: 79
          - species: 'Marowak'
            level: 80
  - text: 'Battle Captain Kaj on his boat'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Alexius'
        x: 838.5
        "y": 116.0
        z: 264.5
        town: 'Findview Port'
        team:
          - species: 'Arbok'
            level: 83
          - species: 'Machoke'
            level: 83
          - species: 'Venomoth'
            level: 81
          - species: 'Nidoqueen'
            level: 83
  - text: 'Head to Targaryen Keep to try and stop Team Rocket'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Isidora'
        x: 850.5
        "y": 135.0
        z: 265.5
        town: 'Findview Port'
        team:
          - species: 'Poliwrath'
            level: 84
          - species: 'Mightyena'
            level: 86
          - species: 'Dugtrio'
            level: 84
          - species: 'Tauros'
            level: 85
  - text: 'Battle Team Rocket member Isidora'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Deodatus'
        x: 833.5
        "y": 145.0
        z: 272.5
        town: 'Findview Port'
        team:
          - species: 'Persian'
            level: 90
          - species: 'Tentacruel'
            level: 88
          - species: 'Crobat'
            level: 88
          - species: 'Roselia'
            level: 90
          - species: 'Houndoom'
            level: 88
          - species: 'Seviper'
            level: 90
  - text: 'Battle Team Rocket member Deodatus'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Kaleigh'
        x: 824.5
        "y": 155.0
        z: 257.5
        town: 'Findview Port'
        team:
          - species: 'Weezing'
            level: 90
          - species: 'Victreebel'
            level: 92
          - species: 'Camerupt'
            level: 90
          - species: 'Sableye'
            level: 92
          - species: 'Marowak'
            level: 90
          - species: 'Golbat'
            level: 92
  - text: 'Battle Team Rocket member Kaleigh'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Orson'
        x: 855.5
        "y": 175.0
        z: 266.5
        town: 'Findview Port'
        team:
          - species: 'Muk'
            level: 95
          - species: 'Nidoking'
            level: 93
          - species: 'Kangaskhan'
            level: 92
          - species: 'Ninjask'
            level: 95
          - species: 'Golem'
            level: 92
          - species: 'Arbok'
            level: 95
  - text: 'Battle Team Rocket member Orson'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Trev'
        x: 822.5
        "y": 185.0
        z: 266.5
        town: 'Findview Port'
        team:
          - species: 'Forretress'
            level: 97
          - species: 'Slowbro'
            level: 95
          - species: 'Seaking'
            level: 97
          - species: 'Dunsparce'
            level: 97
          - species: 'Crobat'
            level: 96
          - species: 'Shiftry'
            level: 96
  - text: 'Battle Team Rocket member Trev'
    location:
      kind: 'npc'
      x: 822.5
      "y": 185.0
      z: 266.5
      label: 'Trev'
      town: 'Findview Port'
  - text: 'Try to make your way to the top of Battle Tower'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'James'
        x: 843.5
        "y": 198.0
        z: 267.5
        town: 'Findview Port'
        team:
          - species: 'Sharpedo'
            level: 100
          - species: 'Arbok'
            level: 100
          - species: 'Clefable'
            level: 100
          - species: 'Weezing'
            level: 100
          - species: 'Dusclops'
            level: 100
          - species: 'Wobbuffet'
            level: 100
  - text: 'Try again to make your way to the top of Battle Tower'
    location:
      kind: 'npc'
      x: -361.5
      "y": 36.0
      z: 490.5
      label: 'Michael'
      town: 'Findview Port'
  - text: 'Head back to Findview to brief Michael'
    location:
      kind: 'npc'
      x: 1580.5
      "y": 28.0
      z: -399.5
      label: 'Michael'
      town: 'Findview Port'
  - text: 'Head to the Team Rocket HQ''s front door in Targaryen Keep'
  - text: 'Use a Water Type Pokémon to get inside of the Team Rocket HQ'
    location:
      kind: 'npc'
      x: 938.5
      "y": 82.0
      z: 1637.5
      label: 'Burkhart'
      town: 'Findview Port'
  - text: 'Battle Team Rocket member Burkhart'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Burkhart'
        x: 938.5
        "y": 82.0
        z: 1637.5
        town: 'Findview Port'
        team:
          - species: 'Nidoking'
            level: 84
          - species: 'Scizor'
            level: 85
          - species: 'Gyarados'
            level: 85
          - species: 'Charizard'
            level: 87
      - trainer: 'Aneurin'
        x: 1028.5
        "y": 79.0
        z: 1538.5
        town: 'Findview Port'
        team:
          - species: 'Lapras'
            level: 85
          - species: 'Absol'
            level: 98
          - species: 'Venusaur'
            level: 88
          - species: 'Tyranitar'
            level: 90
  - text: 'Battle Team Rocket member Aneurin in the lab'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Alexandra'
        x: 1024.5
        "y": 79.0
        z: 1583.5
        town: 'Findview Port'
        team:
          - species: 'Aerodactyl'
            level: 88
          - species: 'Manectric'
            level: 91
          - species: 'Blastoise'
            level: 91
          - species: 'Rapidash'
            level: 90
          - species: 'Feraligatr'
            level: 88
          - species: 'Meganium'
            level: 93
  - text: 'Battle Team Rocket member Alexandra in the lab'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Sif'
        x: 864.5
        "y": 91.0
        z: 1614.5
        town: 'Findview Port'
        team:
          - species: 'Jolteon'
            level: 92
          - species: 'Snorlax'
            level: 94
          - species: 'Houndoom'
            level: 91
          - species: 'Nidoqueen'
            level: 94
          - species: 'Scizor'
            level: 93
          - species: 'Kingdra'
            level: 96
  - text: 'Battle Team Rocket member Sif in the vents'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Archana'
        x: 843.5
        "y": 98.0
        z: 1620.5
        town: 'Findview Port'
        team:
          - species: 'Altaria'
            level: 96
          - species: 'Starmie'
            level: 97
          - species: 'Flareon'
            level: 95
          - species: 'Heracross'
            level: 97
          - species: 'Typhlosion'
            level: 98
          - species: 'Omastar'
            level: 100
  - text: 'Battle Team Rocket member Archana in the room at the end of the vents'
    location:
      kind: 'npc'
      x: 843.5
      "y": 98.0
      z: 1620.5
      label: 'Archana'
      town: 'Findview Port'
  - text: 'Get through the door with a Fighting Type Pokémon'
    location:
      kind: 'region'
      x: 936.0
      "y": 88.0
      z: 1465.5
      bbox:
        x1: 920.0
        "y1": 78.0
        z1: 1459.0
        x2: 952.0
        "y2": 98.0
        z2: 1472.0
      town: 'Findview Port'
  - text: 'Walk to the end of the Shadow Factory room'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Giovanni'
        x: 938.5
        "y": 79.0
        z: 1456.5
        town: 'Findview Port'
        team:
          - species: 'Dragonite'
            level: 100
          - species: 'Salamence'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Blaziken'
            level: 100
          - species: 'Sceptile'
            level: 100
          - species: 'Mewtwo'
            level: 100
  - text: 'Head back to Findview to brief Michael'
    location:
      kind: 'npc'
      x: 1580.5
      "y": 28.0
      z: -399.5
      label: 'Michael'
      town: 'Findview Port'
  - text: 'Head to the Kinetic Island docks'
    location:
      kind: 'npc'
      x: 1434.5
      "y": 22.0
      z: -456.5
      label: 'Lily'
      town: 'Kinetic Island'
  - text: 'Confront Michael''s friend Lily'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Lily'
        x: 1434.5
        "y": 22.0
        z: -456.5
        town: 'Findview Port'
        team:
          - species: 'Breloom'
            level: 100
          - species: 'Houndoom'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Blissey'
            level: 100
          - species: 'Manectric'
            level: 100
          - species: 'Tyranitar'
            level: 100
      - trainer: 'Adon'
        x: 1487.5
        "y": 25.0
        z: -401.5
        town: 'Findview Port'
        team:
          - species: 'Aggron'
            level: 100
          - species: 'Rapidash'
            level: 100
          - species: 'Aerodactyl'
            level: 100
          - species: 'Sceptile'
            level: 100
          - species: 'Nidoqueen'
            level: 100
          - species: 'Feraligatr'
            level: 100
  - text: 'Battle Adon in the city on Kinetic Island'
    location:
      kind: 'npc'
      x: 1513.5
      "y": 39.0
      z: -396.5
      label: 'Nags'
      town: 'Kinetic Island'
  - text: 'Battle Nags in the city on Kinetic Island'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Nags'
        x: 1513.5
        "y": 39.0
        z: -396.5
        town: 'Kinetic Island'
        team:
          - species: 'Charizard'
            level: 97
          - species: 'Manectric'
            level: 100
          - species: 'Meganium'
            level: 95
          - species: 'Marowak'
            level: 96
          - species: 'Milotic'
            level: 98
          - species: 'Kingdra'
            level: 100
  - text: 'Battle Zook near the secret cave on Kinetic Island'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Zook'
        x: 1550.5
        "y": 21.0
        z: -350.5
        town: 'Kinetic Island'
        team:
          - species: 'Jolteon'
            level: 100
          - species: 'Snorlax'
            level: 102
          - species: 'Gardevoir'
            level: 100
          - species: 'Omastar'
            level: 104
          - species: 'Typhlosion'
            level: 103
          - species: 'Aerodactyl'
            level: 102
      - trainer: 'Sekk'
        x: 1582.5
        "y": 28.0
        z: -396.5
        town: 'Kinetic Island'
        team:
          - species: 'Blaziken'
            level: 104
          - species: 'Wailord'
            level: 103
          - species: 'Gyarados'
            level: 104
          - species: 'Flygon'
            level: 105
          - species: 'Blastoise'
            level: 102
          - species: 'Houndoom'
            level: 104
  - text: 'Battle Sekk inside the secret cave on Kinetic Island'
    location:
      kind: 'npc'
      x: 1582.5
      "y": 28.0
      z: -396.5
      label: 'Sekk'
      town: 'Kinetic Island'
  - text: 'Head into Professor Batraz in his lab'
    location:
      kind: 'npc'
      x: 1614.5
      "y": 28.0
      z: -403.5
      label: 'Professor Batraz'
      town: 'Findview Port'
  - text: 'Head back to the Team Rocket HQ and use a Water Type Pokémon again to get inside'
    location:
      kind: 'npc'
      x: 938.5
      "y": 79.0
      z: 1455.5
      label: 'Cipher'
      town: 'Findview Port'
  - text: 'Confront Cipher in the Shadow Factory'
    location:
      kind: 'battle'
      town: 'Findview Port'
    battles:
      - trainer: 'Jovi'
        x: 939.5
        "y": 80.0
        z: 1467.5
        town: 'Findview Port'
        team:
          - species: 'Blissey'
            level: 105
          - species: 'Lapras'
            level: 103
          - species: 'Metagross'
            level: 109
          - species: 'Meganium'
            level: 105
          - species: 'Absol'
            level: 103
          - species: 'Starmie'
            level: 107
      - trainer: 'Michael'
        x: 937.5
        "y": 80.0
        z: 1467.5
        town: 'Findview Port'
        team:
          - species: 'Salamence'
            level: 104
          - species: 'Tyranitar'
            level: 106
          - species: 'Arcanine'
            level: 104
          - species: 'Snorlax'
            level: 105
          - species: 'Swampert'
            level: 106
          - species: 'Aerodactyl'
            level: 106
      - trainer: 'Cipher'
        x: 938.5
        "y": 79.0
        z: 1455.5
        town: 'Findview Port'
        team:
          - species: 'Alakazam'
            level: 108
          - species: 'Metagross'
            level: 109
          - species: 'Salamence'
            level: 104
          - species: 'Mewtwo'
            level: 113
          - species: 'Lugia'
            level: 112
          - species: 'Rayquaza'
            level: 115
---
