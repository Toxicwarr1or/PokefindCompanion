---
title: 'Meteor Discovery'
date: 2026-04-28
layout: questguide
gen: 3
quest_key: 'meteor_discovery'
slug: 'meteor-discovery'
description: 'Talk to Lisa at the Observatory, seems like something big has happened!'
source_file: 'meteor-discovery.json'
start:
  npc: 'Lisa'
  town: 'Kinetic Island'
  x: 1482.0
  "y": 78.0
  z: -610.2
steps:
  - text: 'Meet Scientist Lisa in Occult Island'
    location:
      kind: 'npc'
      x: 1721.9
      "y": 27.0
      z: 121.2
      label: 'Lisa'
      town: 'Occult Island'
  - text: 'Retrieve Lisa''s Poké Gear from behind the Gym'
    location:
      kind: 'npc'
      x: 1482.0
      "y": 78.0
      z: -610.2
      label: 'Lisa'
      town: 'Kinetic Island'
  - text: 'Return the Poké Gear to Lisa'
    location:
      kind: 'npc'
      x: 1721.9
      "y": 27.0
      z: 121.2
      label: 'Lisa'
      town: 'Kinetic Island'
  - text: 'Meet Lisa at the desert north of Stoneridge.'
    location:
      kind: 'npc'
      x: -1219.5
      "y": 53.0
      z: -459.5
      label: 'Lisa'
      town: 'Kinetic Island'
    rewards:
      - '25000 Coins'
      - '10 Tokens'
      - '9500 Trainer XP'
---
