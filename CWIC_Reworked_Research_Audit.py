#!/usr/bin/env python3
"""Static research-tree audit for CWIC Reworked, HOI4 1.19.

Run from the repository root:
    python CWIC_Reworked_Research_Audit.py

This checks source registration and common GUI names only. It cannot prove
that HOI4 parses each technology, displays its icon or handles DLC correctly.
"""

from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent / "Cold War Iron Curtain"
tech_dir = ROOT / "common" / "technologies"
tags_file = ROOT / "common" / "technology_tags" / "00_technology.txt"
tech_gui_file = ROOT / "interface" / "countrytechtreeview.gui"
projects_file = ROOT / "common" / "special_projects" / "projects" / "cwic_space_special_projects.txt"

errors: list[str] = []


def read(path: Path) -> str:
    if not path.is_file():
        errors.append(f"Missing source file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8-sig")


def without_comments(source: str) -> str:
    return "\n".join(row.split("#", 1)[0] for row in source.splitlines())


# These are the intentionally active tabs in the current development branch.
# The space research tab is not listed because the developer removed it in
# July 2026 in favour of special projects; see common/technologies/space.txt.
expected_folders = {
    "infantry_folder",
    "support_folder",
    "artillery_folder",
    "armour_folder",
    "nsb_armor_folder",
    "nsb_armor_modules_folder",
    "naval_folder",
    "mtgnavalfolder",
    "mtgnavalmodulefolder",
    "air_techs_folder",
    "light_air_techs_folder",
    "helicopter_folder",
    "electronics_folder",
    "industry_folder",
    "rocket_folder",
    "wmd_folder",
    # CWIC Reworked: Syrian-only research tab, nine technology placements.
    "cwicr_syr_research_folder",
}

tags = without_comments(read(tags_file))
gui = without_comments(read(tech_gui_file))
folder_counts: Counter[str] = Counter()
source_file_counts: Counter[str] = Counter()

for path in sorted(tech_dir.glob("*.txt")):
    source = without_comments(read(path))
    matches = re.findall(
        r"\bfolder\s*=\s*\{\s*name\s*=\s*([A-Za-z][A-Za-z0-9_]*)",
        source,
    )
    folder_counts.update(matches)
    for name in matches:
        source_file_counts[name] += 1

print("CWIC Reworked — Research source audit")
print()
for folder in sorted(expected_folders):
    has_tag = re.search(r"(?m)^\s*" + re.escape(folder) + r"\s*=\s*\{", tags)
    has_panel = re.search(r'\bname\s*=\s*"' + re.escape(folder) + r'"', gui)
    has_tab = re.search(r'\bname\s*=\s*"' + re.escape(folder) + r'_tab"', gui)
    count = folder_counts[folder]
    print(f"{folder:30} tech placements={count:3d} tag={bool(has_tag)} "
          f"panel={bool(has_panel)} tab={bool(has_tab)}")
    if count <= 0:
        errors.append(f"Research folder has no tech placements: {folder}")
    if not has_tag:
        errors.append(f"Research folder tag missing: {folder}")
    if not has_panel:
        errors.append(f"Research GUI content panel missing: {folder}")
    if not has_tab:
        errors.append(f"Research GUI tab missing: {folder}")

unused_folders = sorted(set(folder_counts) - expected_folders)
for folder in unused_folders:
    errors.append(f"Tech file references a non-active folder: {folder}")

old_folders = (
    "old_land_doctrine_folder",
    "old_naval_doctrine_folder",
    "old_air_doctrine_folder",
    "special_forces_doctrine_folder",
    "space_folder",
)
for folder in old_folders:
    if re.search(r"(?m)^\s*" + re.escape(folder) + r"\s*=\s*\{", tags):
        errors.append(f"Legacy or removed research tab still registered: {folder}")

rocket_widget = re.findall(
    r'\bname\s*=\s*"techtree_rocket_folder_item"', gui
)
if len(rocket_widget) != 1:
    errors.append(f"Expected one rocket tech GUI widget, found {len(rocket_widget)}")

space_source = without_comments(read(tech_dir / "space.txt"))
if not re.search(r"\btechnologies\s*=\s*\{\s*\}", space_source):
    errors.append("Expected documented empty legacy space tech source")
if re.search(r'\bname\s*=\s*"space_folder(_tab)?"', gui):
    errors.append("Obsolete space research tab was reintroduced with no techs")

projects = without_comments(read(projects_file))
space_projects = len(re.findall(r"(?m)^sp_[A-Za-z0-9_]+\s*=\s*\{", projects))
print()
print(f"Space projects declared: {space_projects}")
if space_projects < 10:
    errors.append("The active space special-project system appears to be empty")

for error in errors:
    print("ERROR:", error)
if errors:
    print(f"FAIL: {len(errors)} source inconsistency/inconsistencies.")
    sys.exit(1)
print("PASS: researched tab/folder declarations are internally consistent.")
print("NOTE: This is not an HOI4 runtime or graphic rendering test.")
