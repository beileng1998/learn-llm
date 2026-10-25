# MNIST subset

`mnist-12k.npz` holds 12,000 images from the MNIST database of handwritten digits:
10,000 from its training set and 2,000 from its test set, chosen at random with a fixed seed
(2026), stored as 28 × 28 grayscale images (0 = white, 255 = black) with their labels.

- **Source:** the MNIST database by Yann LeCun (Courant Institute, NYU), Corinna Cortes
  (Google Labs, New York) and Christopher J. C. Burges (Microsoft Research), derived from
  NIST Special Databases 1 and 3. Files fetched from the mirror at
  `https://storage.googleapis.com/cvdf-datasets/mnist/`; their SHA-256 sums match the
  published originals.
- **Licence:** MNIST is distributed under the Creative Commons Attribution-Share Alike 3.0
  licence (CC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0/), copyright
  Yann LeCun and Corinna Cortes. This subset is an adaptation and is shared under the same
  licence. It is not covered by the repository's MIT or CC BY 4.0 licences.
- **Changes:** only the selection of images; pixel values and labels are unchanged.
