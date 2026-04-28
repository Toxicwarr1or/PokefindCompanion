---
title: 'Roaring Flames'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'roaring_flames'
slug: 'roaring-flames'
description: 'Eusine needs your help again! He''s made an amazing discovery!'
source_file: 'roaring-flames.json'
start:
  npc: 'Eusine'
  town: 'Windfall Town'
  x: 566.5
  "y": 54.0
  z: 405.5
steps:
  - text: 'Talk to Kelise at her house on the path between Kouga Academy and Hollow Village'
    location:
      kind: 'npc'
      x: 308.5
      "y": 88.0
      z: -134.5
      label: 'Kelise'
      town: 'Hollow Village'
  - text: 'Battle Kelise'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Kelise'
        x: 308.5
        "y": 88.0
        z: -134.5
        town: 'Windfall Town'
        team:
          - species: 'Sneasel'
            level: 100
          - species: 'Espeon'
            level: 100
          - species: 'Xatu'
            level: 100
          - species: 'Milotic'
            level: 100
          - species: 'Absol'
            level: 100
          - species: 'Ursaring'
            level: 100
  - text: 'Talk to Roen on a boat at Kouga Academy and get Kelise''s package'
    location:
      kind: 'npc'
      x: 232.5
      "y": 79.0
      z: -265.5
      label: 'Roen'
      town: 'Windfall Town'
  - text: 'Battle Roen'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Roen'
        x: 232.5
        "y": 79.0
        z: -265.5
        town: 'Windfall Town'
        team:
          - species: 'Steelix'
            level: 100
          - species: 'Heracross'
            level: 100
          - species: 'Piloswine'
            level: 100
          - species: 'Granbull'
            level: 100
          - species: 'Lapras'
            level: 100
          - species: 'Milotic'
            level: 100
  - text: 'Return the package to Kelise'
    location:
      kind: 'npc'
      x: 308.5
      "y": 88.0
      z: -134.5
      label: 'Kelise'
      town: 'Windfall Town'
  - text: 'Explore the shadowy path into the forest near Kelise''s house'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Continue exploring the path (Make sure to stay on the path!)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Defeat the Shadow Pokémon'
    location:
      kind: 'npc'
      x: 364.5
      "y": 82.0
      z: -138.5
      label: 'Shadow Scizor'
      town: 'Windfall Town'
  - text: 'Continue down the path (Make sure to stay on the path!)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Defeat the Shadow Pokémon'
    location:
      kind: 'npc'
      x: 361.5
      "y": 77.0
      z: -111.5
      label: 'Shadow Alakazam'
      town: 'Windfall Town'
  - text: 'Continue down the path (Make sure to stay on the path!)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Investigate the boulder'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Solve the riddle ''Everyone has it and no one can lose it; what is it?'' (To answer type /youranswer)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Enter the Shadow Lair'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Defeat the Shadow Guards'
    location:
      kind: 'npc'
      x: 404.5
      "y": 65.0
      z: -104.5
      label: 'Shadow Snorlax'
      town: 'Windfall Town'
  - text: 'Investigate the door at the end of the hall'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Solve the Riddle: What common mob drop does a chicken drop that is useful for making arrows? (To answer type /youranswer)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Complete the parkour in Room 1 to get the feather'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Solve the Riddle: This is a type of yellow plant that can grow very tall (To answer type /youranswer)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Complete the maze in Room 2 to get the sunflower'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Solve the Riddle: It falls from the sky in a certain season and it''s cold; What is it? (To answer type /youranswer)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Complete the parkour in Room 3 to get the snow'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Solve the Riddle: This shell can be used to craft a Conduit (To answer type /youranswer)'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Complete the maze in Room 4 to get the nautilus shell'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Proceed into The Great Hall and defeat the guard'
    location:
      kind: 'npc'
      x: 449.5
      "y": 65.1
      z: -104.5
      label: 'Shadow Chansey'
      town: 'Windfall Town'
  - text: 'Go to the cage with Entei'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Battle the Shadow Leader'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Shadow Leader'
        x: 469.5
        "y": 65.0
        z: -104.5
        town: 'Windfall Town'
        team:
          - species: 'Metagross'
            level: 125
          - species: 'Gardevoir'
            level: 125
          - species: 'Salamence'
            level: 125
          - species: 'Feraligatr'
            level: 125
          - species: 'Aggron'
            level: 125
          - species: 'Tyranitar'
            level: 135
  - text: 'Click the dispenser to free Entei'
    location:
      kind: 'npc'
      x: 370.5
      "y": 80.0
      z: -103.5
      label: 'Need to get back into the Shadow Lair?'
      town: 'Windfall Town'
  - text: 'Return to Eusine at his house in Windfall Town'
    location:
      kind: 'npc'
      x: 546.5
      "y": 70.0
      z: 407.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Pick up the Clear Bell piece and give it to Eusine'
    location:
      kind: 'npc'
      x: 546.5
      "y": 70.0
      z: 407.5
      label: 'Eusine'
      town: 'Windfall Town'
    rewards:
      - '150000 Coins'
      - '50 Tokens'
      - '150000 Trainer XP'
      - '10× rare candy'
      - '3× pp_up'
      - 'Rocky Helmet'
---
