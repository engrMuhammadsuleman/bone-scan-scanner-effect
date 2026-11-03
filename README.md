# Scanner effect in deep-learning classification of whole-body bone scintigraphy

Code for the study **"Investigating the Scanner Effect and Developing a Robust Deep Learning Method for the Classification of Whole-Body Bone Scintigraphy"** (M. Suleman, L. Ali, J. Khan, Y. Qandeel, A. Farid, A. Rehman, K. Ullah).

The study measures how much a dual-view CNN loses when it is applied to a gamma camera it was not trained on, and compares strategies to recover the loss: BS-80K pre-training, two-camera training, unsupervised domain adaptation (DANN, Deep CORAL), threshold recalibration with a few labelled patients, and domain generalisation (intensity normalisation, intensity augmentation, MixStyle).

## Contents

| Notebook | Purpose | Hardware |
|---|---|---|
| `01_bs80k_backbones.ipynb` | Trains the four backbones on BS-80K (metastasis vs normal); provides the BS-80K initialisation | GPU |
| `02_prepare_dataset.ipynb` | Builds the classification cohort: pairs ANT/POST images, cleans IDs, image-level duplicate audit, fixed folds | CPU |
| `03_within_and_cross_camera.ipynb` | Within-camera 5-fold CV and cross-camera evaluation (the scanner effect) | GPU |
| `04_two_camera_training.ipynb` | Two-camera training, full and size-matched | GPU |
| `05_domain_adaptation_and_recalibration.ipynb` | DANN, Deep CORAL and threshold recalibration (20 labelled target patients) | GPU |
| `06_domain_generalisation.ipynb` | Intensity normalisation, intensity augmentation, MixStyle | GPU |
| `07_bs80k_only_to_cameras.ipynb` | Models trained on BS-80K only, tested on each camera, with and without adaptation | GPU |
| `08_metastatic_predictions_and_features.ipynb` | Per-patient predictions and image features of the metastatic class | CPU |
| `09_gradcam.ipynb` | Grad-CAM maps for the metastatic class | GPU |
| `make_manuscript_figures.py` | Figures of the manuscript from the summary results | CPU |

All files are in the repository root. Run the notebooks in this order. Each notebook has a `QUICK_TEST` switch: run once with `True` (a few minutes) to check the pipeline, then with `False`. Training notebooks are resume-safe: finished runs are logged and skipped when the notebook is run again.

## Setup

The notebooks were run on Google Colab (T4 GPU) with the data on Google Drive. Set `BASE` in the first cell to your data folder. Expected layout:

```
BASE/
  Anterior/ , Posterior/        whole-body images, one folder per camera and label
  Machine_1.xlsx, Machine_2.xlsx optional label sheets (used only for a consistency check)
  bs80k/                        created by notebook 01
  prepared_v3/                  created by notebook 02
  revision/                     results of notebooks 03-09
```

Optional local files that are not published: `manual_fixes.json` (patient IDs saved under two names) and `relabelled_ids.json` (patients relabelled after training).

Install the requirements with `pip install -r requirements.txt` when running outside Colab.

## Protocol (shared by all notebooks)

- Dual-view network: shared backbone for ANT and POST, concatenated features, MLP head; backbones EfficientNetV2-S, ResNeXt50, RegNetY-1.6GF, Inception-v3 (timm); ImageNet or BS-80K initialisation.
- Five tasks: three-class; metastatic vs non-metastatic; metastatic vs normal; metastatic vs degenerative; degenerative vs normal.
- Within-camera stratified 5-fold CV, 15% class- and camera-stratified inner validation split for early stopping, seeds 42/43/44, probabilities averaged per patient over seeds.
- Patient-level bootstrap (10,000 resamples, shared across models) for confidence intervals and p-values; Holm correction for families of comparisons.

## Data availability

Patient images and labels are **not** included in this repository. The de-identified dataset is available from the corresponding author under a data-use agreement that prohibits re-identification. BS-80K is publicly available (Huang et al., Computers in Biology and Medicine 151 (2022) 106221).

## Contact

Muhammad Suleman, University of Science and Technology Bannu (sulemanktk@ustb.edu.pk).

## License

MIT (see `LICENSE`).
