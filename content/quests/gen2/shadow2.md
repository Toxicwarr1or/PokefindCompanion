---
title: 'Shadow Quest 2'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'shadow2'
slug: 'shadow2'
description: 'Cipher has moved operations to Jataro in a secret base. It will be up to you to fight your way through his followers. This is your moment to stop Cipher once and for all!'
source_file: 'shadow2.json'
video_id: '3uBPavO-E3s'
video_title: 'PokeFind Shadow Quest 2'
start:
  npc: 'Michael'
  town: 'Rosolie City'
  x: -35.5
  "y": 76.0
  z: 438.5
steps:
  - text: 'Find Folly in Zephyrus Tower'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Reath'
        x: -29.5
        "y": 86.0
        z: 447.5
        town: 'Rosolie City'
        team:
          - species: 'Lapras'
            level: 80
          - species: 'Snorlax'
            level: 80
          - species: 'Kangaskhan'
            level: 80
          - species: 'Rhydon'
            level: 80
          - species: 'Tyranitar'
            level: 80
  - text: 'Find Reath in Zephyrus Tower'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Ferma'
        x: -36.5
        "y": 95.0
        z: 458.5
        town: 'Rosolie City'
        team:
          - species: 'Blastoise'
            level: 85
          - species: 'Feraligatr'
            level: 85
          - species: 'Lapras'
            level: 85
          - species: 'Gyarados'
            level: 85
          - species: 'Vaporeon'
            level: 85
          - species: 'Kingdra'
            level: 85
  - text: 'Find Ferma'
    location:
      kind: 'npc'
      x: -360.5
      "y": 78.0
      z: -488.5
      label: 'Sondra'
      town: 'Rosolie City'
  - text: 'Find Sondra in Rosolite City'
    location:
      kind: 'npc'
      x: -36.5
      "y": 95.0
      z: 458.5
      label: 'Ferma'
      town: 'Rosolite City'
  - text: 'Go back to Ferma in Zephyrus Tower'
    location:
      kind: 'npc'
      x: -36.5
      "y": 95.0
      z: 458.5
      label: 'Ferma'
      town: 'Rosolie City'
  - text: 'Enter the portal at the top of Zephyrus Tower'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Ein'
        x: -7.5
        "y": 41.0
        z: 447.5
        town: 'Rosolie City'
        team:
          - species: 'Eevee'
            level: 85
          - species: 'Vaporeon'
            level: 85
          - species: 'Flareon'
            level: 85
          - species: 'Jolteon'
            level: 85
          - species: 'Umbreon'
            level: 85
          - species: 'Espeon'
            level: 85
  - text: 'Find Ein in the Lab'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Venus'
        x: 13.5
        "y": 41.0
        z: 449.5
        town: 'Rosolie City'
        team:
          - species: 'Ampharos'
            level: 90
          - species: 'Lapras'
            level: 90
          - species: 'Raichu'
            level: 90
          - species: 'Jolteon'
            level: 90
  - text: 'Find Venus in the lab'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Dakim'
        x: -41.5
        "y": 48.0
        z: 473.5
        town: 'Rosolie City'
        team:
          - species: 'Scizor'
            level: 95
          - species: 'Exeggutor'
            level: 95
          - species: 'Meganium'
            level: 95
          - species: 'Venusaur'
            level: 95
          - species: 'Aerodactyl'
            level: 95
  - text: 'Find Dakim in the lab'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Nascour'
        x: -3.5
        "y": 41.0
        z: 478.5
        town: 'Rosolie City'
        team:
          - species: 'Ursaring'
            level: 95
          - species: 'Typhlosion'
            level: 95
          - species: 'Charizard'
            level: 95
          - species: 'Arcanine'
            level: 95
          - species: 'Flareon'
            level: 95
          - species: 'Houndoom'
            level: 95
  - text: 'Find Nascour in the lab'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Mirror B.'
        x: -9.5
        "y": 41.0
        z: 495.5
        town: 'Rosolie City'
        team:
          - species: 'Aerodactyl'
            level: 100
          - species: 'Umbreon'
            level: 100
          - species: 'Lapras'
            level: 100
          - species: 'Rhydon'
            level: 100
          - species: 'Charizard'
            level: 100
          - species: 'Espeon'
            level: 101
  - text: 'Find Mirror B. in the lab'
    location:
      kind: 'battle'
      town: 'Rosolie City'
    battles:
      - trainer: 'Cipher'
        x: -36.5
        "y": 41.0
        z: 436.5
        town: 'Rosolie City'
        team:
          - species: 'Alakazam'
            level: 101
          - species: 'Arcanine'
            level: 101
          - species: 'Snorlax'
            level: 101
          - species: 'Tyranitar'
            level: 101
          - species: 'Dragonite'
            level: 101
          - species: 'Lugia'
            level: 102
  - text: 'Find Cipher in the lab'
    location:
      kind: 'npc'
      x: -36.5
      "y": 41.0
      z: 436.5
      label: 'Cipher'
      town: 'Rosolie City'
---
