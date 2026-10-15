#!/usr/bin/env python3
"""Source audit for new Syrian urban construction, intelligence and PMC paths.

Non-runtime verification only. Run from this repository's root. It verifies
registered decision categories, known Syria state IDs, existing building types,
technology dependencies, scripted opinion/idea references, and localisation.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent / "Cold War Iron Curtain"
failures: list[str] = []


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        failures.append("File missing: " + path)
        return ""
    return target.read_text(encoding="utf-8-sig")


def code_only(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def contains_def(source: str, key: str) -> bool:
    return bool(re.search(r"(?m)^\s*" + re.escape(key) + r"\s*=\s*\{", source))


def balance(source: str, name: str) -> None:
    depth = 0
    quote = False
    escaped = False
    for line_no, line in enumerate(source.splitlines(), 1):
        line = line.split("#", 1)[0]
        for ch in line:
            if quote:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quote = False
                continue
            if ch == '"':
                quote = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    failures.append(f"Extra brace: {name}:{line_no}")
                    return
    if depth != 0:
        failures.append(f"Unbalanced braces in {name}: {depth}")


folders = {
    "cities": "common/decisions/CWICR_SYR_City_Construction.txt",
    "security": "common/decisions/CWICR_SYR_Intelligence_and_Contractors.txt",
    "category": "common/decisions/categories/CWICR_SYR_Categories.txt",
    "ideas": "common/ideas/CWICR_SYR_Security_Contractors.txt",
    "events": "events/CWICR_SYR_Security_Diplomacy.txt",
    "opinion": "common/opinion_modifiers/CWICR_SYR_Security_Reactions.txt",
}
raw = {key: read(path) for key, path in folders.items()}
src = {key: code_only(data) for key, data in raw.items()}
for key, data in raw.items():
    balance(data, folders[key])

loc = read("localisation/english/CWICR_SYR_Cities_Security_l_english.yml")
techs = read("common/technologies/CWICR_SYR_Research.txt")
building_rules = (read("common/buildings/00_buildings.txt")
                  + read("common/buildings/00__societalbuildings.txt"))
if not loc.startswith("\ufeffl_english:") and not loc.startswith("l_english:"):
    failures.append("New English localisation header missing")

categories = (
    "CWICR_SYR_city_construction_category",
    "CWICR_SYR_security_directorate_category",
    "CWICR_SYR_private_contractors_category",
)
for cat in categories:
    if not contains_def(src["category"], cat):
        failures.append("Unregistered category: " + cat)
    target = src["cities"] if "city_" in cat else src["security"]
    if not contains_def(target, cat):
        failures.append("Category has no decisions: " + cat)
    if not re.search(r"(?m)^\s*" + re.escape(cat) + r":0\s+", loc):
        failures.append("Category localisation missing: " + cat)

projects = (
    ("damascus_administration", 554, "office_park", "CWICR_SYR_vocational_1949"),
    ("aleppo_industrial_estate", 677, "industrial_complex", "CWICR_SYR_industry_1958"),
    ("homs_defence_workshops", 893, "arms_factory", "CWICR_SYR_machine_tools_1968"),
    ("hama_agro_processing", 895, "agri_industrial_complex", "CWICR_SYR_irrigation_1957"),
    ("latakia_port_modernisation", 809, "dockyard", None),
    ("deir_waterworks", 680, "water_infrastructure", "CWICR_SYR_euphrates_1970"),
    ("hasakah_rural_cooperatives", 777, "agri_industrial_complex", "CWICR_SYR_irrigation_1957"),
    ("rif_dimashq_signal_station", 2046, "radar_station", "CWICR_SYR_air_defence_network_1972"),
)
for short, state, building, tech in projects:
    decision = "CWICR_SYR_URB_" + short
    if not contains_def(src["cities"], decision):
        failures.append("Missing city construction decision: " + decision)
    if not list((ROOT / "history/states").glob(f"{state}-*.txt")):
        failures.append("Unknown state ID " + str(state))
    if not contains_def(building_rules, building):
        failures.append("Unknown CWIC building type " + building)
    for marker in (
        f"{state} = {{ is_owned_and_controlled_by = SYR }}",
        f"type = {building}",
        "subtract_from_variable",
        "days_remove = 120",
        "fire_only_once = yes",
    ):
        if marker not in src["cities"]:
            failures.append("Missing construction safeguard: " + decision + " " + marker)
    if tech and not contains_def(code_only(techs), tech):
        failures.append("Undefined Syrian prerequisite " + tech)
    for key in (decision, decision + "_desc"):
        if not re.search(r"(?m)^\s*" + re.escape(key) + r":0\s+", loc):
            failures.append("City localisation missing " + key)

decision_names = (
    "CWICR_SYR_INT_build_central_directorate",
    "CWICR_SYR_INT_expand_foreign_stations",
    "CWICR_SYR_INT_satellite_analysis_network",
    "CWICR_SYR_PMC_regulation",
    "CWICR_SYR_PMC_lebanese_security_contract",
    "CWICR_SYR_PMC_iraqi_training_contract",
)
for decision in decision_names:
    if not contains_def(src["security"], decision):
        failures.append("Missing intelligence/PMC decision: " + decision)
    if not re.search(r"(?m)^\s*" + re.escape(decision) + r":0\s+", loc):
        failures.append("Security decision localisation missing " + decision)
    if not re.search(r"(?m)^\s*" + re.escape(decision + "_desc") + r":0\s+", loc):
        failures.append("Security decision description missing " + decision)

idea_names = (
    "CWICR_SYR_INT_directorate_idea",
    "CWICR_SYR_INT_regional_network_idea",
    "CWICR_SYR_INT_advanced_analysis_idea",
    "CWICR_SYR_PMC_regulated_idea",
    "CWICR_SYR_PMC_host_advisers_idea",
    "CWICR_SYR_PMC_export_office_idea",
)
for idea in idea_names:
    if not contains_def(src["ideas"], idea):
        failures.append("Missing national spirit " + idea)
    if idea not in src["security"] and idea not in src["events"]:
        failures.append("Unused national spirit " + idea)
    if not re.search(r"(?m)^\s*" + re.escape(idea) + r":0\s+", loc):
        failures.append("Missing idea localisation " + idea)

for number in range(1, 6):
    event = "CWICR_SYR_SEC." + str(number)
    if not re.search(r"(?m)^\s*id\s*=\s*" + re.escape(event) + r"\s*$", src["events"]):
        failures.append("Missing security world event: " + event)
    if event not in src["security"]:
        failures.append("Security event has no decision call: " + event)
    for key in (event + ".t", event + ".d", event + ".a"):
        if not re.search(r"(?m)^\s*" + re.escape(key) + r":0\s+", loc):
            failures.append("World event localisation missing " + key)
    if number != 3 and not re.search(r"(?m)^\s*" + re.escape(event + ".b") + r":0\s+", loc):
        failures.append("World event refusal or alternative missing: " + event)

for mod in (
    "CWICR_SYR_SEC_intelligence_concern",
    "CWICR_SYR_SEC_security_dialogue",
    "CWICR_SYR_SEC_host_contract",
    "CWICR_SYR_SEC_contract_refused",
):
    if not contains_def(src["opinion"], mod):
        failures.append("Opinion modifier is missing " + mod)
    if mod not in src["events"]:
        failures.append("Opinion modifier is never used " + mod)
    if not re.search(r"(?m)^\s*" + re.escape(mod) + r":0\s+", loc):
        failures.append("Opinion modifier localisation missing " + mod)

# Security and contractor modifiers must not simply spawn foreign units, transfer
# provinces, or grant strategic weapons; foreign partners have a decline option.
for forbidden in ("annex_country =", "transfer_state =", "add_nukes =",
                  "add_equipment_to_stockpile =", "create_unit ="):
    if forbidden in src["security"] + src["events"]:
        failures.append("Unsafe unpriced security effect: " + forbidden)
if len(re.findall(r"\boperative_slot\s*=\s*1\b", src["ideas"])) != 3:
    failures.append("Intelligence progression does not define exactly three upgrades.")

for err in failures:
    print("ERROR:", err)
if failures:
    sys.exit(1)
print("PASS: 8 map-grounded Syrian construction projects, 6 security/PMC decisions,")
print("      6 national spirits, 5 international events, and localisation cross-references.")
print("NOTE: Source checks are NOT gameplay/HOI4 UI validation.")
