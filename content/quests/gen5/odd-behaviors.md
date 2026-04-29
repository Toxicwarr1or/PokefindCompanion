---
title: 'Odd Behaviors'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_odd_behaviors'
slug: 'odd-behaviors'
description: 'People have been acting strangely in Findale Harbor, and Officer Jenny needs your help! Can you and Officer Jenny solve the case?'
author: 'Pokécrafter320'
source_file: 'odd_behaviors.json'
start:
  npc: 'Officer Jenny'
  description: 'Talk to Officer Jenny outside of the Pokémon Center in Findale Harbor'
  town: 'Findale Harbor'
  x: 569.5
  "y": 49.0
  z: 601.5
steps:
  - text: 'Talk to Stanley the PokéMart Clerk in the Findale Harbor PokéMart'
    location:
      kind: 'npc'
      x: 525.5
      "y": 55.0
      z: 529.5
      label: 'Stanley'
      town: 'Findale Harbor'
  - text: 'Go to Joe the PokéMart Clerk in the Findale Harbor PokéMart'
    location:
      kind: 'region'
      x: 518.0
      "y": 56.0
      z: 520.0
      bbox:
        x1: 514.0
        "y1": 54.0
        z1: 518.0
        x2: 522.0
        "y2": 58.0
        z2: 522.0
      town: 'Findale Harbor'
  - text: 'Talk to Stanley again'
    location:
      kind: 'npc'
      x: 525.5
      "y": 55.0
      z: 529.5
      label: 'Stanley'
      town: 'Findale Harbor'
  - text: 'Type / followed by Joe''s special code word (Example: /codeword)'
  - text: 'Battle ''Stanley'''
    location:
      kind: 'npc'
      x: 525.5
      "y": 55.0
      z: 529.5
      label: 'Stanley'
      town: 'Findale Harbor'
  - text: 'Talk to Joe the PokéMart Clerk'
    location:
      kind: 'region'
      x: 518.0
      "y": 56.0
      z: 520.0
      bbox:
        x1: 514.0
        "y1": 54.0
        z1: 518.0
        x2: 522.0
        "y2": 58.0
        z2: 522.0
      town: 'Findale Harbor'
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Talk to Aunty Cassie near the largest tree in Findale Harbor'
    location:
      kind: 'npc'
      x: 511.5
      "y": 49.0
      z: 632.5
      label: 'Aunty Cassie'
      town: 'Findale Harbor'
  - text: 'Battle ''Aunty Cassie'''
    location:
      kind: 'npc'
      x: 511.5
      "y": 49.0
      z: 632.5
      label: 'Aunty Cassie'
      town: 'Findale Harbor'
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Go to Professor Hemlock''s lab and talk to him'
    location:
      kind: 'region'
      x: 638.0
      "y": 51.0
      z: 421.0
      bbox:
        x1: 635.0
        "y1": 49.0
        z1: 418.0
        x2: 641.0
        "y2": 53.0
        z2: 424.0
      town: 'Findale Harbor'
  - text: 'Talk to Scientist James upstairs in the Professor''s Lab'
    location:
      kind: 'npc'
      x: 645.5
      "y": 59.0
      z: 431.5
      label: 'Scientist James'
      town: 'Findale Harbor'
  - text: 'Battle ''Scientist James'''
    location:
      kind: 'npc'
      x: 645.5
      "y": 59.0
      z: 431.5
      label: 'Scientist James'
      town: 'Findale Harbor'
  - text: 'Go back to Professor Hemlock and tell him about the Ditto'
    location:
      kind: 'npc'
      x: 525.5
      "y": 55.0
      z: 529.5
      label: 'Ditto'
      town: 'Findale Harbor'
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Talk to Oliver near the fountain outside of the PokéMart'
    location:
      kind: 'npc'
      x: 541.5
      "y": 55.0
      z: 578.5
      label: 'Oliver'
      town: 'Findale Harbor'
  - text: 'Battle ''Oliver'''
    location:
      kind: 'battle'
    battles:
      - trainer: 'Oliver'
        x: 541.5
        "y": 55.0
        z: 578.5
        town: 'Findale Harbor'
        team:
          - species: 'Blitzle'
            level: 30
          - species: 'Skiploom'
            level: 50
          - species: 'Corphish'
            level: 30
          - species: 'Pignite'
            level: 30
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Go to the Findale Harbor Docks and talk to Sailor Jeffrey'
    location:
      kind: 'npc'
      x: 565.5
      "y": 44.0
      z: 466.5
      label: 'Sailor Hilda'
      town: 'Findale Harbor'
  - text: 'Talk to Sailor Hilda'
    location:
      kind: 'npc'
      x: 565.5
      "y": 44.0
      z: 466.5
      label: 'Sailor Hilda'
      town: 'Findale Harbor'
  - text: 'Battle ''Sailor Hilda'''
    location:
      kind: 'npc'
      x: 565.5
      "y": 44.0
      z: 466.5
      label: 'Sailor Hilda'
      town: 'Findale Harbor'
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Go to Aunty Bibby and ask her about Robert'
    location:
      kind: 'npc'
      x: 511.5
      "y": 49.0
      z: 632.5
      label: 'Aunty Cassie'
      town: 'Findale Harbor'
  - text: 'Report back to Officer Jenny'
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Battle ''Officer Jenny'''
    location:
      kind: 'npc'
      x: 569.5
      "y": 49.0
      z: 601.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
  - text: 'Head back to the fountain near the PokéMart to see if Officer Jenny is there'
    location:
      kind: 'npc'
      x: 540.5
      "y": 55.0
      z: 580.5
      label: 'Officer Jenny'
      town: 'Findale Harbor'
    rewards:
      - '50000 Coins'
      - '20000 Trainer XP'
      - '20 Tokens'
      - 'material'
---
