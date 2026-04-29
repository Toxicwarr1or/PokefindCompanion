---
title: 'Main Quest 2 - Ignition of Space'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_2'
slug: 'gen4-main-quest-2-updated'
description: 'Thick black smoke can be seen above Woodburn. Go and see if you can help!'
source_file: 'gen4-main-quest-2_updated.json'
video_id: '3uBPavO-E3s'
video_title: 'PokéFind Shadow Quest 2'
start:
  npc: 'Pokémon Ranger'
  x: 270.5
  "y": 68.0
  z: 714.5
steps:
  - text: 'Run around the city and find Officer Reynolds'
    location:
      kind: 'npc'
      x: 347.5
      "y": 43.0
      z: 727.5
      label: 'Officer Reynolds'
  - text: 'Rescue all the pokémon on the ground trapped by the fire'
    location:
      kind: 'npc'
      x: 270.5
      "y": 68.0
      z: 714.5
      label: 'Pokémon Ranger'
  - text: 'Make your way to Wald''s house'
    location:
      kind: 'npc'
      x: 301.5
      "y": 70.0
      z: 766.5
      label: 'Wald'
  - text: 'Use a Water pokémon to rescue Wald'
    location:
      kind: 'npc'
      x: 270.5
      "y": 68.0
      z: 714.5
      label: 'Pokémon Ranger'
  - text: 'Go to Wald'
    location:
      kind: 'npc'
      x: 301.5
      "y": 70.0
      z: 766.5
      label: 'Wald'
  - text: 'Go outside and meet Wald'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Wald'
        x: 338.5
        "y": 43.0
        z: 724.5
        team:
          - species: 'Carnivine'
            level: 12
          - species: 'Combee'
            level: 14
          - species: 'Kricketune'
            level: 13
    rewards:
      - '10000 Coins'
      - '15 Tokens'
      - '7000 Trainer XP'
      - '3× PP_Up'
---
