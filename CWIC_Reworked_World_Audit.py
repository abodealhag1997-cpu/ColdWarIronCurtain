#!/usr/bin/env python3
"""Static audit of Syrian international-response content for CWIC Reworked.

This checks file references and broadcast flags, not HOI4 runtime validity.
Run from the repository root: python CWIC_Reworked_World_Audit.py
"""
from pathlib import Path
import re
import sys

MOD = Path(__file__).resolve().parent / "Cold War Iron Curtain"
errors = []


def read(path):
    file = MOD / path
    if not file.is_file():
        errors.append(f"Missing file: {path}")
        return ""
    return file.read_text(encoding="utf-8-sig")


def require(ok, message):
    if not ok:
        errors.append(message)


def stripped(source):
    return "\n".join(line.split("#", 1)[0] for line in source.splitlines())


def balanced(source):
    depth, quoted, escaped, commented = 0, False, False, False
    for ch in source:
        if commented:
            if ch == "\n":
                commented = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == "#":
            commented = True
        elif ch == '"':
            quoted = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not quoted


decision_src = read("common/decisions/CWICR_SYR_South_South_Cooperation.txt")
event_src = read("events/CWICR_SYR_South_South_Cooperation.txt")
ideas_src = read("common/ideas/CWICR_SYR_South_South_Cooperation.txt")
local_src = read("localisation/english/CWICR_SYR_South_South_l_english.yml")
regional_src = read("events/CWICR_SYR_Regional_Initiatives.txt")
regional_decisions = read("common/decisions/CWICR_SYR_Regional_Initiatives.txt")

for path, source in (
    ("South-South decision", decision_src),
    ("South-South events", event_src),
    ("South-South ideas", ideas_src),
    ("regional events", regional_src),
    ("regional decisions", regional_decisions),
):
    require(balanced(source), f"Unbalanced braces in {path}")

require("add_namespace = CWICR_SYR_SSC" in event_src, "Missing South-South event namespace")
require("allowed = { original_tag = SYR }" in decision_src, "Syria-only eligibility is missing")
require("date > 1961.9.1" in decision_src, "1961 timing gate missing")
require("exists = YUG" in decision_src and "exists = RAJ" in decision_src,
        "Recipient existence checks missing")

defined = set(re.findall(
    r"(?m)^(?:country_event|news_event)\s*=\s*\{\s*\n\s*id\s*=\s*(CWICR_SYR_SSC\.\d+)",
    event_src,
))
require(defined == {f"CWICR_SYR_SSC.{i}" for i in range(1, 5)},
        f"Unexpected South-South event IDs: {sorted(defined)}")
invoked = set(re.findall(r"\bid\s*=\s*(CWICR_SYR_SSC\.\d+)", decision_src))
require(invoked == {"CWICR_SYR_SSC.1", "CWICR_SYR_SSC.2", "CWICR_SYR_SSC.3"},
        "Decision does not schedule all three country responses")

require("YUG = { country_event" in decision_src, "Yugoslav response not delivered")
require("RAJ = { country_event" in decision_src, "Indian response not delivered")
require("days = 9" in decision_src and "days = 2" in decision_src,
        "Outcome timer must follow foreign reply timers")
require("CWICR_SYR_SSC_YUG_accepted" in event_src, "Missing Yugoslav consent")
require("CWICR_SYR_SSC_RAJ_accepted" in event_src, "Missing Indian consent")
require("CWICR_SYR_SSC_failed" in event_src, "Missing refused-response outcome")
require("add_ideas = CWICR_SYR_SSC_joint_training_idea" in event_src,
        "Cooperation lacks shared substantive effect")
require(re.search(r"\bCWICR_SYR_SSC_joint_training_idea\s*=\s*\{", ideas_src),
        "Missing joint research idea")

for event_id in sorted(defined):
    for suffix in (".t", ".d"):
        require(f" {event_id}{suffix}:0" in local_src,
                f"Missing event localization: {event_id}{suffix}")
for key in (
    "CWICR_SYR_SSC.1.a", "CWICR_SYR_SSC.1.b",
    "CWICR_SYR_SSC.2.a", "CWICR_SYR_SSC.2.b",
    "CWICR_SYR_SSC.3.a", "CWICR_SYR_SSC.4.a",
    "CWICR_SYR_south_south_science_invitations",
    "CWICR_SYR_SSC_joint_training_idea",
):
    require(f" {key}:0" in local_src, f"Missing localization: {key}")

# HOI4 news_event needs major=yes and no fire_only_once=yes for world-wide
# distribution. Only inspect top-level news blocks, not 'news_event' effects.
for label, source in (
    ("regional", regional_src),
    ("South-South", event_src),
):
    blocks = re.findall(
        r"(?ms)^news_event\s*=\s*\{\s*(.*?)(?=^news_event\s*=\s*\{|^country_event\s*=\s*\{|\Z)",
        source,
    )
    require(bool(blocks), f"No {label} news events")
    for block in blocks:
        match = re.search(r"\bid\s*=\s*(CWICR_SYR_(?:REG|SSC)\.\d+)", block)
        event_id = match.group(1) if match else f"{label} unknown event"
        require(re.search(r"(?m)^\s*major\s*=\s*yes\s*$", block),
                f"News not set to major: {event_id}")
        require(not re.search(r"(?m)^\s*fire_only_once\s*=\s*yes\s*$", block),
                f"News broadcast suppressed by fire_only_once: {event_id}")

# Syrian treasury decisions integrate with CWIC's existing currentMoney
# balance, not a second bespoke currency variable or free political bonuses.
treasury_decisions = read("common/decisions/CWICR_SYR_Treasury_Projects.txt")
treasury_ideas = read("common/ideas/CWICR_SYR_Treasury_Projects.txt")
treasury_loc = read("localisation/english/CWICR_SYR_Treasury_l_english.yml")
require(balanced(treasury_decisions), "Unbalanced Syrian treasury decisions")
require(balanced(treasury_ideas), "Unbalanced Syrian treasury ideas")
treasury = {
    "CWICR_SYR_treasury_industrial_credit": (12, 1095),
    "CWICR_SYR_treasury_water_investment": (8, 730),
    "CWICR_SYR_treasury_defence_procurement": (10, 730),
}
for key, (cash, days) in treasury.items():
    require(bool(re.search(r"\b" + key + r"\s*=\s*\{", treasury_decisions)),
            f"Missing treasury decision: {key}")
    require(bool(re.search(r"\b" + key + r"_idea\s*=\s*\{", treasury_ideas)),
            f"Missing treasury idea: {key}")
    require(f" {key}:0" in treasury_loc, f"Missing treasury decision localization: {key}")
    require(f" {key}_idea:0" in treasury_loc, f"Missing treasury spirit localization: {key}")
    # Only check the current project block: previous and next projects must
    # not be mistaken for evidence that this project pays its own bill.
    block = treasury_decisions.split(key + " = {", 1)[-1].split(
        "\n    CWICR_SYR_", 1
    )[0]
    require("allowed = { original_tag = SYR }" in block,
            f"Treasury decision not restricted to Syria: {key}")
    require(f"value = {cash} compare = greater_than_or_equals" in block,
            f"Missing cash threshold: {key}")
    require(f"subtract_from_variable = {{ currentMoney = {cash} }}" in block,
            f"Cash was not charged to the existing CWIC treasury: {key}")
    require(f"idea = {key}_idea days = {days}" in block,
            f"Missing timed benefit: {key}")
    require("fire_only_once = yes" in block, f"Repeat-farming risk: {key}")

if errors:
    for item in errors:
        print("ERROR:", item)
    print(f"FAIL: {len(errors)} international-system source check(s)")
    sys.exit(1)
print("PASS: Syrian external response events, localization, news broadcast flags")
print("NOTE: runtime visibility, AI behaviour and diplomatic balance NOT verified")
