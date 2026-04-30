---
title: 'Join via Bedrock Together'
subtitle: 'Connect Xbox or PlayStation to the Java-edition Pokéfind server through the Bedrock Together mobile app.'
weight: 20
---

Pokéfind is a Java-edition server, but **Bedrock Together** lets Bedrock-edition consoles (Xbox, PlayStation, Switch) connect to it through a small companion app that runs on your **phone**. This guide walks through the setup.

## Reference materials

- **Video walkthrough:** [Pokéfind — How To Join on Xbox (works on PlayStation too)](https://youtu.be/hP984YFqZYs)
- **Written guide (Google Doc):** [open original guide](https://docs.google.com/document/d/1YJsXyD3YJiNv4mbobW0pmVk4-rpAo4pgYtz4CLCItSI/edit?usp=sharing)

The video and the doc are the canonical source — when in doubt, follow them. The summary below is for quick reference.

## What you need

- A **phone** (Android or iOS) that stays nearby while you play, on the **same Wi-Fi network** as the console.
- A **Bedrock-edition console** (Xbox, PlayStation, or Switch) signed into a Microsoft account.
- The **Bedrock Together** app installed on the phone (Google Play / App Store).

## Setup overview

1. **Install Bedrock Together on the phone.** Open the Play Store / App Store, search for *Bedrock Together*, and install it.
2. **Add Pokéfind in the app.** Open Bedrock Together and add a server entry with:
   - **Server address:** `play.pokefind.co`
   - **Port:** `19132`
3. **Start the bridge.** Tap to start the connection in Bedrock Together — it acts as the relay between your console and the Java server long enough for the console to find the LAN entry.
4. **On the console, open Minecraft → Play → Worlds.** With Bedrock Together running on the phone (same Wi-Fi), Pokéfind appears as a **LAN game** in the Worlds tab.
5. **Connect.** Select the Pokéfind LAN entry. First connect can take 30–60 seconds; subsequent joins are quicker.
6. **Close Bedrock Together.** Once the console is in the server, you can close Bedrock Together on the phone — it's only needed for the initial handshake. Reopen and start it again the next time you want to join.

## Tips and troubleshooting

- **Same Wi-Fi.** Phone and console must be on the same Wi-Fi network during connect. Mobile data on the phone won't work for the bridge.
- **Allow local-network access.** Make sure your phone's OS lets Bedrock Together search for devices on your local network. On iOS: *Settings → Bedrock Together → Local Network = on*. On Android: when first launched, accept the nearby-devices / local-network permission prompt; if you missed it, enable it under *Settings → Apps → Bedrock Together → Permissions*.
- **Doesn't show in Worlds?** Make sure Bedrock Together is actively running and connected on the phone, then refresh the Worlds tab on the console.
- **Stuck on the connecting screen?** Quit Minecraft on the console fully, stop and restart the connection in Bedrock Together, then try joining again.
- **Disconnected mid-session?** Reopen Bedrock Together on the phone and reconnect through the Worlds tab the same way you did the first time.

## Once you're in

- Click the **compass** in your inventory to create or join your save file. You'll be sent to whichever region you were last in — or, if you're new, you'll start in **Gen 5: the Zeinova region**.
- See [the PokéWorld guide](/pokefind/pokeworld/) for an overview of the five regions and how progression unlocks more of the National Dex.
- New trainer? Start with [Quests → Generation 1](/quests/) for the Kyoto main-quest walkthrough.
