# CWIC Reworked — single-session integration test (NOT YET EXECUTED)

Target: **Hearts of Iron IV 1.19.3**, No Step Back and La Résistance
enabled, with **CWIC Reworked only**. Do not enable the Steam
Workshop original concurrently.

This is a pre-release quality checklist. A clean source audit is not a
substitute for completing this test. Run it once after the development
batch has stabilized; do **not** launch HOI4 after each individual edit.

## A. Before starting the game

- [ ] Keep a backup of the existing Workshop mod and save games.
- [ ] Check the repository branch is `cwic-reworked`, not
      `development-branch`.
- [ ] Execute `python CWIC_Reworked_Validate.py`,
      `python CWIC_Reworked_Research_Audit.py`, and
      `python CWIC_Reworked_World_Audit.py`.
- [ ] Register the GitHub checkout with `Install-CWIC-Reworked.ps1`
      **after** checking its path. Leave Workshop files untouched.
- [ ] Empty or back up old `error.log` before testing, so stale errors
      are not mistaken for new ones.

## B. One interactive test session

- [ ] Start a **new 1949 Syrian campaign**.
- [ ] Confirm the 1950s Syria focus tree loads, with selectable focuses,
      working focus rewards and no duplicate-tree selection.
- [ ] Open Officer Corps and test army, navy, air and high-command
      adviser slots. Record empty positions and misplaced UI elements.
- [ ] Open land, naval and air grand doctrines and the special-forces
      doctrine view; verify visibility, XP costs and unlock conditions.
- [ ] Open every research tab (not just the Syria tab). In particular
      verify whether blank tabs also occur on a Western power and
      another minor country. The old 53-tech space research folder was
      deliberately removed upstream in favour of special projects:
      verify the **Projects/Facilities** view separately.
- [ ] Open the Syrian-only research tab. Verify nine technology icons,
      three prerequisite branches, research durations and year penalties.
- [ ] Test intel agency creation, first upgrade, agent recruitment and
      availability of a valid portrait. The creation/upgrade durations
      should both be 30 days.
- [ ] Open **Economic Decisions** and **Economic Investments**; verify
      descriptions do not overlap pictures or other UI.
- [ ] Verify Syrian-only categories for institutions, economy,
      regional initiatives, strategic programmes, and treasury projects.
      Verify they do not appear as actionable Syrian initiatives for
      other countries.
- [ ] Verify treasury decisions use **currentMoney** thresholds of
      12, 8 and 10 and deduct those exact amounts. Ensure no decisions
      activate when the player lacks money, and that ideas expire.
- [ ] Test Syria's 1961+ South-South scientific invitation in a
      controlled state (use test saves/console only if necessary).
      Confirm YUG and RAJ can **independently** accept or refuse;
      a joint idea appears only if both accept, otherwise no shared
      research reward. Check world news is visible to other countries.
- [ ] Verify earlier initiatives: LEB transit, IRQ water, EGY exchange,
      TUR tripartite talks, Jordan border and Syrian superpower outreach.
- [ ] Save and reload the campaign; check idea durations and diplomatic
      decisions persist correctly.
- [ ] Start a **new 1960 Syrian campaign** and ensure the intended 1960s
      tree is chosen from history.
- [ ] Start or switch to USA and a non-Syrian minor (e.g., EGY) to
      check grand doctrines, research tabs, UI spacing and espionage
      remain functional outside Syria.

## C. Collect once at the end

After exiting HOI4, preserve `Documents/Paradox Interactive/Hearts of
Iron IV/logs/error.log` and `game.log` plus a clear screenshot of
any missing or overlapping UI. For any failing step, record:

- Country, start date, and game date
- Enabled DLC and exact version from the main menu
- Tab / event / decision name
- Expected vs actual result and one screenshot
- The last 10–20 relevant lines from the new log

## Release rule

Do **not** label this project compatible or error-free until this
single-session checklist passes. Any failure becomes a GitHub issue or
tracked fix, not an unrecorded local edit. A second test should be
reserved for verifying identified failures after the integrated patch,
not random trial and error.
