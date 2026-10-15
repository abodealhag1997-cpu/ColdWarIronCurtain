# CWIC Reworked — integrated HOI4 1.19.3 test plan

**Current status: integration build / not certified as final release.**

Run these tests on a NEW campaign after downloading the `cwic-reworked`
branch and using `Install-CWIC-Reworked.ps1` from the repository root.
The Workshop version MUST be disabled, not combined with this branch.
The independent `development-branch` and Steam copy are unaffected.

## Preconditions

- HOI4 1.19.3 (game version actually shown in launcher).
- Cold War Iron Curtain Reworked selected **alone** in the playset.
- Record enabled DLCs: No Step Back, La Resistance, Man the Guns etc.
- Set GUI scale and screen resolution; screenshots should show both.
- Back up saves before using console/debug mode.

## Test A — universal interfaces

On one new Syria campaign, then on one major and one additional minor:

1. Open `Officer Corps` and select land/sea/air doctrine paths.
2. Inspect agency creation, recruitment, portrait render, agency upgrades.
3. Visit every *active* technology tab and open at least one technology.
4. Confirm the Syrian applied-research tab is available for Syria and
   is absent for other countries. Test its three original branches
   plus the added satellite/weather branch.
5. Inspect armor, industry, rocketry, helicopters, electronic engineering,
   WMD and naval tabs. No visible tab should have zero active technologies.
6. Check overlapping widgets and missing sprites at normal and reduced
   UI scales. Attach screenshots with the layout issue and `error.log`.
7. **Historical space-branch distinction:** July 2026 upstream removed its
   53-technology research tree. Space is now represented primarily by
   Special Projects rather than a normal research tab. Do NOT mark this
   intentional removal as an empty-tab bug, but check that Special
   Projects themselves render and are accessible.

## Test B — Syrian decisions, economy and provinces

1. Confirm the Syria-only categories appear; other countries do not get
   their contents.
2. Check the `currentMoney` requirements on every new decision.
3. Confirm construction plans correspond to these *state IDs*:
   Dimashq 554; Aleppo 677; Homs 893; Hama 895; Latakia 809;
   Deir ez-Zor 680; Al-Hasakah 777; Rif Dimashq 2046.
4. Verify that an eligible decision spends political power and treasury,
   waits 120 days, and then queues its building construction.
5. Verify loss of control prevents the later building from being started.
6. Test at least two technology-gated construction plans and one non-gated.
7. Review 1958–61 United Arab Republic ownership changes, 1967 Golan
   occupation and 1960 focus-tree selection for incompatible conditions.

## Test C — intel and contractors (later-date scenario)

1. Begin in the historical campaign and progress normally or use a
   controlled, separate debug copy. Console-forced dates may skip events.
2. Complete the budgeting, officer and intelligence prerequisites.
3. Test central directorate, overseas network and strategic analysis
   in chronological order, with large political/treasury costs.
4. Confirm each stage adds **one** additional operative slot (up to three
   cumulative) and imposes the stated economic/political penalties.
5. Confirm U.S. and Soviet reactions are separate choices.
6. License private contractors and verify the *Syrian Contract Security
   Brigade* template appears. Only then recruit ONE paid unit.
7. The brigade should appear near Syria's then-capital, understrength,
   needing normal equipment reinforcement (no free stockpile).
8. Verify Lebanon and Iraq can independently decline the advisory
   contracts, and that acceptance creates time-limited shared effects.
9. Inspect warnings for unknown `operative_slot`, `division_template`,
   `create_unit`, `add_building_construction`, and custom building types.

## Test D — integration and save/reload

- Play multiple months with the AI enabled and check performance.
- Confirm political proposals respond rather than auto-force annexation,
  puppet status or peace treaties.
- Save, close, reload, and check research, operative slots, timed
  contracts, scripted event flags, and urban decisions.
- Run `Collect-CWIC-Reworked-Logs.ps1` if an error appears and include
  the extracted log plus screenshots with the next report.

## Exit criteria for FINAL release

- CI source checks green on the *exact* commit being tested.
- Zero new startup **ERROR** entries attributable to CWIC Reworked
  additions, no red parser errors in decisions/events/technologies.
- No global empty research tabs other than intentionally replaced
  historical content; no critical UI overlap with the tested resolution.
- Syrian adviser slots and doctrine panel usable for eligible characters.
- Paid contractor division spawns correctly and receives no free gear.
- Syrian construction projects build only in owned/controlled states.
- Foreign diplomatic responses are independently selectable.
- Save/reload works; gameplay balance and AI path reviewed.

**This checklist has not yet been completed by a real HOI4 play session.**
Passing GitHub Actions only verifies the source-code invariants.
