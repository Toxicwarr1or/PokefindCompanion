---
title: 'Embrace the Shadows'
date: 2026-04-28
layout: questguide
gen: 4
quest_key: 'shadow_quest_5'
slug: 'shadow-quest-5'
description: 'You walk past a cave in Duskburn when you hear a weird noise coming from the inside. Little did you know that your curiosity would lead to your most cursed adventure yet...'
source_file: 'shadow-quest-5.json'
start:
  npc: 'Cipher'
  town: 'Underwater Temple'
  x: -1678.5
  "y": 32.0
  z: 498.5
steps:
  - text: 'Investigate the nearby cave'
    location:
      kind: 'region'
      x: -582.0
      "y": 25.0
      z: 663.0
      bbox:
        x1: -584.0
        "y1": 21.0
        z1: 660.0
        x2: -580.0
        "y2": 29.0
        z2: 666.0
      town: 'Underwater Temple'
  - text: 'Make sure you have space in your party or pc. Talk to Cipher in the HQ when you are ready.'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Scientist Lisa in the lab across the hall in the HQ'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Return to Cipher'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to HM Tutor at the Pokémon League to learn HM 07 Dive'
    location:
      kind: 'region'
      x: 655.5
      "y": 58.0
      z: -280.0
      bbox:
        x1: 538.0
        "y1": 20.0
        z1: -359.0
        x2: 773.0
        "y2": 96.0
        z2: -201.0
      town: 'Underwater Temple'
  - text: 'Head to Seabrooke after you have taught Dive to a Pokémon'
    location:
      kind: 'region'
      x: 729.0
      "y": 25.5
      z: -288.5
      bbox:
        x1: 691.0
        "y1": 16.0
        z1: -333.0
        x2: 767.0
        "y2": 35.0
        z2: -244.0
      town: 'Underwater Temple'
  - text: 'Look for signs of an underwater temple in Seabrooke'
    location:
      kind: 'npc'
      x: 540.5
      "y": 18.0
      z: 1615.5
      label: 'Temple Guardian'
      town: 'Underwater Temple'
  - text: 'Investigate the lake'
    location:
      kind: 'region'
      x: 352.0
      "y": 45.0
      z: 1610.0
      bbox:
        x1: 347.0
        "y1": 40.0
        z1: 1605.0
        x2: 357.0
        "y2": 50.0
        z2: 1615.0
      town: 'Underwater Temple'
  - text: 'Dive to the Underwater Caves'
    location:
      kind: 'region'
      x: 523.0
      "y": 21.0
      z: 1610.0
      bbox:
        x1: 518.0
        "y1": 15.0
        z1: 1607.0
        x2: 528.0
        "y2": 27.0
        z2: 1613.0
      town: 'Underwater Temple'
  - text: 'Find the Underwater Temple'
    location:
      kind: 'npc'
      x: 540.5
      "y": 18.0
      z: 1615.5
      label: 'Temple Guardian'
      town: 'Underwater Temple'
  - text: 'Quickly find a place to hide'
    location:
      kind: 'npc'
      x: 975.45
      "y": 19.0
      z: 1610.5
      label: 'orb1'
      town: 'Underwater Temple'
  - text: 'Find a way past the guards and pick up the Orb.'
    location:
      kind: 'destination'
      x: 1.0
      "y": 963.5
      z: 17.0
      town: 'Underwater Temple'
  - text: 'Defeat the Temple Guardian and get out of the temple'
    location:
      kind: 'npc'
      x: 540.5
      "y": 18.0
      z: 1615.5
      label: 'Temple Guardian'
      town: 'Underwater Temple'
  - text: 'Defeat Danielle and head back to the HQ'
    location:
      kind: 'npc'
      x: -1647.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Return to Cipher'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Find the forgotten castle in the outskirts of Silverkeep'
    location:
      kind: 'npc'
      x: -1194.5
      "y": 25.0
      z: 321.5
      label: 'Castle Guard'
      town: 'Underwater Temple'
  - text: 'Defeat the castle guardians'
    location:
      kind: 'npc'
      x: -1194.5
      "y": 25.0
      z: 321.5
      label: 'Castle Guard'
      town: 'Underwater Temple'
  - text: 'Defeat the remaining Castle Guardians'
    location:
      kind: 'npc'
      x: -1485.55
      "y": 11.0
      z: -195.5
      label: 'orb2'
      town: 'Underwater Temple'
  - text: 'Return to Cipher in the HQ'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Reach the entrance of The Hall Of Origin'
    location:
      kind: 'npc'
      x: 383.5
      "y": 45.0
      z: -819.5
      label: 'pedestal3'
      town: 'Underwater Temple'
  - text: 'Place the Orbs on the statues'
    location:
      kind: 'region'
      x: 358.0
      "y": 26.0
      z: -23.5
      bbox:
        x1: 320.0
        "y1": 4.0
        z1: -59.0
        x2: 396.0
        "y2": 48.0
        z2: 12.0
      town: 'Underwater Temple'
  - text: 'Enter The Hall Of Origin'
  - text: 'Break the seals and reach the top floor of The Hall Of Origin'
    location:
      kind: 'region'
      x: 356.0
      "y": 29.5
      z: -59.0
      bbox:
        x1: 353.0
        "y1": 24.0
        z1: -62.0
        x2: 359.0
        "y2": 35.0
        z2: -56.0
      town: 'Underwater Temple'
  - text: 'Defeat Cynthia and catch Arceus'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Go to the Shadow HQ and talk to Cipher'
    location:
      kind: 'npc'
      x: -1647.5
      "y": 32.0
      z: 524.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Cipher'
    location:
      kind: 'npc'
      x: -2410.5
      "y": 25.0
      z: 398.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Cipher'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Go to Marshbarrow'
  - text: 'Catch a Shadow Pokémon'
    location:
      kind: 'npc'
      x: -1651.5
      "y": 32.0
      z: 426.5
      label: 'Shadow Guard'
      town: 'Underwater Temple'
  - text: 'Defeat Michael and go back to the Shadow HQ'
    location:
      kind: 'npc'
      x: -1654.5
      "y": 32.0
      z: 459.5
      label: 'Scientist Lisa'
      town: 'Underwater Temple'
  - text: 'Give the caught Shadow to Scientist Lisa'
    location:
      kind: 'npc'
      x: -1647.5
      "y": 32.0
      z: 524.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Cipher'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Go to the Crystal View Castle'
    location:
      kind: 'npc'
      x: -1194.5
      "y": 25.0
      z: 321.5
      label: 'Castle Guard'
      town: 'Crystal View Castle'
  - text: 'Defeat the old man and enter Crystal View Castle'
    location:
      kind: 'npc'
      x: 208.5
      "y": 60.0
      z: 455.5
      label: 'Old Man'
      town: 'Crystal View Castle'
  - text: 'Go to Findville Cape'
    location:
      kind: 'npc'
      x: 768.5
      "y": 46.0
      z: 875.5
      label: 'Professor Hemlock'
      town: 'Underwater Temple'
  - text: 'Find Professor Hemlock and Michael'
    location:
      kind: 'npc'
      x: 208.5
      "y": 60.0
      z: 440.5
      label: 'Professor Hemlock'
      town: 'Underwater Temple'
  - text: 'Go to the docks in front of the Shadow HQ'
    location:
      kind: 'npc'
      x: -1651.5
      "y": 32.0
      z: 426.5
      label: 'Shadow Guard'
      town: 'Underwater Temple'
  - text: 'Search for an accessible vent around the HQ'
    location:
      kind: 'region'
      x: -1647.5
      "y": 38.5
      z: 426.0
      bbox:
        x1: -1653.0
        "y1": 31.0
        z1: 419.0
        x2: -1642.0
        "y2": 46.0
        z2: 433.0
      town: 'Underwater Temple'
  - text: 'Enter the HQ'
    location:
      kind: 'npc'
      x: -1597.5
      "y": 22.0
      z: 545.5
      label: 'Michael'
      town: 'Underwater Temple'
  - text: 'Find Michael in the vents in the HQ'
    location:
      kind: 'npc'
      x: -2410.5
      "y": 25.0
      z: 398.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Cipher in the main lab'
    location:
      kind: 'npc'
      x: -1678.5
      "y": 32.0
      z: 498.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Go to the Main Power Room'
  - text: 'Electrocute the Main Power Supply'
    location:
      kind: 'destination'
      x: 2.0
      "y": -1618.0
      z: 32.0
      town: 'Underwater Temple'
  - text: 'Defeat the Shadow Guard and exit the room'
    location:
      kind: 'npc'
      x: -1651.5
      "y": 32.0
      z: 426.5
      label: 'Shadow Guard'
      town: 'Underwater Temple'
  - text: 'Head to the main lab'
  - text: 'Defeat the Shadow Admins and stop the lockdown'
    location:
      kind: 'npc'
      x: -1651.5
      "y": 32.0
      z: 426.5
      label: 'Shadow Guard'
      town: 'Underwater Temple'
  - text: 'Put the code in the keypad'
    location:
      kind: 'npc'
      x: -2410.5
      "y": 25.0
      z: 398.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Talk to Cipher'
    location:
      kind: 'npc'
      x: -1649.5
      "y": 27.0
      z: 303.5
      label: 'Michael'
      town: 'Underwater Temple'
  - text: 'Head back to the docks in front of the HQ and talk to michael'
    location:
      kind: 'npc'
      x: 208.5
      "y": 60.0
      z: 454.5
      label: 'Cipher'
      town: 'Underwater Temple'
  - text: 'Confront Cipher in Crystal View'
    location:
      kind: 'battle'
      town: 'Underwater Temple'
    battles:
      - trainer: 'Cipher'
        x: 208.5
        "y": 60.0
        z: 454.5
        town: 'Underwater Temple'
        team:
          - species: 'Lugia'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Mewtwo'
            level: 100
          - species: 'Garchomp'
            level: 100
          - species: 'Arceus'
            level: 100
---
