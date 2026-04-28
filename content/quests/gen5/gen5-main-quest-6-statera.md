---
title: 'Main Quest 6 - Tasks Of A Newbie'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_main_quest_6_statera'
slug: 'gen5-main-quest-6-statera'
description: 'Being the new one isn''t always easy but there is no other option. Statera needs you!'
author: 'Mmaarten'
source_file: 'gen5-main-quest-6-statera.json'
video_id: 'VGaAQuHXty4'
video_title: 'Tasks For A Newbie (Episode 17: Main Quest 6 - Statera)'
start:
  npc: 'Jeff'
  description: 'H.A.P.P.Y. in Watterson City'
  town: 'Watterson City'
  x: 76.5
  "y": 61.0
  z: 347.5
steps:
  - text: 'Talk to the Statera Members on the first floor'
    location:
      kind: 'npc'
      x: 76.5
      "y": 61.0
      z: 347.5
      label: 'Jeff'
      town: 'Watterson City'
  - text: 'Pick up the super secret delivery from the farmer in Findale Harbor'
    location:
      kind: 'destination'
      x: 535.5
      "y": 55.0
      z: 545.5
      label: 'Pick up the super secret delivery from the farmer in Findale Harbor'
      town: 'Findale Harbor'
  - text: 'Return the package to Jeff at the Statera HQ'
    location:
      kind: 'npc'
      x: 76.5
      "y": 61.0
      z: 347.5
      label: 'Jeff'
      town: 'Watterson City'
  - text: 'Speak to Mark'
    location:
      kind: 'npc'
      x: 73.5
      "y": 61.0
      z: 346.5
      label: 'Mark'
      town: 'Watterson City'
  - text: 'Collect a small sample of obsidian from the lava fountain in Redgrove'
    location:
      kind: 'destination'
      x: -567.5
      "y": 51.0
      z: 874.5
      label: 'Head to the lava fountain in Redgrove'
      town: 'Redgrove'
  - text: 'Pick up the obsidian sample at the top of the fountain'
    location:
      kind: 'destination'
      x: -558.5
      "y": 67.5
      z: 874.5
      town: 'Redgrove'
  - text: 'Bring the obsidian sample back to Mark at Statera HQ'
    location:
      kind: 'npc'
      x: 73.5
      "y": 61.0
      z: 346.5
      label: 'Mark'
      town: 'Watterson City'
  - text: 'Check up on Evan'
    location:
      kind: 'npc'
      x: 71.5
      "y": 61.0
      z: 345.5
      label: 'Evan'
      town: 'Watterson City'
  - text: 'Collect the report from the field agent in Findale Harbor'
    location:
      kind: 'destination'
      x: 615.5
      "y": 50.0
      z: 596.5
      label: 'Collect the report from the field agent in Findale Harbor'
      town: 'Findale Harbor'
  - text: 'Bring a Pidgeotto to Grandma Lucy'
    location:
      kind: 'npc'
      x: 615.5
      "y": 50.0
      z: 596.5
      label: 'Grandma Lucy'
      town: 'Findale Harbor'
  - text: 'Make sure Evan received the recipe at Statera HQ'
    location:
      kind: 'npc'
      x: 71.5
      "y": 61.0
      z: 345.5
      label: 'Evan'
      town: 'Watterson City'
  - text: 'Ask Steven why he asked about you'
    location:
      kind: 'npc'
      x: 72.5
      "y": 61.0
      z: 335.5
      label: 'Steven'
      town: 'Watterson City'
  - text: 'Find a Lily of the Valley in the garden in Findale Harbor (HINT> It''s near /spawn)'
    location:
      kind: 'destination'
      x: 589.5
      "y": 53.0
      z: 573.5
      label: 'Find a Lily of the Valley near spawn in Findale Harbor'
      town: 'Findale Harbor'
  - text: 'Bring the rare Lily of the Valley back to Steven at Statera HQ'
    location:
      kind: 'npc'
      x: 72.5
      "y": 61.0
      z: 335.5
      label: 'Steven'
      town: 'Watterson City'
    rewards:
      - 'lily_of_the_valley'
  - text: 'Travel back to the Ancient Temple in Greenholm to catch Zekrom'
    location:
      kind: 'destination'
      x: -498.5
      "y": 73.0
      z: 39.5
      label: 'Travel back to the Ancient Temple in Greenholm'
      town: 'Greenholm'
  - text: 'Prove your worth by battling the first Guardian'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Guardian 1'
        x: -424.5
        "y": 33.0
        z: 52.5
        town: 'Greenholm'
        team:
          - species: 'Scolipede'
            level: 62
          - species: 'Bisharp'
            level: 62
          - species: 'Liepard'
            level: 65
  - text: 'Collect the first key shard'
    location:
      kind: 'destination'
      x: -424.5
      "y": 36.0
      z: 35.5
      town: 'Greenholm'
  - text: 'Battle the second Guardian'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Guardian 2'
        x: -424.5
        "y": 33.0
        z: 66.5
        town: 'Greenholm'
        team:
          - species: 'Banette'
            level: 61
          - species: 'Accelgor'
            level: 63
          - species: 'Absol'
            level: 65
  - text: 'Collect the second key shard'
    location:
      kind: 'destination'
      x: -424.5
      "y": 36.0
      z: 83.5
      town: 'Greenholm'
  - text: 'Proceed to the next room to unlock the door'
    location:
      kind: 'region'
      x: -402.0
      "y": 36.0
      z: 59.0
      bbox:
        x1: -407.0
        "y1": 31.0
        z1: 50.0
        x2: -397.0
        "y2": 41.0
        z2: 68.0
      town: 'Greenholm'
  - text: 'Proceed to the end of the Ancient Temple'
    location:
      kind: 'region'
      x: -345.0
      "y": 25.5
      z: 59.5
      bbox:
        x1: -354.0
        "y1": 1.0
        z1: 33.0
        x2: -336.0
        "y2": 50.0
        z2: 86.0
      town: 'Greenholm'
  - text: 'Battle Danielle'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Danielle'
        x: -327.5
        "y": 33.0
        z: 59.5
        town: 'Greenholm'
        team:
          - species: 'Liepard'
            level: 65
          - species: 'Unfezant'
            level: 65
          - species: 'Haxorus'
            level: 65
          - species: 'Gigalith'
            level: 65
          - species: 'Simipour'
            level: 65
          - species: 'Emboar'
            level: 67
  - text: 'Pick up the masterball with Zekrom inside'
    location:
      kind: 'destination'
      x: -313.5
      "y": 36.0
      z: 59.5
      town: 'Greenholm'
  - text: 'Bring Zekrom to the Statera Leader'
    location:
      kind: 'destination'
      x: 78.5
      "y": 61.0
      z: 337.5
      label: 'Bring Zekrom to Vidar at Statera HQ'
      town: 'Watterson City'
    rewards:
      - '35000 Coins'
      - '35 Tokens'
      - '40000 Trainer XP'
      - '20× material'
      - 'Thunder Stone'
      - 'Fire Stone'
      - 'Leaf Stone'
      - 'Water Stone'
      - 'Dawn Stone'
      - 'Moon Stone'
      - 'Dusk Stone'
      - 'Shiny Stone'
      - 'Sun Stone'
      - 'Grassy Seed'
      - 'Misty Seed'
      - 'Electric Seed'
      - 'Psychic Seed'
---
