---
title: 'Northern Winds> Click to Start'
date: 2026-04-28
layout: questguide
gen: 2
quest_key: 'northern_winds'
slug: 'northern-winds'
description: 'A run in with a Pokémon Researcher leads you on a journey to find Legendary Pokémon.'
source_file: 'northern-winds.json'
start:
  npc: 'Eusine'
  town: 'Windfall Town'
  x: 554.5
  "y": 70.0
  z: 412.5
steps:
  - text: 'Meet with Eusine in Waitomo'
    location:
      kind: 'npc'
      x: -1154.5
      "y": 100.0
      z: 697.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Battle Parsin'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Parsin'
        x: -1154.5
        "y": 100.0
        z: 700.5
        town: 'Windfall Town'
        team:
          - species: 'Donphan'
            level: 100
          - species: 'Raticate'
            level: 100
          - species: 'Rampardos'
            level: 100
          - species: 'Dusclops'
            level: 100
          - species: 'Machamp'
            level: 100
  - text: 'Go and investigate Waitomo Cave'
    location:
      kind: 'region'
      x: -1197.0
      "y": 95.5
      z: 670.5
      bbox:
        x1: -1204.0
        "y1": 87.0
        z1: 662.0
        x2: -1190.0
        "y2": 104.0
        z2: 679.0
      town: 'Waitomo Cave'
  - text: 'Investigate the cave further'
    location:
      kind: 'region'
      x: -1237.5
      "y": 63.5
      z: 714.5
      bbox:
        x1: -1246.0
        "y1": 60.0
        z1: 708.0
        x2: -1229.0
        "y2": 67.0
        z2: 721.0
      town: 'Windfall Town'
  - text: 'Defeat the wild Pokémon'
    location:
      kind: 'npc'
      x: -1240.5
      "y": 63.0
      z: 707.5
      label: 'Noctowl'
      town: 'Windfall Town'
  - text: 'Pick up the crystal object'
    location:
      kind: 'npc'
      x: 86.5
      "y": 71.0
      z: -162.5
      label: 'Crystal'
      town: 'Windfall Town'
  - text: 'Head out of the cavern and talk to Eusine'
    location:
      kind: 'npc'
      x: -1183.5
      "y": 99.9375
      z: 675.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Talk to Parsin about the crystal object'
    location:
      kind: 'npc'
      x: -1154.5
      "y": 100.0
      z: 700.5
      label: 'Parsin'
      town: 'Windfall Town'
  - text: 'Find Eusine in Rosolite City'
    location:
      kind: 'npc'
      x: -365.5
      "y": 78.5
      z: -444.5
      label: 'Eusine'
      town: 'Rosolite City'
  - text: 'See if anyone near the entrance of Rosolite City knows where Monae is'
    location:
      kind: 'battle'
      town: 'Rosolite City'
    battles:
      - trainer: 'Marques'
        x: -308.5
        "y": 78.0
        z: -398.5
        town: 'Rosolite City'
        team:
          - species: 'Alakazam'
            level: 100
          - species: 'Slowbro'
            level: 100
          - species: 'Porygon2'
            level: 100
          - species: 'Scizor'
            level: 100
          - species: 'Slowking'
            level: 100
          - species: 'Ditto'
            level: 100
  - text: 'Find Earvin by the Pokémart'
    location:
      kind: 'npc'
      x: -239.5
      "y": 75.0
      z: -434.5
      label: 'Earvin'
      town: 'Windfall Town'
  - text: 'Catch a Misdreavus and give it to Earvin'
    location:
      kind: 'npc'
      x: -239.5
      "y": 75.0
      z: -434.5
      label: 'Earvin'
      town: 'Windfall Town'
  - text: 'Battle Earvin'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Earvin'
        x: -239.5
        "y": 75.0
        z: -434.5
        town: 'Windfall Town'
        team:
          - species: 'Hitmonchan'
            level: 100
          - species: 'Primeape'
            level: 100
          - species: 'Heracross'
            level: 100
          - species: 'Machamp'
            level: 100
          - species: 'Hitmontop'
            level: 100
          - species: 'Misdreavus'
            level: 100
  - text: 'Find Monae down at the Rosolite Docks'
    location:
      kind: 'npc'
      x: -272.5
      "y": 66.0
      z: -514.5
      label: 'Monae'
      town: 'Windfall Town'
  - text: 'Talk to Cazel on his boat'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Cazel'
        x: -249.5
        "y": 65.0
        z: -524.5
        town: 'Windfall Town'
        team:
          - species: 'Masquerain'
            level: 100
          - species: 'Golem'
            level: 100
          - species: 'Snorlax'
            level: 100
          - species: 'Gengar'
            level: 100
          - species: 'Vaporeon'
            level: 100
          - species: 'Chansey'
            level: 100
  - text: 'Talk to Monae again'
    location:
      kind: 'npc'
      x: -269.5
      "y": 66.0
      z: -516.5
      label: 'Monae'
      town: 'Windfall Town'
  - text: 'Battle Monae'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Monae'
        x: -269.5
        "y": 66.0
        z: -516.5
        town: 'Windfall Town'
        team:
          - species: 'Pelipper'
            level: 100
          - species: 'Feraligatr'
            level: 100
          - species: 'Gorebyss'
            level: 100
          - species: 'Mantine'
            level: 100
          - species: 'Quagsire'
            level: 100
          - species: 'Gyarados'
            level: 100
  - text: 'Go back to Crystal''s house in Rosolite City and talk to Eusine'
    location:
      kind: 'npc'
      x: -365.5
      "y": 78.5
      z: -444.5
      label: 'Eusine'
      town: 'Rosolite City'
  - text: 'Find Crystal at Misty Lake'
    location:
      kind: 'npc'
      x: 86.5
      "y": 71.0
      z: -162.5
      label: 'Crystal'
      town: 'Misty Lake'
  - text: 'Talk to Crystal'
    location:
      kind: 'npc'
      x: 86.5
      "y": 71.0
      z: -162.5
      label: 'Crystal'
      town: 'Windfall Town'
  - text: 'Battle Crystal'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Crystal'
        x: 86.5
        "y": 71.0
        z: -162.5
        town: 'Windfall Town'
        team:
          - species: 'Arcanine'
            level: 100
          - species: 'Shedinja'
            level: 100
          - species: 'Alakazam'
            level: 100
          - species: 'Blissey'
            level: 100
          - species: 'Hitmonchan'
            level: 100
          - species: 'Metagross'
            level: 100
  - text: 'Head to Mt. Iron Temple'
    location:
      kind: 'npc'
      x: 1091.5
      "y": 79.0
      z: 377.5
      label: 'Temple Monk'
      town: 'Iron Temple'
  - text: 'Make your way inside the temple'
    location:
      kind: 'npc'
      x: 1091.5
      "y": 79.0
      z: 377.5
      label: 'Temple Monk'
      town: 'Windfall Town'
  - text: 'Battle the first Temple Monk'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Temple Monk'
        x: 963.5
        "y": 110.0
        z: 326.5
        town: 'Windfall Town'
        team:
          - species: 'Golem'
            level: 100
          - species: 'Aerodactyl'
            level: 100
          - species: 'Quagsire'
            level: 100
          - species: 'Onix'
            level: 100
          - species: 'Sandslash'
            level: 100
          - species: 'Donphan'
            level: 100
  - text: 'Battle the second Temple Monk'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Temple Monk'
        x: 965.5
        "y": 110.0
        z: 326.5
        town: 'Windfall Town'
        team:
          - species: 'Skarmory'
            level: 100
          - species: 'Magnezone'
            level: 100
          - species: 'Alolan_Sandslash'
            level: 100
          - species: 'Steelix'
            level: 100
          - species: 'Alolan_Dugtrio'
            level: 100
          - species: 'Scizor'
            level: 100
  - text: 'Speak to the Temple Elder'
    location:
      kind: 'npc'
      x: 964.5
      "y": 107.0
      z: 320.5
      label: 'Meganu'
      town: 'Windfall Town'
  - text: 'Follow Meganu'
    location:
      kind: 'npc'
      x: 964.5
      "y": 107.0
      z: 320.5
      label: 'Meganu'
      town: 'Windfall Town'
  - text: 'Speak with Eusine'
    location:
      kind: 'npc'
      x: 964.5
      "y": 110.0
      z: 332.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Climb down the stairs on the other side of the door into the labyrinth'
    location:
      kind: 'region'
      x: 945.5
      "y": 77.5
      z: 301.0
      bbox:
        x1: 944.0
        "y1": 75.0
        z1: 300.0
        x2: 947.0
        "y2": 80.0
        z2: 302.0
      town: 'Windfall Town'
  - text: 'Make your way through the labyrinth and defeat any Pokémon you discover'
    location:
      kind: 'npc'
      x: 980.5
      "y": 76.0
      z: 264.5
      label: 'Steelix'
      town: 'Windfall Town'
  - text: 'Continue through the labyrinth and defeat any Pokémon you discover'
    location:
      kind: 'npc'
      x: 959.5
      "y": 76.0
      z: 333.5
      label: 'Scizor'
      town: 'Windfall Town'
  - text: 'Continue through the labyrinth and defeat any Pokémon you discover'
    location:
      kind: 'npc'
      x: 1022.5
      "y": 76.0
      z: 254.5
      label: 'Aggron'
      town: 'Windfall Town'
  - text: 'Continue through the labyrinth and defeat any Pokémon you discover'
    location:
      kind: 'npc'
      x: 997.5
      "y": 76.0
      z: 321.5
      label: 'Metagross'
      town: 'Windfall Town'
  - text: 'Continue through the labyrinth and defeat any Pokémon you discover'
    location:
      kind: 'npc'
      x: 1027.5
      "y": 76.0
      z: 319.5
      label: 'Registeel'
      town: 'Windfall Town'
  - text: 'Enter the newly discovered room'
    location:
      kind: 'region'
      x: 1027.0
      "y": 78.0
      z: 316.5
      bbox:
        x1: 1026.0
        "y1": 76.0
        z1: 316.0
        x2: 1028.0
        "y2": 80.0
        z2: 317.0
      town: 'Windfall Town'
  - text: 'Pick up the Crystal Object'
    location:
      kind: 'npc'
      x: 86.5
      "y": 71.0
      z: -162.5
      label: 'Crystal'
      town: 'Windfall Town'
  - text: 'Find Eusine at the Burnt Tower in Eerie City'
    location:
      kind: 'npc'
      x: -310.5
      "y": 81.0
      z: 10.5
      label: 'Eusine'
      town: 'Eerie City'
  - text: 'Follow Eusine into the Burnt Tower'
    location:
      kind: 'npc'
      x: 554.5
      "y": 70.0
      z: 412.5
      label: 'Eusine'
      town: 'Windfall Town'
  - text: 'Battle Morty'
    location:
      kind: 'battle'
      town: 'Windfall Town'
    battles:
      - trainer: 'Morty'
        x: -337.5
        "y": 97.0
        z: 0.5
        town: 'Windfall Town'
        team:
          - species: 'Gengar'
            level: 100
          - species: 'Weavile'
            level: 100
          - species: 'Gengar'
            level: 100
          - species: 'Sableye'
            level: 100
          - species: 'Dusclops'
            level: 100
          - species: 'Kyoto Gengar'
            level: 100
  - text: 'Climb to the top of the Burnt Tower'
    location:
      kind: 'region'
      x: -343.0
      "y": 102.0
      z: 0.0
      bbox:
        x1: -343.0
        "y1": 99.0
        z1: -2.0
        x2: -343.0
        "y2": 105.0
        z2: 2.0
      town: 'Windfall Town'
  - text: 'Talk to Eusine at the top of the Burnt Tower'
    location:
      kind: 'npc'
      x: -347.5
      "y": 136.0
      z: 8.5
      label: 'Eusine'
      town: 'Windfall Town'
    rewards:
      - '150000 Coins'
      - '100 Tokens'
      - '150000 Trainer XP'
      - '3× Max PP'
      - 'Assault Vest'
      - '10× Rare Candy'
---
