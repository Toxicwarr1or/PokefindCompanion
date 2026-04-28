---
title: 'Main Quest 1 - Visions of Victory'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'gen3_main_quest_1'
slug: 'gen3-main-quest-1'
description: 'The gym leaders seem to have disappeared. There is a shady person outside Springdale gym. Go and investigate!'
source_file: 'gen3-main-quest-1.json'
video_id: 'fiySnCshdFI'
video_title: 'PokeFind Visions of Victory (Main Quest 1: Generation 3)'
start:
  npc: 'Ayumu'
  town: 'Sleepy Hollow'
  x: -681.5
  "y": 32.0
  z: 700.5
steps:
  - text: 'Beat Officer Biceroy in the prison'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Homphray'
        x: -652.5
        "y": 38.0
        z: 460.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Whismur'
            level: 8
  - text: 'Beat Officer Homphray in the prison to unlock Control Room'
    location:
      kind: 'npc'
      x: -652.5
      "y": 38.0
      z: 460.5
      label: 'Homphray'
      town: 'Sleepy Hollow'
  - text: 'Use the switch in the prison!'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Sergeant Bo'
        x: -692.5
        "y": 20.0
        z: 459.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Sableye'
            level: 9
          - species: 'Spinda'
            level: 10
  - text: 'Beat Sergeant Bo in the Block B'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Lieutenant Tico'
        x: -708.5
        "y": 20.0
        z: 460.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Poochyena'
            level: 10
          - species: 'Gastly'
            level: 11
  - text: 'Beat Lieutenant Tico in the prison'
    location:
      kind: 'npc'
      x: -708.5
      "y": 20.0
      z: 460.5
      label: 'Lieutenant Tico'
      town: 'Sleepy Hollow'
  - text: 'Enter Solitary confinement behind Tico!'
    location:
      kind: 'npc'
      x: -686.5
      "y": 20.0
      z: 431.5
      label: 'Gordon'
      town: 'Sleepy Hollow'
  - text: 'Talk to Gordon in Jail'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Beth'
        x: -678.5
        "y": 20.0
        z: 444.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Slakoth'
            level: 12
          - species: 'Zubat'
            level: 12
  - text: 'Beat Beth in the prison'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Warden Blair'
        x: -659.5
        "y": 60.0
        z: 458.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Absol'
            level: 11
          - species: 'Shuppet'
            level: 13
          - species: 'Duskull'
            level: 13
  - text: 'Beat Warden Blair at the top of the prison'
    location:
      kind: 'npc'
      x: -659.5
      "y": 60.0
      z: 458.5
      label: 'Warden Blair'
      town: 'Sleepy Hollow'
  - text: 'Run down the stairs and escape!'
    location:
      kind: 'battle'
      town: 'Sleepy Hollow'
    battles:
      - trainer: 'Minoru'
        x: -652.5
        "y": 47.0
        z: 454.5
        town: 'Sleepy Hollow'
        team:
          - species: 'Abra'
            level: 15
          - species: 'Meditite'
            level: 15
          - species: 'Beldum'
            level: 15
  - text: 'Beat Minoru in the prison'
    location:
      kind: 'npc'
      x: -652.5
      "y": 47.0
      z: 454.5
      label: 'Minoru'
      town: 'Sleepy Hollow'
    rewards:
      - '7000 Trainer XP'
      - '3× PP Up'
      - '10 Tokens'
---
