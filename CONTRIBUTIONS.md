# Merged Pull Requests

This ledger separates verified public upstream contributions from personal repositories, forks, and other public collaboration. Search matches alone are not proof of authorship: every included PR is checked against its detail endpoint.

Technical summaries describe the merged diff and public discussion. Reported upstream test or benchmark results are evidence in the linked PRs, not experiments independently rerun for this profile.

<!-- BEGIN AUTO:MERGED_PRS -->
Author: **cola1917** · **27 verified public merged PRs**.

Search scope: all visible merged-PR matches (31); 4 public matches excluded after verification. Non-public repository content is never exported. Dates below are UTC.

## Verified Upstream — Robotics & 3D

### newton-physics/newton [#4905](https://github.com/newton-physics/newton/pull/4905) — Reject non-finite contact materials at finalization

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-31T19:53:01Z
- **Contribution type:** bug_fix
- **Technical summary:** Rejected NaN and infinite contact-material values on colliding shapes during ModelBuilder.finalize(), with array/shape diagnostics. Covered direct, imported USD, and replicated inputs while preserving visual-only exemptions and validation opt-outs; this is not an importer-wide audit.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 5 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4905/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4905).

Key files: `newton/_src/sim/builder.py`, `newton/tests/steel/test_contacts.py`, `newton/tests/test_import_usd.py`, `newton/tests/test_model.py`.

### google-deepmind/mujoco\_warp [#1853](https://github.com/google-deepmind/mujoco_warp/pull/1853) — Fix contact sensor directions after reduction sorting

- **Repository:** [google-deepmind/mujoco_warp](https://github.com/google-deepmind/mujoco_warp)
- **Merged date:** 2026-10-30T18:11:10Z
- **Contribution type:** algorithm_correctness_fix, performance_preservation
- **Technical summary:** Kept contact direction attached to contact IDs through mindist/maxforce reduction sorting by complement-encoding negative directions. Removed the separate direction buffer while retaining the single-int GPU sort; regressions compare native MuJoCo across heterogeneous worlds and CPU/CUDA graph replay. Public PR measurements describe removal of a regression, not a general speedup.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 2 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/google-deepmind/mujoco_warp/pull/1853/files) · [API](https://api.github.com/repos/google-deepmind/mujoco_warp/pulls/1853).

Key files: `mujoco_warp/_src/sensor.py`, `mujoco_warp/_src/sensor_test.py`.

### newton-physics/newton [#4890](https://github.com/newton-physics/newton/pull/4890) — Fix runtime shape colors in the single-model RTX viewer

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-28T21:00:01Z
- **Contribution type:** bug_fix
- **Technical summary:** Restored runtime shape-color updates in the single-model RTX path through per-instance USD display-color readers. Kept built-instance mappings stable across viewer repacking and used a device-side change flag to avoid full color readback on unchanged frames, without rebuilding geometry.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 6 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4890/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4890).

Key files: `newton/_src/viewer/kernels.py`, `newton/_src/viewer/viewer_rtx.py`, `newton/_src/viewer/viewer_viser.py`, `newton/_src/viewer/viewer_viser_kernels.py`.

### colmap/colmap [#4892](https://github.com/colmap/colmap/pull/4892) — Expose Ceres solver thresholds in incremental mapping

- **Repository:** [colmap/colmap](https://github.com/colmap/colmap)
- **Merged date:** 2026-10-28T10:11:15Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Exposed five existing Ceres solver-selection image-count thresholds for local and global incremental bundle adjustment through C++ pipeline options, Mapper CLI/project settings, and PyCOLMAP. Preserved defaults and added propagation, round-trip, and reconstruction tests; no GPU performance claim.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 8 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/colmap/colmap/pull/4892/files) · [API](https://api.github.com/repos/colmap/colmap/pulls/4892).

Key files: `doc/faq.rst`, `src/colmap/controllers/incremental_pipeline.cc`, `src/colmap/controllers/incremental_pipeline.h`, `src/colmap/controllers/incremental_pipeline_test.cc`.

### newton-physics/newton [#4942](https://github.com/newton-physics/newton/pull/4942) — Preserve high-valence Style3D matrix connections

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-27T17:45:58Z
- **Contribution type:** algorithm_correctness_fix
- **Technical summary:** Prevented silent truncation of high-valence Style3D projective-dynamics matrix connections. Retry overflowed 32-wide assembly with topology-derived capacity and reject incomplete builders; regressions compare entries against dense assembly, symmetry, and translation-nullspace checks.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 4 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4942/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4942).

Key files: `newton/_src/solvers/style3d/builder.py`, `newton/_src/solvers/style3d/solver_style3d.py`, `newton/tests/test_solver_style3d.py`.

### colmap/colmap [#4903](https://github.com/colmap/colmap/pull/4903) — Improve CUDA driver failure diagnostics

- **Repository:** [colmap/colmap](https://github.com/colmap/colmap)
- **Merged date:** 2026-10-27T11:07:39Z
- **Contribution type:** bug_fix
- **Technical summary:** Added actionable insufficient-driver diagnostics and a common CUDA/HIP error formatter while preserving the zero-device return used by CPU-fallback callers. Added error-code/description tests; does not claim to fix Windows CLI exception termination or verify HIP execution.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 5 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/colmap/colmap/pull/4903/files) · [API](https://api.github.com/repos/colmap/colmap/pulls/4903).

Key files: `src/colmap/util/CMakeLists.txt`, `src/colmap/util/cuda.cc`, `src/colmap/util/cudacc.cc`, `src/colmap/util/cudacc.h`.

### newton-physics/newton [#4871](https://github.com/newton-physics/newton/pull/4871) — Fix IK tree-joint and body indexing

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-27T08:26:46Z
- **Contribution type:** algorithm_correctness_fix
- **Technical summary:** Corrected analytic IK forward-kinematics and Jacobian indexing when joint and body indices differ. Follow articulation-tree ancestors, seed external root poses, and reject unsupported objective links or multiply articulated bodies; loop-closure constraints are not enforced.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 8 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4871/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4871).

Key files: `newton/_src/sim/ik/ik_common.py`, `newton/_src/sim/ik/ik_lbfgs_optimizer.py`, `newton/_src/sim/ik/ik_lm_optimizer.py`, `newton/_src/sim/ik/ik_objectives.py`.

### pypose/pypose [#439](https://github.com/pypose/pypose/pull/439) — Preserve expanded views in Lie-group input broadcasting

- **Repository:** [pypose/pypose](https://github.com/pypose/pypose)
- **Merged date:** 2026-10-25T23:50:12Z
- **Contribution type:** performance_optimization, bug_fix
- **Technical summary:** Preserved expanded views instead of flattening and copying broadcast Lie-group inputs across SO3, SE3, RxSO3, and Sim3. Made Act outputs contiguous for downstream view compatibility; regressions cover non-contiguous/empty inputs and forward/backward equivalence. PR-reported allocation measurements support input-copy removal, not resolution of the original full bundle-adjustment OOM.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 3 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/pypose/pypose/pull/439/files) · [API](https://api.github.com/repos/pypose/pypose/pulls/439).

Key files: `pypose/lietensor/lietensor.py`, `pypose/lietensor/operation.py`, `tests/lietensor/test_broadcast_inputs.py`.

### newton-physics/newton [#4894](https://github.com/newton-physics/newton/pull/4894) — Fix runtime shape opacity in the single-model RTX viewer

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-22T22:44:18Z
- **Contribution type:** bug_fix
- **Technical summary:** Restored runtime shape-opacity updates in the single-model RTX viewer using per-instance opacity/IOR primvars and stable instance mappings. Preserved explicit fractional-opacity settings, reused device-side change detection, and added rendered-pixel regressions.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 3 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4894/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4894).

Key files: `newton/_src/viewer/viewer_rtx.py`, `newton/tests/test_viewer_rtx.py`.

### newton-physics/newton [#4874](https://github.com/newton-physics/newton/pull/4874) — Preserve L-BFGS autodiff line-search residuals

- **Repository:** [newton-physics/newton](https://github.com/newton-physics/newton)
- **Merged date:** 2026-10-22T10:36:06Z
- **Contribution type:** algorithm_correctness_fix
- **Technical summary:** Gave L-BFGS candidate residuals independent gradient storage so Warp tape.zero() cannot erase line-search costs and accept an increasing step. Added a CPU/CUDA regression through public IKSolver behavior.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 3 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/newton-physics/newton/pull/4874/files) · [API](https://api.github.com/repos/newton-physics/newton/pulls/4874).

Key files: `newton/_src/sim/ik/ik_lbfgs_optimizer.py`, `newton/tests/test_ik_lbfgs.py`.

## Fork Merges — Not Upstream Acceptance

### eric-heiden/newton [#17](https://github.com/eric-heiden/newton/pull/17) — Test MJCF camera intrinsics and mount transforms

- **Repository:** [eric-heiden/newton](https://github.com/eric-heiden/newton) (fork of newton-physics/newton)
- **Merged date:** 2026-10-29T19:01:42Z
- **Contribution type:** test_enhancement
- **Technical summary:** Added MJCF camera-import tests comparing inherited/physical/pixel intrinsics and moving-body mount transforms against native MuJoCo. Test-only merge into eric-heiden/newton, a fork; not a merged contribution to newton-physics/newton.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 1 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/eric-heiden/newton/pull/17/files) · [API](https://api.github.com/repos/eric-heiden/newton/pulls/17).

Key files: `newton/tests/test_import_mjcf.py`.

## Personal Repositories

### cola1917/ad-eval-suite [#11](https://github.com/cola1917/ad-eval-suite/pull/11) — refactor\(final\): unify CLI, module boundaries, config split and README

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T08:13:52Z
- **Contribution type:** refactor
- **Technical summary:** Unified evaluation, mining, simulation, and visualization entry points under one CLI; reorganized module boundaries, split configurations, and updated imports/tests/documentation.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 25 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/11/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/11).

Key files: `README.md`, `configs/eval.yaml`, `configs/sim.yaml`, `failure_mining/__init__.py`.

### cola1917/ad-eval-suite [#10](https://github.com/cola1917/ad-eval-suite/pull/10) — ci\(sim\): add xosc validation workflow with optional esmini smoke

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T04:48:13Z
- **Contribution type:** engineering_enhancement
- **Technical summary:** Added simulation-validation CI with default XOSC checks, opt-in manual esmini smoke execution, report artifacts, and temporary-file ignore rules.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 2 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/10/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/10).

Key files: `.github/workflows/sim-validation.yml`, `.gitignore`.

### cola1917/ad-eval-suite [#9](https://github.com/cola1917/ad-eval-suite/pull/9) — feat\(sim\): add xosc validation and esmini smoke tooling

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T04:39:11Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added OpenSCENARIO XML/semantic and optional XSD validation plus a batch esmini smoke runner with timeout/dry-run reports and unit tests.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 5 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/9/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/9).

Key files: `scripts/run_esmini_smoke.py`, `scripts/validate_xosc.py`, `simulator_export/__init__.py`, `simulator_export/validation.py`.

### cola1917/ad-eval-suite [#8](https://github.com/cola1917/ad-eval-suite/pull/8) — fix: include location metadata in failure-mining snapshots

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T03:12:44Z
- **Contribution type:** bug_fix
- **Technical summary:** Propagated map-location metadata into failure-mining snapshots so replay can select the appropriate map.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 1 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/8/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/8).

Key files: `failure_mining/pipeline.py`.

### cola1917/ad-eval-suite [#7](https://github.com/cola1917/ad-eval-suite/pull/7) — feat\(v2\): scenario replay and map overlay \(GIF export + lane/drivable-area overlay\)

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T03:01:53Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Extended replay integration with GIF export options, Pillow-based GIF handling, progress reporting, and export tests; the underlying map loader was introduced separately in #6.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 3 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/7/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/7).

Key files: `scripts/run_perception_eval.py`, `tests/unit/test_phase2_tools.py`, `tools/replay_scene.py`.

### cola1917/ad-eval-suite [#6](https://github.com/cola1917/ad-eval-suite/pull/6) — feat\(v2\): map overlay – lane lines and drivable area in replay outputs

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T02:53:00Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added raw nuScenes map geometry loading, viewport queries, lane/drivable-area overlays, snapshot location metadata, and replay export options.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 5 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/6/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/6).

Key files: `scenario/map_overlay.py`, `scenario/snapshot_schema.py`, `scripts/run_perception_eval.py`, `tests/unit/test_phase2_tools.py`.

### cola1917/ad-eval-suite [#5](https://github.com/cola1917/ad-eval-suite/pull/5) — Add scenario snapshot replay and xosc milestone

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-16T01:57:06Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added failure-case ranking, serialized scenario snapshots, frame replay, and initial OpenSCENARIO export with unit tests.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 13 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/5/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/5).

Key files: `failure_mining/__init__.py`, `failure_mining/error_aggregation.py`, `failure_mining/pipeline.py`, `failure_mining/rank_frames.py`.

### cola1917/ad-eval-suite [#4](https://github.com/cola1917/ad-eval-suite/pull/4) — Add perception CI and golden regression checks

- **Repository:** [cola1917/ad-eval-suite](https://github.com/cola1917/ad-eval-suite)
- **Merged date:** 2026-03-15T08:53:39Z
- **Contribution type:** test_enhancement
- **Technical summary:** Added fast/nightly perception CI, deterministic detection/tracking fixtures, golden metrics, and a regression runner.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 9 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/cola1917/ad-eval-suite/pull/4/files) · [API](https://api.github.com/repos/cola1917/ad-eval-suite/pulls/4).

Key files: `.github/workflows/ci-fast.yml`, `.github/workflows/ci-nightly.yml`, `eval/perception/regression_fixture.py`, `requirements.txt`.

## Other Public Collaboration

### ForgeAI-Robotics/fq-assets [#1](https://github.com/ForgeAI-Robotics/fq-assets/pull/1) — Add reviewed asset fq:scenes/room\_table\_can\_candidate

- **Repository:** [ForgeAI-Robotics/fq-assets](https://github.com/ForgeAI-Robotics/fq-assets)
- **Merged date:** 2026-11-01T00:27:36Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added a simulation-scene asset package with assembly manifests, MuJoCo/USD assets, provenance, previews, validation evidence, and catalog/checksum updates. Public merge verified; asset physics and approval process were not independently rerun.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 36 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/ForgeAI-Robotics/fq-assets/pull/1/files) · [API](https://api.github.com/repos/ForgeAI-Robotics/fq-assets/pulls/1).

Key files: `assets.lock.json`, `assets/generated/fq_scenes_room_table_can_candidate_a1b951c4/SOURCE_NOTICE.md`, `assets/generated/fq_scenes_room_table_can_candidate_a1b951c4/assembly.json`, `assets/generated/fq_scenes_room_table_can_candidate_a1b951c4/asset.json`.

### zwan0616/FIT5120\_TM11 [#51](https://github.com/zwan0616/FIT5120_TM11/pull/51) — Update sections 7 and 8 in PAIR\_PROGRAMMING.md with new content

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-05-12T14:35:25Z
- **Contribution type:** documentation
- **Technical summary:** Updated pair-programming documentation; this is a documentation contribution rather than an algorithm or simulation change.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 1 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/51/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/51).

Key files: `PAIR_PROGRAMMING.md`.

### zwan0616/FIT5120\_TM11 [#41](https://github.com/zwan0616/FIT5120_TM11/pull/41) — This PR improves Iteration 2 backend test coverage and cleans up the test/reporting workflow.

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-04-30T11:34:30Z
- **Contribution type:** test_enhancement, engineering_enhancement
- **Technical summary:** Expanded challenge-status and rule-based backend tests, migrated API smoke checks to pytest, added integration metrics/retry support and mock-AI controls, and revised report/coverage configuration.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 18 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/41/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/41).

Key files: `.github/workflows/test-flow.yml`, `nutri-health-api/app/routers/scan.py`, `nutri-health-api/app/services/gemini.py`, `tests/api-deploy/README.md`.

### zwan0616/FIT5120\_TM11 [#35](https://github.com/zwan0616/FIT5120_TM11/pull/35) — Revise feedback messages in daily healthy challenge

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-04-25T09:36:56Z
- **Contribution type:** content_update
- **Technical summary:** Revised user-facing feedback strings in daily-challenge seed data.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 1 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/35/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/35).

### zwan0616/FIT5120\_TM11 [#31](https://github.com/zwan0616/FIT5120_TM11/pull/31) — Fix whitebox test regressions

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-04-21T10:37:10Z
- **Contribution type:** bug_fix
- **Technical summary:** Removed the pytest-asyncio dependency from daily-challenge white-box tests using asyncio.run and aligned scan-recognition fixtures with the current contract.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 2 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/31/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/31).

Key files: `tests/whitebox/test_daily_challenge_router.py`, `tests/whitebox/test_scan_router.py`.

### zwan0616/FIT5120\_TM11 [#30](https://github.com/zwan0616/FIT5120_TM11/pull/30) — Add daily healthy challenge API

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-04-20T10:16:48Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added a seeded daily-challenge database model, selection/completion API routes, startup initialization, and white-box/integration tests.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 15 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/30/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/30).

Key files: `DATA_DICTIONARY.md`, `nutri-health-api/README.md`, `nutri-health-api/app/etl/sql/check_seed_counts.sql`, `nutri-health-api/app/main.py`.

### zwan0616/FIT5120\_TM11 [#27](https://github.com/zwan0616/FIT5120_TM11/pull/27) — ci: organize test flow with smoke/regression suites and reporting

- **Repository:** [zwan0616/FIT5120_TM11](https://github.com/zwan0616/FIT5120_TM11)
- **Merged date:** 2026-04-18T09:48:10Z
- **Contribution type:** engineering_enhancement
- **Technical summary:** Organized CI into white-box, API smoke, and API regression jobs, with coverage/JUnit artifacts and consolidated Markdown reports.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 20 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/zwan0616/FIT5120_TM11/pull/27/files) · [API](https://api.github.com/repos/zwan0616/FIT5120_TM11/pulls/27).

Key files: `.github/workflows/test-flow.yml`, `tests/README.md`, `tests/api-deploy/README.md`, `tests/api-deploy/scripts/api_regression_test.sh`.

### yipingho/FIT5120\_TM11 [#1](https://github.com/yipingho/FIT5120_TM11/pull/1) — Add CN2026 ETL seed pipeline and anomaly reporting

- **Repository:** [yipingho/FIT5120_TM11](https://github.com/yipingho/FIT5120_TM11)
- **Merged date:** 2026-04-03T13:41:57Z
- **Contribution type:** feature_enhancement
- **Technical summary:** Added PostgreSQL catalog models, raw-to-seed ETL, configurable nutrition rules, seed loading, consistency SQL, and anomaly reporting with generated seed/staging artifacts.
- **Evidence / verification:** author `cola1917`; non-null `merged_at`; public base; 32 changed files verified. Summary: diff_and_discussion_reviewed. [Merged diff](https://github.com/yipingho/FIT5120_TM11/pull/1/files) · [API](https://api.github.com/repos/yipingho/FIT5120_TM11/pulls/1).

Key files: `DATA_DICTIONARY.md`, `nutri-health-api/README.md`, `nutri-health-api/app/database.py`, `nutri-health-api/app/etl/__init__.py`.

## Excluded Search Matches

Search can include bot-authored matches. These are not counted above.

- [PR](https://github.com/cola1917/FIT5120_TM11/pull/1): author_mismatch; detail-endpoint author `Copilot`.
- [PR](https://github.com/cola1917/ad-eval-suite/pull/2): author_mismatch; detail-endpoint author `Copilot`.
- [PR](https://github.com/cola1917/cola1917.github.io/pull/1): author_mismatch; detail-endpoint author `Copilot`.
- [PR](https://github.com/zwan0616/FIT5120_TM11/pull/54): author_mismatch; detail-endpoint author `Copilot`.
<!-- END AUTO:MERGED_PRS -->

## Maintenance

See [MAINTENANCE.md](MAINTENANCE.md) for synchronization, editorial review, and validation instructions.
