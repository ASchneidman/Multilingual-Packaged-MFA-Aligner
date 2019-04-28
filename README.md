# Multilingual-Packaged-MFA-Aligner

## align.py
Given a youtube video id and language, aligns audio to transcript using the Montreal Forced Aligner. Before using, must have MFA
downloaded and installed. https://montreal-forced-aligner.readthedocs.io/en/latest/introduction.html

For the language you'd like to align to, place the language and g2p models (.zip files) in the working directory

https://montreal-forced-aligner.readthedocs.io/en/latest/pretrained_models.html

and change the `G2P_MODEL` and `LANG_MODEL` paramters to their locations. Additionally, change the `MFA_ALIGNER`
parameter to the directory where you downloaded the Montreal Forced Aligner.

