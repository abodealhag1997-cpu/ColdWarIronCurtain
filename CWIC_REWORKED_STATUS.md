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
  `gfx/leaders/leader_unknown.dds` asset name used by HOI4
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

## Syrian decisions with international consequences (new module)

Added an exclusive `CWICR_SYR_regional_initiatives_category` under
`common/decisions/categories`, using no full-sized background image so
the category should avoid additional decorative text clutter.

Five one-use Syrian foreign-policy initiatives now dispatch independent
response events to non-Syrian countries:

1. **Levantine transit corridor (1950+):** Lebanon can accept or reject
   an infrastructure/customs proposal. Acceptance applies a modest
   infrastructure-construction bonus and consumer-goods cost **to
   both Lebanon and Syria**, plus temporary bilateral opinion changes.
2. **Euphrates water dialogue (1961+):** Iraq may accept a technical
   commission or reject it, with different Syrian/Iraqi diplomatic
   effects and modest administrative ideas on acceptance. This does
   **not** simulate actual river allocation or annex Iraqi resources.
3. **Jordanian border commission (1950+):** Jordan decides whether to
   establish liaison talks, with bilateral reputation and stability
   consequences.
4. **Egyptian technical exchange (1952+):** once Syria has funded a
   budget commission, Egypt may join a reciprocal, small one-use
   radio research bonus, or decline.
5. **Two-bloc outreach (1955+):** Washington and Moscow independently
   decide whether to entertain Syrian consultations. Acceptance
   influences their opinions of Syria, while the rival bloc may
   become suspicious. A neutral news event tells the world about the
   initiative without inventing a US or Soviet commitment.

Across these initiatives there are **seven** triggered foreign/news
events, eight temporary opinion modifier types, two small
bilateral national spirits and **51 English localisation keys**.
Foreign AI choices are weighted rather than guaranteed; neither
Syria nor another country receives automatic territory, puppet
governments, nuclear weapons or free armies.

These decisions use the same political-power cost system as the
rest of CWIC and are available to **Syria only**. The receiving states
participate as decision responders, not as decision initiators.
Source checks confirmed all event IDs, national spirits, opinion
identifiers, focus-independent dates and text keys resolve. This is
**source validation only**, not tested game balance or UI rendering.

The user's screenshot of the pre-existing Economic Decisions category
shows busy text overlapping the category artwork. This visual issue
belongs to the legacy economic GUI and is not yet proven repaired.
Our new Syria decision category intentionally omits a large picture;
we should audit the old economic category artwork and GUI separately.

## October 2026 — new source-level development batch

**A. South-South scientific diplomacy (1961+)**
- Added the Syrian-only `CWICR_SYR_south_south_science_invitations`
  decision under the existing regional-international decisions category.
  It costs 135 political power and requires a prior Syrian budget
  commission, Yugoslavia and India's continued existence, and peace
  with both recipient states.
- YUG and RAJ receive separate invitation events with independent
  AI acceptance/refusal choices. A scheduled Syrian outcome event
  waits nine days for both replies; a partnership requires **both**
  countries to agree. Failure imposes lost political capital and a
  small domestic stability cost, with no research reward.
- If both agree, all three countries receive a modest research-speed
  idea (+0.8%) counterbalanced by a consumer-goods burden (+1.2%)
  and the recipients paid 20 political power apiece. A **major
  international news event** broadcasts the agreement.
- This is explicitly an *alternate-history* scientific outreach after
  1961, not an assertion that a formal three-state treaty existed.
  No nuclear technology, free equipment, military alliance or
  industrial buildings are granted.

**B. World news delivery correction**
- Six Syrian international `news_event` definitions formerly lacked
  `major = yes` and had `fire_only_once = yes`, which could
  suppress delivery beyond a single player country.
  All six now use `major = yes` with the global-suppressing
  `fire_only_once` removed. This changes news visibility, not
  geopolitical leverage by itself.
- Added `CWIC_Reworked_World_Audit.py` and integrated it into the
  GitHub Actions static checks. It covers international event
  references, response prerequisites, translations, news broadcast
  flags, and finance projects.

**C. Treasury-linked Syrian development**
- Three additional Syria-exclusive, **one-use** initiatives use the
  actual CWIC `currentMoney` variable rather than minting free funds:
  industrial credit (12 treasury units + 80 political power),
  rural water works (8 treasury units + 70 political power), and
  supervised defence procurement (10 treasury units + 95 political power).
- Each requires a funded Syrian budget commission and further
  development prerequisites. Successful projects give *temporary*
  national ideas for approximately 2–3 years, combining small
  economic/industrial benefits with consumer-goods or political
  administration costs. These are not perpetual compounding bonuses.
- The currentMoney scale is inherited from CWIC; dollar-equivalent
  balance and AI affordability **have not been runtime-tested**.

**D. Intel portrait reference correctness**
- The previously used `gfx/leaders/operative_unknown.dds` was not
  present in the project repository. The fallback now references
  the real `gfx/leaders/leader_unknown.dds` file.
  Static validation now requires the referenced DDS to exist.
  Visual quality and multiplayer/DLC sync still need runtime checks.

**Validation limits:** each newly added scripted decision, event and
idea file passed structural brace checks, and event IDs, national
spirits, localisation and treasury payments were cross-referenced.
These are *text/source audits only*. No HOI4 executable gameplay
test has run on this GitHub branch, and CI results have not been
confirmed in this environment. Existing research, Officer Corps
layout, the intentional July 2026 space-tab removal, and all
historical-coup timelines still need the integrated test plan.

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

## Syrian applied space services and regional weather diplomacy

**Research tree expansion:** added a fourth Syrian-only research column
to `common/technologies/CWICR_SYR_Research.txt` and the matching
`countrytechtreeview.gui` panel. The new chain is:

- 1968: `CWICR_SYR_satellite_reception_1968`, basic reception of
  foreign satellite broadcasts and signals.
- 1978: `CWICR_SYR_meteorology_1978`, weather and drought
  interpretation using available satellite information.
- 1988: `CWICR_SYR_earth_observation_1988`, remote sensing for
  agriculture and irrigation planning.

These represent **access to foreign space data**, not a fabricated
Syrian satellite launch programme. The technologies require research
slots and normal research time, with low country-modifier benefits.
All twelve Syrian exclusive technologies remain restricted by
`original_tag = SYR`, and the four starting research branches
have matching gridboxes, icons and English localisation.

**Syria-only global diplomatic action:** added the
`CWICR_SYR_satellite_weather_network` decision (1979 onward).
It requires that Syria first research satellite-assisted meteorology,
spends political capital, and invites Iraq, Jordan and Lebanon
separately. Each partner can accept or reject; acceptance applies
a small *shared* research/civil-administration cost idea and improves
bilateral relations. An international news event reports the
**invitations**, not an agreement that may never materialise.
Four new events, one idea and nineteen English localisation keys
are present.

**Research tree emptiness distinction:** the public development
source intentionally removed the old 53-node `space_folder`
technology tree in July 2026 and transferred that area of gameplay
to the special-project system. Restoring a button without technology
nodes would only create an empty tab again; the Syrian applied
space-services column is separate from that removed global tree.
Other missing/empty global research sections still need individual
data/GUI investigation and in-game checking.

**Validation:** static checks confirmed paired research IDs,
their icons/localisation, four UI branches, all independent recipient
event IDs, balanced braces and absence of fabricated equipment or
territorial grants. GitHub Actions should be consulted for results;
no live HOI4 1.19.3 runtime verification has been performed.

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

## Second Syria-led international initiatives (source-level changes)

- **Golan ceasefire observation, post-1967:** Syria must first file its
  UN mediation dossier and not be at war with Israel. Israel may accept
  or refuse bilateral observation contacts. Consent triggers limited
  staff costs, shared stability benefits, temporary opinions in Syria,
  Israel, USA and USSR, and a public event. No formal UN mandate,
  territorial change or ceasefire guarantee is created.
- **Euphrates three-government consultation, from 1965:** Syria must
  first secure Iraqi acceptance of bilateral water talks. Turkey can
  independently join or reject a technical conference. Acceptance
  creates a small shared planning benefit and consumer-goods cost in
  Syria, Iraq and Turkey; no river resources change hands.
- **Regional civilian relief, from 1975:** Syria must already fund its
  displaced-family services. Lebanon and Jordan independently decide
  on relief administration; each consenting state receives a modest
  stability/cost trade-off. A world news event announces the invitation
  but does not pretend either government already accepted.

All eight Syria-exclusive foreign initiatives are in
`common/decisions/CWICR_SYR_Regional_Initiatives.txt`; 15 independent
foreign/news events reside in `events/CWICR_SYR_Regional_Initiatives.txt`.
Associated effects and descriptions are in the existing regional
ideas, opinion modifiers and localisation files. The source validator
now checks all event references, localisation keys, the recipient
countries' ability to respond, and the absence of instant annexations
or free weapons. Runtime event routing and UI behaviour are **not yet
verified**. The pre-existing global Economic Decisions text overlap
shown in the user's screenshot is a separate unresolved UI issue.

## Economic decisions category visual cleanup (source fix)

The earlier user screenshot showed the full-width Economic Decisions
and Economic Investments background banners interfering with text.
On branch `cwic-reworked` we disabled the `picture` attribute in
`common/decisions/categories/00_decision_categories.txt` for:

- `economy_decisions`
- `economy_decisions_reenable`
- `economic_investments`

The category headings and icons remain, as do all economic decisions,
prices and game rules. This is a conservative source-level legibility
fix; exact layout must be checked during the final in-game test.
The Python source checker now warns if those large category banners
are inadvertently restored.

## Syria cities, strategic intelligence and contractors (new integration)

The following implementation is committed, but its exact in-game operation
still requires a new 1949/1960 campaign and DLC compatibility smoke test:

- **Eight Syrian state-level investments** in
  `common/decisions/CWICR_SYR_City_Construction.txt`: Damascus
  (554, office park), Aleppo (677, civilian industry), Homs
  (893, arms factory), Hama (895, agri-industry), Latakia
  (809, dockyard), Deir ez-Zor (680, water infrastructure),
  Al-Hasakah (777, agri-industry) and Rif Dimashq (2046, radar).
  These are *game states*, not separate city-building UI assets.
  All require Syrian ownership/control and CWIC treasury plus political
  expenditure. Preparation takes 120 days. Buildings then join the
  construction queue, so deployment and build slots still matter.
  Several decisions require the corresponding new Syria research.
- **Three-tier strategic intelligence path** in
  `CWICR_SYR_Intelligence_and_Contractors.txt`: the central directorate,
  foreign station network and satellite-analysis service require
  progressively later techs, large political/treasury costs and long
  preparation times. Three cumulative spirits use the documented
  `operative_slot = 1` modifier, offset by escalating consumer-goods
  and political-power burdens. CIA-level parity is NOT asserted:
  operatives, agency upgrades and foreign intel outcomes remain subject
  to the underlying HOI4 systems.
- **World-facing reactions:** the United States and Soviet Union
  independently choose concern or guarded security dialogue upon
  the second intelligence tier. A separate one-time news event covers
  the publicly acknowledged expansion. Opinion changes are temporary.
- **Licensed Syrian private military contractors:** first register
  a legal framework. This creates a separate template of three regular
  infantry battalions (avoiding the old `pmc` unit type in CWIC,
  currently marked `active = no`). A subsequent paid one-time decision
  recruits one *understrength* Syrian Contract Security Brigade at the
  national capital with `start_equipment_factor = 0.0`, making normal
  military equipment supply necessary.
- **Host consent is mandatory:** Lebanon or Iraq may independently
  reject training/advisory contracts. If accepted, both countries
  receive bounded temporary ideas; otherwise no foreign unit spawns.
  A contract does not imply annexation, coercive basing rights or
  automatically deployed Syrian units.
- **Static safeguards:** `CWIC_Reworked_Security_Cities_Audit.py`
  checks map states, building types, Syria-only categories,
  localisation keys, advisor research dependencies, foreign response
  event IDs and the contractor brigade template. The GitHub Actions
  source-validation workflow now includes this audit.

**Still unresolved:** user-reported Officer Corps and research layout
overlaps across screen resolutions/DLC; remaining empty tabs beyond
the intentionally removed 53-technology legacy space branch; future
budget/AI balancing; actual division template spawning; and full
interactive 1.19.3 compatibility. Treat this as an integration build,
not a release certified by an HOI4 run.
