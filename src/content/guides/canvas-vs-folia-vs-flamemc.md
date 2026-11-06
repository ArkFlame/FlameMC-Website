---
title: 'Canvas vs Folia vs FlameMC: Minecraft Server Forks Compared'
description: 'Compare CanvasMC, upstream Folia, and FlameMC by region threading, stability focus, plugin expectations, and migration requirements.'
publishedAt: 2026-11-05
category: Comparison
takeaway: 'All three use Folia-style region threading. Their differentiation is what each project builds on top of the concurrency foundation.'
readingMinutes: 6
---

[CanvasMC](https://canvasmc.io/), [Folia](https://papermc.io/software/folia/) and FlameMC operate in a related architectural space: Minecraft server software that can tick independent world regions on multiple threads. Their goals and compatibility expectations are not identical.

## Start with the shared constraint

Folia is a fork of Paper that introduces regionized multithreading. Each region must operate within its own ownership rules. This means a server fork cannot safely make every traditional Bukkit plugin “Folia compatible” by simply allowing arbitrary cross-thread world access.

Canvas explicitly states that it does **not** bypass Folia threading safety rules. FlameMC likewise aims to preserve those rules, adding explicit compatibility handling for supported legacy plugin operations.

## What Canvas focuses on

Canvas describes itself as a Folia fork focused on gameplay correctness, region-threading fixes, performance optimizations and configuration. Its published material also describes region-specific profiling and the ability to update its maintained region-threading patch set. These are [Canvas's published project claims](https://github.com/CraftCanvasMC/Canvas), not independent measurements in this article.

Canvas is especially relevant if you already use Folia-aware plugins and want to evaluate another Folia-derived implementation with a different set of fixes and optimizations. Canvas's own documentation says it is **not** a drop-in replacement for ordinary Paper setups.

## What FlameMC focuses on

FlameMC targets a different adoption obstacle: the legacy Bukkit/Paper ecosystem. It provides a Folia-based server with a compatibility architecture designed to mediate supported plugin operations according to actual region/entity/global ownership.

The important qualifier is **supported**. No server-fork architecture can promise correct execution for every arbitrary plugin, especially code that relies on direct NMS access, unmodeled cross-region synchronous behavior or plugin-owned unsynchronized state.

## Feature comparison

| Decision criterion | Folia | CanvasMC | FlameMC |
| --- | --- | --- | --- |
| Regionized multithreading | Core architecture | Folia-based | Folia-based |
| Main published focus | Parallel region simulation | Stability fixes and performance | Region threading plus Paper-workflow compatibility |
| Traditional Paper plugins | Not drop-in | Not drop-in | Selected legacy operations targeted; test each plugin |
| Ownership safety | Required | Explicitly preserved | Explicitly preserved by design |
| Guaranteed higher TPS | No | No | No |

This table describes documented project direction, not a controlled speed ranking.

## A fair migration test

Use identical worlds, Minecraft versions, Java/runtime settings and plugin sets where supported. Test not only TPS, but tick time distribution, player interactions, entity transfers, inventory operations and world shutdown. If an application needs the old synchronous Bukkit contract, test the functionality before prioritizing a few milliseconds of measured difference.

**Choose the implementation whose real semantics match your workload.** More patches or stronger marketing claims are not a substitute for correctness and reproducible measurements.

## Sources and next steps

- [Folia official project overview](https://papermc.io/software/folia/)
- [CanvasMC official site](https://canvasmc.io/)
- [CanvasMC GitHub and compatibility notes](https://github.com/CraftCanvasMC/Canvas)
- [Folia API ownership rules](https://docs.papermc.io/folia/reference/overview/)
- [FlameMC vs Folia](/guides/flamemc-vs-folia/)
