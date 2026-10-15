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
    "common/decisions/categories/00_decision_categories.txt",
    "common/decisions/categories/CWICR_SYR_Categories.txt",
    "common/decisions/CWICR_SYR_State_Reforms.txt",
    "common/ideas/CWICR_SYR_State_Reforms.txt",
    "common/decisions/CWICR_SYR_Political_Economy_Diplomacy.txt",
    "common/decisions/CWICR_SYR_Regional_Initiatives.txt",
    "common/ideas/CWICR_SYR_Regional_Agreements.txt",
    "events/CWICR_SYR_Regional_Initiatives.txt",
    "common/ideas/CWICR_SYR_Institutions_and_Policies.txt",
    "common/opinion_modifiers/CWICR_SYR_Diplomatic_Reactions.txt",
    "events/CWICR_SYR_Institutional_Choices.txt",
    "common/technologies/CWICR_SYR_Research.txt",
    "common/special_projects/projects/cwic_space_special_projects.txt",
    "common/national_focus/50s_SYR.txt",
    "common/national_focus/60s_SYR.txt",
    "history/countries/SYR - Syria.txt",
    "interface/topbar.gui",
]

masked = {name: balanced(name) for name in CHECK_BRACES}
idea = masked[CHECK_BRACES[0]]
characters = masked[CHECK_BRACES[1]]
history = masked["history/countries/SYR - Syria.txt"]
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

# Second-stage Syria diplomacy, economy, constitutional institutions and civilian
# nuclear feasibility: make every referenced idea/event/opinion modifier resolvable.
new_decisions = masked["common/decisions/CWICR_SYR_Political_Economy_Diplomacy.txt"]
new_ideas = masked["common/ideas/CWICR_SYR_Institutions_and_Policies.txt"]
new_events = masked["events/CWICR_SYR_Institutional_Choices.txt"]
new_diplomacy = masked["common/opinion_modifiers/CWICR_SYR_Diplomatic_Reactions.txt"]
new_l10n = read("localisation/english/CWICR_SYR_Policy_l_english.yml")

policy_choices = (
    "CWICR_SYR_constitutional_bargain", "CWICR_SYR_development_model",
    "CWICR_SYR_anti_corruption_audit", "CWICR_SYR_arab_consultations",
    "CWICR_SYR_un_mediation_dossier", "CWICR_SYR_displaced_families_services",
    "CWICR_SYR_nuclear_feasibility",
)
new_categories = (
    "CWICR_SYR_institutions_category", "CWICR_SYR_economic_paths_category",
    "CWICR_SYR_diplomacy_category", "CWICR_SYR_strategic_programme_category",
)
new_spirits = (
    "CWICR_SYR_civilian_compact_idea", "CWICR_SYR_army_guardianship_idea",
    "CWICR_SYR_public_development_idea", "CWICR_SYR_regulated_enterprise_idea",
    "CWICR_SYR_rural_credit_idea", "CWICR_SYR_displaced_families_idea",
    "CWICR_SYR_nuclear_safeguards_idea", "CWICR_SYR_nuclear_opaque_idea",
)
new_opinions = (
    "CWICR_SYR_regional_consultation", "CWICR_SYR_un_dialogue",
    "CWICR_SYR_open_safeguards", "CWICR_SYR_opaque_programme",
)

for category in new_categories:
    if not re.search(r"(?m)^\s*" + category + r"\s*=\s*\{", policy_categories):
        fail("Syria category registration missing: " + category)
    if not re.search(r"(?m)^\s*" + category + r"\s*=\s*\{", new_decisions):
        fail("Syria decisions category missing: " + category)
for decision in policy_choices:
    if not re.search(r"(?m)^\s*" + decision + r"\s*=\s*\{", new_decisions):
        fail("Syria policy decision missing: " + decision)
for idea_name in new_spirits:
    if not re.search(r"(?m)^\s*" + idea_name + r"\s*=\s*\{", new_ideas):
        fail("Syria policy spirit missing: " + idea_name)
for modifier in new_opinions:
    if not re.search(r"(?m)^\s*" + modifier + r"\s*=\s*\{", new_diplomacy):
        fail("Syria diplomatic opinion missing: " + modifier)
for event_id, options in ((1, 2), (2, 3), (3, 2)):
    full = "CWICR_SYR." + str(event_id)
    if not re.search(r"\bid\s*=\s*" + re.escape(full) + r"\b", new_events):
        fail("Syria policy event missing: " + full)
    if not re.search(r"\bid\s*=\s*" + re.escape(full) + r"\b", new_decisions):
        fail("Syria policy decision does not call event: " + full)
    for suffix in (".t", ".d", *(f".{chr(ord('a') + n)}" for n in range(options))):
        key = full + suffix
        if not re.search(r"(?m)^\s*" + re.escape(key) + r":0", new_l10n):
            fail("Syria policy event localisation missing: " + key)
for key in (*new_categories, *policy_choices, *new_spirits, *new_opinions):
    if not re.search(r"(?m)^\s*" + re.escape(key) + r":0", new_l10n):
        fail("Syria policy localisation missing: " + key)

# Does not equate a UN mediation dossier with UN Council mechanics,
# or feasibility with production of a nuclear weapon.
if not re.search(r"\bhas_tech\s*=\s*atomic_research\b", new_decisions):
    fail("The Syrian nuclear feasibility decision must require atomic research.")
if not re.search(r"\bdate\s*>\s*1969\.12\.31", new_decisions):
    fail("The Syrian nuclear feasibility programme should not start before 1970.")
if re.search(r"\b(add_nukes|add_equipment_to_stockpile)\s*=", new_decisions + new_events):
    fail("The Syrian feasibility decision must not grant weapons or stockpiles.")

# Syrian technology tab: unique identifiers, game-defined tech categories,
# nine sprites, three visible roots, UI templates and localisation.
syrian_techs = [
    "CWICR_SYR_hydrology_1949", "CWICR_SYR_irrigation_1957",
    "CWICR_SYR_euphrates_1970", "CWICR_SYR_vocational_1949",
    "CWICR_SYR_industry_1958", "CWICR_SYR_machine_tools_1968",
    "CWICR_SYR_signal_corps_1950", "CWICR_SYR_staff_college_1962",
    "CWICR_SYR_air_defence_network_1972",
    "CWICR_SYR_satellite_reception_1968", "CWICR_SYR_meteorology_1978",
    "CWICR_SYR_earth_observation_1988",
]
syrian_tech = masked["common/technologies/CWICR_SYR_Research.txt"]
technology_categories = read("common/technology_tags/00_technology.txt")
technology_gui = read("interface/countrytechtreeview.gui")
technology_gfx = read("interface/CWICR_SYR_Research.gfx")
technology_loc = read("localisation/english/CWICR_SYR_Research_l_english.yml")
for tech in syrian_techs:
    if len(re.findall(r"(?m)^\s*" + tech + r"\s*=\s*\{", syrian_tech)) != 1:
        fail("Syrian applied technology missing or duplicated: " + tech)
    if ('name = "GFX_' + tech + '_medium"') not in technology_gfx:
        fail("Syrian technology icon missing: " + tech)
    for key in (tech, tech + "_desc"):
        if not re.search(r"(?m)^\s*" + key + r":0\s+\"", technology_loc):
            fail("Syrian technology localization missing: " + key)
for first in ("CWICR_SYR_hydrology_1949", "CWICR_SYR_vocational_1949",
              "CWICR_SYR_signal_corps_1950", "CWICR_SYR_satellite_reception_1968"):
    if ('name = "' + first + '_tree"') not in technology_gui:
        fail("Syrian technology root gridbox absent in research GUI: " + first)
if syrian_tech.count("allow_branch = { original_tag = SYR }") != 4:
    fail("Expected four Syrian-only research branch gates")
if syrian_tech.count("allow = { original_tag = SYR }") != 12:
    fail("Expected all twelve Syrian research technologies to be tag-gated")
for key in ("cwicr_syr_research_folder", "cwicr_syr_research_folder_tab",
            "techtree_cwicr_syr_research_folder_item"):
    if key not in technology_gui:
        fail("Custom Syrian research interface element missing: " + key)
if not re.search(r"cwicr_syr_research_folder\s*=\s*\{\s*available\s*=\s*\{\s*original_tag\s*=\s*SYR", technology_categories):
    fail("Syrian research folder not gated by original_tag")
for label in ("CWICR_SYR_RESEARCH_TITLE", "CWICR_SYR_HYDRO_HEADING",
              "CWICR_SYR_INDUSTRY_HEADING", "CWICR_SYR_DEFENCE_HEADING",
              "CWICR_SYR_SPACE_SERVICES_HEADING",
              "CWICR_SYR_TECH_TAB"):
    if not re.search(r"(?m)^\s*" + label + r":0\s+\"", technology_loc):
        fail("Syrian research interface localization missing: " + label)

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
if "gfx/leaders/leader_unknown.dds" not in default_portrait:
    fail("Default operative portrait fallback sprite is missing.")
if not (MOD / "gfx/leaders/leader_unknown.dds").is_file():
    fail("Operative portrait fallback points to an absent DDS file.")

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

# The two full-width economic banners in older CWIC were obscuring
# instructional and financial text in the user's Decisions screenshot.
# Preserve legibility: category icons stay, banner images are disabled.
econ_source = read("common/decisions/categories/00_decision_categories.txt")
for cat in ("economy_decisions", "economy_decisions_reenable", "economic_investments"):
    start = re.search(r"(?m)^" + cat + r"\s*=\s*\{", econ_source)
    if not start:
        fail("Economy decision category missing: " + cat)
        continue
    preview = econ_source[start.end(): start.end() + 230]
    if re.search(r"(?m)^\s*picture\s*=", preview):
        fail("Economic decision image overlay regression: " + cat)

# Syria's bilateral and global decisions must be exclusive to Syria.
regional_decisions = masked["common/decisions/CWICR_SYR_Regional_Initiatives.txt"]
regional_events = masked["events/CWICR_SYR_Regional_Initiatives.txt"]
regional_ideas = masked["common/ideas/CWICR_SYR_Regional_Agreements.txt"]
regional_modifiers = masked["common/opinion_modifiers/CWICR_SYR_Diplomatic_Reactions.txt"]
regional_categories = masked["common/decisions/categories/CWICR_SYR_Categories.txt"]
regional_loc = read("localisation/english/CWICR_SYR_Regional_Initiatives_l_english.yml")

regional_decision_ids = (
    "CWICR_SYR_levante_trade_corridor",
    "CWICR_SYR_euphrates_water_dialogue",
    "CWICR_SYR_jordan_border_commission",
    "CWICR_SYR_egypt_technical_exchange",
    "CWICR_SYR_two_bloc_non_alignment_dialogue",
    "CWICR_SYR_golan_observation_request",
    "CWICR_SYR_tripartite_euphrates_conference",
    "CWICR_SYR_regional_relief_conference",
)
if not re.search(r"\bCWICR_SYR_regional_initiatives_category\s*=\s*\{", regional_categories):
    fail("Syria-exclusive regional initiatives category missing.")
for decision in regional_decision_ids:
    if not re.search(r"(?m)^\s*" + decision + r"\s*=\s*\{", regional_decisions):
        fail("Missing international Syrian decision: " + decision)
    if not re.search(r"(?m)^\s*" + decision + r":0\s+", regional_loc):
        fail("Missing Syrian international decision translation: " + decision)
if len(re.findall(r"\ballowed\s*=\s*\{\s*original_tag\s*=\s*SYR\s*\}", regional_decisions)) != len(regional_decision_ids):
    fail("Every Syria-exclusive international decision must have an explicit tag restriction.")
if "CWICR_SYR_regional_initiatives_category" not in regional_decisions:
    fail("Syria regional decision category is not linked to the decisions.")

for event_number in range(1, 16):
    event = f"CWICR_SYR_REG.{event_number}"
    if not re.search(r"(?m)^\s*id\s*=\s*" + re.escape(event) + r"\s*$", regional_events):
        fail("Syrian international event not defined: " + event)
    callsites = regional_decisions + regional_events
    if len(re.findall(r"\bid\s*=\s*" + re.escape(event) + r"\b", callsites)) < 2:
        fail("Syrian international event not called by decisions/events: " + event)
    for key in (event + ".t", event + ".d", event + ".a"):
        if not re.search(r"(?m)^\s*" + re.escape(key) + r":0\s+", regional_loc):
            fail("Missing international event text: " + key)
    if event_number in (1, 2, 3, 4, 5, 6, 8, 11, 12, 13):
        key = event + ".b"
        if not re.search(r"(?m)^\s*" + re.escape(key) + r":0\s+", regional_loc):
            fail("Missing international event choice: " + key)
for idea_name in (
    "CWICR_SYR_transit_agreement_idea", "CWICR_SYR_water_commission_idea",
    "CWICR_SYR_observation_liaison_idea", "CWICR_SYR_tripartite_water_idea",
    "CWICR_SYR_regional_relief_idea",
):
    if not re.search(r"\b" + idea_name + r"\s*=\s*\{", regional_ideas):
        fail("Missing regional cooperation idea: " + idea_name)
    if not re.search(r"(?m)^\s*" + idea_name + r":0\s+", regional_loc):
        fail("Missing regional idea description: " + idea_name)
for modifier in (
    "CWICR_SYR_transit_partners", "CWICR_SYR_diplomatic_refusal",
    "CWICR_SYR_water_partners", "CWICR_SYR_water_dispute",
    "CWICR_SYR_border_partners", "CWICR_SYR_science_partners",
    "CWICR_SYR_balanced_outreach", "CWICR_SYR_bloc_suspicion",
    "CWICR_SYR_observation_cooperation", "CWICR_SYR_observation_refusal",
    "CWICR_SYR_tripartite_water_partners", "CWICR_SYR_relief_partners",
):
    if not re.search(r"\b" + modifier + r"\s*=\s*\{", regional_modifiers):
        fail("Missing Syrian international opinion modifier: " + modifier)
    if not re.search(r"(?m)^\s*" + modifier + r":0\s+", regional_loc):
        fail("Missing international opinion modifier translation: " + modifier)

# Syria's new world-facing actions must retain foreign consent and no
# direct territorial, military or nuclear grants. Partners can decline.
for country, event in (("ISR", "CWICR_SYR_REG.8"),
                       ("TUR", "CWICR_SYR_REG.11"),
                       ("LEB", "CWICR_SYR_REG.12"),
                       ("JOR", "CWICR_SYR_REG.13")):
    if not re.search(r"\b" + country + r"\s*=\s*\{\s*country_event\s*=\s*\{\s*id\s*=\s*" +
                     re.escape(event), regional_decisions):
        fail(f"Required independent recipient response missing: {country} -> {event}")
for item in ("CWICR_SYR_golan_observation_request",
             "CWICR_SYR_tripartite_euphrates_conference",
             "CWICR_SYR_regional_relief_conference"):
    if not re.search(r"\b" + item + r"\s*=\s*\{", regional_decisions):
        fail("New Syria-only international initiative missing: " + item)
if re.search(r"\b(transfer_state|annex_country|add_nukes|add_equipment_to_stockpile)\s*=",
             regional_decisions + regional_events):
    fail("International Syria diplomacy must not directly annex land or create weapons.")
event_ids = re.findall(r"(?m)^\s*id\s*=\s*(CWICR_SYR_REG\.\d+)\s*$", regional_events)
if len(event_ids) != len(set(event_ids)) or len(event_ids) != 15:
    fail("Syrian foreign-policy event IDs must be unique and cover 1 through 15.")

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
