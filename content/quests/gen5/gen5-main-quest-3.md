---
title: 'Main Quest 3 - A Soothing Melody'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_3'
slug: 'gen5-main-quest-3'
description: 'Music is said to be one of the most powerful forces of nature. And in times of trouble, that is exactly what you need!'
author: 'Mmaarten'
source_file: 'gen5-main-quest-3.json'
video_id: 'CUEQ5M_fvgg'
video_title: 'A Soothing Melody (Episode 9: Main Quest 3)'
start:
  npc: 'Tommy'
  description: 'Spiritvale'
  town: 'Spiritvale'
  x: 390.5
  "y": 53.5
  z: -18.5
steps:
  - text: 'Locate the suspicious activity in Spiritvale'
    location:
      kind: 'destination'
      x: 385.5
      "y": 55.0
      z: -33.5
      label: 'Locate the suspicious activity in Spiritvale'
      town: 'Spiritvale'
  - text: 'Talk to the citizens at the bridge to see how you can help calm the Pokémon'
    location:
      kind: 'npc'
      x: 390.5
      "y": 53.5
      z: -18.5
      label: 'Tommy'
      town: 'Spiritvale'
  - text: 'Go to Nurse Daisy''s home and find her flute (Hint> Her house is near a gym structure outside of town)'
    location:
      kind: 'destination'
      x: 470.5
      "y": 65.0
      z: 30.5
      label: 'Go to Nurse Daisy''s home and find her flute'
      town: 'Spiritvale'
  - text: 'Try to find Nurse Daisy''s flute in the chest'
  - text: 'Try to find the four digits to unlock the chest (Talk to Michael)'
    location:
      kind: 'destination'
      x: 375.5
      "y": 53.0
      z: -53.5
      label: 'Talk to Michael to find the first digit of the code'
      town: 'Spiritvale'
  - text: 'Bring a Normal type Pokémon to Michael'
    location:
      kind: 'npc'
      x: 375.5
      "y": 53.0
      z: -53.5
      label: 'Michael'
      town: 'Spiritvale'
  - text: 'Find the second digit of the code by talking to Amelia'
    location:
      kind: 'destination'
      x: 411.5
      "y": 55.0
      z: -95.5
      label: 'Talk to Amelia to find the second digit of the code'
      town: 'Spiritvale'
  - text: 'Give Amelia a generic postcard (HINT> The post office is in Findale Harbor)'
    location:
      kind: 'npc'
      x: 411.5
      "y": 55.0
      z: -95.5
      label: 'Amelia'
      town: 'Spiritvale'
  - text: 'Find the third digit of the code by talking to Mia'
    location:
      kind: 'destination'
      x: 405.5
      "y": 58.0
      z: -48.5
      label: 'Talk to Mia to find the third digit of the code'
      town: 'Spiritvale'
  - text: 'Solve the riddle located near Mia (Answer by typing /youranswer)'
    location:
      kind: 'npc'
      x: 405.5
      "y": 58.0
      z: -48.5
      label: 'Mia'
      town: 'Spiritvale'
  - text: 'Find the last digit of the code by talking to Kevin'
    location:
      kind: 'destination'
      x: 396.5
      "y": 54.0
      z: -110.5
      label: 'Talk to Kevin to find the fourth digit of the code'
      town: 'Spiritvale'
  - text: 'Battle Kevin'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Kevin'
        x: 396.5
        "y": 53.9
        z: -110.5
        town: 'Spiritvale'
        team:
          - species: 'Litwick'
            level: 38
          - species: 'Zoroark'
            level: 39
          - species: 'Cofagrigus'
            level: 40
  - text: 'Click the chest to enter the code digit by digit (The code is 9740)'
    location:
      kind: 'destination'
      x: 470.5
      "y": 66.0
      z: 32.5
      label: 'Open the chest at the Nurse''s home'
      town: 'Spiritvale'
  - text: 'Click the chest to enter the code'
  - text: 'Fight Nurse Daisy''s Snorlax'
    location:
      kind: 'npc'
      x: 472.5
      "y": 66.0
      z: 39.0
      label: 'AnniSnorlax'
      town: 'Spiritvale'
  - text: 'Return to the bridge and play the flute to calm down the Pokémon'
    location:
      kind: 'destination'
      x: 384.5
      "y": 53.0
      z: -33.5
      label: 'Return to the bridge and calm the Pokémon'
      town: 'Spiritvale'
  - text: 'Talk to Thomas at the bridge in Spiritvale.'
    location:
      kind: 'npc'
      x: 383.7
      "y": 52.9
      z: -37.9
      label: 'Thomas'
      town: 'Spiritvale'
    rewards:
      - '20000 Coins'
      - '25 Tokens'
      - '15000 Trainer XP'
      - '2× material'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
---
