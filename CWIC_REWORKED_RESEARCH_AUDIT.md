# CWIC Reworked — Research Screen Source Audit

Scope: CWIC Reworked branch `cwic-reworked`, intended for HOI4 1.19.3.
These are **source-level** observations, not a screenshot, a mod loading test, or a guarantee of graphical correctness.

## What actually happened to the space research tab?

The upstream developers deliberately removed **53 space technologies** and the
old `space_folder` research tab on **2026-07-05**, moving the feature to
`common/special_projects/projects/cwic_space_special_projects.txt`.
The `common/technologies/space.txt` file contains only `technologies = {}`
plus an explanatory comment. A space research tab with the old design
would be empty; restoring a button alone would not restore any technologies.

The replacement file currently declares **92 CWIC special projects**. Those
projects are part of the special-project/facility system, not a conventional
research-tree folder. The old space localisations and GFX references may
remain as unused assets.

**Decision:** Retain the upstream project-based space model, do not mix
the old 53-tech tree with the special-project progression until each
dependency, event reward, research icon and AI behavior is ported deliberately.

## Populated technology folders audited

All folders listed below have an active technology source, an enabled
registration in `common/technology_tags/00_technology.txt`, a panel and
tab named in `interface/countrytechtreeview.gui`, and a tab sprite
identifier declared in the mod's interface `.gfx` sources.

| Technology folder | Tech placements in direct technology files |
|---|---:|
| infantry_folder | 105 |
| support_folder | 79 |
| artillery_folder | 85 |
| armour_folder (without No Step Back) | 52 |
| nsb_armor_folder (with No Step Back) | 84 |
| nsb_armor_modules_folder (with No Step Back) | 115 |
| naval_folder (without Man the Guns) | 48 |
| mtgnavalfolder (with Man the Guns) | 67 |
| mtgnavalmodulefolder (with Man the Guns) | 76 |
| air_techs_folder | 47 |
| light_air_techs_folder | 86 |
| helicopter_folder | 40 |
| electronics_folder | 108 |
| industry_folder | 176 |
| rocket_folder | 79 |
| wmd_folder | 36 |

These are **folder placements** read from the Clausewitz files, not independently
counted unique valid game technologies. Folders for alternative DLC modes
can exist in the files while being hidden by the game correctly.

## Fixes committed on this branch

1. Removed four orphan technology-era doctrine folder registrations
   (`old_land_doctrine_folder`, `old_naval_doctrine_folder`,
   `old_air_doctrine_folder` and `special_forces_doctrine_folder`)
   from `common/technology_tags/00_technology.txt`. The old doctrine
   GUI override and empty 1.19 doctrine overrides were removed earlier.
2. Found two top-level widgets named `techtree_rocket_folder_item`.
   The earlier, complete definition had three subtechnology slots.
   The later, incomplete duplicate had just one. Kept the three-slot
   version and removed the incomplete duplicate.
3. Corrected the legacy space file comment to point to the real
   `cwic_space_special_projects.txt` location.
4. Added `CWIC_Reworked_Research_Audit.py` to statically check tech
   placements, registered folder names, GUI panels/tabs, the empty
   historic space source, the 1.19 project source and GUI duplication.

## What is not yet verified

- In-game research panel rendering at the player's UI scale and resolution.
- Whether all tab sprites point to textures available on the user's system.
- Engine parsing of each technology's individual prerequisite, module,
  AI weight and scripted reward.
- Facility availability and space project interaction on 1.19.3.
- Which of the user's blank tabs came from their older local Workshop
  installation rather than the current GitHub branch.

Therefore no claim of an in-game full repair is made yet. When engine-level
work is integrated, test one new campaign on the **GitHub Reworked build**,
not simultaneously with Steam Workshop CWIC, and record any remaining blank
tab by its visible title.
