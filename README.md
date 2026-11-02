# Jiangtao Wang

**Robotics Simulation | Physical AI | Sim2Real**

I work on robot simulation, demonstration retargeting, and simulation data pipelines.
My open-source contributions focus on numerical correctness, GPU memory efficiency, and reproducible regression tests.

## Open Source Contributions

<!-- BEGIN AUTO:SELECTED_CONTRIBUTIONS -->
**10 merged upstream PRs** across Newton, MuJoCo Warp, PyPose, and COLMAP. Selected work:

- **[Newton](https://github.com/newton-physics/newton)** — Corrected IK tree/body indexing and autodiff L-BFGS residual ownership; repaired high-valence cloth matrix assembly. [#4871](https://github.com/newton-physics/newton/pull/4871) · [#4874](https://github.com/newton-physics/newton/pull/4874) · [#4942](https://github.com/newton-physics/newton/pull/4942)
- **[MuJoCo Warp](https://github.com/google-deepmind/mujoco_warp)** — Fixed signed contact-sensor reductions with complement-encoded IDs, preserving the single-int GPU sort. [#1853](https://github.com/google-deepmind/mujoco_warp/pull/1853)
- **[PyPose](https://github.com/pypose/pypose)** — Removed expanded-input copies in Lie-group broadcasting while preserving gradient behavior and contiguous Act outputs. [#439](https://github.com/pypose/pypose/pull/439)
- **[COLMAP](https://github.com/colmap/colmap)** — Exposed incremental bundle-adjustment solver thresholds in C++ / CLI / Python and improved CUDA driver diagnostics. [#4892](https://github.com/colmap/colmap/pull/4892) · [#4903](https://github.com/colmap/colmap/pull/4903)

[View All Merged PRs](https://github.com/pulls?q=is%3Apr+is%3Amerged+author%3Acola1917) · [Verified contribution ledger](CONTRIBUTIONS.md)

*Upstream merges only above; personal repositories and fork merges are listed separately in the ledger.*
<!-- END AUTO:SELECTED_CONTRIBUTIONS -->

## Selected Projects

*The following projects and metrics are self-reported; public code and experiment records have not been independently verified.*

**Ego Demonstration Retargeting**<br>
DaID-based egocentric dexterous manipulation reconstruction and hand–object retargeting, with MPPI physical search and PPO feedback control.<br>
276-frame reference build: **1,564 → 354 s (4.41×)**; fixed development-set basket success: **34.4% → 73.4%**.

**3D Reconstruction & Simulation Assets**<br>
RGB-D / 3DGS / mesh workflows for scene geometry and material recovery, including metric scale and collision-proxy repair.<br>
Differentiable rendering and PBR material optimization with Lambert + GGX.

**Simulation Data Generation & Sim2Real**<br>
SIMPLE / CuRobo pipelines for G1 + O6/O7: **1,000 successful physical manipulation trajectories**, GR00T fine-tuning, and closed-loop evaluation.<br>
Reported experiment results: **86.7% simulation / 60% real-robot success**, with no real-robot training data.

## Technical Stack

- **Robotics:** Robot kinematics · collision detection · MPPI · CuRobo
- **Physics:** MuJoCo · Newton · NVIDIA Warp
- **Learning:** PPO · GR00T · VLA · Sim2Real
- **Graphics:** RGB-D · 3DGS · differentiable rendering · PBR
- **Engineering:** Python · C++ · Git · regression testing

## Links

[GitHub](https://github.com/cola1917) · [Engineering Notes](https://cola1917-github-io-six.vercel.app/en/)
