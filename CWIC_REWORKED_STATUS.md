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
   tracks and subdoctrines. Also removed the outdated
   `common/doctrines/folders/doctrine_folders.txt` override which only
   defined land/naval/air, so that the 1.19 native special-forces
   doctrine folder can load. This is an **integration choice for current
   grand doctrines**, not a restoration of CWIC's parked 646 legacy
   doctrine technology nodes. The modern doctrine UI and historic focus
   bonuses still need manual compatibility checks.
5. **Special forces doctrine:** restored the missing
   `can_unlock_second_track_of_sf_doctrine` scripted trigger.
6. **Officer Corps GUI:** removed CWIC's obsolete
   `interface/countryofficercorpview.gui` override so that vanilla 1.19
   draws the window. Also removed the legacy
   `interface/countrydoctrinetreeview.gui` override, which still laid out
   defunct technology-era doctrine folders. The old file is preserved in Git history.
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

## Additional fixes from the previously supplied error.log

- Corrected the Egyptian focus `EGY_farouk_leads_troops` by replacing
  invalid general trait `incompetent` with existing
  `inflexible_strategist` in `common/national_focus/EGY_50s.txt`.
- Corrected `infant_ryofficer` to the existing
  `infantry_officer` trait in `GDR_1953_Reimann.txt`.
- Removed a case-insensitive decision ID collision: `Bomb_insurgents`
  in Cuba and `bomb_insurgents` in the Dominican Republic are now
  `CUB_bomb_insurgents` and `DOM_bomb_insurgents`, each with new
  English text in `CWIC_Reworked_l_english.yml`.
- Replaced two invalid `excavation_tech` faction-goal technology
  categories with defined `synth_resources` (oil-supply goal) and
  `construction_tech` (military-base goal). This is a mechanical
  fallback and should be reviewed for historical balance.

These address *specific* logged script errors. The user's original
error.log came from a differently patched local Workshop build, so not
every logged problem is necessarily reproducible on this GitHub branch.
Existing Greek and Indonesian decision category files already define
the category names cited in that log; these were not changed speculatively.

## Automated offline preflight

Run `python CWIC_Reworked_Validate.py` from the repository root after
downloading a full checkout. The Python script inspects balanced Clausewitz
braces, five Syrian recruited advisors, Syrian focus references, espionage
defines, old doctrine override files, the new Syria reform decisions,
period-specific focus-tree loads, and the corrected error patterns.
**The validator file has been added to GitHub, but it has not yet been
executed in Python in this ChatGPT environment due to the unavailable
local execution environment.** Equivalent spot checks of edited text
and source references were performed.

## Syria state-capacity expansion (new work)

- The Syrian history file now explicitly loads `50s_SYR` at the
  1949 starting position and loads `60s_SYR` in the historical
  `1960.1.1` block. The previously commented-out 1960 switch is
  active in `history/countries/SYR - Syria.txt`. These are explicit
  historical start-date selections, not a full dynamic mid-game
  scenario system.
- Added two unique decision categories and four one-time Syrian
  decisions: national budget commission; irrigation cooperatives;
  professional officer education; and intelligence coordination.
  The latter three require historically relevant Syrian focus
  completions, recognised in either the 1950s or 1960s tree.
- New national spirits balance small benefits (administration,
  construction, organisation, planning, decryption) against consumer
  goods or political-power costs. No extra factories, equipment,
  invented historical personalities or free stockpiles were added.
- Added 20 English localisation keys for the new Syria projects.
- All new policy category IDs, decision IDs, idea IDs, source focus
  prerequisites and localisation keys were checked against their
  definitions by source inspection, with balanced Clausewitz braces.
- Converted four Syrian historical doctrine-evaluation rewards, which
  used legacy tech-doctrine discounts, to small military XP rewards
  compatible with the new HOI4 doctrine model: 10 air XP, 10 army XP,
  10 navy XP in the 1950s; 20 army XP from the 1960s Soviet Doctrine
  focus. These values need gameplay balance review.

### Remaining technology bonus fixes

The old runtime log listed several missing research bonus categories,
but some were **already repaired on the GitHub development branch**
and therefore should not be modified again. We changed only those
still reproducible in this source tree:

- `BRA_50s.txt`: `radio` -> `radio_tech`
- `DOM_49.txt`: `screen_hull_light` -> `screen_tech_hull`
- `HUN_60s_Kadar.txt`: `electronic_mechanical_engineering` -> `electronics`
- `HUN_60s_Kadar.txt`: `air_techs` -> `air_equipment`

The replacements are defined in `common/technology_tags/00_technology.txt`.
They are conservative technical mappings, not a balance test.

### Soviet special projects: orphaned Buran parent

- `common/special_projects/projects/cwic_space_special_projects.txt`
  named `sp_lv_sov_zenit` as the parent of `sp_orbiter_sov_buran`,
  but never defined that parent project. The previously supplied
  `error.log` explicitly reports this mismatch.
- Removed the nonexistent parent reference, retaining Buran's existing
  technology prerequisites, cost, rewards and AI parameters.
- This removes one invalid project-tree reference; it does **not**
  model the Energia launcher historically used by Buran. A full Energia
  launcher project is still future work.

### Intelligence operative portrait fallback

- `portraits/027_lar_portraits.txt` is deliberately empty upstream to
  prevent DLC-ownership-dependent multiplayer portrait pools.
- `portraits/00_portraits.txt` originally had no `operative = {`
  entry in its fallback `default` pool. The prior user log reported
  failed operative portrait generation for Syria.
- Added male and female operative fallbacks using the generic
  `gfx/leaders/operative_unknown.dds` asset name used by HOI4
  portrait mods. This is a generic contingency portrait, **not a
  country-specific historical operative portrait**.
- Added a source preflight check; exact rendering and DLC behavior
  still need in-game verification.

## Research tree / blank tab investigation

The user reported blank research tabs, including space, in several countries.
An audit of `common/technologies`, `common/technology_tags`,
`interface/countrytechtreeview.gui` and three interface GFX sources found:

- The upstream 53-technology space research tree was deliberately
  deleted on **5 July 2026**, being replaced by the special-project
  system. The live project source currently lists **92 projects**.
  Do not resurrect an empty space tab without actually porting its
  underlying technology system and dependencies.
- Sixteen research folders are registered with at least 36 matching
  technology placements each, including industry, engineering,
  military equipment, rocketry and WMD. All have content panels,
  tabs and declared tab sprite identifiers in the current mod source.
- Removed the four legacy technology-era doctrine folder registrations
  still present after the 1.19 doctrine integration.
- Removed the second `techtree_rocket_folder_item` GUI definition,
  which duplicated a more complete three-subtechnology-slot widget
  and contained just one subslot itself. Retained the complete version.
- Updated the old space source comment to point at its actual
  `cwic_space_special_projects.txt` replacement file.
- Added the standalone `CWIC_Reworked_Research_Audit.py` verifier.
  The detailed tab inventory is in `CWIC_REWORKED_RESEARCH_AUDIT.md`.

**Open question:** the user's screenshots and testing were from the
earlier locally patched Workshop build. We have *not yet established*
whether the GitHub branch still displays the same empty panes. This
requires one integrated runtime test at the end, not repetitive launches.

For the full tree-by-tree source audit, see
[`CWIC_RESEARCH_AUDIT.md`](CWIC_RESEARCH_AUDIT.md).
A source scan found matching GUI folder containers and tabs for
all 16 pre-existing non-Syrian research folders. These checks
cannot diagnose a specific blank tile seen on the local Steam
Workshop version until that build is compared at runtime.

## New Syrian-only applied science research tab

**Source-level implementation committed, runtime UI test pending.**
The user's symptom is global: a few other research windows and the
space category had blank/missing content in the installed Steam version.
The GitHub development branch **deliberately retired** the old
53-technology space tree on 2026-07-05. It left an empty
`common/technologies/space.txt` and migrated intended space progression
to special projects. We must not re-create an empty `space_folder`
button and call that a fix.

Separate from the global empty-tab audit, a new Syria-specific applied
science tab has been built:

- `common/technology_tags/00_technology.txt` — the
  `cwicr_syr_research_folder` is gated by `original_tag = SYR`.
- `common/technologies/CWICR_SYR_Research.txt` — nine linked
  technologies in three branches, with `allow_branch` on each
  first technology and `allow` on each technology.
- `interface/countrytechtreeview.gui` — Syrian folder, matching tab,
  three root gridboxes, and one dedicated research-item UI template.
- `interface/CWICR_SYR_Research.gfx` — nine sprite aliases referring
  only to existing technology textures.
- `localisation/english/CWICR_SYR_Research_l_english.yml` —
  23 English keys, including technology names and descriptions.

The branches develop water surveys and irrigation (1949/1957/1970),
technical education and industrial maintenance (1949/1958/1968),
and military communication / staff coordination (1950/1962/1972).
Cumulative bonuses are deliberately small, and none grants free
equipment, infrastructure, nuclear weapons, or fictional historic
personnel. These are plausible tech pathways, not assertions that
every programme actually existed as named.

Source inspection confirmed:
- All 9 technology IDs and all 6 dependency paths are defined.
- All 9 medium-icon sprite names and textures are mapped to asset
  references already used in `Technologies.gfx`.
- All technology category IDs exist and all 23 localisation keys exist.
- Three root gridboxes, the folder tab, and the research item template
  match the tech root IDs.
- Synergy with other countries remains intentionally limited: this
  tab **does not fix empty global tabs or disabled space research**.
- Balanced Clausewitz braces on newly edited technology, GUI and sprite files.

**Unverified:** actual tab visibility at the user's UI scale,
whether all nine icons display, in-game research/AI behaviour,
and interactions with the 1.19.3 research UI. Do not ship as finished
until these have been checked in one comprehensive test.

## Syria 1949–1991: institutional and geopolitical expansion (new batch)

- Added seven opt-in policy decisions in
  `common/decisions/CWICR_SYR_Political_Economy_Diplomacy.txt`:
  constitutional compact, national development choice, annual
  anti-corruption procurement audit, Arab regional consultation,
  United Nations mediation dossier, services for displaced families,
  and a post-1969 nuclear feasibility commission.
- Added three separate `CWICR_SYR` event choices, without touching
  the historic 1949–1970 Syria coup event scripts:
  civilian constitutional safeguards versus military guardianship;
  state-led industry versus regulated private enterprise versus rural
  credit; and internationally safeguarded versus opaque preliminary
  nuclear research. Each choice has nontrivial domestic costs.
- Added eight state ideas, four **temporary** diplomatic opinion
  modifiers and 55 English localization keys. The decisions rely
  on the actual `atomic_research` technology ID, existing budget
  oversight spirit and historical timing; they never grant equipment,
  reactor buildings or nuclear weapons.
- The `CWICR_SYR_un_mediation_dossier` currently has only a
  limited diplomatic/opinion effect: a genuine United Nations
  vote/veto/mission system remains **unimplemented**.
- These are initial systemic hooks for realism, **not** a complete
  budget, unemployment, corruption, refugee demography or nuclear
  deterrent simulation. They were checked for basic bracket balance,
  registration and cross-file references, not runtime outcomes.
- Corrected an indexing regression in
  `CWIC_Reworked_Validate.py`: the Syria history file is now
  addressed by its full pathname rather than the outdated list index.
- Added `.github/workflows/cwic-reworked-static.yml` to run static
  and research-file audits on commits. Workflow results still need
  confirmation before claiming CI success.

**Do not forget remaining approved scope:** historical government
paths and parties/elections, competing unions and coups, taxation,
debt, inflation, unemployment, oil/trade/sanctions, oversight and
military procurement, the United Nations, migration and refugees,
private military contractors, and a costly optional nuclear
deterrent over the 1949–1991 time frame. Full engineering order and
acceptance criteria are recorded in
[`CWIC_REWORKED_SYRIA_ROADMAP.md`](CWIC_REWORKED_SYRIA_ROADMAP.md).

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
  systems beyond the first four optional reform decisions, after the
  engine-level bugs are stable.
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
