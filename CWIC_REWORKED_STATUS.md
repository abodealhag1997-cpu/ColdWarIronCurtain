# CWIC Reworked — Work in progress / قيد التطوير

**Target:** Hearts of Iron IV 1.19.3, Cold War Iron Curtain development branch.  
**Status:** Source-level fixes committed; **not** verified in an interactive HOI4 session yet.

This is a separate development branch. Do not enable this and the original
Workshop version together.

## Implemented on the `cwic-reworked` branch

1. **Intelligence agency:** enabled creation/upgrade (30 days each), removed
   CWIC's other operatives-disabling overrides, and moved the topbar agency
   button back on screen. These settings were previously tested by the user
   in a separate local Workshop copy, **not on this GitHub build**.
2. **Advisor categories:** restored three political-advisor slots, the
   research theorist, army/navy/air chiefs, and three high-command slots.
   Also restored their ledger assignments.
3. **Syrian officers:** added five advisor roles to already existing and
   recruited Syrian characters: Aram Karamanoukian, Fawzi Selu, Sami al-Hinnawi,
   Adib Shishakli, and Afif al-Bizri. New mild staff traits and English
   localisations are provided. Navy and air chiefs still need researched
   historical candidates and suitable portraits; don't invent names.
4. **Current doctrines:** removed 21 empty .txt overrides in
   `common/doctrines` that suppressed vanilla 1.19 grand doctrines,
   tracks and subdoctrines. This is an **integration choice for current
   grand doctrines**, not a restoration of CWIC's parked 646 legacy
   doctrine technology nodes. The modern doctrine UI and historic focus
   bonuses still need manual compatibility checks.
5. **Special forces doctrine:** restored the missing
   `can_unlock_second_track_of_sf_doctrine` scripted trigger.
6. **Officer Corps GUI:** removed CWIC's obsolete
   `interface/countryofficercorpview.gui` override so that vanilla 1.19
   draws the window. The old file is preserved in Git history.
   The user's local screenshot still showed some UI/layout issues even
   after switching to the native window. Therefore the visual issue is
   **not claimed as fully fixed**.
7. **Syria focus trees:** restored `50s_SYR.txt` and `60s_SYR.txt`
   from `common/national_focus/Toberemoved/` into the live
   `common/national_focus/` directory. The originals remain in
   Git history and the archival folder.
8. **Descriptor:** removed a developer's absolute D-drive path and
   declared `supported_version="1.19.*"`. This describes the *target*
   version, not proof of compatibility.

## Static checks done

- Balanced `{}` checked in the modified `idea_tags`, character,
  trait, scripted-trigger, focus, history and GUI files.
- Five Syrian advisor roles were found; all five referenced characters
  are recruited by `history/countries/SYR - Syria.txt`.
- Restored two Syria focus-tree files contain valid top-level
  `focus_tree = {` sections.
- Verified the agency defines contain 30-day creation timing.
- Deleted the 21 known empty doctrine overrides and the obsolete Officer
  Corps GUI in Git, retaining reversibility by branch history.

**Static validation cannot confirm gameplay, GUI position, DLC behavior,
the suitability of all doctrine/focus rewards or absence of error.log
warnings.** An interactive run on HOI4 1.19.3 with the enabled DLCs
is still required before release.

## Remaining work / ما زال يحتاج عمل

- Determine why the Officer Corps screen still has overlapping
  stat/portrait elements at the user's display and UI scale.
- Finish army/navy/air/theorist coverage across countries.
- Reconcile 1.19 grand doctrines with Cold War-specific focus bonuses
  and any legacy XP paths; decide whether to port the historical
  doctrine rework rather than mix incompatible frameworks.
- Audit military design interfaces, tanks, templates, aircraft, espionage
  portraits and other `error.log` warnings.
- Expand Syria's political, economic, military, diplomatic and historical
  systems after the engine-level bugs are stable.
- Do a **single comprehensive** new-campaign run after integration.

## Installing *later* from a complete checkout

The repository root includes `Install-CWIC-Reworked.ps1`; it generates
a launcher `.mod` registration pointing at the working copy without
overwriting Steam's Workshop installation. It does **not** download or
build the repository. Keep the GitHub checkout in a stable folder and
run the installer there. The project is not ready for final gameplay
release yet.

## Reverting

The original `development-branch` and Steam Workshop subscription
remain unchanged. Each modification is committed separately on the
`cwic-reworked` branch; Git history permits any patch to be reverted.
