---
title: 'Paper vs Folia: Which Minecraft Server Architecture Should You Use?'
description: 'Understand Paper’s primary tick thread, Folia regionized multithreading, plugin compatibility, and when FlameMC is worth evaluating.'
publishedAt: 2026-11-05
category: Architecture
takeaway: 'Paper is the lower-friction default. Folia offers parallel region ticking when workloads are spread out—but changes the plugin threading contract.'
readingMinutes: 6
---

**Paper and Folia solve different bottlenecks.** Neither is automatically faster for every Minecraft server. The critical decision is how the server distributes world simulation and how your plugins use the Bukkit/Paper API.

## What Paper does well

[Paper](https://papermc.io/software/paper/) is a performance-focused Minecraft server built around the Bukkit/Spigot ecosystem. It improves chunk loading, entity behavior, lighting and other game-server internals while exposing a mature plugin API. World simulation still has a dominant primary tick-thread model, though Paper also uses additional threads for particular asynchronous tasks. It is incorrect to say Paper “uses only one CPU core.”

For a minigame or SMP whose players crowd the same arena, Paper is often a straightforward choice: scheduling conventions are familiar, plugins commonly assume one primary thread, and administration tooling is widely available.

## What Folia changes

[Folia](https://papermc.io/software/folia/) builds on Paper and divides loaded worlds into independently ticking regions. Regions that can safely execute independently may tick in parallel on multiple CPU cores. Entities, blocks and region-owned state must still be accessed by their correct owner.

This is a change in the **execution contract**, not an “async everything” switch. A plugin callback cannot safely inspect a remote entity or block just because multiple tick threads exist. Folia introduces region, entity and global scheduling mechanisms to target the proper owner.

### Workload distribution matters

Imagine 800 players in a tightly packed spawn versus 800 players spread across distant SMP bases. The first workload can remain concentrated in a limited number of region owners; the second offers more opportunities for parallel ticking. Folia can improve the second pattern, but it cannot guarantee a specific TPS increase.

## The plugin compatibility trade-off

PaperMC explicitly states that Folia is **not a drop-in replacement for Paper**. The `folia-supported: true` declaration is a declaration by the plugin author, not a substitute for correctly handling ownership, shared mutable data and scheduling. See [PaperMC's plugin development guidance](https://docs.papermc.io/paper/dev/folia-support/).

| Question | Paper | Folia |
| --- | --- | --- |
| World tick scheduling | Dominant primary tick thread | Independently ticking owned regions |
| Plugin ecosystem | Broad Bukkit/Paper compatibility | Plugins must be Folia-aware |
| Ideal high-load shape | Existing plugins, concentrated workloads | Geographically distributed player activity |
| Main migration risk | Version/API changes | Thread-ownership and shared-state assumptions |
| Guaranteed speedup | No | No |

## Where FlameMC fits

FlameMC combines Folia's region-threading foundation with a compatibility layer designed to route **supported** legacy Bukkit/Paper operations to the correct owner. That can reduce migration friction without weakening Folia's thread-ownership rules. It does **not** mean every Paper plugin works unchanged. For details, read [FlameMC vs Folia](/guides/flamemc-vs-folia/) and the [plugin migration checklist](/guides/folia-plugin-compatibility/).

## How to choose

1. **Stay on Paper** when plugin compatibility is the decisive requirement or your players mostly share one heavily loaded area.
2. **Test Folia** when players naturally spread across multiple independent areas and your plugin set is built for Folia.
3. **Evaluate FlameMC** when you want Folia's parallel region model but need to test supported legacy Paper workflows against FlameMC's compatibility layer.

Use a cloned world, identical player simulations and the same hardware. Compare per-region tick times, TPS, CPU saturation, plugin errors and correctness—not just a single synthetic maximum-player figure.

## Sources and further reading

- [PaperMC: Paper server overview](https://papermc.io/software/paper/)
- [PaperMC: Folia overview and limitations](https://papermc.io/software/folia/)
- [PaperMC: Folia region architecture](https://docs.papermc.io/folia/reference/overview/)
- [PaperMC: Supporting Paper and Folia](https://docs.papermc.io/paper/dev/folia-support/)
