# CWIC Reworked — Research tree audit
Checked against the `cwic-reworked` branch on 2026-10-15.

## User symptoms

Reported: several research-tree cells/tabs are empty when playing
multiple nations; the space section is specifically missing or empty.
The symptoms were seen in the user's *local Steam Workshop build*,
which is not identical to this GitHub development checkout.

## What the source actually shows

- `common/technologies/space.txt` is deliberately an empty
  `technologies = { }` file. Its comment attributes deletion of
  53 old space technologies to **2026-07-05**, in favour of
  `common/special_projects/projects/cwic_space_special_projects.txt`.
- `common/technology_tags/00_technology.txt` has no active
  `space_folder` entry; `interface/countrytechtreeview.gui`
  likewise has no `space_folder` or `space_folder_tab` widgets.
  Restoring only a visible space tab would therefore create an empty
  research window, not fix the intended space gameplay.
- All 16 other normal technology folders declared in
  `common/technology_tags/00_technology.txt` have matching named
  folder containers **and** tabs in the custom research GUI.
  Their supplied technology files have nonzero technologies.
- HOI4 1.19-era doctrines were formerly hidden by obsolete tech
  folder definitions. The branch removed the four legacy
  doctrine-folder declarations and the empty doctrine override files.
- The mod includes No Step Back armoured-vehicle and module techs;
  `interface/cwic_tank_rework_icons.gfx` contains the relevant
  `GFX_nsb_*_medium` sprite definitions (over 200 sprite mappings).
  Searching only `Technologies.gfx` would falsely report missing
  NSB tank icons.
- Many generic science, rocket, electronics, industrial, aircraft and
  naval technologies have medium-icon definitions in
  `Technologies.gfx` or `New_Technology.gfx`.
  This does **not** guarantee that their underlying DDS files render
  correctly on the user's installed copy.

## New Syrian technology folder

- `cwicr_syr_research_folder` is restricted to `original_tag = SYR`.
- A matching country-tech tab and three root gridbox containers were
  added in `countrytechtreeview.gui`, plus an icon UI template.
- Nine new gated research technologies are present in
  `common/technologies/CWICR_SYR_Research.txt` across three tracks.
- Nine medium-icon sprite aliases point to texture filenames that
  are already defined by existing CWIC technology graphics files.
- 23 English localization entries define the tab, three track
  headings, and nine technology names/descriptions.
- Static cross-reference scan: 9 IDs, 6 prerequisite links, 3 roots,
  9 icons, 23 localization entries, all known categories,
  matching UI containers, no missing links, balanced braces.

## What remains for the comprehensive runtime test

1. Launch only this built branch with HOI4 1.19.3 and appropriate DLC.
2. Start Syria and one unrelated country at 1949 and 1960 dates.
3. Confirm Syrian tab appears only for SYR, all nine icons and three
   linked branches render, and each technology is researchable in its
   intended time period.
4. Check each globally visible research tab for empty rows/cells,
   invisible tiles, missing textures and misplaced GUI controls.
5. Check special-project facilities and space projects separately
   from standard research tabs, including prerequisites and assets.
6. Save the new `error.log` and compare with the earlier Steam log,
   because those older messages may already have been repaired in
   the development source tree.

**Do not claim that the global research UI or space system is fixed
until this runtime comparison has been completed.** Keep the
Syrian tab separate from the deliberately retired global space tree.
