---
title: 'Main Quest 4 - Observing the End!'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'gen3_main_quest_4'
slug: 'gen3-main-quest-4'
description: 'Gordon has discovered that Minoru has created a very powerful weapon. You must stop her before she uses it!'
source_file: 'gen3-main-quest-4.json'
video_id: '1ZFm38ne5z4'
video_title: 'PokéFind Observing the End (Main Quest 4: Generation 3)'
start:
  npc: 'Gordon'
  town: 'Kinetic Island'
  x: 1468.5
  "y": 28.0
  z: -527.5
steps:
  - text: 'Speak to Dr. Rein at the entrance to the observatory'
    location:
      kind: 'npc'
      x: 1506.5
      "y": 29.0
      z: -436.5
      label: 'Dr. Van Nostrand'
      town: 'Kinetic Island'
  - text: 'Find Dr. Van Nostrand at his home on Kinetic Island'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Ayumu'
        x: 1362.5
        "y": 56.0
        z: -647.5
        town: 'Kinetic Island'
        team:
          - species: 'Slowbro'
            level: 65
          - species: 'Grumpig'
            level: 65
  - text: 'Beat Ayumu'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Dr. Luminaut'
        x: 1377.5
        "y": 56.0
        z: -655.5
        town: 'Kinetic Island'
        team:
          - species: 'Crawdaunt'
            level: 68
          - species: 'Umbreon'
            level: 68
  - text: 'Beat Dr. Luminaut'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Richard'
        x: 1354.5
        "y": 56.0
        z: -680.5
        town: 'Kinetic Island'
        team:
          - species: 'Shiftry'
            level: 69
          - species: 'Whiscash'
            level: 69
  - text: 'Beat Richard'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Dr. Partly'
        x: 1335.5
        "y": 56.0
        z: -641.5
        town: 'Kinetic Island'
        team:
          - species: 'Sharpedo'
            level: 70
          - species: 'Absol'
            level: 70
          - species: 'Espeon'
            level: 70
  - text: 'Beat Dr. Partly'
    location:
      kind: 'npc'
      x: 1335.5
      "y": 56.0
      z: -641.5
      label: 'Dr. Partly'
      town: 'Kinetic Island'
  - text: 'Find where Haru is hiding.'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Haru'
        x: 1334.5
        "y": 56.0
        z: -677.5
        town: 'Kinetic Island'
        team:
          - species: 'Blaziken'
            level: 71
          - species: 'Houndoom'
            level: 71
          - species: 'Arcanine'
            level: 71
          - species: 'Flareon'
            level: 71
  - text: 'Beat Haru'
    location:
      kind: 'battle'
      town: 'Kinetic Island'
    battles:
      - trainer: 'Mysterious Pokémon'
        x: 1436.5
        "y": 105.0
        z: -604.5
        town: 'Kinetic Island'
        team:
          - species: 'Alakazam'
            level: 74
          - species: 'Medicham'
            level: 75
          - species: 'Metagross'
            level: 74
  - text: 'Beat the Mysterious Pokémon at the top of the observatory'
    location:
      kind: 'npc'
      x: 1436.5
      "y": 105.0
      z: -604.5
      label: 'Mysterious Pokémon'
      town: 'Kinetic Island'
    rewards:
      - '20000 Coins'
      - 'Ability Capsule'
      - 'Wise Glasses'
      - 'Moon Stone'
      - '180000 Trainer XP'
---
