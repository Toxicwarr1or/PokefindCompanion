---
title: 'Learning The Basics'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'learning_the_basics'
slug: 'learning-the-basics'
description: 'A trainer in Findville Cape seems to be having trouble learning how to battle. See if you can help her out!'
author: 'Cool51'
source_file: 'learning-the-basics.json'
start:
  npc: 'Dennies'
  x: 863.6
  "y": 43.0
  z: 853.4
steps:
  - text: 'Meet Dennies and her Chimchar outside of Findville Cape'
    location:
      kind: 'npc'
      x: 750.5
      "y": 43.0
      z: 858.5
      label: 'Dennies'
  - text: 'Battle Dennies'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Dennies'
        x: 750.5
        "y": 43.0
        z: 858.5
        team:
          - species: 'Chimchar'
            level: 13
  - text: 'Speak to Dennies'
    location:
      kind: 'npc'
      x: 750.5
      "y": 43.0
      z: 858.5
      label: 'Dennies'
    rewards:
      - '1000 Coins'
      - '5 Tokens'
      - '5000 Trainer XP'
---
