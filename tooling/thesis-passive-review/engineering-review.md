# Engineering cross-review: Chapters 01–08

No findings.

The P2 finding in `Chapters/01_Introduction/05_Contributions_Attribution.tex:8` was resolved and re-reviewed: output voltage, load response, input power quality, conversion loss, and surface temperature are now described as “assessed from the measurements.” This preserves calculated screening loss as an assessment and no longer implies independent direct loss measurement.

No qualifying findings remain in the complete prose diff for Chapters 01–08. Inherited/author attribution, missing checks, conditional future tests, calibrated versus uncalibrated/raw observations, nominal timing, and continuous-rating limits were retained. Neutral definitions and device relationships were accepted without forcing passive constructions. The root agent's seven intended personal-heading renames are separate prose/table-of-contents edits and are excluded as findings. Hashes below identify the reviewed source snapshot before any later heading-only edits.

Review scope: all 96 TeX files in Chapters 01_Introduction, 02_Background, 03_Requirements_Architecture, 04_Topology_Analysis, 05_Modeling_Simulation, 06_Magnetics_Integration, 07_Hardware, and 08_Control_Firmware, compared to `/workspace/tooling/thesis-passive-review/before`. Complete changed paragraphs were reviewed with their original wording and surrounding technical context. Chapters 07–08 were reviewed after their owner confirmed stable completion. The review focused on regressions introduced by the voice rewrite; original engineering issues were outside scope. No thesis files were edited, no compilation was run, and no hardware/source validation was performed for this prose-only review.

Snapshot time (UTC): 2026-10-25T15:23:36.865390+00:00

SHA-256 hashes identify the exact baseline and reviewed source snapshot. Later changes require review of their additional diff.

| Source | Baseline SHA-256 | Reviewed SHA-256 |
|---|---|---|
| `Chapters/01_Introduction/01_Motivation.tex` | `0768acf8ed8533431c2b683fe30cc364090eaf408f346dccb854711a368d7134` | `24447a9145a9f47ab21eac1cf60106dea97abf8e084c93add3ea2c2b39adf697` |
| `Chapters/01_Introduction/02_Problem_Statement.tex` | `7c7014e64e854c3a581b39f7fc8bd209f59ba8898deceb130ff106096af45121` | `6d2b8c0a9d1667b4eec57c4be739e573773f8d8b5d54c78df17ab764ce4937a1` |
| `Chapters/01_Introduction/03_Aim_Objectives.tex` | `7654a0469697d790ec022e9070a96644e14048f2eea4707fdd3f67fb0e0a036b` | `fe169683b6831c9bf74d4334ae0184a4120d6060d45b567edf531f9a93a11fc9` |
| `Chapters/01_Introduction/04_Research_Questions.tex` | `586100d78a7e65a593790fd86385009767a5dee8325961ee298945deadd6eb88` | `969cee80695328a9e1962f7edeeb42f7f43e113a7c9346dc957db9617269c5b5` |
| `Chapters/01_Introduction/05_Contributions_Attribution.tex` | `51de6262374cf30b36ce4660731ecfef6832d3556e96fafac7f7261cd8fff530` | `afe3045fd69ff4afa82cd6bd7636f696747b1b72c8d3c01c88894d602defc11e` |
| `Chapters/01_Introduction/06_Scope_Limitations.tex` | `0e11965d26b7598b222e7d69e9492fb29183268fc1205007cfb182162539bf70` | `0902be888b0fc820dc8580fc2520b5694def56218d693d0a66e67f4a27ef91c5` |
| `Chapters/01_Introduction/07_Thesis_Structure.tex` | `a4249875446d67e100d44d472d79ada9be94b54bc552979593f0af58f5570900` | `7356a4bab8d09801bcc25fd20a1ad0d8c5c68e860579d62650a755a9d927dbe1` |
| `Chapters/01_Introduction/chapter.tex` | `63eb75c44565d553d04bbd9993a7dafad247ea26cfa33010a38adce0579e16da` | `03bd2ce2894bc78cace9c090e5aa34320b37314c47dc3c8fe2c49b08e0f16abb` |
| `Chapters/02_Background/01_Offline_ACDC_PFC.tex` | `4575917bd665707853a082ba5161b4245922afdf0ce25b93f2319072eb6dcdfd` | `27e2b20ee4f372bcfb6258b5c29b0ad48eb903b0b3253c345c959f14a244aa8b` |
| `Chapters/02_Background/02_Charge_Pump_Principle.tex` | `59117ad075be3f742b1552e7c77422deba6e1b885d0571dcbe05723512fe6465` | `6d8119481a5b0a4ed13a738d65a8a36a25acee498091e4acb768c2a1f6feb841` |
| `Chapters/02_Background/03_ClassDE_Resonant.tex` | `47f562abdb209f3a5dfb0001f66888fdab4d4a1253e7a80238e23c38a2051eb3` | `8712a1b46f6e852603bad39cb02ef26b03d93339ac7060bcb9dced42aef01bd7` |
| `Chapters/02_Background/04_Soft_Switching_GaN.tex` | `3b44b9a37f78e37933c299c3f7504f0dde528f3f28ffb9b0976221aa90346b82` | `077838a485c5370b44c1b98eea2c3a72eba754f5e645f8b1f55dcb9dce1ebc06` |
| `Chapters/02_Background/05_Reference_2020.tex` | `b4ef72ec645216b4903d8173c0896bf6585721fd9dcb1ab598879027d184cf0b` | `78a9d075c31e06c0d098c57705c8df20cec3878ec07594138f2f4e9f5b08196e` |
| `Chapters/02_Background/06_Reference_2021.tex` | `0824bf391f298dc783e97eb4ac76cd735cced3b389e127d94de5eb1a87ff84ea` | `e11b21e91674ba5ef3d215cce3db76a1223a28cb7bb2dffc536f6cb9ca28c681` |
| `Chapters/02_Background/07_USBC_Context.tex` | `d4c62d69f6e0dcbcb66842904c0219e936926d7cb72a02f1d47442f5f6aa050f` | `46af267c6da14b5a5a8e9f18cd7c58b4e7670fc5e418e9d669096ea91fec5717` |
| `Chapters/02_Background/08_Research_Gap.tex` | `1a39177ab297c204c325d281102d6e614911f00572239626f27049e9f6e9343c` | `1e6a6731e85b0a06fb1f55071bef32829de43376bebeb2ef47f51439b2d5dcad` |
| `Chapters/02_Background/chapter.tex` | `f77f6a69ffe40f35418d245bb29e13a32b3a8913abc11308cd9cfb96d460ecee` | `8ce1dbfe679c2d86387db006d7b356332db519cb74223524e8f41f764eb64d4d` |
| `Chapters/03_Requirements_Architecture/01_Use_Case.tex` | `90468d669d04907775a0fcd0c18d7a1683f55248d647e8901061e3cab3ced61c` | `65837777d80f6f2bb9366dbb89e138b7c182c2682c6df29b03efd8bc368063d0` |
| `Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex` | `caa5eead759c471ed77dfa2bb6fc98f2a6bae8c01f3e0929bc59a06bc3c26b66` | `65b484921ac939ad475910295e156884b906fd306f56bf89eec6ca0b4bb3ebc5` |
| `Chapters/03_Requirements_Architecture/03_Functional_Requirements.tex` | `bfe4b125fc3f8e6b49cb3272d95ac6b1c385fe416a7bfdc4861d22d9998d02bd` | `ecbcec3074bac250f8b15ecfc3f244196a24e7b33aaba793520941418bf0140a` |
| `Chapters/03_Requirements_Architecture/04_USBC_Interface.tex` | `848af99f822ee7898f2edf15f9f95bf5f94c7ea303c8fe1bb7bc8929646a6a1b` | `8dc1e7f6f77c392780c29df5c61979b8dffd4a5328e9f0b2e3f9f1301988637f` |
| `Chapters/03_Requirements_Architecture/05_Safety_Protection.tex` | `10b815b831be1ba6c330b88ae6ba123680d0bb60f6793a5f36344b07c932ac40` | `d514877ba9e90cb93e589f009023adb0377c94f21c45ce764a0ce7da2a4fae12` |
| `Chapters/03_Requirements_Architecture/06_System_Architecture.tex` | `cf5dc39cddf880a965e640d971e3b5b7dfaa21d7de0facd717ec81e0ac111bd0` | `7fa2bf973c05f1f9149d5a3cf5db5bd49cfb0c3648117ca493b4924608c47668` |
| `Chapters/03_Requirements_Architecture/07_Operating_Modes.tex` | `83506277fa182fd98ed34f12848c8cbd8614e1723e24cd7aa370cdde083a9202` | `a173c25f2f8a2d565cd10e9438db8bf5ef91df62a87eb9709ad2de09f427b206` |
| `Chapters/03_Requirements_Architecture/08_Verification_Matrix.tex` | `c1edc8a72ec92094afafa26813edc597c82ec8427daec814881d9845fbf499da` | `5a9e0e7aa08eedda9f1796543622d471a4e024288d85430cbcea9fedbe6db044` |
| `Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex` | `d8d55f74197f899ffd58406de1d0dad2ebaebb64ef96954ac9cca692db36a2a1` | `57a7e33fa8da0080a73dd26bb25fa6521117b502d8c22b0fdae08294421ae212` |
| `Chapters/03_Requirements_Architecture/chapter.tex` | `3c25169df4d5ab5a5a618d507cafac3989f63bd9c854258156f2065d98c66244` | `386adb021f8554457cfd2fa8b5edb3798695f5a5340d82f9e862d19806b22216` |
| `Chapters/04_Topology_Analysis/01_Topology_Overview.tex` | `073be8819d6f5294949301445ce10d6ff54a31ed8562c6980b93e93ca17bc37a` | `50872af70b32a05294209d2abe553befbe23a65b768f35e62d29a7b1cf3c434e` |
| `Chapters/04_Topology_Analysis/02_Switching_Cycle.tex` | `0081a0743fb8e4801bb325b1dcc09e32937ec5fed0769ef9e49072301a37ea6b` | `6720baf5f19c0b281dfeb00adf99461abc66193997a9b7e38e7a785acf603feb` |
| `Chapters/04_Topology_Analysis/03_Line_Cycle_PFC.tex` | `270d6b9eb425860e4235a0a4d8e511e4506bf5f15ab9983802512bd31b6410aa` | `4b26d9df95a79095512d355e159349d1302f83619b5b13147d714115fd96ef01` |
| `Chapters/04_Topology_Analysis/04_Pump_Capacitor.tex` | `44b22aa197977dfc3c4222e1c68012c4cc00431423d1fac01cc2a7f94c99999b` | `dd4b42ae7ee303f0a4a8986fa82d26c38ca74be0e38ab89206767c76e5e3d009` |
| `Chapters/04_Topology_Analysis/05_Pump_Inductor.tex` | `e07213dec1ef8610d880aaac9a8e03a95a506d6120fa0a28bd6d5e75cda54241` | `41416d2786012d68063170bdf471aad9c1f3d0cbbfa98f669501276580ef399b` |
| `Chapters/04_Topology_Analysis/06_DC_Link.tex` | `143e3d20ab6103301e40814144a169193f0e7ff6cf137ffccb85c1ca0c580f9a` | `68cddd36ea1aa8517e3b9a1760d80e270f50b9d109923c8747f2eb1bee0d6e4a` |
| `Chapters/04_Topology_Analysis/07_Resonant_Stage.tex` | `e7c1de7e45da94863913587740894a76d15392206336fb99a9cc7109cde990d2` | `88532de2a4946559aed12326f00d6a18b7d217f4ee8121141d71d141ebb9e252` |
| `Chapters/04_Topology_Analysis/08_ZVS.tex` | `ef77be9cd1ba1ed1e98246b3d8c48ceb7d4d928145e5b3c1d356d874b62b546c` | `d621b785888badd28c4b1bc63dbe5ab631ed4d30faf8772f6e79a50b963d6fe0` |
| `Chapters/04_Topology_Analysis/09_Device_Stress.tex` | `adb75e4fcd97ad12ad693d8d37984cb53bf94764c82071a6c39c53a33d0155f9` | `e2b14b560237c560f9e1295816c6fbeeb7936d340ff693abd3e1cd714957b053` |
| `Chapters/04_Topology_Analysis/10_USBC_Adaptation.tex` | `ed35185e1881eafa754a14e4c3debc0affaa6bc9b4754c0c22317c95f028672d` | `f595512c1c840405e64fc25f530b93ed06ed2f5faeaf73b1cd7b9a0121276d94` |
| `Chapters/04_Topology_Analysis/11_Design_Summary.tex` | `7003780c59ffa96f7e6779d14bcd6dfcf196babf11b9b944f06c2aedf19a7405` | `2a01f7a1f7e0a8c2bda4e1acab05abea10814d83e5591361fa2637fbdc73a209` |
| `Chapters/04_Topology_Analysis/chapter.tex` | `36f59fd8af4fa5016ccda9e916ee78f1a7c247ba406bca2a848fa2f9f7da239c` | `2473efced6b8d397329940e8b7ef0be2f6004f2d9ea52495f1569e0ced2b1f9a` |
| `Chapters/05_Modeling_Simulation/01_Objectives.tex` | `d8a39f332727f7f9e71671badde4933bff1c0ed1e84c1cbc0a635135942eab17` | `fc9a9675580c5645a46369ccd1f2de6c09b36f821a1725d063252cdded3d47ee` |
| `Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex` | `d4c824f0415b119f5d4f77c9e9438ada8cf5dd6e436241eb1821e5950bc41554` | `f1bfbfb1f9fb2b32aa8ee1e50cb6bb107c1fe310e1b4f8f82dc4ab612de69b37` |
| `Chapters/05_Modeling_Simulation/03_GaN_Model.tex` | `f1459674b42faf1285a1cd2267b66332e02933855e31c57d9b70fdcadc4dcab8` | `75254da375c9942b7f9d400aee3794d8ac918badcb33108408c4f0fe33ca9286` |
| `Chapters/05_Modeling_Simulation/04_Simulation_Setup.tex` | `134267ec5438ddf1b3d39f5fa5fb7ad6a6cb56f8b1daa2659a4448659de7525e` | `faf3188e44c1421bef3ea58f40259e64ff115d391db83dbe94bc1aaa4abccb19` |
| `Chapters/05_Modeling_Simulation/05_Simulation_Cases.tex` | `448c9d6d78504fe471f430ff867346d85717a0b058474759a111e82170388ccd` | `9c24344b112c33352a822637459c81b1f2fcfde6c35e642554f29ba7cf590367` |
| `Chapters/05_Modeling_Simulation/06_Steady_State.tex` | `c67bd0184038854d5c8a1cf9c52901704f3dccb22c5fff84c1a9e7669e9e99b8` | `b2b322589f964468ccdb524c1f408b6c30f876e553a8e15979727183132fce4d` |
| `Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex` | `b78873018f2abc02df7c55303ccc9d6daf071e28e9455e4975df1a2ba633700a` | `4586d52eeccd3a9e8d7bf53b5d8951ce331e838e3e1b64d4b6cfdde154bc4033` |
| `Chapters/05_Modeling_Simulation/08_Parameter_Sweeps.tex` | `3390f3458bc3fa91cd133bf5f486219bfa7089ad39fb58a6b02f262f6f994c76` | `d81a9f090f737298eafaf7cf40f7acb1abff7189f95e0478a0af5da99c364986` |
| `Chapters/05_Modeling_Simulation/09_Loss_Estimation.tex` | `d1c8c76ca93a720a69132792a71cc76bcb49192a72bc07883d346331163313f3` | `c8c71c72adbb1a2e9214fda7487e5c1fa12a1d28df68f941bdbf5d2e716fb68e` |
| `Chapters/05_Modeling_Simulation/10_Data_Limitations.tex` | `984df0a6e033a375b4ebcbb9fd2c6a694eedc65db2548abe2a2e40acccae348a` | `a37ec895da742c281af4c4b4ce1139fd4d00677133dd7c698535a8da57cc2653` |
| `Chapters/05_Modeling_Simulation/chapter.tex` | `c58785dbde3f7cbde764c6e51a25ce4d916913a56e9b7889eb51e7924cdf3187` | `4bda0dd9e7ebb4e5f457c55bcf764595826f994da4515317f6e0139caae249aa` |
| `Chapters/06_Magnetics_Integration/01_Provenance.tex` | `b976c97d73bea71c3140b6c9d34d5d031e2922956fbfad4450826606073d1ffc` | `056ffae6f9b25667f13789bed5d4bc056ea93de101660472e5dd3f3f08d5fb15` |
| `Chapters/06_Magnetics_Integration/02_Inherited_Specifications.tex` | `fbb9a1f6c5d8bfac89928ec1b2f2a9ec130131b93e6a0b12fcfba05009274d39` | `4de7e51a53a4132d81f8704bc8f29962ef1e72db6d392085c74d9d41a93ae322` |
| `Chapters/06_Magnetics_Integration/03_Integration_Requirements.tex` | `9b3c30c0e09f172c7b06749987f52242f8e5314b6e9830a2b5109f4691acb584` | `96781d0e824f8756ab8af0e55b21347975fadf73516151278082599aab91d041` |
| `Chapters/06_Magnetics_Integration/04_Mounting_Concept.tex` | `874590aed471aa39d6185b07aeaf28299007812ee435f6b71eb6011898a5f592` | `a4339227c71fee0268c51567ae42dd87d2bbe02bc40e62dea206c2035f04e995` |
| `Chapters/06_Magnetics_Integration/05_Footprint_Interconnection.tex` | `f57181e19226c08d6c4cc647f71fe11b6f3c207c9f1d6a118d086920d9eec57e` | `177add897168a012b9bcf00d69f20c97314efc82f67f61e8455805d0de468fc3` |
| `Chapters/06_Magnetics_Integration/06_Mechanical_Assembly.tex` | `48abce0333175218f866c4417c4207b18c61d394928c45a86ee470b8ea1e96dc` | `3af7d675abe4151551cd39a9939c960f075d5fdbafe3b483343f0562719108b5` |
| `Chapters/06_Magnetics_Integration/07_Isolation_Clearance.tex` | `99a9bea47a3a29bd525d633da7d1c0cec6966e9af5a019869e2a58f8b5ab74fb` | `757965164c3717029afb9b9ccd58d13df8d914889800832a0fca6bef94d2613f` |
| `Chapters/06_Magnetics_Integration/08_Parasitics.tex` | `0455f4e268fb8be1fca2ce7e36288aac105215b13630e2be1d813810692e383b` | `aa5aab5ecd85a7d9b98f2661832b406a3777bab017e50b581a1b480abc3ef599` |
| `Chapters/06_Magnetics_Integration/09_Thermal_Integration.tex` | `021b1cd2d93091d5f08ce739765f775d0a15a35de2abd1ce5e114bf0a346e943` | `1baa76c3a7d89bd59da601d06522efc7e8ef2104dc9cfb17da093a1d39adcf85` |
| `Chapters/06_Magnetics_Integration/10_Verification.tex` | `80b0c0f81d1f2a34dd78e3dd8ce4b08e3c7d2d4e461fc5f6c19d526f18c12636` | `6e8f9451a599521a3a59c10dff31f8911f86cade110bfd9d344bc05f01367200` |
| `Chapters/06_Magnetics_Integration/11_Limitations.tex` | `f75aa18bd9c19075dbdd7fb61f19c8c726717834c2fa5ada98f4ccf2b9fc2aa6` | `02b68bc54062700a95c8dfe52b79c9c93bff30385e67acffe4fa92e481eb0af1` |
| `Chapters/06_Magnetics_Integration/chapter.tex` | `473f37c126a3e502b8be358253b7e3a178e30dde4315e8eadc996c37f8095a19` | `b20d8f1a61eb7fd812d8546d217c842c523615271245b86f19b395aab7f3fa59` |
| `Chapters/07_Hardware/01_Prototype_Overview.tex` | `0ed1b6ba727e4c800f4b6d3bbd12febb5f0b52ebf57eed2b1f2db38fc04887e8` | `1af1ad54d7bb0e477610a4e5560ff353f3ef2f4a38a9161bb1577791bdb31e8d` |
| `Chapters/07_Hardware/02_Input_Filter_Bridge.tex` | `711dea356bcd7f522e7b948e900c37172c42853fe3dbe215169096530e57828f` | `fc00e642a04be332f2192a67a1859cf833bd2d50ade5d3c16a8091fd84a8e062` |
| `Chapters/07_Hardware/03_Charge_Pump_Network.tex` | `c102f3a232b1bc0dcbf348b173095c7a7d22f91bd34e4caf8d5968ee534d1a14` | `aabf75389fe06affe4d276cef2b88561bfe26f982a124bc1780849afac0ca818` |
| `Chapters/07_Hardware/04_GaN_Half_Bridge.tex` | `ac3f13a7320dade522a4bf8b95dc12072eb80ee9938029dc145a6758f7a101eb` | `0b6c67b056bf9f892f2840adbae4a5268ac7d09af64f3a34652e720cb3d7bef3` |
| `Chapters/07_Hardware/05_Gate_Drive.tex` | `958f321da43c15f2a25581dc3537b8aacf9564f486d568c7854894763cc163c8` | `51d97a4d9b6969407ef37fe44691d6340455e67495d1ab4bac914672f0fd1a5c` |
| `Chapters/07_Hardware/06_Resonant_Output.tex` | `742801d2f5679f5fb5901de8fbf9feddcd65c1b77b46bea77d75f651cc072fb3` | `95c0225cb94ed6f8909cfb33f3069258fec003677696878fb242996c7938c4b6` |
| `Chapters/07_Hardware/07_USBC_Interface.tex` | `13ed9315ff52a3910aea3d752b72e36c4f695ef986b30d07fd1855838a8c46e0` | `7f21cc28ed772517cad78a80ed8bb2f918ae3af16e102aadac8ae86a1a719910` |
| `Chapters/07_Hardware/08_Sensing.tex` | `f4170ba5fe50d305b4b1bd72cc80cbcd19aedd04df32e0cc55da5823d8a4e1c2` | `c2772314a478f3508eee594fa6729f6ad85c11ddaff1f004e59984d5a81635a5` |
| `Chapters/07_Hardware/09_Protection.tex` | `98a46227392645e588518ce7e2816e08d370ba32234cef019ce067ddf1718997` | `52c986defdabe615fba674d7ce33a206f19783ae6e432c9d7bc1fb4ea69c63a6` |
| `Chapters/07_Hardware/10_Auxiliary_Power.tex` | `94436b3f26e0aee524705f8eeb5d90628379e7666e462f1464bfa722fb0b2804` | `6d0798076eb7c60f4f1dcc75e81ca5fabaee6686daee1d40dd384e34d83c19cd` |
| `Chapters/07_Hardware/11_PCB_Layout.tex` | `7aa60eb1a08333415515b28dac38caeaef293b4f54fe02efd678c9051e7520f6` | `6b75906e5f7fdf751432ebd243dcc6e17a5861277689ae86d52542864175da80` |
| `Chapters/07_Hardware/12_EMI.tex` | `61c713e90da77d53a0e354aead264cc13205b0e70985941a0ea3302195c5339c` | `1393845596eaad2b560640a1ea2a489e7d7235c4a25d18a6b98f910269352572` |
| `Chapters/07_Hardware/13_Thermal.tex` | `dcb3cbb862d2e54f5dcdc155f2334fd5e480f58b439fb1d2273b0d93bf41ee20` | `39b31c45cc3c48743c58fd4a7a678f465e41c48d890251da3f9dceff706bdf7b` |
| `Chapters/07_Hardware/14_BOM_Manufacturing.tex` | `a420d67105e13e1d59ec6f1e357f947a9c7737340d09641f4932811f5ec920b1` | `0f3944ca1cc30ad1f9d1177d8b2385b53b0dbc12ae23a75ad26d45cb7c481e47` |
| `Chapters/07_Hardware/15_Unmanufactured_Revisions.tex` | `deab21ffe2b1b4c585c2fb1d68689c11fef66c4a320cd9fd63603ae298007210` | `904f70098ad3654921135f776cbac31bc8293e4153c6ce0b09327ad4b2fcb79d` |
| `Chapters/07_Hardware/16_V2_F410.tex` | `01348ed31a3a1d8169a6a259a166191127975b2958278e3493a0ff4226f25f8b` | `7959712a3e1562aaf658286b831f074f1a372918c1da9216654fe6d91458f943` |
| `Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex` | `b1e06421b488f4df391c89ae7b22fb7167e52fdb644b3083b326a21f9d651bd0` | `dff695287fd8bcb3a5d0cb1af337d91ad3a35ad80bf93c17f4cdbf3231f0019b` |
| `Chapters/07_Hardware/chapter.tex` | `061a5139388d2a295eab7f37577837bcffd7675eb6d1488a2f0b196a1b4e5bdb` | `b0c26e000ecb98e4604ada1e3fc649820d9df6d5bcb1be5bdc15bc278a1b79ee` |
| `Chapters/08_Control_Firmware/01_Control_Objectives.tex` | `6cf93b8b9e210d4b7dec28815917902ca538ed3206fb19615a6c4ca355f2c962` | `2a939a907debd463be02bc851ae9672a99c434bcdba4a8c95fe807e071b8b05e` |
| `Chapters/08_Control_Firmware/02_Architecture_Timing.tex` | `82385ceb104e3f892d1be7200479b968fb34fc43f9f572fa64cd881e174bcb0b` | `335bbd6acb350a9a2004bd5bf45554d9804f4c5c12254af1894dd2517b5165e6` |
| `Chapters/08_Control_Firmware/03_Feedback_Calibration.tex` | `37e5407e6863ab69d09541040e996e1ee6efd23b6c41a6e836a2b357c2b1f3e5` | `bb18bf6197361e662c37df10cae9140d39fdb4a725253de7612a2416f25ccfc6` |
| `Chapters/08_Control_Firmware/04_V0_Open_Loop.tex` | `76ad968c10cb561f8f9b5974524834e772d102beb2d7130b0d97d42c30e5e048` | `40b6719da9dd50004e8bd8f7e0f6c96ff72436020262e74e81a61b875bc8dc95` |
| `Chapters/08_Control_Firmware/05_V1_Blocking_Closed_Loop.tex` | `ec89861f84da4eb827b9d98daced5d240d07469b0dd779e9bd5371c568374773` | `cc28319e175758acda671f49dad975c3c7299d5540fc7517c25039c62131d74e` |
| `Chapters/08_Control_Firmware/06_Blocking_Limitations.tex` | `7da016658fc7611fae38e31edf00c0420e16db6af09a6efc626d39c3fb57343a` | `0053584a9b7e527507c1854fc378cc76e4842ca85fe27bf088e17c3c6224bff1` |
| `Chapters/08_Control_Firmware/07_V2_DMA.tex` | `6acd49062e73e1ad2c9f7293518f84df255eef1a6eaa6ea7531f35dff356c84e` | `bc6f2d445da21d6b91362556471a2a97aa907f33b502701e7442dff1ebf30b01` |
| `Chapters/08_Control_Firmware/08_Control_Law.tex` | `a29fa415ed6af690b23eb19bb867c7d3e379808fb049c5da0923dd99f30498a8` | `cc9ae073176001fe19914b7f70796b254cd51a142db0e8c3d2f38899d10f96eb` |
| `Chapters/08_Control_Firmware/09_Limits_Antiwindup.tex` | `d61a2c16673c8cbd3d21ced65c450597dea8f486615e2eae89d5d34e2e5a2490` | `e1f376e65bdb59e95edf6c7fe0cbc663b2ab2717c23da44c2400ae5f7892b25c` |
| `Chapters/08_Control_Firmware/10_Open_Circuit_Safety.tex` | `2d2da41cb17596a544882d98a35451f91c487afd80475f9bb6a8ffc1be348bde` | `31ee71768b848854ccb5966da426018b4bcb85b300008ed9db56f39a7b6fe5ee` |
| `Chapters/08_Control_Firmware/11_State_Machine.tex` | `416df7145e6874d710e3aaca39a725dc86d201ac838fd34db268e0cde5b02390` | `3d43ac4eca026c2972290c80118ef6a331a3505375d5d021aa9ff6797de36cdc` |
| `Chapters/08_Control_Firmware/12_Fault_Handling.tex` | `7b892a4bec06753094864debd704fbaa1e23e66ae33cdd16b31a3b5c5eeebf7b` | `9df9e071c05f57403c12b58d814f56a3781b03e394c2b0ac595ce17e2637bb96` |
| `Chapters/08_Control_Firmware/13_Timing_Resources.tex` | `fda61fb187c75d25819329868a9c0ec4e7a8ac47fe3451190e9b04dd9f197cc3` | `628d53171ba35583ddf7c78e1c804f39243bf450721b92a4fb9822ef7a1955f2` |
| `Chapters/08_Control_Firmware/14_Version_Comparison.tex` | `ba87aef0600cf737d6d5f99fd33f6ed0ff0f0abe946d02ff04203cf0a37fada5` | `433c380837bacfe05c9563df31c4895cc2987afec2bd4de8c5dbdbc37ed77cef` |
| `Chapters/08_Control_Firmware/15_PWR_2_Port.tex` | `085f36aea538c33ae57bee78f5000773b326952435791c171f6b0ba13152d925` | `c435b9ce64afa87ebcfb12e0899f0fd557fcc6ecdec2f97187ce6e2f9380ebb5` |
| `Chapters/08_Control_Firmware/chapter.tex` | `3e0f73f64a5168472dab034a9f030edf79c45ab9c6374fbff30394d989d3a539` | `09c766520b9ee1c4ee04c8327f404bc2ebc0eed640f87a57eb4df9d0890ff700` |
