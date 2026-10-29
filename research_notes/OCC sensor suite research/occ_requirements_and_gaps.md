# NASA TechLeap Orbital Clarity Challenge (OCC): Requirements, Scoring, and the Thermospheric Data Gaps It Targets

Research date: 2026-10-11. Sources: the OCC website pages, the official sample submission form PDF (text extracted locally with pdftotext), the official Sept 22 2026 information-session transcript PDF (text extracted locally), and Bruinsma et al. 2023 (full text extracted from the NSF PAR copy).

Labeling convention: **VERBATIM** marks text copied exactly from the PDFs I extracted (the sample form and the transcript). **NEAR-VERBATIM** marks wording from the HTML pages, which I could only read through a summarizing fetch tool. That tool quotes short fragments accurately but may have paraphrased the connecting words. Direct curl access to occ.nasatechleap.org was blocked by Cloudflare. Anything labeled "Inference" is my interpretation.

Key source URLs:
- Technical guidelines: https://occ.nasatechleap.org/technical-guidelines/
- Evaluation criteria: https://occ.nasatechleap.org/evaluation-criteria/
- Phases and timeline: https://occ.nasatechleap.org/challenge-phases-and-timeline/
- Awards: https://occ.nasatechleap.org/awards/
- FAQ: https://occ.nasatechleap.org/frequently-asked-questions/
- About: https://occ.nasatechleap.org/about-the-challenge/
- Sample submission form (PDF): https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf
- Info-session page: https://occ.nasatechleap.org/info-session-recording/
- Info-session transcript (PDF): https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf
- Bruinsma et al. 2023, "Thermosphere and satellite drag", Adv. Space Res., DOI 10.1016/j.asr.2023.05.011. The OCC technical guidelines link this as the "review article by Bruinsma et al" (https://insu.hal.science/insu-04114503/document). I read the full text from https://par.nsf.gov/servlets/purl/10500438.

---

## 1. Exact OCC technical guidelines (measurands, benchmark table, composition definition, hosted-payload constraints)

### Takeaway
Mass density is the lead measurand. Pressure and drag acceleration are accepted as routes to density. Composition, defined as "individual number density of major neutral species", is "valued but not required". The benchmark numbers are explicitly "target floors, not fixed requirements". No SWaP, EMI, TID or magnetic envelope is published, so teams must state their own assumptions. The hard rules are:
- it must fly as a hosted payload (no free flyers);
- it must include flying hardware;
- no debris;
- no interference with the host;
- at least 1 year of life;
- it must be buildable in quantities of at least 100 at a unit cost far below $1M–$10M.

### Cited Findings

**Objective and measurands**
- NEAR-VERBATIM: the goal is low-cost measurement of thermospheric density in LEO, at a cost and form factor that lets measurements proliferate across commercial satellites. Mass density is the lead measurand. Pressure and drag acceleration are in scope as means of determining density, "including approaches that use the host spacecraft as the drag sensor" — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- Composition definition, NEAR-VERBATIM: "Measurements of thermospheric/neutral composition (individual number density of major neutral species)" are "valued but not required" — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- VERBATIM (Doug Rowland, NASA, at the info session): "Mass density is the lead measurement. Thermospheric pressure and drag acceleration are in scope as a means of determining density, including approaches that use the host spacecraft itself as a sensor of drag acceleration. Measurements of composition, major species number density, are valued but not required. If you can measure composition alongside density, that is the most valuable input to density models and the evaluation criteria reflect that." — [Info-session transcript p.4](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- VERBATIM (on altitude regimes): "Solutions should target one or both of two altitude regimes, very low earth orbit, below 300 kilometers and low earth orbit between 300 and 800 kilometers. Every applicant identifies the regime and the altitude range within that regime where their solution meets its stated performance. Be specific about this. The relevance criteria looks at the altitude range you cover as well as what you measure." — [Transcript p.4](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Benchmark table, as rendered from the technical guidelines page** — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/), with the numbers confirmed verbatim in the [transcript p.4–5](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf):

| Type | Measurand | Regime | Accuracy | Precision | Resolution |
|---|---|---|---|---|---|
| In situ | Mass density (major-species composition preferred) | LEO or VLEO | 20% or better | 10% or better | 30 s or faster |
| In situ | Neutral gas pressure | LEO or VLEO | 20% or better | 5% or better | 30 s or faster |
| In situ | Drag acceleration | LEO or VLEO | 5% or better | 1% or better | 10 s or faster |
| Remote sensing | Major species neutral density (NO, O2, N, or O depending on altitude) | VLEO (90–300 km) | 10% or better | 10% or better | 5° horizontal; 10 km altitude |
| Remote sensing | Temperature profile | VLEO (90–300 km) | 10% or better | 10% or better | 5° horizontal; 10 km altitude |

- Target-floor language, NEAR-VERBATIM from the page: "The performance figures on this page are target floors, not fixed requirements." Applicants may propose different targets with justification, for example trading some performance for large cost or scalability gains — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- VERBATIM (Rowland): "the single most useful thing to know about this table is these are target floors, not fixed requirements. They describe the level of performance NASA believes would make a solution useful for thermospheric density specification and modeling. You may propose a different target with justification, a solution that trades some measurement performance for substantial gain in cost or scalability can still be highly competitive." — [Transcript p.4](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- VERBATIM: "Whatever you measure, state your prospective performance against the relevant target with quantitative figures of merit and expected uncertainty supported by test data, prior data or analysis. The performance criterion scores exactly this. The technical guideline page links the NRLMSIS empirical atmosphere model as a reference for expected conditions across VILEO and LEO, and also a review article on density measurement approaches." — [Transcript p.5](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf). The page links an NRLMSIS web tool (swx-trec.com/msis) and Bruinsma et al. (insu.hal.science/insu-04114503) — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- Remote sensing, NEAR-VERBATIM: cover "as wide a range in altitude, latitude, and local time as possible" and "should provide the rationale for their chosen region of operation in altitude, latitude, and local time" — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)

**Eligibility of the solution type**
- Every solution must fly as a hosted payload on a commercial spacecraft. Standalone satellites, including calibration satellites, are ineligible. A flying hardware deliverable is required, and software, analysis or purchased data alone are ineligible. The illustrative pathways are hosted in situ sensors, drag-acceleration approaches and hosted remote sensing, and "other approaches are welcome" — [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- VERBATIM, Q&A: "every solution must fly as a hosted payload above a commercial spacecraft. Standalone free flying satellites, including standalone calibration satellites are not eligible for this challenge, and a companion free flyer would fall into that category." — [Transcript p.10](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- VERBATIM, Q&A: "An existing instrument adapted to fly as a low SWaP hosted payload and a new measurement approach are both eligible as long as the solution meets the target benchmarks and the additional requirements." — [Transcript p.9–10](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- VERBATIM, Q&A: an external drag-interaction surface with internal calibration is "not excluded as long as it flies as a hosted payload meets the low SWaP durability, debris safety and non-interference requirements and any deployable elements are retained." — [Transcript p.10](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Hosted-payload constraints.** Unless marked otherwise, these come from the [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/) and are confirmed verbatim in the [transcript p.5–6](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf).
- **SWaP.** VERBATIM: "keep in mind this is a low size weight and power challenge. Solutions should be designed for ready accommodation on planned and existing commercial satellites without significant modification to the host beyond mounting thermal and electrical interfaces. A specific host spacecraft has not yet been selected, so no fixed mass volume or power envelope is published. State the assumptions you are making about the host and the range of conditions your solution could accommodate, mass, volume, power draw, data rate and format, pointing, radiation tolerance, thermal and vibration tolerances, EMI, EMC, and any safety or handling limitations. Designs that remain robust across a range of host conditions will be better positioned for flight."
- **SWaP Q&A.** Someone asked whether the budget was about "one kilobyte per second and 0.1 watts or 10 megabytes per second and 50 watts". The answer was that "there are no fixed mass volume power or data rate envelopes available at this time" (VERBATIM, p.12).
- **Interfaces.** Design toward typical commercial small-satellite hosted-payload interfaces and state assumptions on supply voltage, data interface and mounting. Interface specifications will be published as flight arrangements mature, and Phase 2 teams will finalize against them.
- **Contamination and high voltage.** VERBATIM: "If your instrument has exposed detectors, high voltage elements or sensitivity to volatile contamination, explain how it will tolerate that environment or what workaround you will use, covers or caps deployed after initial [outgassing] period, for example."
- **Magnetic.** No magnetic cleanliness requirement is stated anywhere I found.
- **Data.** Describe the data product and estimate daily volume and peak rate. "Downlink is provided through the host spacecraft. You're not expected to carry your own communication systems." (VERBATIM)
- **Pointing.** Attitude control comes from the host. State any pointing needs, such as ram orientation or field of view (Q&A, p.10). The form also asks for "field-of-view, pointing, ram orientation, or thermal" needs.
- **Scale and cost.** VERBATIM: "buildable and deliverable in quantities of at least 100 units at a per unit cost far below the current state of the art where comparable measurements cost roughly $1 to $10 million per copy. Per unit cost excludes non-recurring engineering, launch, deployment, and operations."
- **Durability.** VERBATIM: "designed to withstand launch loads and to operate for at least one year in the LEO or VLEO thermal and radiation environment. No t[otal] ionizing dose figure is available yet. State your own radiation assumptions."
- **Debris.** VERBATIM: "Any deployable elements must be retained and approaches that intentionally release objects must describe how they meet orbital debris mitigation requirements."
- **Non-interference.** VERBATIM: "there's no interference with the host spacecraft systems or other payloads. No EMI or EMC requirements are published yet, so assume reasonable compliance will be expected. State what you assume that entails and explain how your design accommodates it."
- **Orbit.** The vehicle, provider, mission, inclination, duration and ground contact are all undefined. Teams state their orbital assumptions and show the design stays robust if those change.
- **The 100-unit question.** VERBATIM Q&A: "The challenge does not require the delivery of multiple instruments and only one flight opportunity per team is currently available ... Information on cost and scalability should be provided to describe how multiple copies can be provided and at what cadence in the future, but not during the challenge." — [Transcript p.13](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- **Proving accuracy.** VERBATIM Q&A: "applicants are expected to propose their verification and validation approach as part of their proposal to meet the challenge accuracy requirements. Later phase proposals require the evidence be provided that the sensor provides the requirement measurements with the required accuracy." — [Transcript p.13](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

### Inferences
- The density row has only a 20% accuracy and 10% precision floor at 30 s. A hosted gauge plus composition channel competes on that row, not the 5%/1% drag-acceleration row, unless the team also claims a drag product.
- The composition definition is "individual number density of major neutral species". So reporting an O/N2 ratio or mean molecular mass alone may be read as less than full composition. Reporting n(O), n(N2) and n(He) individually, with uncertainties, matches the wording most directly.
- With no published envelope, "robust across a range of host conditions" is the scoring lever. Presenting a SWaP and interface range (for example a 5 V/12 V/28 V input range, UART/I2C/CAN options, and a ram-facing and off-ram performance model) is likely to read well.

### Gaps
- I could not get a byte-exact copy of the technical-guidelines HTML because curl was blocked by Cloudflare. The table cell wording comes through the fetch tool, but the numbers are confirmed verbatim by the transcript.
- No published magnetic, high-voltage-specific, outgassing (TML/CVCM), or TID requirement exists.
- The promised updated FAQ with the unanswered info-session questions was not yet visible on the FAQ page as fetched.

---

## 2. Exact Phase 1 evaluation rubric (Relevance, Performance, Cost & Scalability, Flight Readiness)

### Takeaway
There are four criteria, each scored 1–5 by five judges and statistically normalized. No weights are published. A Relevance score of 5 explicitly requires "density together with composition" over "a clearly identified and extensive altitude regime", plus an evidenced case for model improvement or for filling coverage gaps. Density alone (or density plus composition over a narrow span) caps at 4. Pressure or drag alone caps at 3. NASA publicly declined to change this, but noted the selecting official can pick across a range of scores.

### Cited Findings
Unless noted, everything below is NEAR-VERBATIM fragments from the [Evaluation criteria page](https://occ.nasatechleap.org/evaluation-criteria/). The fetch tool returned them as quoted strings joined with "/".

**Process**
- Each criterion is scored 1–5 with qualitative comments. Each valid submission gets five reviews, which are statistically normalized. No weightings are given. The selection committee picks up to four winners from the top scores "plus programmatic considerations" — [Evaluation criteria](https://occ.nasatechleap.org/evaluation-criteria/). The transcript (p.6) confirms this verbatim.
- The FAQ says a physical prototype is not required for Phase 1 and hardware maturity is not ranked. Performance and flight readiness reward credible evidence such as test data, prior development, or analysis — [FAQ #19](https://occ.nasatechleap.org/frequently-asked-questions/)

**Relevance**
- 5: "Measures the most valuable input to density models — density together with composition — for a clearly identified and extensive altitude regime. Makes a specific, well-evidenced case for how the data would improve model accuracy or fill known coverage gaps."
- 4: "Measures a high-value input — density directly, or density with composition over a narrower altitude span — with a credible, well-supported case for how the data would serve density models across a meaningful part of the range."
- 3: "Measures pressure or drag as an indirect means of determining density, or covers only a narrow slice of the altitude range. The case for usefulness is plausible but limited by the indirect measurement, the coverage, or unsubstantiated assumptions."
- 2: "Measures a parameter only loosely connected to thermospheric density needs, or covers a very narrow altitude range of limited value. The case that the data would be a useful input to density models is tenuous."
- 1: "Does not identify a measurement or altitude coverage that would serve as a useful input to density models, or does not make a credible case that the data would improve them."
- VERBATIM (Hakimzadeh): "The strongest submissions measure density together with composition over a clearly identified extensive altitude regime and make a specific well evidenced case for how the data would improve model accuracy or fill known coverage gaps. Make that case explicitly. Don't assume it's obvious." — [Transcript p.6](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Can density-only score well? (VERBATIM Q&A, transcript p.12–13)**
- An applicant asked whether the rubric could be changed so composition is not required for the top Relevance score. The applicant argued that composition "is not a primary input for satellite drag specification" and that "most, if not all, proven assimilation techniques for specifying the drag environment do not assimilate composition".
- NASA answer: "the highest relevance score reflects the most valuable measurement types to advance our knowledge of thermospheric density, a combination of the primary input to drag density together with the composition that produces that density. We don't anticipate changing the rubric. Note that the selecting official is free to select solutions with a range of rubric scores in order to achieve NASA's goals, including a breadth of different types of approaches or regimes of applicability." — [Transcript](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Performance**
- 5: "Presents strong, quantitative evidence that makes a compelling case the solution will meet or exceed the applicable benchmarks for its measurand and altitude regime. Expected uncertainty is characterized and realistic."
- 4: "Presents solid evidence and a credible calibration plan supporting a strong case that the benchmarks will be met. Most figures of merit are substantiated, with minor gaps in the data or in how uncertainty is characterized."
- 3: "Presents some supporting evidence, but the case that benchmarks will be met relies on optimistic assumptions or incomplete data. The calibration and validation approach is described but underdeveloped."
- 2: "Offers limited or largely qualitative evidence. The case for meeting benchmarks is weak or inconsistent, and the calibration and validation plan is vague or missing key elements."
- 1: "Provides little or no evidence that the solution would meet the applicable benchmarks. Figures of merit are absent or unsupported, and no credible calibration or validation approach is presented."
- VERBATIM (Hakimzadeh): "to what extent does the evidence presented, such as test data, prior development calibration plan, make a credible case that the solution will meet the performance benchmarks ... Strong submissions are quantitative and characterize their expected uncertainty realistically." — [Transcript p.6](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- Form prompt "Technology performance" (350 words), VERBATIM: "Describe the measurement performance your solution would deliver and why it is useful as an input to thermospheric density models. What accuracy, precision, and spatial or temporal resolution would it achieve at your target altitudes? How will you calibrate and validate your measurements to establish that performance? Use quantitative figures of merit, with supporting data and expected uncertainty, to show how your solution will meet or exceed the benchmarks NASA has identified for your measurand and altitude regime." — [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf)

**Cost and Scalability**
- 5: "Projects a unit cost dramatically lower than current instruments, well-substantiated with quantitative backing. Names a specific, credible manufacturing methodology and a production rate that together make a convincing case the solution can be reproduced at volume."
- 4: "Projects a unit cost well below current instruments with reasonable supporting assumptions. The manufacturing approach and production rate credibly support volume reproduction, with minor gaps in the cost basis or in how the approach scales."
- 3: "Projects a lower unit cost, but the target rests on limited or unsubstantiated assumptions. The manufacturing approach and production rate are described in general terms, without enough detail to judge whether volume reproduction is realistic."
- 2: "Claims a cost advantage that is weakly supported or not clearly better than current instruments. The manufacturing methodology or production rate is vague, and the case for reproducing the solution at volume is thin."
- 1: "Provides no credible cost advantage over current instruments. Target unit cost, production rate, or manufacturing approach is absent, unsupported, or implausible."
- VERBATIM: "We look at projected unit cost, production rate, manufacturing approach and ease of accommodation across a broad range of commercial launches. Name a specific manufacturing methodology and a production rate with quantitative backing." — [Transcript p.6](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- Form prompt "Projected cost and scalability" (350 words), VERBATIM: "Describe your target per-unit cost and explain what makes your approach significantly less expensive -- for example, your design choices, component selection, or manufacturing approach. What production rate do you believe is achievable, and how would per-unit cost change as volume increases? ... Use quantitative figures, with the assumptions behind them, to support your projected costs." — [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf)

**Flight Readiness**
- 5: "Presents a credible, detailed path to a flight-ready unit within the competition timeline, with milestones, dependencies, and resources clearly articulated. Integration into a hosted payload is realistically addressed, the development budget is aligned with scope, and key risks carry actionable mitigations and margin."
- 4: "Presents a strong, largely detailed path to flight readiness. Milestones, integration approach, and resources are well-defined and the development budget is reasonable. Minor gaps in risk mitigation, margin, or schedule specificity do not undermine overall confidence."
- 3: "Outlines a reasonable path to flight readiness but lacks detail in key areas such as milestone sequencing, integration, or risk mitigation. The development budget is present but may be incomplete or insufficiently justified."
- 2: "Outlines a path that raises feasibility concerns. Milestones, integration requirements, or resource needs are underdeveloped, and the budget is misaligned or unrealistic in places. Risk identification is incomplete."
- 1: "Does not present a credible path to flight readiness within the timeline. Key elements — milestones, integration, resources, or risk identification — are absent or inadequate, and the budget, if present, is unrealistic. Little confidence the team could deliver a flight-ready unit."
- VERBATIM: "supported by a realistic plan, scheduled budget and risk register." — [Transcript p.7](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Submission form structure.** All of this is VERBATIM from the [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf).

Word limits by section:

| Section | Word limit |
|---|---|
| Technology description | 50 |
| Capabilities | 250 |
| Technology overview | 350 |
| Technology performance | 350 |
| Projected cost and scalability | 350 |
| Technology development status | 300 |
| Resource needs and accommodation | 300 |
| Flight demonstration and integration | 150 |
| Solution development plan | 250 |
| Intellectual property | 200 |
| Other considerations (optional) | 150 |
| Project plan | 200 |
| Budget narrative | 200 |

Other form elements:
- **Visual representation:** one PDF, at most 5 pages and 10 MB. It must not be used to dodge word counts, and the minimum font is 10 pt. "Gantt charts, schedules, budgets, and other similar content are not acceptable", and "Pages beyond the five-page limit and unrelated content will render the submission ineligible."
- **Video:** a YouTube video of at most 90 seconds, captioned, set to public or unlisted, with embedding on.
- **Budget:** a Total cost field plus budget line items.
- **Technology development status** asks for evidence that the technology was "successfully tested in the laboratory or relevant flight environment (at least the component or breadboard level) to demonstrate current development status and that a solution could be ready for a flight test in eight months."
- **Technology overview** asks: "What do you measure, over what altitude range, and by what physical principle or measurement approach?"
- **Other considerations** invites justification of any deviation: "If your proposed technology does not meet some of the requirements in the technical guidelines, describe why you have made the choices you did".
- **Development status URLs:** URLs may be cited, but "judges are not required to read this content".

### Inferences
- Relevance arithmetic: a density-only hosted gauge tops out at 4. A density plus composition suite can reach 5, but only if the altitude coverage is "extensive" and the model-improvement case is "well-evidenced". An OSSE showing model-error reduction is direct evidence for "how the data would improve model accuracy".
- Performance 5 needs "characterized and realistic" uncertainty. Separating accuracy (calibration bias) from precision (noise), per measurand and per altitude, and backing each with test data or analysis maps directly onto the rubric wording.
- Calibration and validation plans appear explicitly at the 2–4 levels of Performance. A missing cal/val plan alone pushes the score toward 2.
- The visual PDF cannot carry budgets or schedules, so those must fit in the 200-word Project plan, the budget fields, and the 200-word Budget narrative.

### Gaps
- The criterion weights are unpublished, and probably unweighted, but this is not stated.
- The "Scoring fairness" page (https://occ.nasatechleap.org/fairness/) was not fetched. It may describe the normalization method.
- Levels 2 and 4 come through the fetch tool's quoted fragments. Exact punctuation and dashes may differ slightly from the page.

---

## 3. Phase 2 and Phase 3 requirements, timeline, prizes, eligibility, and FAQ/info-session clarifications

### Takeaway
- **Phase 2:** 4 months. Build an engineering model and demonstrate the measurement in ground testing. Scored at a site visit on four 25-point criteria, one of which is a documented finalized design with trade studies and rationale. A score of 80/100 or more is needed for the extra $200k.
- **Phase 3:** 4 months. Complete the flight build and demonstrate it in a relevant space environment, plus a test matrix and an operational validation plan. A score of 80/100 or more is needed for $100k.
- **Prizes:** up to 4 winners, at most $500k each, plus a no-cost flight that NASA "intends" to provide.
- **Phase 1 deadlines:** registration closes 2026-10-28 at 5 pm ET, and submissions close 2026-11-11 at 5 pm ET.

### Cited Findings

**Timeline**
- Launch Aug 19 2026; info session Sep 22 2026; registration closes Oct 28 2026 at 5:00 pm ET; submissions close Nov 11 2026 at 5:00 pm ET; Phase 1 winners in January 2027; Phase 2 starts early 2027; site visits and winners in spring 2027; Phase 3 runs spring to summer 2027 — [Phases and timeline](https://occ.nasatechleap.org/challenge-phases-and-timeline/); [Home](https://occ.nasatechleap.org/)
- Conflict: at the info session Cameron Fox said "We'll be announcing those winners in December of this year" and that evaluations run "November through December" — [Transcript p.3, p.8](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf). The website says January 2027.
- Registration and submission are "two separate steps" (VERBATIM, transcript p.3). The form says that after the registration deadline "you will not be able to start a submission" (VERBATIM) — [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf)
- The form describes 8 months to flight-ready: "If your team is named as a winner, you will have eight months to finalize the design and build a flight-ready solution." (VERBATIM) — [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf). That is Phase 2 plus Phase 3 at 4 months each.

**Prizes**
- Phase 1: up to 4 winners at $200,000 each. Phase 2: an additional $200,000 each. Phase 3: an additional $100,000 each. Maximum $500,000 per team, from a $2M pool. NASA "intends to offer" a no-cost flight test to Phase 3 winners, also described as "a potential opportunity", so it is not guaranteed — [Awards](https://occ.nasatechleap.org/awards/); [Home](https://occ.nasatechleap.org/)
- There are no down-selects between phases beyond meeting the 80-point thresholds. VERBATIM: "it is certainly possible that we select four winners in Phase 1 and all four of those winners are retained through phases two and phases three." — [Transcript p.11](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- The budget may be above or below $500k, and flight-test cost is excluded. Integration and payload preparation costs are the team's and may come from prize money — [FAQ #14](https://occ.nasatechleap.org/frequently-asked-questions/); [Transcript p.11–12](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

**Phase 2 (4 months).** Four criteria worth 25 points each, with at least 80/100 needed for the additional $200k — [Evaluation criteria](https://occ.nasatechleap.org/evaluation-criteria/). VERBATIM from the [transcript p.7](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf):
1. "evidence that a finalized design has been completed and documented, including key design decisions, trade studies and the rationale for the chosen approach."
2. "evidence that the design is mechanically, electrically and dimensionally compatible with integration as a hosted payload consistent with the interface specifications in the technical guidelines."
3. "evidence that a credible development and testing plan is in place with clear ties to system requirements and to the schedule the team proposed in its submission and that the team is on track against that schedule."
4. "evidence that the team has built an engineering model of sensing technology identified in its submission and demonstrate that it can make the required measurement in ground testing. The engineering model is at the heart of Phase 2."

Field judges make site visits at the end of the phase. Teams get NASA SME support toward interface compatibility — [Phases and timeline](https://occ.nasatechleap.org/challenge-phases-and-timeline/)

**Phase 3 (4 months).** Four criteria worth 25 points each, with at least 80/100 needed for $100k — [Evaluation criteria](https://occ.nasatechleap.org/evaluation-criteria/). VERBATIM from the [transcript p.7–8](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf):
1. "the build is complete and on track for on-time delivery to the flight provider and integration into the host spacecraft"
2. "the solution has been built to the requirements of the host spacecraft interface"
3. "testing and analysis for the anticipated flight conditions have been completed, including a demonstration that the solution operates in a relevant space environment and that the results indicate it's ready for flight"
4. "the potential risks for the flight have been considered and mitigation plans developed and that a test matrix and operational validation plan are in place ahead of the flight test"

After the flight, each winner submits a final report — [Sample form](https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf)

**Eligibility.** This matters for the team's lead and prize recipient.
- Individuals must be US citizens or permanent residents aged 18+. Organizations must be US-incorporated with a primary place of business in the US. Teams must be led by an eligible US citizen or permanent resident — [FAQ #5](https://occ.nasatechleap.org/frequently-asked-questions/)
- VERBATIM: "Teams can include foreign nationals, but there are a few caveats here. First, it's subject to FAR trade agreements, and the team will still be eligible to receive a prize as long as foreign nationals sign and deliver a foreign participant acknowledgement form, acknowledging they're not eligible to receive a prize from NASA." The form is in the Rules page — [Transcript p.8–9, p.12](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- If an organization submits, the prize is paid to that organization (Q&A, p.12). The team needs $250k liability insurance or demonstrated financial responsibility, running through at least Dec 31 2028 (Q&A, p.9). No TRL is specified (Q&A, p.9). Letters of support are not required (Q&A, p.13) — [Transcript](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- Teams with government funding for a similar flight-ready solution are ineligible. Each lead applicant gets one submission — [FAQ #6–9](https://occ.nasatechleap.org/frequently-asked-questions/)

**Cost evidence expected**
- No price target beyond "far below" $1M–$10M. When asked for an affordability target, NASA pointed back to the guidelines — [Transcript p.13](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

### Inferences
- Phase 2 explicitly scores "trade studies and the rationale for the chosen approach". An OSSE trade study comparing candidate suites (density-only, density plus O, density plus O/N2/He) is directly scorable evidence in Phase 2, not just Phase 1.
- "Demonstrate that it can make the required measurement in ground testing" implies a vacuum-chamber calibration against a reference, such as a spinning-rotor or capacitance-diaphragm gauge, and for composition a known gas mix and/or an atomic-oxygen source, within the 4-month window. The team should plan chamber access now.
- "Relevant space environment" in Phase 3 likely means thermal-vacuum testing and possibly vibration. This is not defined on the site.
- Prize eligibility depends on a US citizen or permanent resident lead. A foreign national can contribute but must sign the acknowledgement form and cannot receive prize money.

### Gaps
- The Rules page was not fetched in full, including the foreign participant acknowledgement form text and FAR trade-agreement countries.
- The updated FAQ answering the remaining info-session questions had not appeared as of the fetch.
- The video recording and slide deck themselves were not reviewed. Only the transcript was.
- "Relevant space environment" and the Phase 3 test requirements are undefined.

---

## 4. The science gaps OCC is built on (Bruinsma et al. 2023 and related)

### Takeaway
Bruinsma et al. 2023, the review OCC links, identifies several gaps:
- sparse and inconsistent density data (missions disagree by 5–20%, and by up to 45% at 800 km);
- no in situ composition since Dynamics Explorer 2 in the early 1980s;
- almost no high-resolution data below about 250 km or above about 550 km;
- a tiny storm database (only two Kp=9 storms since 2000, each seen by one or two satellites);
- drag-coefficient and gas-surface-interaction uncertainty of up to about 20–30%;
- a lack of continuous, low-latency density data for assimilation.

Empirical models do worst in storms, and NRLMSISE-00 systematically underestimates storm densities.

### Cited Findings
All of these are verbatim sentences from [Bruinsma et al. 2023](https://par.nsf.gov/servlets/purl/10500438), DOI 10.1016/j.asr.2023.05.011, unless another source is named.

**Composition**
- "It is important to note here that the bulk of thermosphere composition and temperature measurements were taken in the 1970s and 1980s with mass spectrometers on the Atmosphere Explorers (Pelz et al. 1973; Nier et al. 1973) and the Dynamics Explorer 2 (Carignan et al. 1981)."
- "In situ composition measurements have not been taken since the Dynamics Explorer 2 mission in the early 1980 s (Carignan et al. 1981)."
- "So, we are in the delicate situation of having most composition and temperature data, and accurate in situ total density data, but 18 years apart, i.e. almost two solar cycles."
- On the CHAMP/GRACE/GOCE era: "Unfortunately, concurrent composition and temperature measurements were not made." Limb remote sensing of O, O2 and N2 profiles came from TIMED/GUVI (2002–2007) and ICON.

**Altitude coverage**
- "Fig. 6 ... shows the sparsity of data for high solar activity, in particular below 400 km (and no data above 550 km)."
- "Observations are also necessary for model assessment and validation, which often is impossible simply because of the absence (composition) or paucity of data, notably at low and high altitude, below about 250 km and above 550 km, respectively."
- "Relative errors and uncertainties also increase with altitude, due to the Helium-Oxygen transition at 450- 550 km under low solar activity, and the absence of high[-]resolution observations, and notably accelerometer[-]inferred, above that altitude. Presently, thermosphere models can only be assessed using orbit-mean or daily-mean densities above 500 km, which includes therefore the 700- 800 km altitude range where many Earth Observation satellites operate."
- "inferring densities for altitudes above 600 km is complicated due to the very low drag and consequently data is sparse there too."
- At 100–200 km: "observing in situ in that altitude region is very complicated due to the very high atmospheric drag".

**Dataset consistency**
- "Datasets inferred from different missions typically disagree 5-20%, but the numbers vary regarding altitude and solar activity. They are largest at 800 km, where they can reach 45%."
- "inconsistency at the level of 5% or less is hard to confidently identify."

**Storms**
- "The effects of severe and extreme geomagnetic storms on the thermosphere total mass density are not well-known because these are rare events on the one hand (only two storms with Kp = 9 after 2000), and because each storm was monitored by just one or two satellites, i.e. observations are restricted to two altitudes and local time planes."
- "The largest errors are observed, unsurprisingly, during geomagnetic storms."
- Kp forecast models "tend to underestimate storms". Under Kp>4, the RMSE is "already larger than one after three hours and larger than two after 9 h".
- Recommendation 3.2.3: "Uninterrupted high-resolution monitoring of geomagnetic storms is needed to augment the current small database of storm events, which severely penalizes both modeling and model assessment. At present, only GRACE-FO (data of opportunity, climate mission ...) provides high-resolution total mass density data."
- Bruinsma et al. 2021 (JSWSC 11, 12) compared NRLMSISE-00, JB2008, DTM2013, TIE-GCM and CTIPe across 13 storms using CHAMP/GRACE/GOCE. All models were worse in storms with larger standard deviations. NRLMSISE-00 "systematically and significantly underestimates the storm densities", while DTM2013, JB2008 and CTIPe showed no significant average bias. This is from a search-result summary of the abstract; the full text was not read — [SWSC abstract](https://www.swsc-journal.org/articles/swsc/abs/2021/01/swsc210039/swsc210039.html); [CU Scholar](https://scholar.colorado.edu/concern/articles/nz806093f)
- Bruinsma & Laurens 2024 (JSWSC, DOI 10.1051/swsc/2024027) covered 152 storms (ap ≥ 80, 2001–2023) for NRLMSISE-00, JB2008 and three DTM2020 versions. Model precision degrades with altitude over 250–550 km while bias is roughly altitude-independent. Debiasing with pre-storm density data leaves the models only slightly biased. This is from a search summary; the full text returned 403 — [SWSC abstract](https://www.swsc-journal.org/articles/swsc/abs/2024/01/swsc240020/swsc240020.html)

**May 2024 Gannon storm**
- Parker & Linares (2024): "Across all time horizons from 0-3 days, the initial increase in [ap] was underpredicted by 100-300."
- "Automated station-keeping, especially from the Starlink constellation, caused nearly half of all the active satellites in LEO to maneuver at once in response to the storm."
- Storm "magnitude and duration ... were poorly predicted, even one day in advance."
- Source: [arXiv 2406.08617](https://arxiv.org/abs/2406.08617)
- A search summary of a GRACE-FO-based evaluation over 80 storms (2001–2024) reported an NRLMSISE-00 mean absolute percentage error of 12.31%. That is a multi-storm mean; the primary paper was not read — [search result](https://www-app2.gfz.de/grace-references/b2hd-2025SpWea..2304317G.html)

**Drag coefficient and gas-surface interaction**
- "The drag force can vary by more than 30% depending on the model selected, for which presently no standard is accepted (Mehta et al. 2022)."
- "Even when the object and environment parameters are perfectly known, significant differences or errors can be imparted by the choice of gas-surface interactions models (up to 20%) and computational methods for estimating the drag coefficient (up to 15%) (Mehta et al. 2022)."
- For GRACE-A, "The largest differences of around 30% are between quasi[-]specular ... and diffuse with fixed accommodation". These are worst cases near 500 km at low solar activity.
- The physical CD "is a function of ... atmospheric temperature and composition ... and gas-surface interactions"; "The physical drag coefficient is most influenced by gas-surface interactions (GSI)."
- "In reality the drag coefficient varies both spatially (due to change in atmospheric composition with location - latitude, longitude, and altitude) and temporally".

**Latency and assimilation**
- "the lack of continuous, low latency density measurements impedes its operational application." This refers to Kalman-filter driver estimation.
- "data assimilation methods require a continuous stream of high-quality and high-resolution observations to adjust the model state, and this condition is presently far from being met."
- On EnKF/EnOI: "in order for this approach to be operationally useful, a large amount of real-time, publicly- or commercially-available (e.g. orbit determination, mass spectrometer or accelerometer) data is required."
- "The greatest limitation to improving thermosphere models today is inconsistency between observation datasets, inconsistent quality, and above all the sparse distribution in space and time of upper atmosphere density and composition observations."
- Since 2000, CHAMP, GRACE and GOCE accelerometer densities "have greatly advanced thermosphere research and modeling, but in truth these are data of opportunity."
- Bruinsma explicitly recommends OSEs and OSSEs: "In order to demonstrate the benefit of investing in a particular modeling framework or a particular real-time data stream, a series of Observing System Experiments (OSEs) and Observing System Simulation Experiments (OSSEs) should be carried out."

**Abstract and OCC framing**
- Abstract: "Substantial progress can only be made by means of setting up a full-blown observing system, including not only density and composition measurements, but equally the necessary model drivers."
- OCC framing, VERBATIM from the info session: "Measurements taken in orbit are sparse, often disagree for one instrument to the next and are expensive to collect. A single sensor can run from a million to $10 million." Sensors deployed across constellations "could take continuous measurements from many points at once and give drag prediction models the global low latency coverage they lack today." — [Transcript p.2](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)
- Info-session speakers included Doug Rowland, GDC Project Scientist. Bruinsma notes GDC "is planned to provide in-situ measurements of low-resolution total mass density, composition, temperature and wind at 300-400 km" — [Info-session page](https://occ.nasatechleap.org/info-session-recording/); [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)

### Inferences
- The strongest "fill known coverage gaps" arguments, each tied to a quotable Bruinsma sentence, are:
  - in situ composition, absent since about 1982;
  - more than 550 km, and especially 700–800 km, where only orbit-mean densities exist;
  - storm-time multi-point sampling;
  - below about 250–300 km (VLEO), where data are sparse;
  - continuous low-latency streams for assimilation.
- A proliferated suite that measures composition helps break the CD and GSI ambiguity in drag-derived densities. That is a secondary relevance argument beyond model fitting.
- Bruinsma's explicit call for OSSEs gives the team's OSSE work a citable justification inside the Relevance section.

### Gaps
- I could not verify the "LLITED May 2024 storm 58%" figure. Searches found LLITED mission pages ([eoPortal](https://www.eoportal.org/satellite-missions/llited)), whose density instrument is a UNH miniature ionization gauge, but no source giving a 58% figure. Treat it as unverified until a primary source is found.
- I found no primary-source percentage for NRLMSIS underestimation during the May 2024 storm. A Swarm-C/NRLMSIS 2.1 study reportedly finds main-phase underestimation, but the number was not retrieved.
- The numeric density ratios and standard deviations in Bruinsma 2021 and 2024 were not retrieved (SWSC full text returned 403).
- Emmert 2015 (ASR 56, 773–824, DOI 10.1016/j.asr.2015.05.038) was identified but not read.

---

## 5. Which composition quantities matter most (O, N2, He, O/N2, O–He transition, mean molecular mass) and why

### Takeaway
Bruinsma explicitly names "(O2, N2, O, He)" as the composition species needed, measured "simultaneous[ly]" with high-quality mass density. Composition matters for two reasons:
- **Model construction:** composition data is stale, dating from the 1970s–80s.
- **Drag:** the drag coefficient depends on composition, and the O-to-He transition at about 450–550 km under low solar activity drives model error with altitude.

OCC's own definition, "individual number density of major neutral species", points to per-species number densities.

### Cited Findings
- Recommendation 3.2.2, verbatim: "An observation system is needed to achieve significant progress in thermosphere modeling. Simultaneous high quality mass density (e.g. GOCE, CHAMP) and composition (O2, N2, O, He) data by means of mass spectrometers (e.g. DE2) or the Terahertz microwave technique (Wu et al. 2016) are necessary to revise the composition information in the models." — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)
- On the O-to-He transition: "At the higher altitudes, Helium takes over as the dominant neutral species from atomic Oxygen, which must be accounted for in the physics-based model approaches. The transition height of atomic Oxygen to Helium varies greatly with solar and geomagnetic activity." — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)
- On the O-to-He transition and drag: "A well-known effect of these dynamics is change in the dominant species from atomic oxygen to helium during solar minimum and with altitude, otherwise known as oxygen-to-helium transition." This appears in the GSI and drag-coefficient section — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)
- "Temperature and composition are used in some orbit determination software to compute the aerodynamic coefficient". Empirical models return "temperature, total and partial densities of the main constituents" at low spatial resolution (4500–9000 km) — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)
- "The space environment parameters are winds, atmospheric temperature and composition, all of which dictate the specifics of energy and momentum exchange between the atmosphere and the spacecraft, otherwise known as gas-surface interaction (GSI)." — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)
- Storm-time composition: "As the density and composition variation in the thermosphere during storm-time is mainly driven by Joule heating and NO cooling, ideally temperature, composition, wind, and NO cooling measurements in the lower thermosphere from 100 to 200 km will complement the total density measurements". This matches OCC's remote-sensing species list (NO, O2, N, O) for 90–300 km — [Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438); [Technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- NASA's info-session answer frames composition as "the composition that produces that density" (VERBATIM). The objection NASA declined to act on was that assimilation for drag does not currently assimilate composition — [Transcript p.12–13](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)

### Inferences
These are mine, from atmospheric physics, and are not from the sources above.
- Mass density is the sum over species of n_i·m_i. Below about 450 km, O and N2 dominate, so n(O), n(N2) and their ratio fix the mean molecular mass and therefore the conversion between number density or pressure and mass density.
- Above the O–He transition, n(He) controls mass density and scale height, so a He channel is what makes composition "extensive" in altitude for LEO from 300 to 800 km.
- O/N2 is the standard storm-response composition diagnostic: Joule heating upwells N2 and lowers O/N2. It is the quantity most likely to show storm-time model error.
- A hot- or cold-cathode gauge alone measures total number density or pressure weighted by species-dependent ionization cross-sections. It therefore needs composition, measured or modeled, to convert to mass density. This links the composition channels directly to the accuracy of the density channel, which is a strong Relevance and Performance argument.
- Suggested quantities for a suite: n(O), n(N2) and n(He) individually, plus a derived mean molecular mass and O/N2. O2 matters mainly below about 200 km.

### Gaps
- I found no primary source in this session quantifying drag-coefficient sensitivity to O/N2 or He fraction specifically. Mehta et al. 2022 and Pilinski et al. are the likely sources but were not read.
- I found no source quantifying assimilation benefit from composition versus density-only. This is the exact objection raised in the Q&A, and it is a gap the team's OSSE could fill.
