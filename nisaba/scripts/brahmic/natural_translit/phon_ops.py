# Copyright 2022 Nisaba Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Multilingual phonological operations."""

import pynini as p
from pynini.export import multi_grm
import nisaba.scripts.brahmic.natural_translit.constants as c

# TODO: Phonological model
_NASAL = p.union('m', 'n', 'ni', 'ng', 'nn', 'ny', 'nsl')


def _rw_ph_context(
    gr, in_ph, out_ph, post_str=c.EPSILON, pre_str=c.EPSILON) -> p.Fst:
  """Rewrites the phoneme assigned to a grapheme in context.

  In an alignment (gr=ph_in), changes the assigned phoneme, resulting in
  (gr=ph_out), based on the context such as post-nasal or word final.

  Following call

  ```
  _rw_ph_context('ans', 'nsl', 'm', pre_str=labial)
  ```
  would return:
  ```
  p.cdrewrite(p.cross('(ans=nsl)', '(ans=m)'),
                      '',
                      c.L_SIDE + labial + c.PH_END,
                      c.SIGMA_STAR).optimize()
  ```

  Args:
    gr: grapheme, ans in the example
    in_ph: input phoneme, nsl in the example
    out_ph: output phoneme, m in the example
    post_str: preceeding context, eg. if nasal, the rule is post-nasal
    pre_str: following context, eg. if labial, the rule is pre-labial

  Returns:
    Rewrite rule FST.
  """

  in_algn = c.L_BOUND + gr + c.ASSIGN + in_ph + c.R_BOUND
  out_algn = c.L_BOUND + gr + c.ASSIGN + out_ph + c.R_BOUND

  return p.cdrewrite(p.cross(in_algn, out_algn),
                     post_str,
                     pre_str,
                     c.SIGMA_STAR).optimize()


def _rw_ph_phoneme(
    gr, in_ph, out_ph, post_ph=c.EPSILON, pre_ph=c.EPSILON) -> p.Fst:
  """_rw_ph_context special case, context is defined by phonemes.

  Sample argument is 'ans' instead of c.L_SIDE + ans + c.PH_END

  Args:
    gr: grapheme, ans in the example
    in_ph: input phoneme, nsl in the example
    out_ph: output phoneme, m in the example
    post_ph: preceeding phoneme, eg. if nasal, the rule is post-nasal
    pre_ph: following phoneme, eg. if labial, the rule is pre-labial

  Returns:
    Rewrite rule FST.
  """

  post_str = c.EPSILON
  pre_str = c.EPSILON
  if post_ph is not c.EPSILON:
    post_str = c.PH_BEGIN + post_ph + c.R_BOUND
  if pre_ph is not c.EPSILON:
    pre_str = c.L_SIDE + pre_ph + c.PH_END
  return _rw_ph_context(gr, in_ph, out_ph, post_str, pre_str)


def _rw_ph_word_final(gr, in_ph, out_ph, post_ph=c.EPSILON) -> p.Fst:
  """_rw_ph_context special case, preceeding phoneme, following eos."""

  post_str = c.EPSILON
  if post_ph is not c.EPSILON:
    post_str = c.PH_BEGIN + post_ph + c.R_BOUND
  return _rw_ph_context(gr, in_ph, out_ph, post_str, c.EOS)


## Anusvara place of articulation assimilation functions
def _anusvara_assimilation_labial() -> p.Fst:
  labial = p.union('b', 'm', 'p')
  return _rw_ph_phoneme('ans', 'nsl', 'm', pre_ph=labial)

ANUSVARA_ASSIMILATION_LABIAL = _anusvara_assimilation_labial()


def _anusvara_assimilation_dental() -> p.Fst:
  dental = p.union('di', 'ni', 'ti')
  return _rw_ph_phoneme('ans', 'nsl', 'ni', pre_ph=dental)

ANUSVARA_ASSIMILATION_DENTAL = _anusvara_assimilation_dental()


def _anusvara_assimilation_alveolar() -> p.Fst:
  alveolar = p.union('t', 'd', 'n')
  return _rw_ph_phoneme('ans', 'nsl', 'n', pre_ph=alveolar)

ANUSVARA_ASSIMILATION_ALVEOLAR = _anusvara_assimilation_alveolar()


def _anusvara_assimilation_palatal() -> p.Fst:
  palatal = p.union('y', 'ny')
  return _rw_ph_phoneme('ans', 'nsl', 'ny', pre_ph=palatal)

ANUSVARA_ASSIMILATION_PALATAL = _anusvara_assimilation_palatal()


def _anusvara_assimilation_retroflex() -> p.Fst:
  retroflex = p.union('dd', 'nn', 'tt')
  return _rw_ph_phoneme('ans', 'nsl', 'nn', pre_ph=retroflex)

ANUSVARA_ASSIMILATION_RETROFLEX = _anusvara_assimilation_retroflex()


def _anusvara_assimilation_velar() -> p.Fst:
  velar = p.union('g', 'ng', 'k')
  return _rw_ph_phoneme('ans', 'nsl', 'ng', pre_ph=velar)

ANUSVARA_ASSIMILATION_VELAR = _anusvara_assimilation_velar()

ANUSVARA_ASSIMILATION = (ANUSVARA_ASSIMILATION_LABIAL @
                         ANUSVARA_ASSIMILATION_DENTAL @
                         ANUSVARA_ASSIMILATION_ALVEOLAR @
                         ANUSVARA_ASSIMILATION_PALATAL @
                         ANUSVARA_ASSIMILATION_RETROFLEX @
                         ANUSVARA_ASSIMILATION_VELAR).optimize()

# Unassimilated anusvara defaults to n.
DEFAULT_ANUSVARA_DENTAL = _rw_ph_phoneme('ans', 'nsl', 'ni')

# Unassimilated anusvara defaults to m.
DEFAULT_ANUSVARA_LABIAL = _rw_ph_phoneme('ans', 'nsl', 'm')

# Word final anusvara nasalizes the preceding vowel.
FINAL_ANUSVARA_NASALIZATION = _rw_ph_word_final('ans', _NASAL, 'nsl')


def _intersonorant_voicing() -> p.Fst:
  """Voicing between vowels, approximants, and nasals."""

  vowel = p.union('a', 'a_l', 'ae',
                  'e', 'e_l',
                  'i', 'i_l',
                  'o', 'o_l',
                  'u', 'u_l')
  approximant = p.accep('y')
  sonorant = p.union(vowel, _NASAL, approximant)
  return _rw_ph_phoneme('t', 'ti', 'di', sonorant, sonorant)

INTERSONORANT_VOICING = _intersonorant_voicing()


def _jny_to_gny() -> p.Fst:
  """jny pronounced as gny."""

  return p.cdrewrite(p.cross('(j=jh)(ny=ny)', '(j,ny=g,ny)'),
                     '',
                     '',
                     c.SIGMA_STAR).optimize()

JNY_TO_GNY = _jny_to_gny()


def _jny_to_gy() -> p.Fst:
  """jny pronounced as gy."""

  return p.cdrewrite(p.cross('(j=jh)(ny=ny)', '(j,ny=g,y)'),
                     '',
                     '',
                     c.SIGMA_STAR).optimize()

JNY_TO_GY = _jny_to_gy()


def _jny_to_ny() -> p.Fst:
  """jny pronounced as ny."""

  return p.cdrewrite(p.cross('(j=jh)(ny=ny)', '(j,ny=ny)'),
                     '',
                     '',
                     c.SIGMA_STAR).optimize()

JNY_TO_NY = _jny_to_ny()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for multilingual phonological operations."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['VOICING'] = INTERSONORANT_VOICING
      exporter['ANUSVARA_ASSIMILATION_LABIAL'] = ANUSVARA_ASSIMILATION_LABIAL
      exporter['ANUSVARA_ASSIMILATION_DENTAL'] = ANUSVARA_ASSIMILATION_DENTAL
      exporter[
          'ANUSVARA_ASSIMILATION_ALVEOLAR'] = ANUSVARA_ASSIMILATION_ALVEOLAR
      exporter['ANUSVARA_ASSIMILATION_PALATAL'] = ANUSVARA_ASSIMILATION_PALATAL
      exporter[
          'ANUSVARA_ASSIMILATION_RETROFLEX'] = ANUSVARA_ASSIMILATION_RETROFLEX
      exporter['ANUSVARA_ASSIMILATION_VELAR'] = ANUSVARA_ASSIMILATION_VELAR
      exporter['ANUSVARA_ASSIMILATION'] = ANUSVARA_ASSIMILATION
      exporter['DEFAULT_ANUSVARA_DENTAL'] = DEFAULT_ANUSVARA_DENTAL
      exporter['DEFAULT_ANUSVARA_LABIAL'] = DEFAULT_ANUSVARA_LABIAL
      exporter['FINAL_ANUSVARA_NASALIZATION'] = FINAL_ANUSVARA_NASALIZATION
      exporter['JNY_TO_GNY'] = JNY_TO_GNY
      exporter['JNY_TO_GY'] = JNY_TO_GY
      exporter['JNY_TO_NY'] = JNY_TO_NY


if __name__ == '__main__':
  multi_grm.run(generator_main)
