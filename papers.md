# 論文ダイジェスト

生成日時: 2026-08-17 19:45 / 収録 191 件

## トピック

- [Occupancy](#occupancy) — 45 件
- [Gaussian Splatting](#gaussian-splatting) — 32 件
- [AD Perception](#ad-perception) — 29 件
- [HD Map](#hd-map) — 26 件
- [3D Detection](#3d-detection) — 20 件
- [Open-world](#open-world) — 10 件
- [Reconstruction](#reconstruction) — 9 件
- [Scene Understanding](#scene-understanding) — 8 件
- [World Model](#world-model) — 6 件
- [Occupancy Forecasting](#occupancy-forecasting) — 3 件
- [Topology](#topology) — 3 件

## Occupancy

### OccAnyScene: Towards Unified Indoor-Outdoor 3D Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.08696
- Code: -

### Group-wise Supervision with Focal-Dice Loss for Long-Tailed Indoor Semantic Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.28935
- Code: -

### Learning Adaptive Semantic Gaussian Allocation for 3D Occupancy

arXiv 2026 / Occupancy

**概要**

Semantic 3D Gaussians を用いた 3D semantic occupancy prediction では、Gaussian の総数をメモリ・計算量の都合で制限する必要があるが、従来研究は primitive の形状表現・初期化・densification といった「どう表現し、どう増やすか」に注力してきた。本論文は、限られた本数の中で「どの Gaussian を残すか」という配分の問題が未解決であり、単純な領域に冗長な Gaussian が残る一方で難しい領域が不足する偏りが生じると指摘する。そこで、Gaussian の属性と局所的な幾何・意味特徴からスコアを付け、固定サイズの最終 Gaussian 集合を選択する Semantic Gaussian Allocation Transformer (SAGFormer) を提案する。nuScenes-SurroundOcc と SSCBench-KITTI-360 で評価している。

**新規性**

primitive の表現力向上や追加戦略ではなく、限られた容量をどの領域に割り当てるかという選択問題を明示的に扱い、Transformer によるスコアリングで最終的な Gaussian 集合を決める点が従来と異なる。同程度の最終本数・カバレッジ条件下で semantic mixing の低減や未使用 Gaussian の削減を示している。

**読む理由**

Gaussian ベースの occupancy 表現において、精度を左右するのが表現力だけでなく容量配分であることを示しており、コンパクトな 3D 表現を車載環境で実用化する際の設計指針として参考になる。

- Paper: https://arxiv.org/abs/2607.21896
- Code: -

### RayOcc: Occlusion-Aware Ray Occupancy Estimation via Gaussian Mixture Intensity

IROS 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.17660
- Code: -

### SparseOcc++: Geometry-Aware Sparse Latent Representation for Semantic Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

カメラ画像から3D semantic occupancyを予測する際、dense voxel表現は空領域に計算を浪費し、BEVやTPVへの投影は細かい3D構造を失うという課題に取り組んだ研究。従来のfully sparseな手法(SparseOccなど)は、空領域へ高次元特徴を無差別に伝播させたうえでvoxel単位の分類を行うため、scene completionとsemantic predictionが絡み合い、余計な活性化と計算負荷、幾何的な曖昧さを生んでいた。SparseOcc++はこの2つを明示的に分離し、completionをsparse anchor voxel上のsigned distance回帰(scene completion field, SCF)として定式化する。SCFから完全な体積シーンを構成するgeometry-guided propagationを介し、幾何的に検証された領域に限定してsemantic segmentationを適用する。

**新規性**

scene completionをsemantic segmentationから切り離し、voxel分類ではなくsparse anchor voxel上のsigned distance回帰として扱う点が従来のfully sparse occupancy手法と異なる。屋外の複雑な幾何に対応するため、orthogonal decompositionとdiscretized distance learningを組み合わせている点も特徴。

**読む理由**

occupancy predictionにおけるsparse表現の効率と精度の両立という主要な論点に対し、幾何と意味の役割分担という設計指針を示している。nuScenesでSparseOcc比IoU +2.3、3.9倍高速、SemanticKITTIでOccFormer比5.9倍高速と報告されており、実用的な計算コストの観点でも参照価値がある。

- Paper: https://arxiv.org/abs/2607.04732
- Code: -

### Sparse-Aware Vector Quantization for Bandwidth-Efficient Collaborative 3D Semantic Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.01928
- Code: -

### Semantic Occupancy Prediction with Dual Range-Voxel Representation

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.31688
- Code: -

### UnsOcc: 3D Semantic Occupancy Prediction in Unstructured Scene via Rendering Fusion

arXiv 2026 / Occupancy

**概要**

整備された道路とは異なる非構造化シーン(露天掘り鉱山など)では、不規則な障害物や疎なシーン構造のため従来の3D物体検出ベースの認識が機能しにくい。本論文はそうした環境向けの多モーダル3D semantic occupancy predictionフレームワークUnsOccを提案する。シーンの疎性によるcross-modal fusionの難しさと、より深刻なlong-tail分布という2つの課題に取り組み、検証のために露天掘り鉱山で収集した専用データセットも構築している。鉱山データセットとnuScenesの双方で既存手法を上回る性能を報告している。

**新規性**

双方向のrendering supervisionでcamera-LiDAR特徴を整合させるRenderFusionと、疎な3D occupancy予測をGaussian Splattingで密な2D semantic segmentationへ射影して補助監督とするGSRefinementを組み合わせた点が従来と異なる。特に非構造化シーンとlong-tailカテゴリを明示的な設計目標に据えている。

**読む理由**

occupancy predictionをGaussian Splattingベースのrendering supervisionで補強する流れの具体例であり、監督信号の設計として参考になる。また、都市道路以外の非構造化屋外環境向けデータセットを提示している点で、環境認識の適用範囲拡大の動向を追ううえで有用。

- Paper: https://arxiv.org/abs/2606.03581
- Code: -

### VGGT-Occ: Geometry-Grounded and Density-Aware Gated Fusion for 3D Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.16911
- Code: -

### WeatherOcc3D: VLM-Assisted Adverse Weather Aware 3D Semantic Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.16127
- Code: -

### World2Minecraft: Occupancy-Driven Simulated Scenes Construction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.27578
- Code: -

### ProOOD: Prototype-Guided Out-of-Distribution 3D Occupancy Prediction

CVPR 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.01081
- Code: https://github.com/7uHeng/ProOOD

### Gau-Occ: Geometry-Completed Gaussians for Multi-Modal 3D Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.22852
- Code: -

### DriveTok: 3D Driving Scene Tokenization for Unified Multi-View Reconstruction and Understanding

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.19219
- Code: https://github.com/paryi555/DriveTok

### SGR-OCC: Evolving Monocular Priors for Embodied 3D Occupancy Prediction via Soft-Gating Lifting and Semantic-Adaptive Geometric Refinement

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.14076
- Code: -

### $M^2$-Occ: Resilient 3D Semantic Occupancy Prediction for Autonomous Driving with Incomplete Camera Inputs

arXiv 2026 / Occupancy

**概要**

カメラベースのsemantic occupancy predictionは、surround-viewの全カメラが正常に得られる前提で設計されているが、実運用では遮蔽やハードウェア故障、通信障害で一部の視点が欠けることがある。本論文は視点欠損下でも幾何構造と意味的整合性を保つフレームワーク$M^2$-Occを提案する。隣接カメラ間の空間的な重なりを利用して欠損視点の表現をfeature空間で復元するMulti-view Masked Reconstruction (MMR)と、クラスごとのsemantic prototypeを蓄えたmemory bankから大域的な事前情報を引き出して曖昧なvoxel特徴を補正するFeature Memory Module (FMM)の2つで構成される。nuScenesベースのSurroundOccベンチマーク上に、決定的な単一視点欠損と確率的な複数視点ドロップアウトを含む欠損視点評価プロトコルも整備している。

**新規性**

従来のocc手法が暗黙に前提としていた「全周カメラが揃っている」という仮定を明示的に外し、feature空間での欠損視点復元とクラスレベルのsemantic prototype memoryを組み合わせて頑健性を確保した点が異なる。さらに欠損視点を体系的に評価するプロトコル自体を提示している。

**読む理由**

occupancy予測の精度競争ではなくセンサ欠損時の頑健性という実運用上の観点を扱っており、環境認識モジュールの信頼性評価の枠組みとして参考になる。欠損視点に対する評価プロトコルは他のBEV/occ手法のロバスト性検証にも流用しやすい。

- Paper: https://arxiv.org/abs/2603.09737
- Code: https://github.com/qixi7up/M2-Occ

### 4DRC-OCC: Robust Semantic Occupancy Prediction Through Fusion of 4D Radar and Camera

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.07794
- Code: -

### Can we Trust Unreliable Voxels? Exploring 3D Semantic Occupancy Prediction under Label Noise

IROS 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.06279
- Code: https://github.com/mylwx/OccNL

### VG3S: Visual Geometry Grounded Gaussian Splatting for Semantic Occupancy Prediction

IROS 2026 / Occupancy

**概要**

カメラ画像のみから 3D semantic occupancy を予測するタスクを扱う論文。3D Gaussian splatting を occupancy 表現に使うと計算コストを抑えられる一方、良質な Gaussian を作るには幾何的な手がかりが必要で、vision-centric な設定ではそれが不足する点を課題としている。そこで凍結した Vision Foundation Model (VFM) が持つ 3D 幾何の事前知識を occupancy 予測側に取り込む VG3S を提案する。nuScenes の occupancy ベンチマークで baseline に対し IoU +12.6%、mIoU +7.5% の改善を報告している。

**新規性**

VFM のトークンを特徴集約・タスク固有のアライメント・マルチスケール再構成の三段で変換する階層的な geometric feature adapter を plug-and-play で挿入し、cross-view の幾何 grounding を Gaussian ベース occupancy に持ち込む点が従来と異なる。特定の VFM に依存せず、複数の VFM で一貫して精度が向上することも示している。

**読む理由**

Gaussian splatting による効率的な occupancy 表現と、汎用 vision foundation model の幾何事前知識をどう接続するかという、近年の環境認識研究の主要な合流点を具体的に示している。adapter が plug-and-play で複数 VFM に効くという報告は、既存の occupancy パイプラインへの転用可能性を考えるうえで参考になる。

- Paper: https://arxiv.org/abs/2603.06210
- Code: -

### VLMFusionOcc3D: VLM Assisted Multi-Modal 3D Semantic Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

カメラとLiDARを統合した3D semantic occupancy predictionにおいて、voxel特徴の意味的曖昧さと悪天候下での性能劣化を課題として扱った論文。多視点画像と点群を共通のvoxel空間に投影する二分岐パイプラインを土台に、VLM由来の言語事前知識をvoxelへ注入するInstVLM(gated cross-attentionとLoRA適応したCLIP埋め込み)を提案する。さらに、車両メタデータと天候条件のプロンプトからセンサ寄与を動的に再重み付けするWeathFusion、カメラ由来の密な幾何とLiDARの疎で正確な点を整合させるDAGA lossを導入する。nuScenesとSemanticKITTIで既存のvoxelベース手法に対する上乗せ効果を検証している。

**新規性**

従来の幾何・特徴融合中心のoccupancy手法に対し、CLIP由来の言語事前知識をvoxelレベルに直接注入し、さらに天候条件に応じてセンサ融合の重みを動的に切り替える点が異なる。既存のvoxelベース手法に後付けできるplug-and-playモジュールとして設計されている点も特徴。

**読む理由**

occupancy predictionにVLMの意味事前知識を持ち込む流れと、悪天候などセンサ信頼度が変動する状況でのマルチモーダル融合設計の両方を押さえられる。環境認識のロバスト性向上の設計指針として参考になる。

- Paper: https://arxiv.org/abs/2603.02609
- Code: -

### Dr.Occ: Depth- and Region-Guided 3D Occupancy from Surround-View Cameras for Autonomous Driving

CVPR 2026 / Occupancy

**概要**

サラウンドビューカメラ画像から3D semantic occupancy を予測する手法の提案。カメラのみの手法では、ピクセル単位で正確な深度が得られないために2D→3Dの view transformation で幾何的なズレが生じること、さらにセマンティッククラスが空間的に偏って分布する(spatial class imbalance / anisotropy)ことが課題だと整理している。これに対し、深度手がかりで幾何を揃える view transformer と、空間領域ごとに専門家を割り当てる Mixture-of-Experts 型の transformer を組み合わせた Dr. Occ を提案する。Occ3D-nuScenes 上でベースラインの BEVDet4D に対し mIoU +7.43%、IoU +3.09% の改善を報告している。

**新規性**

MoGe-2 による高品質な dense depth を幾何プライアとして使う D²-VFormer で voxel 特徴の位置合わせ精度を高める点と、MoE に着想を得て空間領域ごとに expert を切り替える R/R²-EFormer でクラスの空間的偏りに対処する点を組み合わせたことが従来手法との違い。幾何アラインメントとセマンティック学習をそれぞれ別モジュールで補完的に扱う設計になっている。

**読む理由**

カメラのみの occupancy 予測において依然としてボトルネックである深度精度の問題に、外部の汎用深度モデル(MoGe-2)を持ち込むという最近の潮流を示す例として参考になる。また、occupancy タスク特有の空間的クラス不均衡を条件付き計算(MoE)で扱うアプローチは、BEV/voxel 系の環境認識モデル設計全般に転用しうる視点を与える。

- Paper: https://arxiv.org/abs/2603.01007
- Code: -

### TFusionOcc: T-Primitive Based Object-Centric Multi-Sensor Fusion Framework for 3D Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2602.06400
- Code: https://github.com/DanielMing123/TFusionOcc

### GaussianOcc3D: A Gaussian-Based Adaptive Multi-modal 3D Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

自動運転の3D semantic occupancy predictionにおいて、カメラの意味情報とLiDARの幾何情報を単一モダリティで両立できない問題と、voxel表現の計算コスト・BEV表現の情報損失という表現上のジレンマを扱っている。著者らはシーンを連続的な3D Gaussianのプリミティブで表現し、そこにカメラとLiDARの特徴を統合するマルチモーダル枠組みGaussianOcc3Dを提案する。疎なLiDAR信号をdepth-wise deformable samplingでGaussianに載せるLDFA、ドメインノイズを抑えるEBFS、センサ信頼度に応じてuncertainty-awareに重み付けするACLF、そしてSelective State Space Modelで線形計算量の大域文脈を得るGauss-Mamba Headの4モジュールから構成される。Occ3D・SurroundOcc・SemanticKITTIでmIoU 49.4%/28.9%/25.2%を報告し、雨天・夜間条件での頑健性も示している。

**新規性**

voxelでもBEVでもなく連続的な3D Gaussian表現をマルチモーダル融合の共通基盤として用い、モダリティ間の空間的ズレと信頼度差をdeformable samplingと不確実性に基づく再重み付けで吸収している点が従来のocc予測手法と異なる。加えて、occupancy headにMamba系のselective SSMを導入し、線形計算量で大域文脈を扱う構成をとっている。

**読む理由**

3D Gaussianを認識タスク側の中間表現として使う流れと、camera-LiDAR融合occupancyの設計指針が同時に見える論文であり、環境認識のための3D表現選択の動向を追ううえで参考になる。悪天候・夜間を含む条件での評価が報告されている点も、実運用に近い頑健性の議論として押さえておく価値がある。

- Paper: https://arxiv.org/abs/2601.22729
- Code: -

### Gaussian Based Adaptive Multi-Modal 3D Semantic Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.14448
- Code: -

### SUG-Occ: Explicit Semantics and Uncertainty Guided Sparse Learning for Efficient 3D Occupancy Prediction

arXiv 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.11396
- Code: -

### ST-GS: Vision-Based 3D Semantic Occupancy Prediction with Spatial-Temporal Gaussian Splatting

ICRA 2026 / Occupancy

**概要**

カメラ画像のみから3D semantic occupancyを推定する研究。3D semantic Gaussianで占有を表現する近年の手法は計算量を抑えられる一方、multi-view間の空間的な相互作用が不十分で、複数フレームにわたる時間的一貫性も弱いという課題があった。本論文はこの2点を補う ST-GS というフレームワークを提案し、Gaussianベースのパイプラインに空間・時間方向のモデリングを組み込む。nuScenesのoccupancy predictionベンチマークで評価している。

**新規性**

dual-mode attention の中に guidance-informed な空間集約を設けてGaussian表現間の空間的相互作用を強め、さらに geometry-aware な時間融合により過去フレームの文脈をscene completionに活かす点が、既存のGaussianベースoccupancy手法との違い。

**読む理由**

occupancy predictionの表現としてGaussian Splattingを使う流れの最新例であり、空間集約と時間融合という改良の方向性が把握できる。特に時間的一貫性の改善を明示的に扱っている点は、動的な屋外シーンの認識・地図生成を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2509.16552
- Code: -

### Semantic Causality-Aware Vision-Based 3D Occupancy Prediction

ICCV 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2509.08388
- Code: -

### SliceSemOcc: Vertical Slice Based Multimodal 3D Semantic Occupancy Representation

arXiv 2025 / Occupancy

**概要**

自動運転の3D semantic occupancy predictionにおいて、voxel特徴の高さ方向(height-axis)の情報が十分に活用されていない点を課題とした研究。従来のSENet系channel attentionが全ての高さ層に一様な重みを与えてしまう問題に対し、高さ方向のスライスに基づくマルチモーダルな表現手法SliceSemOccを提案する。global/localの垂直スライスからvoxel特徴を抽出し、global-local fusionモジュールで細かい空間的ディテールと大域的な文脈を統合する。nuScenes-SurroundOccとnuScenes-OpenOccupancyでmIoUの向上、特に小物体カテゴリでの改善を報告している。

**新規性**

voxel特徴を垂直スライス単位で扱い、global/localスライスの融合によって高さ方向の意味変化を明示的に捉える点が新しい。さらにaverage poolingで高さ方向の解像度を保持しつつ各高さ層ごとに動的なchannel attention重みを割り当てるSEAttention3Dを導入し、従来の高さ方向に一様なattentionとの差別化を図っている。

**読む理由**

occupancy表現において高さ方向の扱いがどこまで性能に効くのかを、attention設計の観点から具体的に検証した事例として参考になる。BEVでは落ちてしまう垂直方向の情報をどう設計に組み込むかは、occupancyベースの環境認識を追ううえで押さえておきたい論点である。

- Paper: https://arxiv.org/abs/2509.03999
- Code: -

### Vision-Only Gaussian Splatting for Collaborative Semantic Occupancy Prediction

AAAI 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.10936
- Code: -

### GTAD: Global Temporal Aggregation Denoising Learning for 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

自動運転やロボットの動的環境認識において、既存の occupancy 手法は隣接フレーム間の局所的な時系列相互作用に依存しており、系列全体の情報を十分に活かせていないという課題を扱う。本論文は、過去の観測を含むグローバルな時系列特徴をどのように集約すれば有効な occupancy 表現が得られるかを検討する。提案手法 GTAD は、モデル内部の latent denoising network によって、現在時刻の局所的な時系列特徴と履歴系列からのグローバルな時系列特徴を統合する。nuScenes および Occ3D-nuScenes ベンチマークと ablation study で有効性を示している。

**新規性**

隣接フレーム中心の局所的な temporal fusion にとどまらず、履歴系列全体を対象としたグローバル時系列集約を3Dシーン理解の枠組みとして導入した点が従来手法と異なる。さらに、その集約を in-model の latent denoising network として実現している点も特徴である。

**読む理由**

occupancy prediction における時系列情報の使い方は精度と一貫性を左右する主要な設計軸であり、局所から大域へと拡張する本手法の方向性は環境認識モデルの temporal 設計を追ううえで参考になる。denoising を特徴集約機構として使うアプローチも、他の BEV/occupancy 系タスクへの転用可能性がある。

- Paper: https://arxiv.org/abs/2507.20963
- Code: -

### GaussianFusionOcc: A Seamless Sensor Fusion Approach for 3D Occupancy Prediction Using 3D Gaussians

arXiv 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.18522
- Code: -

### From Binary to Semantic: Utilizing Large-Scale Binary Occupancy Data for 3D Semantic Occupancy Prediction

ICCV 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.13387
- Code: https://github.com/ToyotaInfoTech/b2s-occupancy

### FMOcc: TPV-Driven Flow Matching for 3D Occupancy Prediction with Selective State Space Model

arXiv 2025 / Occupancy

**概要**

少数フレーム入力での3D semantic occupancy predictionにおいて、遮蔽領域や遠方シーンの推定精度が落ちる問題と3D空間の冗長性に取り組んだ研究。TPV(Tri-perspective View)表現をベースに、flow matchingで欠損した特徴を生成するFMSSMモジュールと、選択的state space model(SSM)によるTPV特徴のフィルタリングを組み合わせている。さらにセンサデータ欠損に対する頑健性を高めるMask Training手法を導入した。Occ3D-nuScenesとOpenOccで、2フレーム入力でRayIoU 43.1%/mIoU 39.8%(Occ3D-nuScenes val)を報告している。

**新規性**

履歴フレームを多数積み上げて精度を稼ぐ従来手法と異なり、flow matchingによる特徴補完で少数フレームのまま欠損情報を補う点が特徴。加えてPlane Selective SSM(PS3M)により空気voxelが非空気voxelに与える影響を抑え、計算効率と遠方予測の両立を狙っている。

**読む理由**

occupancy predictionに生成モデル(flow matching)とstate space modelを持ち込む流れを示す事例であり、多フレーム依存を減らしつつ遮蔽・遠方を扱う設計指針として参考になる。推論メモリ5.4G・330msといった実用性寄りの数値も報告されている。

- Paper: https://arxiv.org/abs/2507.02250
- Code: -

### Out-of-Distribution Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

3D semantic occupancy predictionは自動運転向けの密な意味表現として有用だが、既存手法は学習分布内のシーンを前提としており、未知物体やlong-tailな対象を見落とすリスクがあるという課題を扱っている。本論文はvoxel空間でのOoD検出を行う新しいタスク設定「Out-of-Distribution Semantic Occupancy Prediction」を提案する。データ不足を補うため、現実的な空間配置とocclusionのパターンを保ったまま合成異常物体を挿入するRealistic Anomaly Augmentationを設計し、VAA-KITTIとVAA-KITTI-360という2つのデータセットを構築した。さらに、occupancy予測にOoD検出を統合したフレームワークOccOoDを提案している。

**新規性**

従来のoccupancy予測が既知クラスの意味推定に閉じていたのに対し、voxel空間でのOoD検出をタスクとして定式化した点が新しい。手法面では、voxel表現とBEV表現という相補的な2つの空間から意味予測を補正するCross-Space Semantic Refinement (CSSR) を導入している。

**読む理由**

occupancyベースの環境認識を実運用に近づけるうえで避けられない未知物体への対応を正面から扱っており、open-world perceptionとoccupancy予測を接続する事例として参考になる。異常物体を含むベンチマークとコードが公開予定である点も、評価基盤として追う価値がある。

- Paper: https://arxiv.org/abs/2506.21185
- Code: https://github.com/7uHeng/OccOoD

### OC-SOP: Enhancing Vision-Based 3D Semantic Occupancy Prediction by Object-Centric Awareness

arXiv 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.18798
- Code: -

### YouTube-Occ: Learning Indoor 3D Semantic Occupancy Prediction from YouTube Videos

ECCV 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.18266
- Code: -

### A Synthetic Benchmark for Collaborative 3D Semantic Occupancy Prediction in V2X-Enabled Autonomous Driving

arXiv 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.17004
- Code: https://github.com/tlab-wide/Co3SOP

### QueryOcc: Query-based Self-Supervision for 3D Semantic Occupancy

CVPR 2026 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2511.17221
- Code: -

### RIOcc: Efficient Cross-Modal Fusion Transformer with Collaborative Feature Refinement for 3D Semantic Occupancy Prediction

ICCV 2025 / Occupancy

**概要**

LiDARとカメラを融合した3D semantic occupancy predictionの効率化を狙った研究。既存手法が大規模なvoxel空間で処理するために計算コストが高く細部が失われる点、さらに遮蔽物体や遠方の情報を捉えにくい点を課題として挙げている。RIOccはマルチモーダル入力を統一されたBEV空間にエンコードして計算量を抑えつつ特徴のアライメントを行い、multi-scale処理で受容野を広げる。Occ3D-nuScenesで54.2 mIoU、nuScenes-Occupancyで25.9 mIoUを報告している。

**新規性**

voxelベースの重い処理ではなくBEV空間での統一表現に落とし込んだうえで、LiDAR側にChannelとGrid両方向のDual-branch Pooling、カメラ側にWavelet/Semantic Encoder、融合にDeformable Dual-Attentionを導入し、モダリティごとに適した特徴精緻化を設計している点が異なる。

**読む理由**

occupancy predictionにおけるBEV表現の使い方と、LiDAR-カメラ融合モジュールの設計指針を押さえられる。計算コストと精度のトレードオフを扱う実装寄りの参考として、環境認識の設計検討時に有用。

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Fan_RIOcc_Efficient_Cross-Modal_Fusion_Transformer_with_Collaborative_Feature_Refinement_for_ICCV_2025_paper.html
- Code: -

### Rethinking Temporal Fusion with a Unified Gradient Descent View for 3D Semantic Occupancy Prediction

CVPR 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2504.12959
- Code: https://github.com/cdb342/GDFusion

### EvOcc: Accurate Semantic Occupancy for Automated Driving Using Evidence Theory

CVPR 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Kalble_EvOcc_Accurate_Semantic_Occupancy_for_Automated_Driving_Using_Evidence_Theory_CVPR_2025_paper.html
- Code: -

### ALOcc: Adaptive Lifting-Based 3D Semantic Occupancy and Cost Volume-Based Flow Predictions

ICCV 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2411.07725
- Code: -

### SDFormer: Vision-based 3D Semantic Scene Completion via SAM-assisted Dual-channel Voxel Transformer

ICCV 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Xue_SDFormer_Vision-based_3D_Semantic_Scene_Completion_via_SAM-assisted_Dual-channel_Voxel_ICCV_2025_paper.html
- Code: -

### TopNet: Transformer-Efficient Occupancy Prediction Network for Octree-Structured Point Cloud Geometry Compression

CVPR 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Wang_TopNet_Transformer-Efficient_Occupancy_Prediction_Network_for_Octree-Structured_Point_Cloud_Geometry_CVPR_2025_paper.html
- Code: https://github.com/xinjiewang1995/TopNet

### Distilling Diffusion Models to Efficient 3D LiDAR Scene Completion

ICCV 2025 / Occupancy

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2412.03515
- Code: https://github.com/happyw1nd/ScoreLiDAR

## Gaussian Splatting

### HumanoidVLN: A Physics-Grounded Simulator and Benchmark for Vision-Language Navigation Across Diverse Humanoid Embodiments

arXiv 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.12860
- Code: -

### Immediate 3D Gaussian Splat Reconstruction of Unordered Input with Global Consistency

arXiv 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.14481
- Code: -

### CodecSplat: Ultra-Compact Latent Coding for Feed-Forward 3D Gaussian Splatting

arXiv 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.25563
- Code: -

### ReconPhys: Reconstruct Appearance and Physical Attributes from Single Video

arXiv 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.07882
- Code: -

### 360-GeoGS: Geometrically Consistent Feed-Forward 3D Gaussian Splatting Reconstruction for 360 Images

arXiv 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.02102
- Code: -

### GigaWorld-0: World Models as Data Engine to Empower Embodied AI

arXiv 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2511.19861
- Code: -

### Gaussian See, Gaussian Do: Semantic 3D Motion Transfer from Multiview Video

arXiv 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2511.14848
- Code: -

### EGS-SLAM: RGB-D Gaussian Splatting SLAM with Events

RAL 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.07003
- Code: https://github.com/Chensiyu00/EGS-SLAM

### From Seeing to Experiencing: Scaling Navigation Foundation Models with Reinforcement Learning

arXiv 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.22028
- Code: -

### Stereo-GS: Multi-View Stereo Vision Model for Generalizable 3D Gaussian Splatting Reconstruction

arXiv 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.14921
- Code: -

### VISTA: Open-Vocabulary, Task-Relevant Robot Exploration with Online Semantic Gaussian Splatting

arXiv 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.01125
- Code: -

### MAPo: Motion-Aware Partitioning of Deformable 3D Gaussian Splatting for High-Fidelity Dynamic Scene Reconstruction

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.19786
- Code: -

### E2EGS: Event-to-Edge Gaussian Splatting for Pose-Free 3D Reconstruction

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.14684
- Code: -

### SDGS: Spatial Difference Guided Gaussian Splatting for Simultaneous Localization and 3D Reconstruction

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Tian_SDGS_Spatial_Difference_Guided_Gaussian_Splatting_for_Simultaneous_Localization_and_CVPR_2026_paper.html
- Code: -

### BA-GS: Bayesian Adaptive Gaussian Splatting for SFM-Free 3D Reconstruction

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Ma_BA-GS_Bayesian_Adaptive_Gaussian_Splatting_for_SFM-Free_3D_Reconstruction_CVPR_2026_paper.html
- Code: -

### ExtrinSplat: Decoupling Geometry and Semantics for Open-Vocabulary Understanding in 3D Gaussian Splatting

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2509.22225
- Code: -

### SR3R: Rethinking Super-Resolution 3D Reconstruction With Feed-Forward Gaussian Splatting

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2602.24020
- Code: -

### OnlinePG: Online Open-Vocabulary Panoptic Mapping with 3D Gaussian Splatting

CVPR 2026 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.18510
- Code: -

### VoteSplat: Hough Voting Gaussian Splatting for 3D Scene Understanding

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.22799
- Code: -

### Toward Real-world BEV Perception: Depth Uncertainty Estimation via Gaussian Splatting

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2504.01957
- Code: -

### SplatAD: Real-Time Lidar and Camera Rendering with 3D Gaussian Splatting for Autonomous Driving

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Hess_SplatAD_Real-Time_Lidar_and_Camera_Rendering_with_3D_Gaussian_Splatting_CVPR_2025_paper.html
- Code: -

### DroneSplat: 3D Gaussian Splatting for Robust 3D Reconstruction from In-the-Wild Drone Imagery

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.16964
- Code: -

### LeanGaussian: Breaking Pixel or Point Cloud Correspondence in Modeling 3D Gaussians

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2404.16323
- Code: -

### AG2aussian: Anchor-Graph Structured Gaussian Splatting for Instance-Level 3D Scene Understanding and Editing

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Wang_AG2aussian_Anchor-Graph_Structured_Gaussian_Splatting_for_Instance-Level_3D_Scene_Understanding_ICCV_2025_paper.html
- Code: -

### LITA-GS: Illumination-Agnostic Novel View Synthesis via Reference-Free 3D Gaussian Splatting and Physical Priors

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Zhou_LITA-GS_Illumination-Agnostic_Novel_View_Synthesis_via_Reference-Free_3D_Gaussian_Splatting_CVPR_2025_paper.html
- Code: -

### PanoGS: Gaussian-based Panoptic Segmentation for 3D Open Vocabulary Scene Understanding

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.18107
- Code: -

### EAP-GS: Efficient Augmentation of Pointcloud for 3D Gaussian Splatting in Few-shot Scene Reconstruction

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Dai_EAP-GS_Efficient_Augmentation_of_Pointcloud_for_3D_Gaussian_Splatting_in_CVPR_2025_paper.html
- Code: -

### FreeSplatter: Pose-free Gaussian Splatting for Sparse-view 3D Reconstruction

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2412.09573
- Code: -

### Robust and Efficient 3D Gaussian Splatting for Urban Scene Reconstruction

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.23006
- Code: -

### UniGS: Modeling Unitary 3D Gaussians for Novel View Synthesis from Sparse-view Images

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2410.13195
- Code: https://github.com/jwubz123/UNIG

### AD-GS: Object-Aware B-Spline Gaussian Splatting for Self-Supervised Autonomous Driving

ICCV 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Xu_AD-GS_Object-Aware_B-Spline_Gaussian_Splatting_for_Self-Supervised_Autonomous_Driving_ICCV_2025_paper.html
- Code: -

### UniPre3D: Unified Pre-training of 3D Point Cloud Models with Cross-Modal Gaussian Splatting

CVPR 2025 / Gaussian Splatting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.09952
- Code: https://github.com/wangzy22/UniPre3D

## AD Perception

### Geometry-Grounded Unified 3D Perception for Autonomous Driving

arXiv 2026 / AD Perception

**概要**

カメラのみの自動運転認識では、複数カメラ・時系列にまたがってmetricな3D構造を保った共有表現が必要だが、既存手法はセマンティック認識向けに事前学習されたバックボーンを使い、3D幾何をタスク固有の下流モジュールで後付けしているため、共有表現が明示的な幾何やシーン構造を保持できないという問題がある。本論文は、再構成向けに学習されたVGGTのlatentを、キャリブレーション済みのストリーミングマルチカメラ運転シーンに適応させるGeoUPを提案する。得られたgeometry-groundedなlatentから、metric depth推定、3D object detection、semantic occupancy predictionという表面・インスタンス・体積レベルの出力をデコードする。マルチタスク・マルチデータセットの同時学習により、異種アノテーションを活用しセンサ構成や認識レンジの違いに対応する。

**新規性**

3D幾何をタスクヘッド側で導入するのではなく、再構成モデル(VGGT)のlatentを起点に据え、self/temporal/view attentionへの分解とcalibration-awareなraymap encodingでmetric scaleとカメラ幾何を表現自体に埋め込んでいる点が従来と異なる。単一の幾何表現からdetection・occupancy・depthを同時に読み出す統一設計になっている。

**読む理由**

3D reconstruction基盤モデルのlatentを自動運転の共有表現として転用する流れを示す例であり、occupancyやdetectionを個別タスクとして扱ってきた従来の設計思想に対する対案として参考になる。nuScenes/Argoverse 2/Waymo/KITTI/DDADと複数データセットで評価しており、汎化性の観点でも追う価値がある。

- Paper: https://arxiv.org/abs/2608.13147
- Code: -

### Object Detection for Autonomous Driving in Chinese Rural Scenes: An Experimental Study on Real-Synthetic Data Mixing and Model Evaluation

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.27058
- Code: -

### Mutual Modality Trust with Lightweight Reconstruction Regularization for Fine-grained Tire Pattern Recognition

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.23979
- Code: -

### TGRIP: A Text-Guided Approach to Vehicle Instance Prediction in Autonomous Driving

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.04812
- Code: https://github.com/miguelag99/TGRIP

### Towards Compact Autonomous Driving Perception with Balanced Learning and Multi-sensor Fusion

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.02979
- Code: https://github.com/oskarnatan/compact-perception

### ATLAS: A Large-Scale Evaluation Benchmark for Adversarial LiDAR Perception

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.02924
- Code: -

### Neuromorphic LiDAR-based Bird's Eye View Object Detection using Energy-efficient Spiking Neural Networks

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.25293
- Code: -

### STELLAR: Scaling 3D Perception Large Models for Autonomous Driving

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.20390
- Code: -

### Towards Trustworthy and Explainable AI for Perception Models: From Concept to Prototype Vehicle Deployment

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.16087
- Code: -

### Generative Texture Diversification of 3D Pedestrians for Robust Autonomous Driving Perception

CVPR 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.13755
- Code: -

### Beyond Fixed Thresholds and Domain-Specific Benchmarks for Explainable Multi-Task Classification in Autonomous Vehicles

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.04299
- Code: -

### WILD SAM: A Simulated-and-Real Data Augmentation for Autonomous Driving Perception under Challenging Weather

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.01081
- Code: https://github.com/Kh-Hamed/WILD-SAM

### Object-Centric Stereo Ranging for Autonomous Driving: From Dense Disparity to Census-Based Template Matching

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.07980
- Code: -

### BEVPredFormer: Spatio-temporal Attention for BEV Instance Prediction in Autonomous Driving

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.02930
- Code: -

### Neural Reconstruction of LiDAR Point Clouds under Jamming Attacks via Full-Waveform Representation and Simultaneous Laser Sensing

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.00371
- Code: -

### Uncertainty Matters: Structured Probabilistic Online Mapping for Motion Prediction in Autonomous Driving

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.20076
- Code: -

### LiDAR Prompted Spatio-Temporal Multi-View Stereo for Autonomous Driving

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.03765
- Code: -

### Dynamic Deception: When Pedestrians Team Up to Fool Autonomous Cars

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2602.18079
- Code: -

### AurigaNet: A Real-Time Multi-Task Network for Enhanced Urban Driving Perception

arXiv 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2602.10660
- Code: https://github.com/KiaRational/AurigaNet

### DrivingGen: A Comprehensive Benchmark for Generative Video World Models in Autonomous Driving

ICLR 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.01528
- Code: -

### AD-SAM: Fine-Tuning the Segment Anything Vision Foundation Model for Autonomous Driving Perception

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2510.27047
- Code: -

### A Style-Based Profiling Framework for Quantifying the Synthetic-to-Real Gap in Autonomous Driving Datasets

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2510.10203
- Code: -

### From Filters to VLMs: Benchmarking Defogging Methods through Object Detection and Segmentation Performance

WACV 2026 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2510.03906
- Code: -

### Foundation Models for Autonomous Driving Perception: A Survey Through Core Capabilities

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2509.08302
- Code: -

### Decoupled Functional Evaluation of Autonomous Driving Models via Feature Map Quality Scoring

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.07552
- Code: -

### Adverse Weather-Independent Framework Towards Autonomous Driving Perception through Temporal Correlation and Unfolded Regularization

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.01583
- Code: -

### VLAD: A VLM-Augmented Autonomous Driving Framework with Hierarchical Planning and Interpretable Decision Process

arXiv 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.01284
- Code: -

### End-to-End Driving with Online Trajectory Evaluation via BEV World Model

ICCV 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2504.01941
- Code: https://github.com/liyingyanUCAS/WoTE

### JarvisIR: Elevating Autonomous Driving Perception with Intelligent Image Restoration

CVPR 2025 / AD Perception

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2504.04158
- Code: -

## HD Map

### PseudoMapLabeler: Confidence-Aware Pseudo-Label Generation for Semi-Supervised Online Mapping

ECCV 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.12600
- Code: -

### MapTCL: Temporal Consistency Learning via Bidirectional Alignment for Vectorized HD Map Construction

IROS 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.05209
- Code: -

### TwinIR: Coordinated Invisible Dual-Point Attacks on Online HD Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.04453
- Code: -

### Driver2Map: Imitating Human Driving for Online High-Definition Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.01338
- Code: -

### GaussianMap: Learning Gaussian Representation for Multi-Sensor Online HD Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.31177
- Code: -

### AerialFusionMapNet: Online HD Map Construction with Aerial-Onboard BEV Fusion

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.24784
- Code: https://github.com/DriverlessMobility/AerialFusionMapNet

### D2HDMap: Non-visible Driveline Map Prior for Online Vectorized HD Map Prediction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.20725
- Code: -

### HRDX: A Large-Scale Vector HD-Map Dataset

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.17080
- Code: https://github.com/honda-research-institute/HRDX

### The Road Ahead in Autonomous Driving: The KITScenes Multimodal Dataset

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.02956
- Code: -

### Systematic Discovery of Semantic Attacks in Online Map Construction through Conditional Diffusion

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.14396
- Code: -

### Learning Ego-Centric BEV Representations from a Perspective-Privileged View: Cross-View Supervision for Online HD Map Construction

ECCV 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.12218
- Code: -

### MapGCLR: Geospatial Contrastive Learning of Representations for Online Vectorized HD Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.10688
- Code: -

### Impact of Localization Errors on Label Quality for Online HD Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.03452
- Code: -

### SatMap: Revisiting Satellite Maps as Prior for Online HD Map Construction

arXiv 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.10512
- Code: -

### AMap: Distilling Future Priors for Ahead-Aware Online HD Map Construction

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.19150
- Code: -

### SATMapTR: Satellite Image Enhanced Online HD Map Construction

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.11319
- Code: -

### NavMapFusion: Diffusion-based Fusion of Navigation Maps for Online Vectorized HD Map Construction

WACV 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.03317
- Code: https://github.com/tmonnin/navmapfusion

### MapRF: Weakly Supervised Online HD Map Construction via NeRF-Guided Self-Training

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2511.19527
- Code: -

### Learning Global Representation from Queries for Vectorized HD Map Construction

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2510.06969
- Code: -

### Mapping like a Skeptic: Probabilistic BEV Projection for Online HD Mapping

BMVC 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.21689
- Code: https://github.com/Fatih-Erdogan/mapping-like-skeptic

### MapKD: Unlocking Prior Knowledge with Cross-Modal Distillation for Efficient Online HD Map Construction

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.15653
- Code: https://github.com/2004yan/MapKD2026

### An Initial Study of Bird's-Eye View Generation for Autonomous Vehicles using Cross-View Transformers

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.12520
- Code: -

### RelMap: Enhancing Online Map Construction with Class-Aware Spatial Relation and Semantic Priors

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.21567
- Code: -

### MapDiffusion: Generative Diffusion for Vectorized Online HD Map Construction and Uncertainty Estimation in Autonomous Driving

IROS 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.21423
- Code: -

### MambaMap: Online Vectorized HD Map Construction using State Space Model

arXiv 2025 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.20224
- Code: https://github.com/ZiziAmy/MambaMap

### OptiMVMap: Offline Vectorized Map Construction via Optimal Multi-vehicle Perspectives

CVPR 2026 / HD Map

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.17135
- Code: https://github.com/DanZeDong/OptiMVMap

## 3D Detection

### NCGR: Noise-Conditional Gated Rectification for Camera Extrinsic Perturbations in BEV 3D Object Detection

arXiv 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2608.03895
- Code: -

### DeGuNet: Depth-Guided Ultra-Compact Backbones for Efficient LiDAR-Camera 3D Detection

ECCV 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.12419
- Code: -

### Distortion-Aware PETR for BEV Object Detection with Mixed Pinhole-Fisheye Cameras

ICRA 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.08680
- Code: -

### Benchmarking Multi-View BEV Object Detection with Mixed Pinhole and Fisheye Cameras

ICRA 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.27818
- Code: https://github.com/CesarLiu/FishBEVOD.git

### StereoMV2D: A Sparse Temporal Stereo-Enhanced Framework for Robust Multi-View 3D Object Detection

arXiv 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.17620
- Code: https://github.com/Uddd821/StereoMV2D

### DGFusion: Dual-guided Fusion for Robust Multi-Modal 3D Object Detection

arXiv 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2511.10035
- Code: -

### BEVUDA++: Geometric-aware Unsupervised Domain Adaptation for Multi-View 3D Object Detection

arXiv 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2509.14151
- Code: -

### Seg2Track-SAM2: SAM2-based Multi-object Tracking and Segmentation

arXiv 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2509.11772
- Code: https://github.com/hcmr-lab/Seg2Track-SAM2

### Collaborative Perceiver: Elevating Vision-based 3D Object Detection via Local Density-Aware Spatial Occupancy

arXiv 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.21358
- Code: https://github.com/jichengyuan/Collaborative-Perceiver

### SToRe3D: Sparse Token Relevance in ViTs for Efficient Multi-View 3D Object Detection

CVPR 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.14110
- Code: -

### Scene Reconstruction as Mapping Priors for 3D Detection

CVPR 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Fu_Scene_Reconstruction_as_Mapping_Priors_for_3D_Detection_CVPR_2026_paper.html
- Code: -

### RaGS: Unleashing 3D Gaussian Splatting from 4D Radar and Monocular Cue for 3D Object Detection

CVPR 2026 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.19856
- Code: https://github.com/shawnnnkb/RaGS

### OcRFDet: Object-Centric Radiance Fields for Multi-View 3D Object Detection in Autonomous Driving

ICCV 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.23565
- Code: -

### FreqPDE: Rethinking Positional Depth Embedding for Multi-View 3D Object Detection Transformers

ICCV 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Su_FreqPDE_Rethinking_Positional_Depth_Embedding_for_Multi-View_3D_Object_Detection_ICCV_2025_paper.html
- Code: -

### OV-SCAN: Semantically Consistent Alignment for Novel Object Discovery in Open-Vocabulary 3D Object Detection

ICCV 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Chow_OV-SCAN_Semantically_Consistent_Alignment_for_Novel_Object_Discovery_in_Open-Vocabulary_ICCV_2025_paper.html
- Code: -

### Leveraging Temporal Cues for Semi-Supervised Multi-View 3D Object Detection

CVPR 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Park_Leveraging_Temporal_Cues_for_Semi-Supervised_Multi-View_3D_Object_Detection_CVPR_2025_paper.html
- Code: -

### CorrBEV: Multi-View 3D Object Detection by Correlation Learning with Multi-modal Prototypes

CVPR 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Xue_CorrBEV_Multi-View_3D_Object_Detection_by_Correlation_Learning_with_Multi-modal_CVPR_2025_paper.html
- Code: -

### DriveGEN: Generalized and Robust 3D Detection in Driving via Controllable Text-to-Image Diffusion Generation

CVPR 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.11122
- Code: -

### Towards Accurate and Efficient 3D Object Detection for Autonomous Driving: A Mixture of Experts Computing System on Edge

ICCV 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.04123
- Code: -

### V2X-R: Cooperative LiDAR-4D Radar Fusion with Denoising Diffusion for 3D Object Detection

CVPR 2025 / 3D Detection

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Huang_V2X-R_Cooperative_LiDAR-4D_Radar_Fusion_with_Denoising_Diffusion_for_3D_CVPR_2025_paper.html
- Code: -

## Open-world

### GeoSAM-3D: Geodesic Prompt Propagation for Open-Vocabulary 3D Scene Segmentation from Monocular Video

arXiv 2026 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.00447
- Code: -

### Contrastive Learning-Driven Traffic Sign Perception: Multi-Modal Fusion of Text and Vision

arXiv 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.23331
- Code: -

### EmbodiedSplat: Online Feed-Forward Semantic 3DGS for Open-Vocabulary 3D Scene Understanding

CVPR 2026 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.04254
- Code: -

### OpenVoxel: Training-Free Grouping and Captioning Voxels for Open-Vocabulary 3D Scene Understanding

CVPR 2026 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2601.09575
- Code: -

### Ov3R: Open-Vocabulary Semantic 3D Reconstruction from RGB Videos

CVPR 2026 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2507.22052
- Code: -

### OpenM3D: Open Vocabulary Multi-view Indoor 3D Object Detection without Human Annotations

ICCV 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.20063
- Code: -

### Open-Vocabulary Octree-Graph for 3D Scene Understanding

ICCV 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2411.16253
- Code: https://github.com/yifeisu/OV-Octree-Graph

### Cross-Modal and Uncertainty-Aware Agglomeration for Open-Vocabulary 3D Scene Understanding

CVPR 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.16707
- Code: -

### JiSAM: Alleviate Labeling Burden and Corner Case Problems in Autonomous Driving via Minimal Real-World Data

CVPR 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.08422
- Code: -

### Occlusion-aware Text-Image-Point Cloud Pretraining for Open-World 3D Object Recognition

CVPR 2025 / Open-world

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2502.10674
- Code: -

## Reconstruction

### RoadVGGT: Road-Structure-Aware Feed-Forward Road Surface Reconstruction

arXiv 2026 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.23758
- Code: -

### GauSSmart: Enhanced 3D Reconstruction through 2D Foundation Models and Geometric Filtering

arXiv 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2510.14270
- Code: -

### Uni3R: Unified 3D Reconstruction and Semantic Understanding via Generalizable Gaussian Splatting from Unposed Multi-View Images

CVPR 2026 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2508.03643
- Code: -

### From None to All: Self-Supervised 3D Reconstruction via Novel View Synthesis

CVPR 2026 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.27455
- Code: -

### SplatFlow: Self-Supervised Dynamic Gaussian Splatting in Neural Motion Flow Field for Autonomous Driving

CVPR 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2411.15482
- Code: -

### Event-boosted Deformable 3D Gaussians for Dynamic Scene Reconstruction

ICCV 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2411.16180
- Code: -

### BezierGS: Dynamic Urban Scene Reconstruction with Bezier Curve Gaussian Splatting

ICCV 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.22099
- Code: -

### DeGauss: Dynamic-Static Decomposition with Gaussian Splatting for Distractor-free 3D Reconstruction

ICCV 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.13176
- Code: -

### RadarSplat: Radar Gaussian Splatting for High-Fidelity Data Synthesis and 3D Reconstruction of Autonomous Driving Scenes

ICCV 2025 / Reconstruction

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.01379
- Code: -

## Scene Understanding

### Distill, Diffuse, Segment: Unsupervised 3D Semantic Segmentation for Autonomous Driving Based on Multi-Level Distillation and Graph Diffusion

arXiv 2026 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2605.08293
- Code: -

### GeoGuide: Hierarchical Geometric Guidance for Open-Vocabulary 3D Semantic Segmentation

CVPR 2026 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.26260
- Code: -

### PanDA: Unsupervised Domain Adaptation for Multimodal 3D Panoptic Segmentation in Autonomous Driving

CVPR 2026 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2604.19379
- Code: -

### CoSMo3D: Open-World Promptable 3D Semantic Segmentation through LLM-Guided Canonical Spatial Modeling

CVPR 2026 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Jin_CoSMo3D_Open-World_Promptable_3D_Semantic_Segmentation_through_LLM-Guided_Canonical_Spatial_CVPR_2026_paper.html
- Code: -

### LightSplat: Fast and Memory-Efficient Open-Vocabulary 3D Scene Understanding in Five Seconds

CVPR 2026 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2603.24146
- Code: -

### Masked Point-Entity Contrast for Open-Vocabulary 3D Scene Understanding

CVPR 2025 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2504.19500
- Code: -

### Identity-aware Language Gaussian Splatting for Open-vocabulary 3D Semantic Segmentation

ICCV 2025 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Jang_Identity-aware_Language_Gaussian_Splatting_for_Open-vocabulary_3D_Semantic_Segmentation_ICCV_2025_paper.html
- Code: -

### HiLoTs: High-Low Temporal Sensitive Representation Learning for Semi-Supervised LiDAR Segmentation in Autonomous Driving

CVPR 2025 / Scene Understanding

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.17752
- Code: -

## World Model

### ASTAD: Asymmetric Style Transfer for Synthetic-to-Real Adaptation in Autonomous Driving

ECCV 2026 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2606.29286
- Code: https://github.com/Dingyi-Yao/ASTAD

### GaussianDWM: 3D Gaussian Driving World Model for Unified Scene Understanding and Multi-Modal Generation

CVPR 2026 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.23180
- Code: -

### GenieDrive: Towards Physics-Aware Driving World Model with 4D Occupancy Guided Video Generation

CVPR 2026 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2512.12751
- Code: -

### HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation

ICCV 2025 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2501.14729
- Code: https://github.com/LMD0311/HERMES

### MaskGWM: A Generalizable Driving World Model with Video Mask Reconstruction

CVPR 2025 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2502.11663
- Code: -

### Epona: Autoregressive Diffusion World Model for Autonomous Driving

ICCV 2025 / World Model

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2506.24113
- Code: -

## Occupancy Forecasting

### SelfOccFlow: Towards end-to-end self-supervised 3D Occupancy Flow prediction

arXiv 2026 / Occupancy Forecasting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2602.23894
- Code: -

### GaussianWorld: Gaussian World Model for Streaming 3D Occupancy Prediction

CVPR 2025 / Occupancy Forecasting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2412.10373
- Code: -

### UniOcc: A Unified Benchmark for Occupancy Forecasting and Prediction in Autonomous Driving

ICCV 2025 / Occupancy Forecasting

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2503.24381
- Code: -

## Topology

### HGeo-TopoMap: Boosting Topological Mapping with Hierarchical Geometric Priors

arXiv 2026 / Topology

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2607.21281
- Code: https://github.com/lynn-yu/HGeo-TopoMap

### TopoHR: Hierarchical Centerline Representation for Cyclic Topology Reasoning in Driving Scenes with Point-to-Instance Relations

CVPR 2026 / Topology

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Bai_TopoHR_Hierarchical_Centerline_Representation_for_Cyclic_Topology_Reasoning_in_Driving_CVPR_2026_paper.html
- Code: -

### T2SG: Traffic Topology Scene Graph for Topology Reasoning in Autonomous Driving

CVPR 2025 / Topology

*(日本語要約は未生成。`paper-digest summarize` を実行してください)*

- Paper: https://arxiv.org/abs/2411.18894
- Code: https://github.com/MICLAB-BUPT/T2SG
