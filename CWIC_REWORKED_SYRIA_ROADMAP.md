# CWIC Reworked — Syria 1949–1991 development specification

**Project goal:** Historically grounded Syrian gameplay for HOI4 1.19.3 / CWIC 0.4.
No instant superpower, free nuclear weapons, ahistorical production miracles or
unconditional bonuses. All alternative history branches require institutional,
economic and diplomatic prerequisites and impose meaningful opportunity costs.

This is a **scope ledger**, not a claim that all systems below are implemented.
All features must remain compatible with the Cold War Iron Curtain economic and
influence systems, historical character roster, and existing Syria events.

## 1. Historical and alternate political order (1949–1991)

- [x] Restore 1950s/1960s Syrian focus trees and active date selections.
- [x] Optional 1949–1962 civilian-institutions versus army-guardianship
  event, with different political/military costs.
- [ ] Review historical coup chains and alternate outcome branches:
  1949 al-Za'im/Hinnawi; Shishakli consolidation and 1954 resignation;
  1958 UAR formation; 1961 Syrian secession; March 1963 Baath coup;
  1966 factional coup; 1970 Corrective Movement, 1971 onward;
  balance to 1991 without rewriting core history dates arbitrarily.
- [ ] Parliament, party competition, election credibility, factions,
  coalition cabinets and intervention risks; constitutional path must
  require real concessions to military elites and competing groups.
- [ ] Conditional union, Baathist, democratic, military and non-aligned
  alternatives with **mutually exclusive** outcomes where appropriate.
- [ ] Regime legitimacy, civilian-military tensions, factional
  defections and corruption as bounded state variables.

## 2. Fiscal and economic simulation

- [x] One-time national budget commission, agricultural irrigation and
  cooperative decisions with modest cost-bearing bonuses.
- [x] Three mutually exclusive national development choices: public
  industry, regulated private business or rural credit; annual
  procurement audit with political-power cost.
- [ ] Integrate with the mod's existing `currentMoney`, industry,
  economic-axis and influence calculations rather than inventing a
  second disconnected treasury.
- [ ] Tax base, inflation, unemployment, debt-service costs, shortages,
  oil-sector development, rural output and public-sector growth; make
  effects measurable and capped; follow actual historic timing.
- [ ] Trade balances, import dependency, external financial support,
  debt, sanctions, corruption enforcement and investment,
  including creditor response and inflationary risk.
- [ ] Regional development of Damascus, Aleppo, Homs, Hama, Latakia,
  Jazira, Golan and Euphrates districts using actual game state IDs,
  not imaginary state references.

## 3. Military, security and intelligence

- [x] Reinstate HOI4 1.19 grand doctrines and four Syrian doctrine-focus
  rewards as experience rather than obsolete doctrine tech discounts.
- [x] Restore military staff category and five existing historical
  Syrian officers' advisory roles; initial officer training decisions.
- [x] Activate intelligence agency and provide fallback operative portraits.
- [x] Nine Syria-only applied research technologies: irrigation,
  vocational/industrial capacity, signals and air-defence coordination.
- [ ] Research historical naval/air chiefs, military reorganisations,
  actual promotion dates and training schools; validate portrait paths.
- [ ] Military procurement based on budget, foreign dependence,
  spare parts, logistics, doctrinal fit and training quality.
- [ ] Intelligence-service jurisdiction and oversight, faction
  pressures, internal security and foreign counterintelligence;
  avoid an unrestricted bonus to surveillance.
- [ ] Optional private military/security contractors subject to
  financial costs, political scrutiny, command reliability, legality
  and host-government consent. Not free extra battalions.

## 4. International politics, United Nations and regional crises

- [x] Regional consultations, UN representation dossier and temporary
  diplomatic-opinion effects. **These are diplomatic signals only;
  no real UN voting or international resolution system yet.**
- [ ] Diplomatic relation calculations with Egypt, Iraq, Jordan,
  Lebanon, Israel, Turkey, USSR, United States and French/British policy.
- [ ] UN proposal/response system: mediation, observation missions,
  sanctions proposals, Security Council votes and vetoes, aid
  requests, recognition, compliance and implementation costs.
  Votes must depend on actual diplomatic alignment, not predetermined wins.
- [ ] Suez aftermath, Arab unity disagreements, Golan crisis,
  Six-Day War, 1973 war, Lebanon involvement, the Euphrates water issue,
  superpower rivalry, and the aftermath through 1991.
- [ ] Arms sales, aid, regional proxy alignments and sanctions
  with constrained options and responses, not unilateral annexation.

## 5. Optional nuclear and strategic programmes

- [x] Post-1969 expensive preliminary feasibility decision,
  gated by the existing `atomic_research` technology and
  budget-oversight spirit; safeguarded versus opaque research paths
  apply domestic and diplomatic costs. **No weapons, fissile material,
  reactor buildings or delivery systems granted by these decisions.**
- [ ] Civilian research facilities and regulator/safeguards stages;
  power grid, trained scientists, imports, finance, uranium sourcing
  and the existing special-project framework must be prerequisites.
- [ ] Any later optional deterrent route must have a multi-decade
  research timeline, very large economic costs, environmental and
  proliferation risks, international monitoring, export sanctions,
  possible raids and diplomatic consequences.
- [ ] Separate missile/delivery development and industrial test
  infrastructure; do not fake real Syrian historical weapons.

## 6. Population and social stability

- [x] Displaced-family services with a modest stability benefit,
  consumer-goods burden and administrative political cost.
- [ ] Population movement, labor markets, education, migration,
  drought/water stress, refugee intake, emigration and regional
  distribution; use the mod's demographic data if available.
- [ ] Unrest, protest and public-service shortfalls tied to actual
  funding, living standards and coercion, with safeguards against
  irreversible AI instability spirals.

## 7. Compatibility, localization and testing

- [x] Dedicated Syrian technology tab added separately from the
  global space research removal; nine research technologies.
- [x] Static Python preflight and GitHub Actions workflow authored.
- [ ] Confirm CI executes and resolve failures.
- [ ] Audit GUI overlap and blank research tiles across multiple
  major/minor countries and different DLC configurations.
- [ ] Verify localization in English, ensure all portraits / sprite
  paths exist and compare correct language fallback behaviour.
- [ ] One integrated fresh campaign smoke test: 1949 Syria,
  1960 start, an alternate-choice path, one major power,
  one minor power, Officer Corps, all research tabs, intel agency,
  industry, AI, log warnings, saves and reloading.
- [ ] Final distributable copy or patch overlay with installation,
  backup, rollback and version manifest. Do not claim a release
  is complete before runtime verification.

## Implementation rules

1. Work on `cwic-reworked`, leaving the original development branch
   and user's Steam Workshop installation untouched.
2. Reuse existing CWIC mechanics where available, avoiding duplicated
   economy, demographic or diplomatic systems.
3. Preserve historic outcomes and only branch through tested
   events/decisions; existing Syria event chains remain untouched so far.
4. Every choice must have political/economic costs and AI constraints.
5. Introduce one namespace per new event family and uniquely-prefixed
   country IDs. Cross-reference localisation, tech IDs, ideas and flags.
6. Static scans are required but **do not replace HOI4 runtime tests**.
7. Keep a change log and known-issues list for every development batch.
