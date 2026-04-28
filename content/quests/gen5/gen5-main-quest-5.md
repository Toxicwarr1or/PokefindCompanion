---
title: 'Main Quest 5 - The Choice Of A Lifetime'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_5'
slug: 'gen5-main-quest-5'
description: 'Making choices is hard. But this choice might be just a little bit harder. Does it define who I am? Who I want to be? ...'
author: 'Mmaarten'
source_file: 'gen5-main-quest-5.json'
video_id: 'Zlsqfla-4_A'
video_title: 'A Choice Of A Lifetime (Episode 15: Main Quest 5 - Sophro)'
start:
  npc: 'Danielle'
  description: 'Danielle just outside Greenholm'
  town: 'Greenholm'
  x: -310.5
  "y": 47.0
  z: -13.5
steps:
  - text: 'Battle Danielle'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: -310.5
        "y": 47.0
        z: -13.5
        town: 'Greenholm'
        team:
          - species: 'Emboar'
            level: 60
          - species: 'Haxorus'
            level: 59
          - species: 'Gigalith'
            level: 58
          - species: 'Unfezant'
            level: 58
          - species: 'Simisage'
            level: 60
          - species: 'Liepard'
            level: 59
  - text: 'Meet the Captain at the Ancient Temple in Greenholm and speak to him'
    location:
      kind: 'destination'
      x: -499.5
      "y": 66.0
      z: 24.5
      label: 'Go to the Ancient Temple in Greenholm'
      town: 'Greenholm'
  - text: 'Investigate the Ancient Door'
    location:
      kind: 'region'
      x: -499.0
      "y": 78.0
      z: 39.0
      bbox:
        x1: -502.0
        "y1": 73.0
        z1: 37.0
        x2: -496.0
        "y2": 83.0
        z2: 41.0
      town: 'Greenholm'
  - text: 'Find batteries somewhere in Greenholm'
    location:
      kind: 'destination'
      x: -497.5
      "y": 59.2
      z: -44.5
      town: 'Greenholm'
  - text: 'Return to the Ancient Temple'
    location:
      kind: 'destination'
      x: -499.5
      "y": 66.0
      z: 24.5
      label: 'Return to the Ancient Temple in Greenholm'
      town: 'Greenholm'
  - text: 'Guide the Sewaddle to the rose bush'
    location:
      kind: 'npc'
      x: -498.5
      "y": 72.0
      z: 46.5
      label: 'Sewaddle'
      town: 'Greenholm'
  - text: 'Explore further into the Ancient Temple'
    location:
      kind: 'region'
      x: -503.0
      "y": 62.0
      z: 56.0
      bbox:
        x1: -505.0
        "y1": 60.0
        z1: 54.0
        x2: -501.0
        "y2": 64.0
        z2: 58.0
      town: 'Greenholm'
  - text: 'Battle Astrid'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Astrid'
        x: -502.5
        "y": 60.0
        z: 46.5
        town: 'Greenholm'
        team:
          - species: 'Samurott'
            level: 58
          - species: 'Musharna'
            level: 59
          - species: 'Mandibuzz'
            level: 60
          - species: 'Lilligant'
            level: 60
          - species: 'Jellicent'
            level: 59
          - species: 'Gothitelle'
            level: 60
  - text: 'Meet Astrid in the next room'
    location:
      kind: 'npc'
      x: -502.5
      "y": 60.0
      z: 46.5
      label: 'Astrid'
      town: 'Greenholm'
  - text: 'Choose which side you want to be on. Click the NPC with the side you want to join'
    location:
      kind: 'npc'
      x: -500.5
      "y": 37.0
      z: 60.5
      label: 'Vidar'
      town: 'Greenholm'
  - text: 'Talk with Vidar outside the temple'
    location:
      kind: 'npc'
      x: -498.5
      "y": 64.0
      z: -4.1
      label: 'Vidar'
      town: 'Greenholm'
  - text: 'Talk with Astrid'
    location:
      kind: 'npc'
      x: -507.0
      "y": 37.0
      z: 59.9
      label: 'Astrid'
      town: 'Greenholm'
    rewards:
      - '30000 Coins'
      - '25 Tokens'
      - '30000 Trainer XP'
      - '5× material'
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
