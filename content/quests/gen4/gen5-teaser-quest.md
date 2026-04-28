---
title: 'Preparing for a New World'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'gen5_teaser_quest'
slug: 'gen5-teaser-quest'
description: 'Talk to Professor Hemlock at the docks in Findville Cape'
source_file: 'gen5-teaser-quest.json'
start:
  npc: 'Professor Hemlock'
  town: 'Hearth Valley'
  x: 956.5
  "y": 28.0
  z: 805.1
steps:
  - text: 'Find the Book on Pokémon inside the Observatory in Findville Cape'
    location:
      kind: 'npc'
      x: -224.5
      "y": 36.9
      z: 288.9
      label: 'Pokémon Trainer'
      town: 'Hearth Valley'
  - text: 'Look for the next item under the giant tree in Woodburn'
    location:
      kind: 'destination'
      x: 312.1
      "y": 41.0
      z: 727.1
      town: 'Hearth Valley'
  - text: 'Find the next piece of equipment in Marshbarrow in the boat'
    location:
      kind: 'npc'
      x: 1245.5
      "y": 23.5
      z: 268.5
      label: 'Roserade'
      town: 'Hearth Valley'
  - text: 'Find the microphone near a tomb in Duskburn'
    location:
      kind: 'destination'
      x: -699.5
      "y": 76.0
      z: 753.5
      town: 'Hearth Valley'
  - text: 'Battle the mysterious ghost'
    location:
      kind: 'battle'
      town: 'Hearth Valley'
    battles:
      - trainer: '???'
        x: -699.5
        "y": 81.0
        z: 739.1
        town: 'Hearth Valley'
        team:
          - species: 'Drifblim'
            level: 50
          - species: 'Mismagius'
            level: 50
          - species: 'Spiritomb'
            level: 50
  - text: 'Find the next item in Eastwind by the docks'
    location:
      kind: 'destination'
      x: 825.5
      "y": 26.0
      z: 541.5
      town: 'Hearth Valley'
  - text: 'Find the next item on a boat in the lake at Seabrooke'
    location:
      kind: 'destination'
      x: 709.5
      "y": 26.0
      z: -284.5
      town: 'Hearth Valley'
  - text: 'Collect the item in the line at the ice track in Frostfort'
    location:
      kind: 'region'
      x: 431.5
      "y": 23.0
      z: 212.5
      bbox:
        x1: 420.0
        "y1": 1.0
        z1: 198.0
        x2: 443.0
        "y2": 45.0
        z2: 227.0
      town: 'Hearth Valley'
  - text: 'Catch a Snorunt for Cooper'
    location:
      kind: 'npc'
      x: 434.5
      "y": 34.0
      z: 209.1
      label: 'Cooper'
      town: 'Hearth Valley'
  - text: 'Pick up the Thermometer in the line at Frostfort'
    location:
      kind: 'destination'
      x: 432.5
      "y": 34.0
      z: 209.5
      town: 'Hearth Valley'
  - text: 'Find the next item near a pool of lava in Hearth Valley'
    location:
      kind: 'destination'
      x: -1079.5
      "y": 32.5
      z: -139.5
      town: 'Hearth Valley'
  - text: 'Find the next piece of equipment near the Gamemaster''s house in Silverkeep'
    location:
      kind: 'destination'
      x: -744.0
      "y": 40.0
      z: 285.5
      town: 'Hearth Valley'
  - text: 'Find the next item near the main Gym at Circuit City'
    location:
      kind: 'region'
      x: -304.0
      "y": 23.0
      z: 631.5
      bbox:
        x1: -327.0
        "y1": 1.0
        z1: 606.0
        x2: -281.0
        "y2": 45.0
        z2: 657.0
      town: 'Circuit City'
  - text: 'Battle the Rotom'
    location:
      kind: 'npc'
      x: -309.5
      "y": 29.9
      z: 638.5
      label: 'Rotom'
      town: 'Hearth Valley'
  - text: 'Pickup the electricity rod'
    location:
      kind: 'destination'
      x: -318.5
      "y": 33.5
      z: 634.5
      town: 'Hearth Valley'
  - text: 'Find the next item in a cave in danger of collapsing in Diggers Peak'
    location:
      kind: 'destination'
      x: -161.5
      "y": 75.0
      z: -144.5
      town: 'Hearth Valley'
  - text: 'Find the next item high up in Crystal View near Jester Parker'
    location:
      kind: 'destination'
      x: 98.5
      "y": 131.0
      z: 480.5
      town: 'Hearth Valley'
  - text: 'Find the final item near a tall tower in Stronghaven'
    location:
      kind: 'region'
      x: -213.5
      "y": 33.0
      z: 287.0
      bbox:
        x1: -238.0
        "y1": 1.0
        z1: 267.0
        x2: -189.0
        "y2": 65.0
        z2: 307.0
      town: 'Hearth Valley'
  - text: 'Bring 2 Hondew berries from Aunty Alma''s shop to the trainer in Stronghaven'
    location:
      kind: 'npc'
      x: -224.5
      "y": 36.9
      z: 288.9
      label: 'Pokémon Trainer'
      town: 'Hearth Valley'
  - text: 'Grab the final piece of equipment in the EV tower in Stronghaven'
    location:
      kind: 'destination'
      x: -219.5
      "y": 54.0
      z: 268.0
      town: 'Hearth Valley'
  - text: 'Return to Professor Hemlock on the docks of Findville Cape'
    location:
      kind: 'npc'
      x: 956.5
      "y": 28.0
      z: 805.1
      label: 'Professor Hemlock'
      town: 'Hearth Valley'
    rewards:
      - '5000 Coins'
      - '20 Tokens'
      - '7500 Trainer XP'
---
