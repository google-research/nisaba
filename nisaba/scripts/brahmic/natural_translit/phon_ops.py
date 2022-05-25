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
_PH_END = (c.SEP | c.R_BOUND)
_NASAL = p.union('m', 'n', 'ni', 'ng', 'nn', 'ny', 'nsl')


def _anusvara_assimilation() -> p.Fst:
  """Place of articulation assimilation of anusvara."""

  labial = p.union('b', 'm', 'p')
  dental = p.union('di', 'ni', 'ti')
  alveolar = p.union('t', 'd', 'n')
  palatal = p.union('y', 'ny')
  retroflex = p.union('dd', 'nn', 'tt')
  velar = p.union('g', 'ng', 'k')

  labial_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=m)'),
                                    '',
                                    (c.L_SIDE + labial + _PH_END),
                                    c.SIGMA_STAR).optimize()

  dental_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=ni)'),
                                    '',
                                    (c.L_SIDE + dental + _PH_END),
                                    c.SIGMA_STAR).optimize()

  alveolar_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=n)'),
                                      '',
                                      (c.L_SIDE + alveolar + _PH_END),
                                      c.SIGMA_STAR).optimize()

  palatal_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=ny)'),
                                     '',
                                     (c.L_SIDE + palatal + _PH_END),
                                     c.SIGMA_STAR).optimize()

  retroflex_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=nn)'),
                                       '',
                                       (c.L_SIDE + retroflex + _PH_END),
                                       c.SIGMA_STAR).optimize()

  velar_assimilation = p.cdrewrite(p.cross('(ans=nsl)', '(ans=ng)'),
                                   '',
                                   (c.L_SIDE + velar + _PH_END),
                                   c.SIGMA_STAR).optimize()

  return (labial_assimilation @
          dental_assimilation @
          alveolar_assimilation @
          palatal_assimilation @
          retroflex_assimilation @
          velar_assimilation)

ANUSVARA_ASSIMILATION = _anusvara_assimilation()


def _default_anusvara_dental() -> p.Fst:
  """Remaining anusvara default to n."""

  dental_anusvara = p.cdrewrite(p.cross('(ans=nsl)', '(ans=ni)'),
                                '',
                                '',
                                c.SIGMA_STAR).optimize()
  return dental_anusvara

DEFAULT_ANUSVARA_DENTAL = _default_anusvara_dental()


def _default_anusvara_labial() -> p.Fst:
  """Remaining anusvara default to m."""

  labial_anusvara = p.cdrewrite(p.cross('(ans=nsl)', '(ans=m)'),
                                '',
                                '',
                                c.SIGMA_STAR).optimize()
  return labial_anusvara

DEFAULT_ANUSVARA_LABIAL = _default_anusvara_labial()


def _wf_anusvara_nasalization() -> p.Fst:
  """Word final anusvara nasalizes the preceding vowel."""

  eos = p.accep('[EOS]')

  wf_anusvara = p.cdrewrite(p.cross(_NASAL, 'nsl'),
                            p.accep('ans='),
                            c.R_BOUND + eos,
                            c.SIGMA_STAR).optimize()
  return wf_anusvara

WF_ANUSVARA_NASALIZATION = _wf_anusvara_nasalization()


def _intersonorant_voicing() -> p.Fst:
  """Voicing between vowels, approximants, and nasals."""

  vowel = p.union('a', 'a_l', 'ae',
                  'e', 'e_l',
                  'i', 'i_l',
                  'o', 'o_l',
                  'u', 'u_l')
  approximant = p.accep('y')
  sonorant = p.union(vowel, _NASAL, approximant)

  voicing_aux = p.cross('(t=ti)', '(t=di)')

  # TODO: add test to cover voicing with substring assignments
  voicing = p.cdrewrite(voicing_aux,
                        (sonorant + c.R_BOUND),
                        (c.L_SIDE + sonorant + _PH_END),
                        c.SIGMA_STAR).optimize()

  return voicing

INTERSONORANT_VOICING = _intersonorant_voicing()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for multilingual phonological operations."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['VOICING'] = INTERSONORANT_VOICING
      exporter['ANUSVARA_ASSIMILATION'] = ANUSVARA_ASSIMILATION
      exporter['DEFAULT_ANUSVARA_DENTAL'] = DEFAULT_ANUSVARA_DENTAL
      exporter['DEFAULT_ANUSVARA_LABIAL'] = DEFAULT_ANUSVARA_LABIAL
      exporter['WF_ANUSVARA_NASALIZATION'] = WF_ANUSVARA_NASALIZATION


if __name__ == '__main__':
  multi_grm.run(generator_main)
