# CWIC Reworked — single-pass acceptance test / خطة اختبار شاملة واحدة

**Branch:** `cwic-reworked`  
**Target:** Hearts of Iron IV 1.19.3 with the user's DLCs  
**Current gate:** Automated GitHub source checks must pass; the mod is NOT certified until an in-game run.

This checklist prevents dozens of separate install / exit / restart cycles.
Do not start it during source development. Perform it once after the
integrated candidate is marked ready for player testing.

## Before launching

1. Keep the subscribed Steam Workshop mod intact. Download the complete
   `cwic-reworked` branch as a separate checkout or ZIP, unpack it, and
   run `Install-CWIC-Reworked.ps1` from the repository root.
2. In Paradox Launcher, make a **new playset** containing only
   `CWIC Reworked (HOI4 1.19)`. Do not enable the Steam Workshop
   copy or other submods in the same playset.
3. Use a test save only. Disable Ironman. Note game version, enabled DLCs,
   display resolution, and interface scale (for the overlapping GUI issue).
4. Check the most recent GitHub Actions job has **success**, not failed/cancelled.

## Test run: Syria 1949

- **Launch and country:** start a NEW 1949 scenario as Syria. Confirm the
  `50s_SYR` national focus tree appears. Do not reuse a save from the
  Steam Workshop build.
- **National focuses:** inspect political, agricultural, military and
  Syrian espionage branches. Note missing prerequisites/invalid rewards.
- **Research tabs:** inspect every ordinary research tab, noting which
  countries/tabs are empty. The old GLOBAL space technology tree was
  intentionally removed upstream; its replacement is under **Special
  Projects**, not a restored global `space_folder` tab.
- **Syrian research:** verify the Syria-only research tab and 12 technologies,
  including the civilian satellite meteorology branch, are visible and
  researchable by Syria.
- **Army/navy/air doctrines:** confirm three grand-doctrine groups and
  Special Forces tracks load; check XP costs and selected doctrine bonuses.
- **Officer Corps:** open and screenshot the entire window. Are senior
  army advisors visible? Can a legitimate Syrian army chief/high-command
  character be selected? Check overlapping/misaligned portraits/stat rows.
  Navy/air chiefs may still be absent without historical roster work.
- **Intelligence:** confirm button exists, agency creation/upgrades take
  about 30 days, recruited agent portraits render and the operative cap is
  not set to zero.
- **Syrian decisions:** check domestic finance, agricultural cooperatives,
  officer training, intelligence, institutions, economic models, corruption
  audits, and foreign-policy decisions. Only Syria should see
  `CWICR_SYR_*` categories.
- **Regional initiative:** initiate one eligible bilateral action. Switch
  recipient countries via a controlled test save or check AI responses;
  ensure they can refuse and outcomes do not spontaneously change borders.
- **Finance decision UI:** verify the global `Economic Decisions` and
  `Economic Investments` texts remain readable after wide banners were
  removed. Verify Syrian new categories likewise have uncluttered text.
- **Special projects:** inspect the space project category and confirm
  the Soviet Buran entry does not generate the missing Zenit-parent error.
  Do not expect the old 53-node space research tree in this build.

## Same QA period: 1960 and other countries

- Start the 1960 Syrian bookmark in a separate new test campaign, checking
  `60s_SYR`. This verifies the date-specific focus-tree switch.
- Check at least one other country (e.g., USA or USSR) for visible
  normal research folders; the Syrian research tab must not appear.
- Check an additional smaller country to distinguish mod-global empty tabs
  from Syria-specific UI problems.
- Do not claim the entire scenario works if a major GUI/technology tab is
  still blank, or if an engine parser error remains.

## What to capture once, at the END of the consolidated test

1. `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log`
2. `Documents/Paradox Interactive/Hearts of Iron IV/logs/game.log` if present
3. At most 3 screenshots: Officer Corps, research tabs (Syria and comparison
   country), and one Syrian decision category
4. A short text: game version; DLCs; whether Steam Workshop CWIC was disabled;
   UI scaling/resolution; what failed or worked

Use `Collect-CWIC-Reworked-Logs.ps1` from the repository root to assemble
the two logs and a fill-in test checklist to the desktop WITHOUT modifying
the game, saves, mod files or Workshop subscription.

## Release criterion

- GitHub source validation passes on the final candidate commit.
- No new major parser errors from this branch in `error.log`.
- General research tabs, Syria-only technologies, doctrines, agency,
  focus trees and Officer Corps have been inspected at HOI4 1.19.3.
- Syrian regional decisions have at least one confirmed
  acceptance AND refusal path checked.
- Known visual/layout defects documented and either corrected or explicitly
  marked as outstanding. Source-only verification is not sufficient.
