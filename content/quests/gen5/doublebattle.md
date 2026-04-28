---
title: 'Double Trouble Research'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'double_battle_sidequest'
slug: 'doublebattle'
description: 'Ranger Ivy of Bridgerun is studying specific Pokémon behaviour and needs some assitance.'
source_file: 'doublebattle.json'
start:
  npc: 'Ranger Ivy'
  description: 'Ranger Ivy in Bridgerun'
  town: 'Bridgerun'
  x: 1209.5
  "y": 52.0
  z: 125.5
steps:
  - text: 'Find the mightyena and luxray and collect data from them'
    location:
      kind: 'npc'
      x: 1124.5
      "y": 46.0
      z: 140.5
      label: 'Mightyena'
      town: 'Bridgerun'
  - text: 'Find Magmar and Electabuzz and collect data from them'
    location:
      kind: 'npc'
      x: 1334.5
      "y": 48.0
      z: 94.5
      label: 'Magmar'
      town: 'Bridgerun'
  - text: 'Return the data collected to Ranger Ivy'
    location:
      kind: 'npc'
      x: 1201.5
      "y": 54.0
      z: 125.5
      label: 'Ranger Ivy'
      town: 'Bridgerun'
  - text: 'Find Tyranitar and Amoonguss and collect final data from them'
    location:
      kind: 'npc'
      x: 1283.5
      "y": 58.0
      z: -24.5
      label: 'Tyranitar'
      town: 'Bridgerun'
  - text: 'Return to Ranger Ivy'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Ranger Ivy'
        x: 1209.5
        "y": 52.0
        z: 125.5
        town: 'Bridgerun'
        team:
          - species: 'eevee'
            level: 35
          - species: 'trapinch'
            level: 35
---
