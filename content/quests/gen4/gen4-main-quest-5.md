---
title: 'Main Quest 5 - The Horrifying truth'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'GEN4_MAIN_QUEST_5'
slug: 'gen4-main-quest-5'
description: 'Team Cosmic Star has been spotted around Stronghaven. Find out what they are up to!'
source_file: 'gen4-main-quest-5.json'
video_id: 'PB4dyEF3PYc'
video_title: 'PokéFind New World (Main Quest 5: Generation 3)'
start:
  npc: 'Isaac'
  town: 'Ice Village'
  x: -182.5
  "y": 38.0
  z: 413.5
steps:
  - text: 'Walk around the town to find clues'
  - text: 'Meet Danielle in the biggest tower of Stronghaven'
    location:
      kind: 'npc'
      x: -182.5
      "y": 38.0
      z: 415.5
      label: 'Danielle'
      town: 'Ice Village'
  - text: 'Return to Isaac'
    location:
      kind: 'npc'
      x: -182.5
      "y": 38.0
      z: 413.5
      label: 'Isaac'
      town: 'Ice Village'
  - text: 'Go to the lake'
    location:
      kind: 'region'
      x: -147.5
      "y": 3.0
      z: 295.0
      bbox:
        x1: -180.0
        "y1": 1.0
        z1: 282.0
        x2: -115.0
        "y2": 5.0
        z2: 308.0
      town: 'Ice Village'
  - text: 'Look for signs of a human settlement in and around the lake'
  - text: 'Defeat the Team Cosmic Grunts'
    location:
      kind: 'battle'
      town: 'Ice Village'
    battles:
      - trainer: 'Cosmic Star Grunt'
        x: -166.5
        "y": 2.0
        z: 284.5
        town: 'Ice Village'
        team:
          - species: 'Toxicroak'
            level: 62
          - species: 'Machamp'
            level: 62
          - species: 'Purugly'
            level: 63
      - trainer: 'Cosmic Star Grunt'
        x: -144.5
        "y": 7.0
        z: 215.5
        town: 'Ice Village'
        team:
          - species: 'Poliwrath'
            level: 64
          - species: 'Honchkrow'
            level: 63
          - species: 'Medicham'
            level: 64
          - species: 'Lucario'
            level: 63
      - trainer: 'Cosmic Star Grunt'
        x: -57.5
        "y": 6.0
        z: 180.5
        town: 'Ice Village'
        team:
          - species: 'Probopass'
            level: 64
          - species: 'Heracross'
            level: 64
          - species: 'Breloom'
            level: 63
          - species: 'Toxicroak'
            level: 64
      - trainer: 'Cosmic Star Grunt'
        x: -54.5
        "y": 2.0
        z: 303.5
        town: 'Ice Village'
        team:
          - species: 'Hitmonchan'
            level: 64
          - species: 'Hitmonlee'
            level: 64
          - species: 'Hitmontop'
            level: 64
          - species: 'Hariyama'
            level: 64
  - text: 'Visit Professor Hemlock in the house next to his lab in Findville Cape'
    location:
      kind: 'npc'
      x: 769.5
      "y": 46.0
      z: 875.5
      label: 'Professor Hemlock'
      town: 'Ice Village'
    rewards:
      - '15 Tokens'
      - '80000 Trainer XP'
      - 'Damp_Rock'
---
