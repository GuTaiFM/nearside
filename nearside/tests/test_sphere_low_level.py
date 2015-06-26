# Copyright (C) 2015  Randy Direen <nearside@direentech.com>
#
# This file is part of NearSide.
#
# NearSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NearSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NearSide.  If not, see <http://www.gnu.org/licenses/>

"""***************************************************************************

         test_sphere_low_level: test spherical case low level routines 

Randy Direen
4/3/2015

Test the low level spherical probe correction routines.

***************************************************************************"""


from __future__ import division
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from unittest import TestCase

from six.moves import range  #use range instead of xrange

import numpy as np
import nearside.spherical as ns
import nearside.spherical.low_level


class TestSphereLowLevelProbeCorrect(TestCase):

    def test_wigner3j_mzero_squared(self):
        """:: Test computation of the Wigner 3j symboles
        
        The test compares the output to the same routine written in Matlab
        """

        sll = ns.low_level

        # These were computed in MATLAB and copied here:
        ml = [[1],
             [0.333333333333333],
             [0.200000000000000],
             [0.142857142857143],
             [0.333333333333333],
             [0.333333333333333, 0.133333333333333],
             [0.133333333333333, 0.085714285714286],
             [0.085714285714286, 0.063492063492063],
             [0.200000000000000],
             [0.133333333333333, 0.085714285714286],
             [0.200000000000000, 0.057142857142857, 0.057142857142857],
             [0.085714285714286, 0.038095238095238, 0.043290043290043],
             [0.142857142857143],
             [0.085714285714286, 0.063492063492063],
             [0.085714285714286, 0.038095238095238, 0.043290043290043],
             [0.142857142857143],
             [0.085714285714286, 0.063492063492063],
             [0.085714285714286, 0.038095238095238, 0.043290043290043],
             [0.142857142857143, 0.038095238095238, 0.025974025974026, 0.033300033300033],
             ]

        idx = 0
        for j2 in range(0,4):
            for j3 in range(0,4):
                value_python = sll.wigner3j_mzero_squared(j2, j3)
                value_matlab = ml[idx]
                max = np.amax(np.abs(value_matlab))
                for n, _ in enumerate(ml[idx]): 
                    self.assertAlmostEqual(value_python[n] / max,
                                           value_matlab[n] / max,
                                           places=12)

                idx += 1

    def test_bc(self):
        """:: Test computation of the bc coefficients used for translation

        The test compares the output to the same routine written in Matlab
        """
        sll = ns.low_level   
        
        # These were computed in MATLAB and copied here:
        ml = [[0.282094791773878, 0.244301255951460, 0.063078313050504],
              [0, 0.189234939151512, 0.244301255951460, 0.082588898361159],
              [0, 0, 0.165177796722317, 0.244301255951460, 0.092337195461186],
              [0, 0.189234939151512, 0.244301255951460, 0.082588898361159],
              [0.282094791773878, 0.081433751983820, 0.045055937893217,
               0.213243618622923, 0.107464682580525],
              [0, 0.220237062296423, 0.106621809311462, 0.021026104350168, 
               0.198678011253707, 0.119807348622282],
              [0, 0, 0.165177796722317, 0.244301255951460, 0.092337195461186],
              [0, 0.220237062296423, 0.106621809311462, 0.021026104350168,
               0.198678011253707, 0.119807348622282],
              [0.282094791773878, 0.040716875991910, 0.094617469575756, 
               0.124392110863372, 0.004274163511725, 0.177197458262763, 
               0.133361962799220]
              ]

        idx = 0
        for nu in range(1,4):
            for n in range(1,4):
                value_python = sll.bc(nu, n)
                value_matlab = ml[idx]
                max = np.amax(np.abs(value_matlab))
                for k, _ in enumerate(ml[idx]): 
                    self.assertAlmostEqual(value_python[k] / max,
                                           value_matlab[k] / max,
                                           places=12)
                idx += 1 
           
    def test_bc_comp_external(self):
        """:: Test computation of the bc external parameters

        The test compares the output to the same routine written in Matlab
        """
        sll = ns.low_level 

        # These were computed in MATLAB and copied here:
        ml = [[0.4052267294011047+0.6311032386059223j, 1.036329968007027+0.2258765092048176j ],
              [0.3006610079459161+0.3128491061825451j, 0.5223265605245948+0.2971297280341666j],
              [0.1777123694421338+0.2875345653086991j, 0.2629590032070414+0.3265483312349936j],
              [0.05467774644856499+0.2737048484103021j, 0.08340440936555486+0.3121597419565548j],
              [-0.05113937292562217+0.2317583332495324j, -0.04721937270173698+0.2592581248217669j],
              [-5.643190262505751+0.1714749578226607j, -0.06006518083029048+3.49054324913069j],
              [-1.062986926992792+0.2191856111542725j, -0.1233054137191623+1.302980712792983j     ],
              [-0.3712055276331935+0.2294256824214813j, -0.1921464004468367+0.7106841410185851j   ],
              [-0.2439182852950529+0.201549671542082j, -0.2518085280532899+0.4394911434825913j    ],
              [-0.2333324522437892+0.141931124479992j, -0.2891545131818455+0.2585587563195896j    ],
              [-0.04011507560421479-53.07187005166399j, -19.06731217376913-0.01031833493048201j   ],
              [-0.08099702600804853-7.14060889902647j, -4.341158234785566-0.0324499535210427j     ],
              [-0.1230018336795443-1.70994047493406j, -1.700555527135983-0.06956590222415626j     ],
              [-0.1550768428056388-0.5751352995821374j, -0.9126235277865632-0.1190558546666578j   ],
              [-0.1679351712257352-0.2760826806921075j, -0.5820135268932484-0.1741970626996904j   ],
              [-5.643190262505751+0.1714749578226607j, -0.06006518083029048+3.49054324913069j     ],
              [-1.062986926992792+0.2191856111542725j, -0.1233054137191623+1.302980712792983j     ],
              [-0.3712055276331935+0.2294256824214813j, -0.1921464004468367+0.7106841410185851j   ],
              [-0.2439182852950529+0.201549671542082j, -0.2518085280532899+0.4394911434825913j    ],
              [-0.2333324522437892+0.141931124479992j, -0.2891545131818455+0.2585587563195896j    ],
              [0.4102355278638679-64.13964613880931j, -16.2978712174548+0.06628558861782666j      ],
              [0.3125187436549701-9.119024052879343j, -3.615164711193845+0.07071860109558374j     ],
              [0.1999325902393102-2.314202837233633j, -1.396713556374066+0.04812734608212305j     ],
              [0.09091713322795866-0.7739078981930662j, -0.7688016534647311+0.00013277761644765j  ],
              [0.002277427910555446-0.3120865733979709j, -0.5237628466103936-0.06563228708994427j ],
              [703.1942451203699+0.2028043218240107j, -0.02514651368476038-117.7470779580234j     ],
              [66.46729002683718+0.2655405807008762j, -0.04870976446396561-16.69103469215919j     ],
              [13.18456238730626+0.2902512834988011j, -0.06898549087193295-4.402931406108083j     ],
              [3.940062202395152+0.2763465962465478j, -0.0772429852182332-1.685050005559056j      ],
              [1.489907859290959+0.2302768190190248j, -0.06687841317899884-0.8573386963711648j    ],
              [-0.04011507560421479-53.07187005166399j, -19.06731217376913-0.01031833493048201j   ],
              [-0.08099702600804853-7.14060889902647j, -4.341158234785566-0.0324499535210427j     ],
              [-0.1230018336795443-1.70994047493406j, -1.700555527135983-0.06956590222415626j     ],
              [-0.1550768428056388-0.5751352995821374j, -0.9126235277865632-0.1190558546666578j   ],
              [-0.1679351712257352-0.2760826806921075j, -0.5820135268932484-0.1741970626996904j   ],
              [703.1942451203699+0.2028043218240107j, -0.02514651368476038-117.7470779580234j     ],
              [66.46729002683718+0.2655405807008762j, -0.04870976446396561-16.69103469215919j     ],
              [13.18456238730626+0.2902512834988011j, -0.06898549087193295-4.402931406108083j     ],
              [3.940062202395152+0.2763465962465478j, -0.0772429852182332-1.685050005559056j      ],
              [1.489907859290959+0.2302768190190248j, -0.06687841317899884-0.8573386963711648j    ],
              [0.3974892258700645+9272.049038548725j, 1031.547812546509+0.03248866375604068j      ],
              [0.2847855486591261+575.1613827766391j, 96.03925951946171+0.0336964352037206j       ],
              [0.1528734861795221+83.62305330403466j, 18.54403487451665+0.02174846674649292j      ],
              [0.0216250224639159+19.77255727816721j, 5.381611574253117-0.0009294433151338516j    ],
              [-0.09058018800984739+6.483530831227505j, 2.036432622537101-0.02840640605168417j    ]
              ]

        idx = 0
        for nu in range(1,4):
            for n in range(1,4):
                for x in np.arange(1, 3.5, 0.5):
                    value_python = sll.bc_comp(nu, n, x, region=sll.external)
                    value_matlab = ml[idx]
                    max = np.amax(np.abs(value_matlab))
                    self.assertAlmostEqual(value_python[0] / max,
                                           value_matlab[0] / max,
                                           places=12)
                    self.assertAlmostEqual(value_python[1] / max,
                                           value_matlab[1] / max,
                                           places=12)
                    idx += 1 

    def test_bc_comp_internal(self):
        """:: Test computation of the bc internal parameters

        The test compares the output to the same routine written in Matlab
        """
        sll = ns.low_level 

        # These were computed in MATLAB and copied here:
        ml = [[0.4052267294011047, 0+0.2258765092048176j     ],
              [0.3006610079459161, 0+0.2971297280341666j     ],
              [0.1777123694421338, 0+0.3265483312349936j     ],
              [0.05467774644856499, 0+0.3121597419565548j    ],
              [-0.05113937292562217, 0+0.2592581248217669j   ],
              [0+0.1714749578226607j, -0.06006518083029048   ],
              [0+0.2191856111542725j, -0.1233054137191623    ],
              [0+0.2294256824214813j, -0.1921464004468367    ],
              [0+0.201549671542082j, -0.2518085280532899     ],
              [0+0.141931124479992j, -0.2891545131818455     ],
              [-0.04011507560421479, 0-0.01031833493048201j  ],
              [-0.08099702600804853, 0-0.0324499535210427j   ],
              [-0.1230018336795443, 0-0.06956590222415626j   ],
              [-0.1550768428056388, 0-0.1190558546666578j    ],
              [-0.1679351712257352, 0-0.1741970626996904j    ],
              [0+0.1714749578226607j, -0.06006518083029048   ],
              [0+0.2191856111542725j, -0.1233054137191623    ],
              [0+0.2294256824214813j, -0.1921464004468367    ],
              [0+0.201549671542082j, -0.2518085280532899     ],
              [0+0.141931124479992j, -0.2891545131818455     ],
              [0.4102355278638679, 0+0.06628558861782666j    ],
              [0.3125187436549701, 0+0.07071860109558374j    ],
              [0.1999325902393102, 0+0.04812734608212305j    ],
              [0.09091713322795866, 0+0.00013277761644765j   ],
              [0.002277427910555446, 0-0.06563228708994427j  ],
              [0+0.2028043218240107j, -0.02514651368476038   ],
              [0+0.2655405807008762j, -0.04870976446396561   ],
              [0+0.2902512834988011j, -0.06898549087193295   ],
              [0+0.2763465962465478j, -0.0772429852182332    ],
              [0+0.2302768190190248j, -0.06687841317899884   ],
              [-0.04011507560421479, 0-0.01031833493048201j  ],
              [-0.08099702600804853, 0-0.0324499535210427j   ],
              [-0.1230018336795443, 0-0.06956590222415626j   ],
              [-0.1550768428056388, 0-0.1190558546666578j    ],
              [-0.1679351712257352, 0-0.1741970626996904j    ],
              [0+0.2028043218240107j, -0.02514651368476038   ],
              [0+0.2655405807008762j, -0.04870976446396561   ],
              [0+0.2902512834988011j, -0.06898549087193295   ],
              [0+0.2763465962465478j, -0.0772429852182332    ],
              [0+0.2302768190190248j, -0.06687841317899884   ],
              [0.3974892258700645, 0+0.03248866375604068j    ],
              [0.2847855486591261, 0+0.0336964352037206j     ],
              [0.1528734861795221, 0+0.02174846674649292j    ],
              [0.0216250224639159, 0-0.0009294433151338516j  ],
              [-0.09058018800984739, 0-0.02840640605168417j  ]
             ]

        idx = 0
        for nu in range(1,4):
            for n in range(1,4):
                for x in np.arange(1, 3.5, 0.5):
                    value_python = sll.bc_comp(nu, n, x, region=sll.internal)
                    value_matlab = ml[idx]
                    max = np.amax(np.abs(value_matlab))
                    self.assertAlmostEqual(value_python[0] / max,
                                           value_matlab[0] / max,
                                           places=12)
                    self.assertAlmostEqual(value_python[1] / max,
                                           value_matlab[1] / max,
                                           places=12)
                    idx += 1 

    def test_translate_mu_plus_minus_one_probe_external(self):
        """:: Test translate_mu_plus_minus_one_probe for external case

        The test compares the output to the same routine written in Matlab
        """
        sll = ns.low_level 

        ml = [
             [ 0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j],
             [ 1.983917242484136e+01 + 2.812291006036135e+01j, -1.983917242484136e+01 - 2.812291006036135e+01j, -9.286324812120267e+00 + 3.419504314248747e+01j,  9.286324812120265e+00 - 3.419504314248747e+01j],
             [-2.527215005219416e+02 + 9.906439638063199e+01j,  2.527215005219417e+02 - 9.906439638063199e+01j, -2.734716137546921e+02 - 1.557033094226680e+01j,  2.734716137546921e+02 + 1.557033094226679e+01j],
             [-5.834431847850769e+02 - 2.029014008793220e+03j,  5.834431847850768e+02 + 2.029014008793220e+03j,  2.019866667727439e+01 - 2.129130221697416e+03j, -2.019866667727441e+01 + 2.129130221697417e+03j],
             [ 1.745258126178047e+04 - 4.054885702944372e+03j, -1.745258126178047e+04 + 4.054885702944372e+03j,  1.802473751188850e+04 - 1.943526505051545e+02j, -1.802473751188850e+04 + 1.943526505051546e+02j],
             [ 3.214426540059490e+04 + 1.631590691641175e+05j, -3.214426540059490e+04 - 1.631590691641175e+05j,  3.359155332139097e+03 + 1.669986663788163e+05j, -3.359155332139098e+03 - 1.669986663788164e+05j],
             [-1.660126146562665e+06 + 2.852469962316631e+05j,  1.660126146562665e+06 - 2.852469962316631e+05j, -1.689673803386683e+06 + 4.151372314939635e+04j,  1.689673803386683e+06 - 4.151372314939634e+04j],
             [-2.798529714808612e+06 - 1.831915103056013e+07j,  2.798529714808612e+06 + 1.831915103056013e+07j, -4.948257334939181e+05 - 1.857504992908826e+07j,  4.948257334939181e+05 + 1.857504992908826e+07j],
             [ 2.182199584082121e+08 - 3.005941394232195e+07j, -2.182199584082121e+08 + 3.005941394232195e+07j,  2.206800486061303e+08 - 6.056618415860053e+06j, -2.206800486061303e+08 + 6.056618415860049e+06j],
             [ 3.506997866559130e+08 + 2.793108201080276e+09j, -3.506997866559131e+08 - 2.793108201080276e+09j,  7.766668801005435e+07 + 2.819082187137821e+09j, -7.766668801005435e+07 - 2.819082187137820e+09j],
             [-3.824638057575533e+10 + 4.415126315766813e+09j,  3.824638057575533e+10 - 4.415126315766813e+09j, -3.854499407928616e+10 + 1.050676720988428e+09j,  3.854499407928616e+10 - 1.050676720988429e+09j],
             [-5.964728438560498e+10 - 5.580457925671991e+11j,  5.964728438560499e+10 + 5.580457925671991e+11j, -1.502233729894957e+10 - 5.617577054213110e+11j,  1.502233729894957e+10 + 5.617577054213110e+11j],
             [ 8.644841070001485e+12 - 8.606085836911228e+11j, -8.644841070001485e+12 + 8.606085836911228e+11j,  8.694434982907522e+12 - 2.269333871056523e+11j, -8.694434982907522e+12 + 2.269333871056523e+11j],
             [ 1.320644890139925e+13 + 1.417208767832011e+14j, -1.320644890139925e+13 - 1.417208767832011e+14j,  3.617307342422639e+12 + 1.424294812252103e+14j, -3.617307342422639e+12 - 1.424294812252103e+14j],
             [-2.451421142564421e+15 + 2.147577629271560e+14j,  2.451421142564421e+15 - 2.147577629271560e+14j, -2.462201293753654e+15 + 6.073599553684859e+13j,  2.462201293753654e+15 - 6.073599553684859e+13j],
             [-3.688855259643090e+15 - 4.462179535932199e+16j,  3.688855259643090e+15 + 4.462179535932199e+16j, -1.072157146938451e+15 - 4.479574820736090e+16j,  1.072157146938451e+15 + 4.479574820736090e+16j],
             [ 8.526379679292959e+17 - 6.673633933336648e+16j, -8.526379679292959e+17 + 6.673633933336648e+16j,  8.556052584106380e+17 - 1.986043991965874e+16j, -8.556052584106380e+17 + 1.986043991965874e+16j],
             [ 1.268342086958845e+18 + 1.706504214377840e+19j, -1.268342086958845e+18 - 1.706504214377840e+19j,  3.853208028218723e+17 + 1.711838901074014e+19j, -3.853208028218723e+17 - 1.711838901074014e+19j],
             [-3.570209240356019e+20 + 2.526372148088040e+19j,  3.570209240356019e+20 - 2.526372148088040e+19j, -3.580290455104756e+20 + 7.815870621411261e+18j,  3.580290455104756e+20 - 7.815870621411261e+18j],
             [-5.262862511389860e+20 - 7.793176772839545e+21j,  5.262862511389860e+20 + 7.793176772839545e+21j, -1.654669897189212e+20 - 7.813153401171673e+21j,  1.654669897189212e+20 + 7.813153401171673e+21j],
             [ 1.771842174334341e+23 - 1.144374575965661e+22j, -1.771842174334341e+23 + 1.144374575965661e+22j,  1.775983944925496e+23 - 3.650262119661086e+21j, -1.775983944925496e+23 + 3.650262119661086e+21j]
             ]


        R_matlab = np.array(ml, dtype = np.complex128)

        NN = 20
        muneg1 = np.ones((5,2), dtype = np.complex128)
        mu1 = np.ones((5,2), dtype = np.complex128)
        kr = 2.2
        R_python = sll.translate_mu_plus_minus_one_probe(NN,
                                                         muneg1, mu1,
                                                         kr,
                                                         region = sll.external)

        # Relative difference
        max_diff = np.amax(np.abs(R_python - R_matlab) / (np.abs(R_matlab) + 1e-15))

        self.assertLess(max_diff, 1e-14)

    def test_translate_mu_plus_minus_one_probe_internal(self):
        """:: Test translate_mu_plus_minus_one_probe for internal case

        The test compares the output to the same routine written in Matlab
        """
        sll = ns.low_level 

        ml = [
              [ 0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j,  0.000000000000000e+00 + 0.000000000000000e+00j],
              [-1.872413505871594e-01 + 4.131026284328057e-01j,  1.872413505871594e-01 - 4.131026284328057e-01j,  1.971066378766496e-01 - 7.416580795124403e-02j, -1.971066378766496e-01 + 7.416580795124403e-02j],
              [-3.037050441738671e-01 + 4.359058371438230e-01j,  3.037050441738671e-01 - 4.359058371438230e-01j,  2.554324214420214e-01 + 4.494231193295538e-01j, -2.554324214420214e-01 - 4.494231193295538e-01j],
              [-3.398074618547861e-01 + 4.769036652967671e-01j,  3.398074618547861e-01 - 4.769036652967671e-01j, -1.112086752693120e-01 + 6.707698256610717e-01j,  1.112086752693120e-01 - 6.707698256610717e-01j],
              [-1.368335978050840e-01 + 4.832192751874627e-01j,  1.368335978050840e-01 - 4.832192751874627e-01j, -5.764297705879613e-02 + 5.453984964638041e-01j,  5.764297705879613e-02 - 5.453984964638041e-01j],
              [-1.117884062474121e-01 + 2.017139383945167e-01j,  1.117884062474121e-01 - 2.017139383945167e-01j, -8.640709493451872e-02 + 2.256224782907263e-01j,  8.640709493451872e-02 - 2.256224782907263e-01j],
              [-1.820666876677330e-01 + 1.992149824805843e-01j,  1.820666876677330e-01 - 1.992149824805843e-01j, -1.604786372162131e-01 + 2.227058919872925e-01j,  1.604786372162131e-01 - 2.227058919872925e-01j],
              [-1.677111606742540e-01 - 8.062128063723340e-02j,  1.677111606742540e-01 + 8.062128063723340e-02j, -1.769130936662183e-01 - 6.311033504703860e-02j,  1.769130936662183e-01 + 6.311033504703860e-02j],
              [ 2.456035866531807e-02 - 7.170439153941070e-02j, -2.456035866531807e-02 + 7.170439153941070e-02j,  1.774116016749047e-02 - 7.417647486517127e-02j, -1.774116016749047e-02 + 7.417647486517127e-02j],
              [ 2.132110654295402e-02 + 5.765528130344747e-03j, -2.132110654295402e-02 - 5.765528130344747e-03j,  2.183768159857495e-02 + 3.921469840179590e-03j, -2.183768159857495e-02 - 3.921469840179590e-03j],
              [-1.105705594261947e-03 + 4.914070473021338e-03j,  1.105705594261947e-03 - 4.914070473021338e-03j, -7.171958289307486e-04 + 5.003168241901503e-03j,  7.171958289307486e-04 - 5.003168241901503e-03j],
              [-9.287800483104400e-04 - 1.796153673456743e-04j,  9.287800483104400e-04 + 1.796153673456743e-04j, -9.419184544948729e-04 - 1.120848364767352e-04j,  9.419184544948729e-04 + 1.120848364767352e-04j],
              [ 2.533509897375499e-05 - 1.490877615261487e-04j, -2.533509897375499e-05 + 1.490877615261487e-04j,  1.530802505515935e-05 - 1.507836587955022e-04j, -1.530802505515935e-05 + 1.507836587955022e-04j],
              [ 2.082085352160368e-05 + 3.159825078061704e-06j, -2.082085352160368e-05 - 3.159825078061704e-06j,  2.101576545093158e-05 + 1.857674202374147e-06j, -2.101576545093158e-05 - 1.857674202374147e-06j],
              [-3.533517007352659e-07 + 2.574945790403099e-06j,  3.533517007352659e-07 - 2.574945790403099e-06j, -2.028978047984292e-07 + 2.595152267231909e-06j,  2.028978047984292e-07 - 2.595152267231909e-06j],
              [-2.858596227084918e-07 - 3.582139446190723e-08j,  2.858596227084918e-07 + 3.582139446190723e-08j, -2.877686048081035e-07 - 2.015103653193068e-08j,  2.877686048081035e-07 + 2.015103653193068e-08j],
              [ 3.321705418204917e-09 - 2.879641471206995e-08j, -3.321705418204917e-09 + 2.879641471206995e-08j,  1.835165972042838e-09 - 2.896213706902707e-08j, -1.835165972042838e-09 + 2.896213706902707e-08j],
              [ 2.655468421475401e-09 + 2.838525511740962e-10j, -2.655468421475401e-09 - 2.838525511740962e-10j,  2.668779777112409e-09 + 1.543311769773737e-10j, -2.668779777112409e-09 - 1.543311769773737e-10j],
              [-2.249379065127184e-11 + 2.258045773253180e-10j,  2.249379065127184e-11 - 2.258045773253180e-10j, -1.205624858955184e-11 + 2.267996458212099e-10j,  1.205624858955184e-11 - 2.267996458212099e-10j],
              [-1.781530245138743e-11 - 1.661889144756821e-12j,  1.781530245138743e-11 + 1.661889144756821e-12j, -1.788487499156584e-11 - 8.793620032867829e-13j,  1.788487499156584e-11 + 8.793620032867829e-13j],
              [ 1.150082712659134e-13 - 1.311046889528326e-12j, -1.150082712659134e-13 + 1.311046889528326e-12j,  6.015149664179104e-14 - 1.315616227350691e-12j, -6.015149664179104e-14 + 1.315616227350691e-12j]
             ]


        R_matlab = np.array(ml, dtype = np.complex128)

        NN = 20
        muneg1 = np.ones((5,2), dtype = np.complex128)
        mu1 = np.ones((5,2), dtype = np.complex128)
        kr = 2.2
        R_python = sll.translate_mu_plus_minus_one_probe(NN,
                                                         muneg1, mu1,
                                                         kr,
                                                         region = sll.internal)

        # Relative difference
        max_diff = np.amax(np.abs(R_python - R_matlab) / (np.abs(R_matlab) + 1e-15))

        self.assertLess(max_diff, 1e-12)










                       




        


