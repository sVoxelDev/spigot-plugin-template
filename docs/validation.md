# Validation evidence

Verified on October 1, 2026. The plugin artifact was tested locally on ARM64 and by GitHub Actions on AMD64. The installed template jar has the same SHA-256 on both architectures:

`c7a9b2a46806f7785431d15ca23362edf08a605e6c2ad543e8fa5b3935bd0383`

## Executed workflows

| Artifact | Paper 26.3 build 140 beta | Paper 26.2 build 129 stable | Evidence |
| --- | --- | --- | --- |
| TemplatePlugin | 16 checks pass | 16 checks pass | [Actual commands and results](validation/2026-10-01/template.json), [lifecycle log excerpts](validation/2026-10-01/template-lifecycle.txt) |
| WelcomePlugin from the setup workflow | 16 checks pass | 16 checks pass | [Actual commands and results](validation/2026-10-01/welcome.json), [lifecycle log excerpts](validation/2026-10-01/welcome-lifecycle.txt) |
| HarborPlugin from a source-blind agent | 16 checks pass | 16 checks pass | [Actual commands and results](validation/2026-10-01/harbor.json), [lifecycle log excerpts](validation/2026-10-01/harbor-lifecycle.txt) |

Each matrix checks the actual server build, plugin identity, help/info/status commands, changed settings, malformed and incorrectly typed reloads, persisted restart, invalid startup disablement, recovery, and clean shutdown. Every successful phase has no exception/error log line. The invalid-startup phase contains exactly the expected configuration error.

The original local run built and tested the plugin. HarborPlugin's retained matrix used `--skip-build`; its earlier full run built and tested the same jar. The report records that distinction. Server jars were verified against their pinned SHA-256 before execution.

[12 focused MockBukkit cases](validation/2026-10-01/unit-tests.json) pass with zero failures, errors, or skipped tests. [The tooling suite has 10 passing tests](validation/2026-10-01/tooling-tests.txt), including identity changes, invalid input preservation, checksum rejection, and failure reporting. [The personalized workflow evidence](validation/2026-10-01/workflow.json) also proves local up/rcon/reload/restart/down, localhost port binding, private RCON, report retention, and container cleanup. CI runs that workflow from a fresh isolated copy.

## Independent probes

The independent agent validated all eight contract/setup clauses through public commands, configuration, logs, and generated artifacts. It tested a different plugin identity, invalid inputs, a corrupted checksum, a bad descriptor, and a missing entrypoint class. A healthy Paper server without the plugin correctly failed validation. Correcting the descriptor-report gap and preserving reports across dev startup both passed independent retests. All six containers it created were removed.

The independent behavior report remains in `build/independent-validation/behavior-report.json`. The GPT-5.6 Sol evidence review also found an ignored author correction; that is fixed with a focused test. It requested a CI lifecycle gate and visibility of alpha-only upstream releases; both are implemented.

## Hosted evidence and limits

[The first complete hosted run](https://github.com/sVoxelDev/spigot-plugin-template/actions/runs/36826690576) passed build, both server profiles, and personalized-plugin validation. Its downloaded jar checksum matches the local jar. [Current branch checks](https://github.com/sVoxelDev/spigot-plugin-template/actions?query=branch%3At3code%2Fmodernize-plugin-template) rerun those gates and the expanded local-server workflow after the final tooling fixes. Workflow artifacts contain full reports and logs; the committed files above preserve the command results and relevant lifecycle evidence.

Player greetings, permissions, and playtime are MockBukkit tests. No real player login or client gameplay was exercised. The latest Paper profile is beta. Remote deployment, tagged release creation, GitHub Packages, and the external JitPack service were not executed. Local Maven publication is checked separately. Merging and external deployment require the user's approval.
