---
title: 'Gen 5 Intro'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_intro'
slug: 'gen5-intro'
description: 'Welcome to Zeinova'
source_file: 'gen5-intro.json'
video_id: 'RMZt4aYZM0k'
video_title: 'Welcome to PokéFind (Episode 1: Gen 5 Introduction)'
start:
  description: 'Triggers automatically when you arrive in Findale Harbor — no NPC required.'
steps:
  - text: 'Follow Professor Hemlock to his new lab'
    location:
      kind: 'npc'
      x: 569.5
      "y": 44.0
      z: 465.5
      label: 'Professor Hemlock'
      town: 'Findale Harbor'
  - text: 'Click your preferred starter!'
    location:
      kind: 'npc'
      x: 639.5
      "y": 52.0
      z: 415.5
      label: 'Bulbasaur'
      town: 'Findale Harbor'
    rewards:
      - 'Starter Pokémon'
      - 'pokégear'
  - text: 'Summon your Pokémon by pressing the drop button or right clicking'
    location:
      kind: 'destination'
      x: 636.5
      "y": 49.0
      z: 376.5
      town: 'Findale Harbor'
  - text: 'Talk to Danielle to start the battle'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: 636.5
        "y": 49.0
        z: 364.5
        town: 'Findale Harbor'
        team:
          - species: 'Oshawott'
            level: 1
    rewards:
      - '16× Poké Ball'
---
