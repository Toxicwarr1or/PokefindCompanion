---
title: 'Fossil Frenzy'
date: 2026-04-28
layout: questguide
gen: 5
quest_key: 'gen5_fossil_frenzy'
slug: 'fossil-frenzy-main2'
description: 'Legend speaks of the existence of prehistoric fossils within Zeinova. Perhaps someone in Sandgate knows something about these old rocks.'
author: 'Toxicwarr1or'
source_file: 'fossil_frenzy_main2.json'
video_id: 'B-m8jCU-pxU'
video_title: 'PokeFind New Fossil Quest (Fossil Frenzy, Zeinova: Generation 5)'
start:
  npc: 'Archaeologist Phrank'
  description: 'Find Archaeologist Phrank in Sandgate'
  town: 'Sandgate'
  x: -1052.5
  "y": 37.0
  z: 245.5
steps:
  - text: 'Go to the bridge next to the excavation site.'
    location:
      kind: 'region'
      x: -1049.0
      "y": 57.5
      z: 289.0
      bbox:
        x1: -1058.0
        "y1": 43.0
        z1: 283.0
        x2: -1040.0
        "y2": 72.0
        z2: 295.0
      town: 'Sandgate'
  - text: 'Pickup a hard hat from the base of the crane.'
    location:
      kind: 'destination'
      x: -1033.5
      "y": 43.0
      z: 307.5
      town: 'Sandgate'
  - text: 'Make your way to the end of the bridge.'
    location:
      kind: 'region'
      x: -1047.5
      "y": 46.0
      z: 357.5
      bbox:
        x1: -1053.0
        "y1": 43.0
        z1: 350.0
        x2: -1042.0
        "y2": 49.0
        z2: 365.0
      town: 'Sandgate'
  - text: 'Have a water type Pokemon in your party.'
    location:
      kind: 'region'
      x: -1047.5
      "y": 46.0
      z: 357.5
      bbox:
        x1: -1053.0
        "y1": 43.0
        z1: 350.0
        x2: -1042.0
        "y2": 49.0
        z2: 365.0
      town: 'Sandgate'
  - text: 'Locate the Cover Fossil under the boat.'
    location:
      kind: 'destination'
      x: -1041.5
      "y": 17.0
      z: 472.5
      town: 'Sandgate'
  - text: 'Defeat the nearby water Pokemon.'
    location:
      kind: 'npc'
      x: -1045.5
      "y": 17.0
      z: 476.5
      label: 'Blastoise'
      town: 'Sandgate'
  - text: 'Return the hard hat to the construction worker on the bridge.'
    location:
      kind: 'npc'
      x: -1048.5
      "y": 45.0
      z: 292.5
      label: 'Construction Worker'
      town: 'Sandgate'
  - text: 'Battle Harrison.'
    location:
      kind: 'battle'
    battles:
      - trainer: 'Harrison'
        x: -1043.5
        "y": 46.0
        z: 283.5
        town: 'Sandgate'
        team:
          - species: 'Kabutops'
            level: 50
          - species: 'Omastar'
            level: 50
          - species: 'Cradily'
            level: 50
          - species: 'Armaldo'
            level: 50
          - species: 'Rampardos'
            level: 50
          - species: 'Bastiodon'
            level: 50
  - text: 'Report back to Archaeologist Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Make your way to the ''Town of Flight'''
    location:
      kind: 'region'
      x: 1034.0
      "y": 58.5
      z: 289.5
      bbox:
        x1: 925.0
        "y1": 39.0
        z1: 198.0
        x2: 1143.0
        "y2": 78.0
        z2: 381.0
      town: 'Breezelton Village'
  - text: 'Ask one of the denizens of Breezelton to see if any of them know of Phrank''s friend.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Go to Bridgerun and pick up the package of seeds. (Try looking outside the Pokemart)'
  - text: 'Take the road back to Breezelton to complete your delivery. (Hint: Make sure to take the road back)'
  - text: 'Find Mama Beth.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Catch a Pidove.'
  - text: 'Give the Pidove to Mama Beth.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Locate Twig in Greenholm.'
  - text: 'Find a tree near the Trainer Gym.'
  - text: 'Defeat the nearby grass/bug Pokemon.'
  - text: 'Mark the nearby tree.'
  - text: 'Return to Sarah.'
    location:
      kind: 'npc'
      x: 942.5
      "y": 42.0
      z: 291.5
      label: 'Sarah'
      town: 'Breezelton Village'
  - text: 'Find Laura in the building next to the Badge Gym.'
    location:
      kind: 'npc'
      x: 1053.5
      "y": 45.0
      z: 250.5
      label: 'Librarian Laura'
      town: 'Breezelton Village'
  - text: 'Battle Laura.'
    location:
      kind: 'npc'
      x: 1053.5
      "y": 45.0
      z: 250.5
      label: 'Librarian Laura'
      town: 'Breezelton Village'
  - text: 'Climb to the top of the mountain on the outskirts of Breezelton. (Hint: Follow the Redstone at the entrance of the cave.)'
    location:
      kind: 'destination'
      x: 951.0
      "y": 117.0
      z: 73.0
      town: 'Breezelton Village'
  - text: 'Battle the Flying type Pokemon.'
    location:
      kind: 'npc'
      x: 948.5
      "y": 117.0
      z: 69.5
      label: 'Fearow'
      town: 'Breezelton Village'
  - text: 'Head back to Sandgate to talk to Harrison. (Hint: He is at the top edge of the excavation site.)'
    location:
      kind: 'npc'
      x: -1040.5
      "y": 46.0
      z: 237.0
      label: 'Harrison'
      town: 'Sandgate'
    rewards:
      - 'Thick Club'
      - '35000 Trainer XP'
      - '50000 Coins'
      - '25 Tokens'
  - text: 'Return to Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Wait for Phrank to revive the fossil.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Return to Phrank to pick up your Tirtouga.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
    rewards:
      - 'Pokémon: Tirtouga (Lv 25)'
      - 'Pokémon: Tirtouga (Lv 25)'
      - 'Pokémon: Tirtouga (Lv 25)'
      - 'Pokémon: Tirtouga (Lv 25)'
  - text: 'Report back to Archaeologist Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Defeat 5 Ground or Rock type Pokemon for Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Return to Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Make your way to the ''Town of Flight'''
    location:
      kind: 'region'
      x: 1034.0
      "y": 58.5
      z: 289.5
      bbox:
        x1: 925.0
        "y1": 39.0
        z1: 198.0
        x2: 1143.0
        "y2": 78.0
        z2: 381.0
      town: 'Breezelton Village'
  - text: 'Ask one of the denizens of Breezelton to see if any of them know of Phrank''s friend.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Go to Bridgerun and pick up the package of seeds. (Try looking outside the Pokemart)'
  - text: 'Take the road back to Breezelton to complete your delivery. (Hint: Make sure to take the road back)'
  - text: 'Find Mama Beth.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Catch a Pidove.'
  - text: 'Give the Pidove to Mama Beth.'
    location:
      kind: 'npc'
      x: 969.5
      "y": 42.0
      z: 304.5
      label: 'Beth'
      town: 'Breezelton Village'
  - text: 'Locate Twig in Greenholm.'
  - text: 'Find a tree near the Trainer Gym.'
  - text: 'Defeat the nearby grass/bug Pokemon.'
  - text: 'Mark the nearby tree.'
  - text: 'Return to Sarah.'
    location:
      kind: 'npc'
      x: 942.5
      "y": 42.0
      z: 291.5
      label: 'Sarah'
      town: 'Breezelton Village'
  - text: 'Find Laura in the building next to the Badge Gym.'
    location:
      kind: 'npc'
      x: 1053.5
      "y": 45.0
      z: 250.5
      label: 'Librarian Laura'
      town: 'Breezelton Village'
  - text: 'Battle Laura.'
    location:
      kind: 'npc'
      x: 1053.5
      "y": 45.0
      z: 250.5
      label: 'Librarian Laura'
      town: 'Breezelton Village'
  - text: 'Climb to the top of the mountain on the outskirts of Breezelton. (Hint: Follow the Redstone at the entrance of the cave.)'
    location:
      kind: 'destination'
      x: 951.0
      "y": 117.0
      z: 73.0
      town: 'Breezelton Village'
  - text: 'Battle the Flying type Pokemon.'
    location:
      kind: 'npc'
      x: 948.5
      "y": 117.0
      z: 69.5
      label: 'Fearow'
      town: 'Breezelton Village'
  - text: 'Head back to Sandgate and find Harrison. (Hint: He is at the top edge of the excavation site.)'
    location:
      kind: 'npc'
      x: -1040.5
      "y": 46.0
      z: 237.0
      label: 'Harrison'
      town: 'Sandgate'
    rewards:
      - 'Thick Club'
      - '35000 Trainer XP'
      - '50000 Coins'
      - '25 Tokens'
  - text: 'Return to Phrank.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Wait for Phrank to revive the fossil.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
  - text: 'Return to Phrank to pick up your Archen.'
    location:
      kind: 'npc'
      x: -1052.5
      "y": 37.0
      z: 245.5
      label: 'Archaeologist Phrank'
      town: 'Sandgate'
    rewards:
      - 'Pokémon: Archen (Lv 25)'
      - 'Pokémon: Archen (Lv 25)'
---
