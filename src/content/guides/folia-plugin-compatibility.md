---
title: 'Folia Plugin Compatibility: A Practical Migration Checklist'
description: 'Audit Bukkit and Paper plugins for Folia: scheduler usage, thread ownership, entity movement, plugin lifecycle, and FlameMC compatibility testing.'
publishedAt: 2026-11-05
category: Compatibility
takeaway: 'A plugin loading on Folia does not prove it is thread-safe. Test real execution paths, ownership boundaries and lifecycle behavior.'
readingMinutes: 7
---

Running existing Paper plugins on a region-threaded server requires more than checking a compatibility flag. **Folia changes who owns live Minecraft state, and when a plugin may touch it.** This checklist is useful whether you migrate directly to Folia or evaluate FlameMC's compatibility layer.

## 1. Inventory your plugin surface

Export your production plugin names, versions and dependencies. Record commands, events, repeating jobs, teleport paths, inventory handling, scoreboard use and world management for each plugin. A plugin with only chat formatting has a very different risk profile from a plugin that moves entities and edits chunks.

Keep a rollback-capable copy of your world and plugin configuration. Do not discover migration failures on your only production save.

## 2. Understand the scheduler contract

Folia exposes region and entity schedulers because world state is not owned by one universal main thread. A block or chunk needs its region owner; a moving entity needs its entity owner, which can change over time. Global metadata has another execution domain.

The [PaperMC compatibility guide](https://docs.papermc.io/paper/dev/folia-support/) warns that the `folia-supported: true` plugin declaration is **necessary for native Folia plugin loading but insufficient for safety**.

Audit these calls in particular:

- Traditional `BukkitScheduler` tasks that assume access to any world or player.
- Reads/writes to blocks or chunks outside the current region.
- Entity operations after teleportation, disconnect or retirement.
- Shared mutable maps, caches and collections used by callbacks in different regions.
- Asynchronous database work that later calls back into live server state.

## 3. Test behavior, not just startup

A plugin can load with no errors and fail only when two players enter different regions. Run smoke tests for:

| Test | What to verify |
| --- | --- |
| Join, quit and reload | No stale scheduler tasks or plugin callbacks after disable |
| Two far-away players | No illegal access to the other's live entity or block state |
| Teleport and world change | Ownership follows the entity, with correct results |
| Inventory and GUI | No unsafe concurrent mutation or lost item updates |
| Region transitions | Correct state after split, merge and player movement |
| Command and event chains | Expected ordering and return values, not fake success |

Include the shutdown path. Cancelling scheduled tasks, flushing data and unloading worlds often expose bugs missed during ordinary gameplay.

## 4. What FlameMC changes—and does not

FlameMC is designed to mediate **supported** legacy Bukkit/Paper operations through ownership-aware routing and compatibility contracts. This may allow workflows that vanilla Folia would otherwise reject or require plugin adaptation for. The scope is not universal: plugin-owned data races, undocumented NMS internals, and unsupported synchronous cross-owner operations may still need a code fix.

Do not disable safety assertions or force world operations onto arbitrary background threads to make a broken test green. That hides the defect rather than repairing it.

## 5. Verify performance separately

Compatibility and speed are different acceptance criteria. After functional tests pass, compare tick times, CPU use, GC activity and region distribution under representative player loads. Folia performs best when the workload allows independent regions to make progress in parallel.

**Migration succeeds when both gameplay correctness and operational performance are demonstrated.** Read [Paper vs Folia](/guides/paper-vs-folia/) for a platform choice framework.

## Sources

- [PaperMC: Supporting Paper and Folia plugins](https://docs.papermc.io/paper/dev/folia-support/)
- [PaperMC: Region scheduling and ownership overview](https://docs.papermc.io/folia/reference/overview/)
- [Folia project compatibility notes](https://github.com/PaperMC/Folia)
