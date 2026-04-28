---
title: 'A Medical Emergency: Part Two'
date: 2026-04-28
layout: questguide
gen: 1
quest_key: 'a_medical_emergency_part_two'
slug: 'a-medical-emergency-part-two'
description: 'Team Rocket has stolen from so many Pokémon Centers and Pokémarts that the Pokémon in Kyoto are starting to seriously suffer. It is up to you to find the Legendary Pokémon Mew and help restore balance to Kyoto.'
author: 'luk_aszek, lego121212, bunstop'
source_file: 'a-medical-emergency-part-two.json'
start:
  npc: 'Officer Jenny'
  town: 'Finderia Town'
  x: -516.0
  "y": 96.0
  z: 650.0
steps:
  - text: 'Find Officer Jenny near the Finderia Town Gym'
    location:
      kind: 'npc'
      x: -516.0
      "y": 96.0
      z: 650.0
      label: 'Officer Jenny'
      town: 'Finderia Town'
  - text: 'Find Elliot in Amethyst Town'
    location:
      kind: 'npc'
      x: 1454.0
      "y": 84.0
      z: -226.0
      label: 'Elliot'
      town: 'Amethyst Town'
  - text: 'Battle Elliot'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Elliot'
        x: 1454.0
        "y": 84.0
        z: -226.0
        town: 'Finderia Town'
        team:
          - species: 'Arbok'
            level: 100
          - species: 'Sandslash'
            level: 100
          - species: 'Gengar'
            level: 100
          - species: 'Vileplume'
            level: 100
  - text: 'Find Aunt Elma in the outskirts of Smog Town'
    location:
      kind: 'npc'
      x: 1401.0
      "y": 67.0
      z: -474.0
      label: 'Aunt Elma'
      town: 'Smog Town'
    rewards:
      - 'full_restore'
  - text: 'Find and catch a Male Nidoran and give it to Aunt Elma'
    location:
      kind: 'npc'
      x: 1401.0
      "y": 67.0
      z: -474.0
      label: 'Aunt Elma'
      town: 'Finderia Town'
  - text: 'Find and catch a Female Nidoran and give it to Aunt Elma'
    location:
      kind: 'npc'
      x: 1401.0
      "y": 67.0
      z: -474.0
      label: 'Aunt Elma'
      town: 'Finderia Town'
  - text: 'Talk to Professor Hemlock in the Finderia Town Event HQ'
    location:
      kind: 'npc'
      x: -551.0
      "y": 96.0
      z: 563.0
      label: 'Professor Hemlock'
      town: 'Finderia Town'
  - text: 'Meet Professor Hemlock on the porch of his house in Finderia Town'
    location:
      kind: 'npc'
      x: -502.0
      "y": 83.0
      z: 533.0
      label: 'Professor Hemlock'
      town: 'Finderia Town'
  - text: 'Find Ryder between Foretree Village and Amber City'
    location:
      kind: 'npc'
      x: -555.0
      "y": 82.0
      z: -6.0
      label: 'Ryder'
      town: 'Foretree Village'
  - text: 'Find a Ground type Pokémon and give it to Ryder'
    location:
      kind: 'npc'
      x: -555.0
      "y": 82.0
      z: -6.0
      label: 'Ryder'
      town: 'Finderia Town'
  - text: 'Find Falkner in Aether Village'
    location:
      kind: 'npc'
      x: -543.0
      "y": 85.0
      z: 1347.0
      label: 'Falkner'
      town: 'Aether Village'
  - text: 'Battle Falkner'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Falkner'
        x: -543.0
        "y": 85.0
        z: 1347.0
        town: 'Finderia Town'
        team:
          - species: 'Butterfree'
            level: 100
          - species: 'Fearow'
            level: 100
          - species: 'Charizard'
            level: 100
          - species: 'Gyarados'
            level: 100
          - species: 'Pidgeot'
            level: 100
  - text: 'Arrive at Amethyst Town'
    location:
      kind: 'region'
      x: 1404.5
      "y": 250.0
      z: -143.5
      bbox:
        x1: 1276.0
        "y1": 0.0
        z1: -256.0
        x2: 1533.0
        "y2": 500.0
        z2: -31.0
      town: 'Amethyst Town'
  - text: 'Find an Amethyst Town local'
    location:
      kind: 'npc'
      x: 1422.0
      "y": 84.0
      z: -97.0
      label: 'Local'
      town: 'Amethyst Town'
  - text: 'Find Agatha in Amethyst Town'
    location:
      kind: 'npc'
      x: 1402.0
      "y": 83.0
      z: -135.0
      label: 'Agatha'
      town: 'Amethyst Town'
  - text: 'Battle Agatha'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Agatha'
        x: 1402.0
        "y": 83.0
        z: -135.0
        town: 'Finderia Town'
        team:
          - species: 'Gengar'
            level: 100
          - species: 'Golbat'
            level: 100
          - species: 'Haunter'
            level: 100
          - species: 'Arbok'
            level: 100
          - species: 'Gengar'
            level: 100
  - text: 'Arrive at Mystical Keep'
    location:
      kind: 'region'
      x: 959.5
      "y": 250.0
      z: -939.5
      bbox:
        x1: 858.0
        "y1": 0.0
        z1: -1025.0
        x2: 1061.0
        "y2": 500.0
        z2: -854.0
      town: 'Finderia Town'
  - text: 'Find and talk to Sabrina in Mystical Keep'
    location:
      kind: 'npc'
      x: 1060.0
      "y": 72.0
      z: -981.0
      label: 'Sabrina'
      town: 'Finderia Town'
  - text: 'Give Sabrina 5 Max Revives from the Mystical Keep Pokémart'
    location:
      kind: 'npc'
      x: 1060.0
      "y": 72.0
      z: -981.0
      label: 'Sabrina'
      town: 'Finderia Town'
  - text: 'Battle the Team Rocket Officer'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Team Rocket Officer'
        x: 921.0
        "y": 71.0
        z: -961.0
        town: 'Finderia Town'
        team:
          - species: 'Onix'
            level: 100
          - species: 'Jolteon'
            level: 100
          - species: 'Starmie'
            level: 100
          - species: 'Nidoking'
            level: 100
          - species: 'Snorlax'
            level: 100
          - species: 'Dragonite'
            level: 100
  - text: 'Talk to Aleris inside the Mystical Keep Pokémart'
    location:
      kind: 'npc'
      x: 911.6
      "y": 73.0
      z: -961.5
      label: 'aleris'
      town: 'Finderia Town'
    rewards:
      - '5× max_revive'
  - text: 'Talk to Sabrina in Mystical Keep'
    location:
      kind: 'npc'
      x: 1060.0
      "y": 72.0
      z: -981.0
      label: 'Sabrina'
      town: 'Finderia Town'
  - text: 'Give Sabrina 5 Max Revives'
    location:
      kind: 'npc'
      x: 1060.0
      "y": 72.0
      z: -981.0
      label: 'Sabrina'
      town: 'Finderia Town'
  - text: 'Battle Sabrina'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Sabrina'
        x: 1060.0
        "y": 72.0
        z: -981.0
        town: 'Finderia Town'
        team:
          - species: 'Mr. Mime'
            level: 100
          - species: 'Jynx'
            level: 100
          - species: 'Hypno'
            level: 100
          - species: 'Slowbro'
            level: 100
          - species: 'Alakazam'
            level: 100
  - text: 'Find the Mystical Keep cave and the entrance to the temple'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Complete the parkour'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Defeat the Temple Guardian'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 36.0
        z: -1121.0
        town: 'Finderia Town'
        team:
          - species: 'Vaporeon'
            level: 105
          - species: 'Kangaskhan'
            level: 105
          - species: 'Venusaur'
            level: 105
  - text: 'Defeat the Temple Guardian again'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 36.0
        z: -1121.0
        town: 'Finderia Town'
        team:
          - species: 'Vaporeon'
            level: 105
          - species: 'Kangaskhan'
            level: 105
          - species: 'Venusaur'
            level: 105
  - text: 'Defeat the Temple Guardian one more time'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 36.0
        z: -1121.0
        town: 'Finderia Town'
        team:
          - species: 'Vaporeon'
            level: 105
          - species: 'Kangaskhan'
            level: 105
          - species: 'Venusaur'
            level: 105
  - text: 'Open the door'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Investigate what the Temple Guardian was talking about'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Try opening the door on the other side of the room'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Find the key hidden in the jungle'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Return to the door and open it'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Try opening the second door'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Go back to the jungle and locate the next key'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Return to the door and open it'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Click the button on the last door'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Find the final key in the jungle'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Return to the last door and open it'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Defeat the Temple Guardian'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 7.0
        z: -1260.0
        town: 'Finderia Town'
        team:
          - species: 'Arcanine'
            level: 110
          - species: 'Gengar'
            level: 110
          - species: 'Dragonite'
            level: 110
  - text: 'Defeat the Temple Guardian again'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 7.0
        z: -1260.0
        town: 'Finderia Town'
        team:
          - species: 'Arcanine'
            level: 110
          - species: 'Gengar'
            level: 110
          - species: 'Dragonite'
            level: 110
  - text: 'Defeat the Temple Guardian one more time'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 951.0
        "y": 7.0
        z: -1260.0
        town: 'Finderia Town'
        team:
          - species: 'Arcanine'
            level: 110
          - species: 'Gengar'
            level: 110
          - species: 'Dragonite'
            level: 110
  - text: 'Open the door'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Enter the next room'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Get through the invisible maze'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Defeat the Temple Guardian'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 949.0
        "y": 7.0
        z: -1326.0
        town: 'Finderia Town'
        team:
          - species: 'Jolteon'
            level: 120
          - species: 'Aerodactyl'
            level: 120
          - species: 'Chansey'
            level: 120
  - text: 'Defeat the Temple Guardian again'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 949.0
        "y": 7.0
        z: -1326.0
        town: 'Finderia Town'
        team:
          - species: 'Jolteon'
            level: 120
          - species: 'Aerodactyl'
            level: 120
          - species: 'Chansey'
            level: 120
  - text: 'Defeat the Temple Guardian one more time'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 949.0
        "y": 7.0
        z: -1326.0
        town: 'Finderia Town'
        team:
          - species: 'Jolteon'
            level: 120
          - species: 'Aerodactyl'
            level: 120
          - species: 'Chansey'
            level: 120
  - text: 'Open the door'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Find out what the final challenge has in store for you'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
  - text: 'Battle the Temple Guardians'
    location:
      kind: 'battle'
      town: 'Finderia Town'
    battles:
      - trainer: 'Temple Guardian'
        x: 944.5
        "y": 7.0
        z: -1370.5
        town: 'Finderia Town'
        team:
          - species: 'Vaporeon'
            level: 125
          - species: 'Venusaur'
            level: 125
          - species: 'Arcanine'
            level: 125
          - species: 'Dragonite'
            level: 125
          - species: 'Aerodactyl'
            level: 125
          - species: 'Chansey'
            level: 125
    rewards:
      - 'master_ball'
      - 'eviolite'
  - text: 'Enter the tomb'
    location:
      kind: 'npc'
      x: 946.5
      "y": 36.0
      z: -1047.5
      label: 'Skip the Parkour'
      town: 'Finderia Town'
    rewards:
      - '50000 Coins'
      - '50 Tokens'
---
