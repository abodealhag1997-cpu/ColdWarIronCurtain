#!/usr/bin/env python3
"""CWIC Reworked static preflight. No HOI4 installation or extra packages required.

Run from a repository checkout:
    python CWIC_Reworked_Validate.py

This checks a deliberately limited set of mechanical invariants. A clean
result does NOT mean that the mod will run without errors in HOI4 1.19.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
MOD = REPO / "Cold War Iron Curtain"
errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def read(relative: str) -> str:
    path = MOD / relative
    if not path.is_file():
        fail(f"Missing: {relative}")
        return ""
    return path.read_text(encoding="utf-8-sig")


def strip_strings_and_comments(source: str) -> str:
    """Mask quotes/comments while retaining actual brace and line positions."""
    masked = []
    in_string = False
    in_comment = False
    escaping = False
    for ch in source:
        if in_comment:
            if ch == "\n":
                in_comment = False
                masked.append("\n")
            else:
                masked.append(" ")
            continue
        if in_string:
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == '"':
                in_string = False
            masked.append("\n" if ch == "\n" else " ")
            continue
        if ch == "#":
            in_comment = True
            masked.append(" ")
        elif ch == '"':
            in_string = True
            masked.append(" ")
        else:
            masked.append(ch)
    return "".join(masked)


def balanced(relative: str) -> str:
    source = read(relative)
    masked = strip_strings_and_comments(source)
    depth = 0
    for line_number, line in enumerate(masked.splitlines(), start=1):
        for ch in line:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    fail(f"Extra closing brace in {relative} line {line_number}")
                    return masked
    if depth:
        fail(f"Unclosed braces in {relative}: {depth}")
    return masked


CHECK_BRACES = [
    "common/idea_tags/00_idea.txt",
    "common/characters/SYR.txt",
    "common/country_leader/zzz_cwic_reworked_syr_military_staff.txt",
    "common/scripted_triggers/zzz_cwic_reworked_sf_doctrine_trigger.txt",
    "common/decisions/categories/CWICR_SYR_Categories.txt",
    "common/decisions/CWICR_SYR_State_Reforms.txt",
    "common/ideas/CWICR_SYR_State_Reforms.txt",
    "common/special_projects/projects/cwic_space_special_projects.txt",
    "common/national_focus/50s_SYR.txt",
    "common/national_focus/60s_SYR.txt",
    "history/countries/SYR - Syria.txt",
    "interface/topbar.gui",
]

masked = {name: balanced(name) for name in CHECK_BRACES}
idea = masked[CHECK_BRACES[0]]
characters = masked[CHECK_BRACES[1]]
history = masked[CHECK_BRACES[6]]
traits = masked[CHECK_BRACES[2]]

for required in (
    "character_slot = army_chief",
    "character_slot = navy_chief",
    "character_slot = air_chief",
    "character_slot = high_command",
    "character_slot = theorist",
):
    if required not in idea:
        fail(f"Missing advisor-slot assignment: {required}")
if idea.count("character_slot = high_command") != 3:
    fail("Expected exactly three high-command slots.")

roster = [
    "SYR_aram_karamanoukian",
    "SYR_fawzi_selu",
    "SYR_sami_alhinnawi",
    "SYR_adib_shishakli",
    "SYR_afif_albizri",
]
if not re.search(r"(?m)^load_focus_tree = 50s_SYR\s*$", history):
    fail("1949 Syrian history must explicitly load the 1950s focus tree")
if not re.search(r"(?m)^\s*1960\.1\.1\s*=\s*\{\s*\n\s*load_focus_tree = 60s_SYR", history):
    fail("1960 Syrian history must explicitly load the 1960s focus tree")

for token in roster:
    if not re.search(r"(?m)^\s*" + re.escape(token) + r"\s*=\s*\{", characters):
        fail(f"Missing Syrian character definition: {token}")
    if not re.search(r"\brecruit_character\s*=\s*" + re.escape(token) + r"\b", history):
        fail(f"Syrian character not recruited in history: {token}")

advisor_tokens = re.findall(r"\bidea_token\s*=\s*(CWIC_SYR_\w+)", characters)
if len(advisor_tokens) != 5 or len(set(advisor_tokens)) != 5:
    fail("Expected five unique CWIC Syrian advisor idea_token values.")

for trait in (
    "cwic_syr_defensive_staff",
    "cwic_syr_reform_staff",
    "cwic_syr_organisation_staff",
    "cwic_syr_offensive_staff",
):
    if not re.search(r"\b" + re.escape(trait) + r"\s*=\s*\{", traits):
        fail(f"Custom staff trait missing: {trait}")

# Ensure Syrian reform decisions, national spirits and localisation refer to each other.
policy_categories = masked["common/decisions/categories/CWICR_SYR_Categories.txt"]
policy_decisions = masked["common/decisions/CWICR_SYR_State_Reforms.txt"]
policy_ideas = masked["common/ideas/CWICR_SYR_State_Reforms.txt"]
policy_l10n = read("localisation/english/CWIC_Reworked_l_english.yml")

for category in ("CWICR_SYR_state_reform_category", "CWICR_SYR_defence_reform_category"):
    if not re.search(r"(?m)^\s*" + category + r"\s*=\s*\{", policy_categories):
        fail("Syrian policy category missing: " + category)
for decision in ("CWICR_SYR_budget_commission", "CWICR_SYR_irrigation_cooperatives",
                 "CWICR_SYR_officer_training", "CWICR_SYR_intelligence_review"):
    spirit = decision + "_idea"
    if not re.search(r"(?m)^\s*" + decision + r"\s*=\s*\{", policy_decisions):
        fail("Syrian policy decision missing: " + decision)
    if not re.search(r"(?m)^\s*" + spirit + r"\s*=\s*\{", policy_ideas):
        fail("Syrian policy idea missing: " + spirit)
    if not re.search(r"(?m)^\s*" + re.escape(decision) + r":0", policy_l10n):
        fail("Syrian decision localisation missing: " + decision)
    if not re.search(r"(?m)^\s*" + re.escape(spirit) + r":0", policy_l10n):
        fail("Syrian idea localisation missing: " + spirit)

# New doctrine focus rewards are XP, not removed legacy doctrine tech discounts.
expected_doctrine_xp = (
    ("common/national_focus/50s_SYR.txt", "add_air_experience", 10),
    ("common/national_focus/50s_SYR.txt", "add_army_experience", 10),
    ("common/national_focus/50s_SYR.txt", "add_navy_experience", 10),
    ("common/national_focus/60s_SYR.txt", "add_army_experience", 20),
)
for file, effect, amount in expected_doctrine_xp:
    if not re.search(r"(?m)^\s*" + effect + r"\s*=\s*" + str(amount) + r"\s*$", masked[file]):
        fail(f"Expected Syrian doctrine reward missing: {file} {effect}={amount}")
for file in ("common/national_focus/50s_SYR.txt", "common/national_focus/60s_SYR.txt"):
    if "add_doctrine_cost_reduction" in masked[file]:
        fail(f"Legacy Syrian doctrine reward remains in {file}")

# The La Resistance operative portrait pool was intentionally emptied
# upstream. Ensure the independent deterministic fallback still exists.
portraits = read("portraits/00_portraits.txt")
default_portrait = portraits.split("continent = {", 1)[0]
if not re.search(r"\boperative\s*=\s*\{", default_portrait):
    fail("Default operative portrait pool is missing.")
if "gfx/leaders/operative_unknown.dds" not in default_portrait:
    fail("Default operative portrait fallback sprite is missing.")

# The Buran launcher-project typo must not recur.
project_source = masked["common/special_projects/projects/cwic_space_special_projects.txt"]
if "sp_orbiter_sov_buran" not in project_source:
    fail("Soviet Buran special project is missing.")
if "sp_lv_sov_zenit" in project_source:
    fail("Undefined Soviet Zenit launcher parent still referenced.")

focus_ids: dict[str, str] = {}
focus_refs: list[tuple[str, str]] = []
for relative in ("common/national_focus/50s_SYR.txt", "common/national_focus/60s_SYR.txt"):
    source = masked[relative]
    if not re.search(r"(?m)^\s*focus_tree\s*=\s*\{", source):
        fail(f"No focus_tree declaration: {relative}")
    # The national focus entries have 'focus = {' followed by 'id ='.
    for match in re.finditer(r"(?m)^\s*focus\s*=\s*\{\s*\n\s*id\s*=\s*(SYR_[A-Za-z0-9_]+)", source):
        focus_id = match.group(1)
        if focus_id in focus_ids:
            fail(f"Duplicate Syrian focus {focus_id} ({focus_ids[focus_id]} and {relative})")
        focus_ids[focus_id] = relative
    for match in re.finditer(r"(?m)^\s*focus\s*=\s*(SYR_[A-Za-z0-9_]+)\b", source):
        focus_refs.append((relative, match.group(1)))
for relative, focus_id in focus_refs:
    if focus_id not in focus_ids:
        fail(f"Unknown Syrian prerequisite or exclusion in {relative}: {focus_id}")
if len(focus_ids) < 175:
    fail(f"Unexpectedly few restored Syrian focus entries: {len(focus_ids)}")

defines = read("common/defines/IC_Defines.lua")
for field in ("AGENCY_CREATION_DAYS", "AGENCY_UPGRADE_DAYS"):
    if not re.search(r"(?m)^NDefines\.NOperatives\." + field + r"\s*=\s*30\s*$", defines):
        fail(f"Agency timing override not 30: {field}")
if re.search(r"(?m)^NDefines\.NOperatives\.(?:MAX_RECRUITED_OPERATIVES|AGENCY_CREATION_FACTORIES)\s*=", defines):
    fail("Espionage-disabling override was reintroduced.")

# Use raw topbar content because quoted GUI object names are deliberately
# erased by the brace scanner.
topbar_original = read("interface/topbar.gui")
btn = re.search(r'name\s*=\s*"intel_agency_button".{0,350}', topbar_original, re.S)
if not btn or not re.search(r'position\s*=\s*\{\s*x\s*=\s*-49\s+y\s*=\s*0\s*\}', btn.group(0)):
    fail("Intel agency button was hidden again.")

for removed in ("interface/countryofficercorpview.gui",
                "interface/countrydoctrinetreeview.gui"):
    if (MOD / removed).exists():
        fail(f"Obsolete custom GUI override is active: {removed}")

for country_file, unsupported in (
    ("common/national_focus/BRA_50s.txt", "radio"),
    ("common/national_focus/DOM_49.txt", "screen_hull_light"),
    ("common/national_focus/HUN_60s_Kadar.txt", "electronic_mechanical_engineering"),
    ("common/national_focus/HUN_60s_Kadar.txt", "air_techs"),
):
    body = strip_strings_and_comments(read(country_file))
    if re.search(r"(?m)^\s*category\s*=\s*" + unsupported + r"\s*$", body):
        fail(f"Outdated research category {unsupported} in {country_file}")

# HOI4 1.19 owns the updated doctrine folder map (including special forces).
# A CWIC-era copy containing only land/naval/air would hide the new SF folder.
if (MOD / "common/doctrines/folders/doctrine_folders.txt").exists():
    fail("Outdated doctrine_folders.txt override still hides 1.19 special forces.")

# Resolve a logged duplicate decision and two logged undefined military traits.
for filename, token in (
    ("common/decisions/Cuban_Insurgency.txt", "CUB_bomb_insurgents"),
    ("common/decisions/DMC_Insurgency.txt", "DOM_bomb_insurgents"),
):
    source = strip_strings_and_comments(read(filename))
    if not re.search(r"(?m)^\s*" + token + r"\s*=\s*\{", source):
        fail(f"Unique insurgency decision missing: {token}")
for filename, obsolete in (
    ("common/national_focus/EGY_50s.txt", "incompetent"),
    ("common/national_focus/GDR_1953_Reimann.txt", "infant_ryofficer"),
):
    source = strip_strings_and_comments(read(filename))
    if re.search(r"\b" + obsolete + r"\b", source):
        fail(f"Unsupported officer trait remains in {filename}: {obsolete}")

for category, filename in (
    ("grand_doctrines", "land_grand_doctrines.txt"),
    ("grand_doctrines", "air_grand_doctrines.txt"),
    ("grand_doctrines", "sea_grand_doctrines.txt"),
    ("tracks", "land_doctrine_tracks.txt"),
    ("tracks", "air_doctrine_track.txt"),
    ("tracks", "sea_doctrine_tracks.txt"),
    ("tracks", "special_forces_tracks.txt"),
):
    path = MOD / "common" / "doctrines" / category / filename
    if path.exists() and path.stat().st_size == 0:
        fail(f"Empty doctrine override suppresses vanilla content: {path.relative_to(MOD)}")

trigger = masked["common/scripted_triggers/zzz_cwic_reworked_sf_doctrine_trigger.txt"]
if not re.search(r"\bcan_unlock_second_track_of_sf_doctrine\s*=\s*\{", trigger):
    fail("Special forces second-track scripted trigger missing.")

descriptor = read("descriptor.mod")
if re.search(r'(?m)^\s*path\s*=', descriptor):
    fail("descriptor.mod includes a machine-specific absolute path.")
if "supported_version=\"1.19.*\"" not in descriptor:
    warn("Check HOI4 1.19 target in descriptor.mod.")

print(f"Syrian focus definitions: {len(focus_ids)}")
print(f"Syrian focus references: {len(focus_refs)}")
print(f"Syrian advisor tokens: {len(advisor_tokens)}")
for issue in warnings:
    print("WARNING:", issue)
for issue in errors:
    print("ERROR:", issue)
if errors:
    print(f"FAIL: {len(errors)} static issue(s).")
    sys.exit(1)
print("PASS: selected static checks. HOI4 runtime test still required.")
