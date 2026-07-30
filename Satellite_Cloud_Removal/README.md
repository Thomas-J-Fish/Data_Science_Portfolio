# Satellite Cloud Removal — Project Reference Document

## The Task,Three-Model Plan

**Cloud removal**: satellite optical imagery is frequently obscured by cloud cover.
Sentinel-1 SAR (radar) imagery of the same location penetrates cloud and is available
regardless of weather. The general task is to reconstruct a cloud-free optical image
using some combination of the cloudy optical image and/or the SAR image as input.

Decided plan: **build three separate models, in this order**, forming a genuine ablation
study rather than picking one architecture upfront:

1. **Cloudy optical → clean optical** (no SAR at all). **← Building this one first.**
   Closest structural parallel to the EBSD project (single image in, single image out),
   simplest architecture, and — critically — buildable *right now* on data that's already
   accessible, since it needs no SAR channel at all.
2. **SAR only → optical** (no cloudy image at all). Deferred until real multi-band SAR
   data is available (see Section 4 — the current data mirror doesn't provide this at
   usable fidelity).
3. **SAR + cloudy optical → clean optical** (the original, full fusion design). Built
   last, once (1) and (2) both exist, so its improvement over each can be measured
   directly rather than assumed.

## Dataset: SEN12MS-CR

Ebel, P., Meraner, A., Schmitt, M., & Zhu, X.X. (2020). "Multisensor Data Fusion for
Cloud Removal in Global and All-Season Sentinel-2 Imagery." *IEEE Transactions on
Geoscience and Remote Sensing.* Project page:
https://patricktum.github.io/cloud_removal/sen12mscr/

- 122,218 co-registered patch triplets, 256×256 px, 175 globally distributed ROIs,
  spanning all four seasons of 2018.
- Each triplet: Sentinel-1 SAR (2 channels, VV/VH backscatter, dB scale), cloudy
  Sentinel-2 optical (13 spectral bands), and **genuinely observed** (not synthetic)
  cloud-free Sentinel-2 optical (13 bands) for the same patch.
- 16-bit GeoTIFFs in the official release. CC BY 4.0 license.
- Official host: TUM's research data server, `dataserv.ub.tum.de` (catalog page:
  `mediatum.ub.tum.de/1554803`).

## Conceptual Grounding

**Why EBSD works with a single image in, single image out, and cloud removal is
harder.** Kinematical → dynamical EBSD patterns are two different-fidelity calculations
from the *same* underlying inputs (same crystal, same orientation, same voltage) —
dynamical is a deterministic refinement of physics the kinematical input already fully
specifies. Nothing is missing; it's "sharpen this approximation." Cloudy → clean optical
is fundamentally different: under an opaque cloud, the sensor's photons never reached the
ground — the true value for those pixels was never recorded anywhere in the input. That's
genuinely missing information, not a coarser version of the answer.

**So does cloudy-only reconstruction just reduce to hallucination?** Partially, under
thick cloud — but there's real, directly relevant precedent showing it's still far better
than nothing. Sarukkai, Uzkent, Jain & Ermon (2020), "Cloud Removal in Satellite Images
Using Spatiotemporal Generative Networks" (arXiv:1912.06838), trained a plain Pix2Pix
model on single cloudy-image-in/clean-image-out pairs — no SAR, no temporal information,
exactly Model 1's setup. Results on a downstream EuroSAT land-cover classification task
(10 classes): 72.48% accuracy on raw cloudy images, 90.60% using the Pix2Pix-reconstructed
images, against a 98.66% ceiling from true cloud-free images — recovering roughly
three-quarters of the total possible accuracy gap with zero auxiliary data. Image-quality
numbers (PSNR 8.78→22.89, SSIM only 0.398→0.437) show the characteristic signature of
this: huge gains from removing haze/washed-out brightness (easy), much smaller gains in
true fine-structure recovery under thick occlusion (hard) — consistent with their own
qualitative description of "reasonable, if sometimes blurry, inferences about the ground
beneath the occlusions."

**Why SAR-only (Model 2) isn't a clean fix either.** SAR backscatter measures physical
structure/roughness/moisture; optical color measures chemical/pigment composition. These
correlate via shared real-world causes (land-cover type) but are not the same quantity —
SAR does not uniquely determine color. The literature's term for this is **color
ill-posedness**, with documented symptoms even in dedicated SAR→optical translation
methods: color inconsistency, blurred/merged buildings in dense urban areas, occasional
hallucinations — despite generally getting scene structure and layout right. A further,
easy-to-miss downside: in the many patches with only *partial* cloud cover, going
SAR-only would replace already-correct, genuinely-observed color in the clear regions
with a lower-fidelity learned guess — a regression relative to cloudy-only precisely
where cloudy-only needs no help at all.

## Repository

```
Satellite_Cloud_Removal/
├── README.md                  (this file)
├── data/
│   └── raw/
│       ├── train/{clean,cloudy}/*.png   ← being built now (Phase 1)
│       └── test/{clean,cloudy}/*.png
├── notebooks/
│   └── 00_recon.ipynb          Phase 0 recon — HF streaming sanity check, done
└── src/                         Dataset class, models, training loop — to be built
```
Local conda env:
`satcloud` (Python 3.11; `datasets`, `pillow`, `matplotlib`, `numpy`).
