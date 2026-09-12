# `manuals/2026-27_BIOCORE/`: the kickoff-day ingest directory

**There is no BIOCORE material in here, and there will not be until 2027-01-09.** `[AUDIT 2026-09-04]`

**In the public repository, this README is the only file tracked in this directory.** `[AUDIT 2026-09-12]`
The DEEP SPACE ingest described below is mostly text extracted from FIRST's copyrighted manual, so it
stays out of the repository, as does `../../review/LATEST` (per-machine run state). To reproduce it on
a clone, run `bash tools/rebuild-corpus.sh --fetch` from the repository root, then
`BASELINE=manuals/archive/frc/2018_POWERUP_GameManual.pdf bash tools/RUN-KICKOFF.sh manuals/archive/frc/2019_DESTINATIONDEEPSPACE_GameManual.pdf DEEPSPACE`.
The new run gets its own timestamp, so its directory names will not match the ones below.

This is where `tools/ingest-manual.sh` writes. On kickoff day it will hold the downloaded BIOCORE
game manual and one `ingest_V1_<stamp>/` directory per ingest.

## What is in here right now, and why it is not BIOCORE

| Path | What it is |
|---|---|
| `ingest_DEEPSPACE_20260824T032851Z/` | A complete ingest of the **2019 DESTINATION: DEEP SPACE** manual, baselined against 2018 POWER UP. 133 pages, 169 rules, 61 violations, 77 glossary terms, 104 mapped sections. Produced by the 2026-08-24 end-to-end beta test |
| `sections/` | Empty. Created by an earlier run and never written to |

The DEEP SPACE ingest is **evidence, not clutter**: it is the proof that the kickoff pipeline runs
from a PDF all the way to a nine-section review, on a game whose answers are already known. Its
review output is `../../review/DEEPSPACE_20260824T032851Z/REVIEW.md`, and `../../review/LATEST`
points at it. The test is written up in `../../review/BETA_TEST_REPORT.md`.

It is kept rather than deleted because deleting it would throw away the only end-to-end proof this
project has. It is labelled here rather than left unexplained because on kickoff morning nobody
should have to work out what a directory in the BIOCORE folder is, and every artifact in it is
already named `DEEPSPACE`.

## On kickoff day

Nothing in here needs cleaning up first. The ingest writes to a new timestamped directory, so the
DEEP SPACE output cannot be confused with or overwritten by the BIOCORE one. If you want it out of
the way, move it to `../../review/` rather than deleting it.

The two commands are in `../../README.md`. Read `../../KICKOFF_PLAYBOOK.md` Step 1 first.
