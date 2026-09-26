# 論文ダイジェスト

生成日時: 2026-09-26 13:51 / 収録 184 件

## トピック

- [Occupancy](#occupancy) — 55 件
- [HD Map](#hd-map) — 36 件
- [3D Detection](#3d-detection) — 29 件
- [AD Perception](#ad-perception) — 20 件
- [Gaussian Splatting](#gaussian-splatting) — 14 件
- [World Model](#world-model) — 11 件
- [Scene Understanding](#scene-understanding) — 5 件
- [Reconstruction](#reconstruction) — 4 件
- [Occupancy Forecasting](#occupancy-forecasting) — 3 件
- [Open-world](#open-world) — 3 件
- [Topology](#topology) — 3 件
- [Map Update](#map-update) — 1 件

## Occupancy

### OccAnyScene: Towards Unified Indoor-Outdoor 3D Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

既存の3D semantic occupancy手法が屋内/屋外など固定シーンタイプ・固定プロトコルに特化している問題に対し、単一モデルでカメラ構成・空間範囲・voxel仕様・セマンティック分類が異なる屋内外シーンを横断的に扱うCross-Scene 3D Semantic Occupancy Predictionという新タスクを提案する。課題は、カメラ設定やシーン規模が変わっても計量的に一貫しつつシーンに適応できるimage-to-3D liftingを実現することである。

**新規性**

事前学習済みdepth foundation modelを基盤に、pixel-frustum中心のGaussian表現を用い、画素ごとのカメラ姿勢を考慮したfrustum queryを構築し、予測深度とfrustum幾何で位置・サイズを制約したGaussianへデコードすることで、シーンごとの再学習なしにスケール適応を実現する点が従来のシーン固有occupancy手法と異なる。

**読む理由**

屋内外を統一的に扱うoccupancy表現の設計思想は、複数センサ構成やドメインをまたぐ自動運転向けoccupancy予測の汎化性・再利用性を考える上で参考になる。

- Paper: https://arxiv.org/abs/2608.08696
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

**概要**

マルチビュー画像からのカメラのみ3D semantic occupancy predictionにおいて、レイ上に複数の占有面が存在する遮蔽状況をどう表現するかを課題としている。従来の単一深度仮説に基づくレイモデリングでは複雑な遮蔽下での体積的なシーンを表現しづらいとし、レイを多ラベル存在問題として再定式化するRayOccを提案する。レイ上の非正規化Gaussian混合強度を推定し、Poissonイベント形式で区間ごとの占有確率に変換することで、深度方向に競合させずに複数の占有仮説を共存させる。推定した混合成分をsparse 3D Gaussianの初期化に用い、ラスタライズしてsemantic occupancyを出力する。

**新規性**

単一の支配的深度仮説を選ぶ従来手法と異なり、レイ上の占有をGaussian混合強度とPoissonイベント形式で表現し複数深度の同時占有を許容する点、およびその混合成分をGaussian Splattingの初期化に直結させている点が新規性。

**読む理由**

occupancy predictionにおける遮蔽・深度多義性の扱いはBEV/occupancy系AD認識の中心課題であり、Gaussian Splattingベースoccupancy手法のSOTAとしてレイ表現設計の参考になる。

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

**概要**

複数車両が3D semantic occupancyの認識結果を共有する協調認識において、通信量と認識性能のトレードオフを解決する手法を提案している。既存手法は3D特徴を2Dに圧縮して空間情報を失うか、密な3D表現をそのまま送って通信負荷が大きいという課題があった。本研究ではシーンのスパース性を利用したベクトル量子化により情報量の多い領域だけを圧縮して伝送するVQSOPフレームワークを構築している。

**新規性**

3D特有のスパース性を活用したSparse-Aware Vector Quantizationで空間情報を保持したまま圧縮し、局所的な高周波情報と広域的な文脈情報を融合するDual-Branch Adaptive Spatial Refinementモジュールを組み合わせている点が従来の2D圧縮・密3D伝送手法と異なる。

**読む理由**

協調認識におけるoccupancy表現の伝送効率化は、複数車両・インフラ間でのマップ更新や環境認識の実運用化に直結する課題であり、通信量82倍削減という具体的な効果が動向把握に有用である。

- Paper: https://arxiv.org/abs/2607.01928
- Code: -

### Semantic Occupancy Prediction with Dual Range-Voxel Representation

arXiv 2026 / Occupancy

**概要**

LiDARベースの3D semantic occupancy predictionでは、点群のスパース性・不完全性を補うために複数スイープを重ねる手法が一般的だが、計算コストの増加や自己位置推定誤差によるノイズが実用上の課題となる。本論文は単一スイープの点群だけを使い、range viewから得られる文脈情報とvoxel viewの幾何情報を組み合わせるDual Range-Voxel Representation (DRVR)を提案している。range-view encoderでコンパクトな文脈特徴を、幾何を考慮したvoxel-view encoderでマルチスケールの空間特徴を抽出し、両者をvoxel-to-range / range-to-voxelの双方向融合で統合する。nuScenes-Occupancy、SemanticKITTI、SemanticPOSSで評価し、nuScenes-Occupancyでは多スイープ手法に対しmIoU +5.4%、2.1倍の高速化を報告している。

**新規性**

multi-sweepの積み上げに頼らず、単一スイープのrange viewとvoxel viewという2つの表現を双方向に融合することで密な空間情報を補う点が従来手法との違いである。これにより多スイープ由来の計算負荷とpose変換ノイズの問題を回避している。

**読む理由**

occupancy予測における入力表現の設計（range view と voxel view の使い分けと融合）という観点で参考になり、単一スイープでの精度と効率の両立は車載でのリアルタイム環境認識を考えるうえで示唆がある。

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

**概要**

カメラ画像からの3D semantic occupancy予測において、2Dから3Dへの特徴射影(lifting)以降の処理(offset学習・attention・cross-camera統合)が幾何情報を無視している問題に着目。VGGT-Occは幾何トークンをパイプライン全体に埋め込み、Projection-Aware Deformable Attention(PA-DA)で3DオフセットをImage平面へ再射影し、射影ヤコビアンをバイアスとして不確かな観測を抑制する。さらにview-quality semantic gateでcross-view統合を行い、coarse-to-fineのデコーダで解像度ごとに計算量を配分する。

**新規性**

従来手法が初期射影のみに幾何拘束を用いるのに対し、attentionやcross-view統合など後段の処理にも射影ヤコビアンによる幾何情報を継続的に注入する点が異なる。

**読む理由**

occupancy予測における2D-3D lifting後の幾何情報活用という設計上の盲点を扱っており、cameraベースoccupancyモデルの精度・効率改善の方向性として参考になる。

- Paper: https://arxiv.org/abs/2605.16911
- Code: -

### WeatherOcc3D: VLM-Assisted Adverse Weather Aware 3D Semantic Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

悪天候下でカメラとLiDARの信頼性が変動する問題に対し、CLIPの潜在空間を用いてテキスト由来の環境情報でセンサ融合比率を動的に制御する3D semantic occupancy予測手法を提案している。視界と照度という2軸で環境不確実性を分解し、アダプタとゲーティング機構でセンサ特徴とテキスト埋め込みを整合させる。

**新規性**

従来の静的な融合戦略と異なり、VLM(CLIP)由来の言語的な天候・照度キューを用いて、昼夜・降雨などの条件に応じカメラとLiDARの寄与度を適応的に切り替える点が新しい。

**読む理由**

悪天候・低照度といった実運用上の課題に対するセンサ融合のロバスト化手法であり、occupancy predictionの実用化に向けた知見として参考になる。

- Paper: https://arxiv.org/abs/2605.16127
- Code: -

### ProOOD: Prototype-Guided Out-of-Distribution 3D Occupancy Prediction

CVPR 2026 / Occupancy

**概要**

自動運転の3D semantic occupancy predictionにおいて、long-tailなクラス分布とOOD入力への脆弱性を課題として扱っている。既存手法は未知物体を稀少クラスに過信して割り当ててしまうため、本論文はプロトタイプを用いた特徴の補完・稀少クラス表現の強化と、学習不要のOODスコアリングを組み合わせたProOODを提案する。遮蔽領域をクラス一貫性のある特徴で埋めるsemantic imputation、tail miningによる稀少クラス強化、局所logitの整合性とプロトタイプ照合を融合したEchoOODの3要素からなる。5つのデータセットでin-distributionのoccupancy予測とOOD検出の双方を評価している。

**新規性**

occupancy予測の精度向上とOOD検出を別々に扱うのではなく、プロトタイプによる稀少クラス表現の強化がOODの誤吸収を抑えるという観点で両者を結び付けた点が特徴。さらにEchoOODは追加学習を必要とせず、既存モデルにplug-and-playで組み込めるvoxel単位のOODスコアを与える。

**読む理由**

occupancy予測を安全性の観点から評価する流れ(未知物体の扱い、予測の校正)は今後の環境認識研究で重要度が増しており、その具体的なアプローチとベンチマーク設定を把握できる。plug-and-play設計のため既存のoccupancyパイプラインへの適用可能性という点でも参考になる。

- Paper: https://arxiv.org/abs/2604.01081
- Code: https://github.com/7uHeng/ProOOD

### Gau-Occ: Geometry-Completed Gaussians for Multi-Modal 3D Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

3D semantic occupancy predictionを、高コストな稠密voxel/BEVテンソルではなくコンパクトな3D Gaussian集合としてモデル化するマルチモーダル手法Gau-Occを提案。LiDAR Completion Diffuserでスパースな点群から欠損構造を補完しGaussian anchorを初期化し、Gaussian Anchor Fusionで多視点画像の意味情報を幾何整合的にサンプリングして統合する。

**新規性**

稠密な3D/BEVボクセル表現に依存せず、幾何補完済みの疎なGaussian表現で計算コストを抑えつつマルチモーダル融合を実現する点が従来手法との違い。

**読む理由**

occupancy predictionにおけるGaussian Splatting的表現とマルチモーダル融合設計の最新動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2603.22852
- Code: -

### DriveTok: 3D Driving Scene Tokenization for Unified Multi-View Reconstruction and Understanding

arXiv 2026 / Occupancy

**概要**

自動運転のマルチビュー高解像度画像に対応するシーントークナイザDriveTokを提案。視覚基盤モデルの特徴を3D deformable cross-attentionでシーントークンに変換し、マルチビュートランスフォーマーでRGB・深度・セマンティクスを再構成しつつ、3D占有予測ヘッドも備える。単視点向けトークナイザではマルチビュー間の非効率・不整合が生じる課題に対応する。

**新規性**

既存の2D/単眼向けトークナイザと異なり、3D空間上のシーントークンを介してマルチビュー一貫性を確保し、再構成と3D占有予測を同一トークン表現で統一的に学習する点が特徴。

**読む理由**

world model・VLA向けの視覚トークナイザ設計は今後のBEV/occupancy研究の基盤要素になりうるため、マルチビュー統一表現の設計動向として参照価値が高い。

- Paper: https://arxiv.org/abs/2603.19219
- Code: https://github.com/paryi555/DriveTok

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

**概要**

悪天候・悪照明下でも頑健な3D semantic occupancy predictionを目指し、4D radarとカメラを融合する手法を提案。radarのrange/velocity/angle情報とカメラの意味的・テクスチャ情報を組み合わせ、カメラ由来の深度手がかりで2D画像を3Dへリフトしてシーン再構成精度を高める。学習用に手動アノテーション負荷を減らす自動ラベリングデータセットも構築している。

**新規性**

カメラ単体やLiDAR融合が主流だったoccupancy predictionに対し、4D radarとカメラの組み合わせを初めて適用し、悪条件下での頑健性を狙っている点が新規性。

**読む理由**

悪天候耐性のあるセンサ融合によるoccupancy推定は、実運用を見据えた環境認識の頑健性向上という重要な研究方向を示している。

- Paper: https://arxiv.org/abs/2603.07794
- Code: -

### Can we Trust Unreliable Voxels? Exploring 3D Semantic Occupancy Prediction under Label Noise

IROS 2026 / Occupancy

**概要**

実世界の3D occupancyアノテーションには構造的アーチファクトや動的物体のトレイリングノイズが混入するため、これに頑健な学習手法を提案している。まずOccNLというラベルノイズ環境での3D occupancy評価ベンチマークを構築し、既存の2Dラベルノイズ対策が疎な3Dボクセル空間では破綻することを示した。続いてDPR-Occという、時間方向のモデル記憶と特徴表現レベルの構造的類似性を組み合わせて信頼できる候補ラベル集合を動的に拡張・剪定するフレームワークを提案している。

**新規性**

2D画像向けのラベルノイズ学習手法をそのまま3D疎ボクセル空間に適用すると性能が崩壊する点を明らかにし、時間的一貫性と構造的近さの両方を使う3D特化の部分ラベル推論という新しい枠組みを導入した点が従来と異なる。

**読む理由**

occupancy予測の教師データ品質問題は実運用でのアノテーションコストや自動生成ラベルの誤りと直結するため、頑健な学習手法の動向を追ううえで参考になる。

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

**概要**

カメラとLiDARを融合して3D semantic occupancyを予測する手法TFusionOccを提案。ボクセル表現の空領域計算冗長性と既存のobject-centric Gaussian primitiveの表現力不足という2つの課題を、Studentのt分布に基づく新しいT-primitive（変形可能なT-Superquadricを含む）で解決する。occupancyとsemanticsを統一的に扱うT-mixture modelと、多段階のカメラ・LiDAR融合アーキテクチャを設計している。

**新規性**

従来のvoxelベースやGaussian primitiveベースの表現に代えて、非凸・非対称な形状も表現できるStudent t分布ベースのT-Superquadric（変形・逆ワーピング付き)を導入し、occupancyとsemanticsを単一の確率モデルで扱う点が新しい。

**読む理由**

object-centricなprimitive表現によるoccupancy予測は近年のBEV/occupancy研究の主要な方向性の一つであり、nuScenes-Cでの頑健性評価も含め、マルチセンサ融合設計の参考になる。

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

**概要**

自動運転における3Dセマンティックオキュパンシー予測を、カメラとLiDARのマルチモーダル入力から軽量なGaussianベース表現で行う手法を提案している。既存のvoxel化手法が計算コスト過大かつ動的環境下での融合が脆弱である点を課題とし、深度特徴集約・エントロピーによるノイズ平滑化・適応的なセンサ融合・Mamba型ヘッドによる文脈デコードの4要素で解決する。

**新規性**

静的な融合に依存する従来のvoxelベース手法と異なり、3D Gaussian表現とモデル出力に基づく動的なカメラ-LiDAR再較正、線形計算量のSelective State Space Model(Gauss-Mamba)ヘッドを組み合わせている。

**読む理由**

occupancy予測におけるマルチモーダル融合の効率化と動的環境への頑健性という、地図生成・環境認識分野の実用上の課題に対する具体的アプローチを示している。

- Paper: https://arxiv.org/abs/2601.14448
- Code: -

### SUG-Occ: Explicit Semantics and Uncertainty Guided Sparse Learning for Efficient 3D Occupancy Prediction

arXiv 2026 / Occupancy

**概要**

voxel単位で意味と幾何を表す3D semantic occupancy predictionは自動運転の認識に有用な一方、大規模シーンでは計算量が膨大でリアルタイム実装が難しい。本論文は、シーンが本質的に疎であることを利用し、semantic priorとuncertainty priorでfree spaceからの画像特徴投影を抑えつつ、unsigned distanceの明示的エンコードで幾何的整合性を保った疎な表現を構築する。その上で、hyper cross sparse convolution・generative upsampling・adaptive pruningを組み合わせたcascade sparse completionモジュールでcoarse-to-fineに補完し、最後にOCRベースのmask decoderで軽量なquery-context相互作用によりvoxel予測を精緻化する。SemanticKITTIとOcc3D-nuScenesで精度と効率の双方の改善を報告している。

**新規性**

密なvolumetric特徴に対する高コストなattentionに頼らず、semanticとuncertaintyという明示的なpriorで疎化の対象を決めたうえで、cascade型のsparse completionとOCRベースのmask decoderを組み合わせた点が従来の疎化手法と異なる。

**読む理由**

occupancy predictionの実用化で最大の障壁である計算コストに対し、疎性の使い方を priorベースで設計する具体例として参考になる。BEV/occupancy系の効率化アーキテクチャの動向を追ううえで押さえておきたい一本。

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

**概要**

既存のvision-based 3D occupancy predictionはモジュール構成で個別最適化されるため誤差が伝播しやすい。本研究は2D-to-3Dのgradient伝播を規定するcausal lossを導入し、パイプライン全体をエンドツーエンドで微分可能にする。これに基づきChannel-Grouped Lifting、Learnable Camera Offsets、Normalized Convolutionから成る変換手法を提案する。

**新規性**

モジュール個別最適化ではなく、2D-to-3D semantic causalityの原理に基づくcausal lossで全体を統一的に学習可能にした点が従来手法と異なる。

**読む理由**

occupancy予測におけるカメラ外乱へのロバスト性と2D-3D間の意味的整合性を扱っており、モジュール型パイプラインの誤差伝播問題への対処法として参考になる。

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

**概要**

3D semantic occupancy predictionにおいて、従来の密なグリッド表現ではなくsemanticな3D Gaussiansを用い、カメラ・LiDAR・レーダーを統合するマルチモーダルセンサフュージョン手法GaussianFusionOccを提案している。modality-agnosticなdeformable attentionで各センサから特徴を抽出しGaussianの属性を洗練することで、精度とスケーラビリティを両立している。

**新規性**

密なvoxelグリッドではなくGaussian表現を採用することでメモリ効率と推論速度を改善しつつ、複数センサの組み合わせに柔軟に対応できるmodality-agnosticな融合機構を導入している点が従来手法との違い。

**読む理由**

occupancy predictionにおけるGaussian表現とマルチモーダルセンサフュージョンの統合設計は、効率的な3D環境認識手法の動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2507.18522
- Code: -

### From Binary to Semantic: Utilizing Large-Scale Binary Occupancy Data for 3D Semantic Occupancy Prediction

ICCV 2025 / Occupancy

**概要**

vision-centricな自動運転における3D semantic occupancy予測は、ボクセルごとの意味ラベル付けにLiDAR点群アノテーションが必要でコストが高い一方、占有/空きのみを示すbinary occupancyデータは安価に大量取得できる。本研究はこのbinary occupancyデータをpre-training用途と学習ベースauto-labeling用途の両面から活用する方法を検討し、予測プロセスをbinaryモジュールとsemanticモジュールに分解する新フレームワークを提案する。

**新規性**

semantic labelを持たない大規模binary occupancyデータの活用余地に着目し、予測をbinary/semanticの2段階に分解することで既存手法にはなかった安価なデータソースの有効利用を実現した点が新しい。

**読む理由**

semantic occupancy予測のアノテーションコスト問題に対し、安価なbinaryデータの転用という現実的な解決策を示しており、occupancy系タスクのデータ効率化を追ううえで参考になる。

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

**概要**

カメラ画像からシーンの幾何形状と意味ラベルを同時に推定するsemantic occupancy predictionにおいて、従来手法が全カテゴリを均等に扱い局所特徴に依存するため動的な前景物体の予測精度が低いという課題を扱っている。提案手法OC-SOPは検出ブランチから得たobject-centricな高次特徴をoccupancy予測パイプラインに統合することでこれを解決する。

**新規性**

物体検出由来のobject-centric情報を明示的に注入することで、局所特徴中心の従来手法に比べ前景の動的物体の予測を強化している点が新規性である。

**読む理由**

occupancy予測における前景/動的物体への対処は自動運転の実用上重要な課題であり、検出情報との統合アプローチは今後の手法設計の参考になる。

- Paper: https://arxiv.org/abs/2506.18798
- Code: -

### A Synthetic Benchmark for Collaborative 3D Semantic Occupancy Prediction in V2X-Enabled Autonomous Driving

arXiv 2025 / Occupancy

**概要**

単一車両視点ではオクルージョンやセンサ範囲の制約により3D semantic occupancy predictionの精度が限られる問題に対し、複数エージェント間で情報を共有する協調認識で補うアプローチを提案。専用データセットが存在しないという課題に対し、CARLA上に高解像度のsemantic voxelセンサを設計してdenseな注釈を生成し、エージェント間特徴を空間整合とattentionで融合するベースラインモデルも構築した。予測範囲を変えた複数のベンチマークで、範囲拡大に伴い協調認識の効果が大きくなることを示している。

**新規性**

単体車両向けoccupancy predictionの研究が中心だった中で、V2X型の協調3D semantic occupancy predictionに特化した合成ベンチマーク・データセットと、それに対応するattentionベースの特徴融合ベースラインを新たに提示した点が従来と異なる。

**読む理由**

occupancy predictionを単一車両からマルチエージェント協調へ拡張する際の評価基盤・ベースライン設計を把握でき、V2X前提の環境認識研究の動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2506.17004
- Code: https://github.com/tlab-wide/Co3SOP

### GraphGSOcc: Semantic-Geometric Graph Transformer with Dynamic-Static Decoupling for 3D Gaussian Splatting-based Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

自動運転の3D semantic occupancy predictionを3D Gaussian Splattingで行う手法。既存の3DGSベース手法が、カテゴリ間・領域間の意味的な相関を無視した一様な特徴集約をしている点、MLPによる反復最適化に幾何的制約がなく境界が曖昧になる点、動的物体と静的シーンを結合したまま最適化することで偏りが生じる点を課題として挙げている。これに対し、幾何グラフと意味グラフの二重構造を動的に構築するDual Gaussians Graph Attentionと、動的・静的を分離して最適化するattention機構を組み合わせたGraphGSOccを提案する。SurroundOcc-nuScenes、Occ3D-nuScenes、OpenOcc、KITTIの各occupancyベンチマークでstate-of-the-artを主張している。

**新規性**

Gaussianのポーズに応じてKNNの探索半径を適応的に変える幾何グラフと、cosine類似度で上位M個のノードを残す意味グラフを併用し、さらに階層ごとに粒度の異なるattentionで境界詳細とobject-level topologyを分けて扱う点が従来の一様な特徴集約と異なる。加えて、semantic probability distributionを用いて動的物体と静的シーンの最適化を明示的に切り離している。

**読む理由**

3DGS表現をoccupancy predictionに使う流れの中で、Gaussian間の関係をグラフとして構造化する設計を示しており、表現の効率と精度を両立させる方向性の参考になる。SurroundOccでmIoU 25.20%、GPUメモリ6.8GBとGaussianWorld比で精度・メモリ双方の改善を報告している点も、実装コストを見るうえで有用。

- Paper: https://arxiv.org/abs/2506.14825
- Code: -

### QuadricFormer: Scene as Superquadrics for 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

自動運転向けの 3D semantic occupancy prediction において、dense voxel 表現は走行シーンの疎性を無視して非効率であり、近年の sparse Gaussian による object-centric 表現も楕円体という形状事前分布のため、直方体・円柱・不規則形状といった多様な物体形状を表すには大量のプリミティブを密に敷き詰める必要があるという課題を扱う。本論文は形状表現力の高い superquadrics をシーンプリミティブとして採用し、各 superquadric を幾何事前を持つ occupancy 確率分布と解釈する probabilistic superquadric mixture model を構成して、混合により semantics を算出する。これを組み込んだ QuadricFormer に、occupied 領域へプリミティブを集約する pruning-and-splitting モジュールを導入する。nuScenes での実験で、効率を保ちながら state-of-the-art の性能を達成したと報告している。

**新規性**

Gaussian(楕円体)ベースの sparse なシーン表現を superquadrics に置き換え、形状の多様性によって少数のプリミティブで複雑な構造を表現できる点が従来との違いである。さらに superquadric を occupancy の確率分布として扱う mixture model と、pruning-and-splitting による配置最適化を組み合わせている。

**読む理由**

occupancy prediction の表現がボクセルから Gaussian、さらに superquadric へと「プリミティブの選び方」で効率と表現力を competing させる流れを示す一例であり、環境認識のシーン表現設計を追う上で参考になる。地図生成・occupancy 系のスパース表現を検討する際の設計選択肢として押さえておく価値がある。

- Paper: https://arxiv.org/abs/2506.10977
- Code: -

### VoxDet: Rethinking 3D Semantic Occupancy Prediction as Dense Object Detection

arXiv 2025 / Occupancy

**概要**

3D semantic occupancy predictionを、従来のvoxelごとの独立分類(dense segmentation)ではなくインスタンス中心の物体検出タスクとして再定式化した研究。voxelクラスラベルからインスタンスレベルのオフセットラベルを無学習で生成するVoxNTを提案し、それを用いてVoxDetという枠組みでオフセット回帰とセマンティック予測を分離して解く。カメラ・LiDAR双方の入力に適用可能で、SemanticKITTIベンチマークでSOTA性能を達成している。

**新規性**

voxelレベルの分類のみに頼る従来手法がインスタンスの不完全性や隣接曖昧性を生む問題に対し、voxelラベルからインスタンス境界へのオフセットを学習させて検出タスクとして扱う点が新しい。

**読む理由**

occupancy predictionをdense segmentationではなくdetectionとして捉え直すアプローチは、インスタンス粒度の一貫性が求められるシーン理解や下流の物体追跡・地図生成タスクへの応用可能性がある。

- Paper: https://arxiv.org/abs/2506.04623
- Code: -

### DSOcc: Leveraging Depth Awareness and Semantic Aid to Boost Camera-Based 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

カメラ画像のみから3D semantic occupancyを推定する研究。従来手法はvoxelが占有されているか否か(occupancy state)を明示的に推論するため、特徴量の割り当て誤りが多く発生し、またサンプル不足によりクラス推論の学習も不十分だという課題を挙げている。DSOccでは、学習を伴わない方法で算出したsoft occupancy confidenceを画像特徴に掛け合わせることでvoxelに深度の情報を持たせ、occupancy stateを暗黙的・適応的に扱いながらクラス推論と同時に解く。さらに、学習済みの画像semantic segmentationの結果をoccupancy確率とともに複数フレーム分融合し、クラス推論を補助する。

**新規性**

occupancy stateを明示的に判定せず、非学習的に求めたsoft confidenceを介して暗黙的に扱う点と、特徴学習を強化するのではなく既存の学習済みsemantic segmentationを多フレーム融合して直接活用する点が従来と異なる。

**読む理由**

カメラのみのoccupancy predictionにおいて、深度手がかりと既存2D認識器をどう組み合わせて精度を底上げするかの一例であり、SemanticKITTI・SSCBench-KITTI-360・Occ3D-nuScenesという主要ベンチマークでの比較も示されているため、occupancy系手法の設計動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2505.20951
- Code: -

### OccLE: Label-Efficient 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

自動運転の3D semantic occupancy predictionでは、full supervisionはvoxel単位の高コストなアノテーションを必要とし、self-supervisionは指導信号が弱く性能が伸びないという二択の問題がある。OccLEはこの中間を狙い、少量のvoxelアノテーションだけで高い性能を保つラベル効率の良い枠組みを提案する。semanticとgeometryの学習を分離し、semantic側は2D foundation modelの蒸留で2D/3D整合の擬似ラベルを得て、geometry側は画像とLiDARをcross-planeで統合し半教師ありで学習する。両者のfeature gridをDual Mambaで融合し、scatter-accumulated projectionで未アノテーション領域も擬似ラベルにより監督する。SemanticKITTIとOcc3D-nuScenesで、voxelアノテーション10%でも競合手法に匹敵する結果を示している。

**新規性**

full supervisionでもself-supervisionでもなく、semanticとgeometricのタスクを明示的に分離し、foundation model蒸留による擬似ラベルと半教師あり幾何学習を組み合わせてラベル依存を大幅に下げた点が従来と異なる。融合にDual Mambaを用い、未アノテーション予測にも整合した擬似ラベルで監督を与える設計も特徴。

**読む理由**

occupancy予測の実用化ではvoxelアノテーションのコストが最大のボトルネックであり、少量ラベルでどこまで到達できるかを示す本研究はデータ構築戦略を考えるうえで参考になる。2D foundation modelの蒸留とLiDAR・画像の役割分担という設計は、地図生成や環境認識の他タスクにも転用しやすい。

- Paper: https://arxiv.org/abs/2505.20617
- Code: https://github.com/NerdFNY/OccLE

### TACOcc:Target-Adaptive Cross-Modal Fusion with Volume Rendering for 3D Semantic Occupancy

arXiv 2025 / Occupancy

**概要**

マルチモーダルな3D semantic occupancy prediction において、点群と画像の特徴のスケールや分布の違いから固定的な近傍融合では対応付けが偏ってしまう問題と、疎でノイズの多いラベルしか使えないために表面の細部が失われる問題を扱っている。前者に対しては、対象のスケールに応じて探索近傍を変える双方向対称の retrieval 機構を導入し、大きな物体では近傍を広げて文脈を取り込み、小さな物体では狭めてノイズを抑える。後者に対しては、融合特徴から画像をレンダリングする 3D Gaussian Splatting ベースの volume rendering を組み込み、photometric consistency による監督で2D-3Dの整合を同時に最適化する。これらをまとめた枠組みを TACOcc として nuScenes と SemanticKITTI で評価している。

**新規性**

固定近傍でのcross-modal融合ではなくターゲットのスケールに適応して近傍幅を変える対称的な特徴対応付けを行う点、および 3D Gaussian Splatting による描画を occupancy 学習の追加監督として使い疎ラベルの不足を補う点が従来のマルチモーダル occupancy 手法との差分である。

**読む理由**

camera-LiDAR融合の occupancy 予測において、レンダリングベースの自己教師的監督をどう組み込むかという最近の流れを具体的に示す例であり、疎なアノテーション下で細部の形状精度を上げる設計指針の参考になる。

- Paper: https://arxiv.org/abs/2505.12693
- Code: -

### GaussianFormer3D: Multi-Modal Gaussian-based Semantic Occupancy Prediction with 3D Deformable Attention

arXiv 2025 / Occupancy

**概要**

自動運転や屋外ロボットの安全な走行には3D semantic occupancy predictionが重要だが、従来主流のvoxel表現はメモリ効率が悪く、カメラのみの構成では幾何精度に限界がある。本論文は3D Gaussianをシーン表現として使い、LiDARとカメラを融合するoccupancy予測フレームワークGaussianFormer3Dを提案する。LiDARから得た幾何情報でGaussianを初期化し、3D空間に持ち上げた融合特徴を用いてGaussianを反復的に更新する。on-road/off-road両方の実データセットで評価している。

**新規性**

Gaussianベースのoccupancy予測をcamera-onlyからmulti-modalへ拡張し、voxel-to-Gaussian初期化でLiDAR由来の幾何priorをGaussianに与える点が新しい。さらに2D画像平面ではなくlifted 3D空間でLiDAR-guided 3D deformable attentionを行い、融合特徴でGaussianを精緻化する。

**読む理由**

occupancy予測の表現がvoxelからGaussianなどの疎・連続表現へ移りつつある流れと、それをLiDAR融合へ広げる具体的な設計が分かる。メモリ・効率の改善を伴う点は車載実装を意識した環境認識研究として参考になる。

- Paper: https://arxiv.org/abs/2505.10685
- Code: -

### OccCylindrical: Multi-Modal Fusion with Cylindrical Representation for 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

自動運転車の3D semantic occupancy予測において、既存のマルチセンサ融合手法がCartesian座標系を使うためセンサの点分布特性を無視し細部情報が失われる問題を扱う。本研究はcylindrical座標系上でモダリティ特徴を融合・refineするOccCylindricalを提案し、より細かい幾何形状を保持する。

**新規性**

従来のCartesian座標系での融合と異なり、cylindrical座標系でマルチモーダル特徴を統合・refineすることでセンサ読み取りの分布特性を活かす点が新しい。

**読む理由**

nuScenesでの雨天・夜間を含む難条件でSOTA性能を報告しており、座標系選択がoccupancy予測の細部再現性に与える影響を知る上で参考になる。

- Paper: https://arxiv.org/abs/2505.03284
- Code: https://github.com/DanielMing123/OccCylindrical

### MS-Occ: Multi-Stage LiDAR-Camera Fusion for 3D Semantic Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

屋外走行環境の3D semantic occupancy予測において、カメラ主体の手法は幾何精度が不足し、LiDAR主体の手法は意味情報に乏しいという相補的な弱点を扱った研究。MS-Occは、特徴レベルの中間段階とvoxelレベルの後段という2つの段階でLiDARとカメラを融合するフレームワークを提案する。中間段階では疎なLiDAR depthをGaussian kernel renderingで密な幾何priorに変換して画像特徴を補強し、逆にdeformable cross-attentionでLiDAR voxelに意味情報を与える。後段ではモダリティ間のvoxel特徴を適応的に重み付けし、分類確信度の高いvoxelを基準にself-attentionで意味的な不整合を解消する。nuScenes-OpenOccupancyとSemanticKITTIで既存手法を上回る結果を報告している。

**新規性**

融合を単一段階で行う従来のマルチモーダルoccupancy手法と異なり、画像特徴とvoxel特徴の両方のレベルで双方向に補完する多段構成を採る点が特徴。特に、LiDAR depthのGaussian kernel renderingによる密な幾何prior注入と、確信度に基づくvoxel単位の意味的整合化モジュールを組み合わせている。

**読む理由**

occupancy予測におけるLiDAR-camera融合の設計をどの段階で行うべきかという論点に対する具体的な回答例であり、環境認識の融合アーキテクチャ動向を追ううえで参考になる。小物体の認識改善に言及している点も、実用的なocc手法の評価軸として押さえておく価値がある。

- Paper: https://arxiv.org/abs/2504.15888
- Code: -

### Collaborative Learning of Local 3D Occupancy Prediction and Versatile Global Occupancy Mapping

ICRA 2026 / Occupancy

**概要**

車載カメラからの3D semantic occupancy predictionは、遮蔽や低照度といった条件下では現在の観測だけでは不十分になる。本論文はLMPOccとして、過去の走行で蓄積したglobal occupancy mapをlong-term memory priorとして現在の推論に与え、同時に新しい観測でglobal mapを更新する枠組みを提案する。priorと現在特徴を適応的に統合する軽量なCurrent-Prior Fusionモジュールと、モデル非依存のprior形式を導入し、既存のoccupancy予測手法にplug-and-playで組み込めるようにしている。Occ3D-nuScenesでの評価に加え、複数車両のcrowdsourcingによる大規模global occupancy map構築と、occupancy由来のdense depthを用いた3D open-vocabulary map構築も示している。

**新規性**

単一走行・単一車両の時系列集約に留まっていた従来のoccupancy予測に対し、過去走行由来のglobal occupancy mapをpriorとして再利用しつつ継続的に更新するループを作った点が新しい。prior形式をモデル非依存に設計したことで、特定のbaselineに縛られずplug-and-playで適用できる。

**読む理由**

occupancyを「その場の予測結果」ではなく継続更新される地図資産として扱う設計であり、HD mapのmap update/クラウドソーシング更新の議論とoccupancy予測を橋渡しする事例として参考になる。occupancy由来のdepthをopen-vocabulary mapに繋げている点も、地図表現の拡張方向を追ううえで見どころがある。

- Paper: https://arxiv.org/abs/2504.13596
- Code: -

### Rethinking Temporal Fusion with a Unified Gradient Descent View for 3D Semantic Occupancy Prediction

CVPR 2025 / Occupancy

**概要**

GDFusionは、視覚ベースの3D semantic occupancy prediction(VisionOcc)における時系列融合手法。scene-level consistency、motion calibration、geometric complementationという3つの時系列的手がかりを整理し、これらをVanilla RNNの定式化をgradient descentとして再解釈することで異種表現間で統一的に融合する。

**新規性**

従来のVisionOcc手法が見落としていた3種類の時系列的手がかりを体系的に特定し、RNNの更新式を特徴量に対するgradient descentとして再解釈することで、多様な時系列情報を単一の枠組みに統合する点が新しい。

**読む理由**

occupancy predictionにおける時系列融合の設計原理を整理しており、mIoU向上とメモリ削減を両立する具体策として今後のBEV/occupancy系手法の設計に参考になる。

- Paper: https://arxiv.org/abs/2504.12959
- Code: https://github.com/cdb342/GDFusion

### AGO: Adaptive Grounding for Open World 3D Occupancy Prediction

arXiv 2025 / Occupancy

**概要**

Open-worldな3D semantic occupancy予測、つまり事前定義したクラス以外の未知物体も含めてvoxel表現を作る問題に取り組んでいる。VLMの知識を使うアプローチとして、2D pseudo-labelを従来の教師あり学習で使う方法はラベル空間に縛られ、逆に画像埋め込みへ直接アラインする方法はVLM内の画像・テキスト表現の不整合で性能が安定しない、という二つの弱点を指摘する。提案手法AGOは、サラウンド画像を3D埋め込み、クラスプロンプトをテキスト埋め込みに変換し、3D pseudo-labelを用いた類似度ベースのgrounding学習を行う。さらにmodality adapterで3D埋め込みをVLM画像埋め込みと整合する空間へ写し、モダリティ間のギャップを縮める。

**新規性**

固定ラベル空間の疑似ラベル学習とVLM埋め込みへの直接アラインのどちらにも寄らず、類似度ベースのgrounding学習とmodality adapterを組み合わせて両者の欠点を回避している点が異なる。Occ3D-nuScenesでzero-shot/few-shotの未知物体予測を改善しつつ、closed-worldの自己教師あり設定でも従来を4.09 mIoU上回ると報告している。

**読む理由**

occupancy予測をclosed-setのセマンティクスからopen-vocabularyへ拡張する流れの代表例で、VLMを3D空間表現に接続する際の実践的な設計(pseudo-labelとembedding alignmentの折り合い)が参考になる。未知物体を扱えるocc表現は地図生成や走行可能領域推定の前段としても重要。

- Paper: https://arxiv.org/abs/2504.10117
- Code: https://github.com/EdwardLeeLPZ/AGO

### Inverse++: Vision-Centric 3D Semantic Occupancy Prediction Assisted with 3D Object Detection

arXiv 2025 / Occupancy

**概要**

車載サラウンドビューカメラのみを入力として、周囲環境の幾何と意味を表す3D semantic occupancyを推定する研究。従来はサンプリングや特徴表現などモデル内部の構造改良に注力してきたが、本論文は3D object detectionを補助ブランチとして加えるマルチタスク学習で追加の3D教師信号を与えるアプローチを取る。これにより中間特徴が小さな動的物体を捉える能力が強化され、自転車・バイク・歩行者といったvulnerable road user (VRU) の表現が改善される。nuScenesで雨天・夜間を含む条件で評価し、IoU 31.73%、mIoU 20.91%を報告している。

**新規性**

occupancyネットワーク内部の構造設計を工夫する従来路線ではなく、3D detectionの補助タスクによる追加の3D監督で中間特徴自体を鍛える点が異なる。特に小さな動的物体・VRUの検出性能向上を狙いとして明示している。

**読む理由**

occupancy predictionと3D detectionをタスク統合する流れの具体例であり、安全上重要な小物体をocc表現でどう扱うかという課題設定を把握できる。雨天・夜間を含む評価設定も環境認識の頑健性を追う上で参考になる。

- Paper: https://arxiv.org/abs/2504.04732
- Code: https://github.com/DanielMing123/Inverse

### MinkOcc: Towards real-time label-efficient semantic occupancy prediction

arXiv 2025 / Occupancy

**概要**

3Dセマンティックオキュパンシー予測は密な3Dアノテーションを要し高コストであることを課題とし、少量の3Dラベルで学習を温間開始した後、蓄積LiDARスイープと画像を基盤モデルで自動意味ラベル付けした疑似supervisionで学習を継続する半教師あり手法MinkOccを提案する。カメラとLiDARを早期融合し、スパース畳み込みでリアルタイム推論を実現する。

**新規性**

手動3Dアノテーションを90%削減しつつ精度を維持する点、および視覚基盤モデルによる自動ラベリングとLiDAR蓄積を組み合わせた2段階の半教師あり学習手順が従来の全教師あり手法と異なる。

**読む理由**

ラベルコストを大幅に削減しながら実用的な精度を保つ手法は、Occupancy予測の実運用展開における重要な障壁を扱っており動向把握に有用。

- Paper: https://arxiv.org/abs/2504.02270
- Code: -

### L2COcc: Lightweight Camera-Centric Semantic Scene Completion via Distillation of LiDAR Model

arXiv 2025 / Occupancy

**概要**

自動運転の認識で重要な Semantic Scene Completion (SSC) を、カメラ中心の軽量な構成で解こうとした研究。従来手法は精度を上げるために計算量とメモリ消費の大きい 3D 演算を多用しており、学習・推論時のプラットフォーム負荷が課題だった。本論文は efficient voxel transformer (EVT) を用いた軽量なアーキテクチャに、LiDAR モデルからのクロスモーダル蒸留(feature similarity distillation、TPV distillation、prediction alignment distillation)を組み合わせ、計算負荷を抑えつつ精度を保つ枠組み L2COcc を提案している。LiDAR 入力にも対応する構成となっている。

**新規性**

重い 3D 演算に頼らず EVT で occupancy を推定しつつ、feature・TPV 表現・予測結果の3レベルで LiDAR モデルの知識をカメラモデルへ蒸留する点が従来のカメラベース SSC と異なる。結果として SemanticKITTI と SSCBench-KITTI-360 で既存の vision-based SSC を上回りつつ、メモリと推論時間を 23% 以上削減したと報告している。

**読む理由**

occupancy 推定は BEV/HD Map と並ぶ車載環境認識の中核表現であり、精度と実車搭載可能な計算コストを同時に satisfy する方向性の実例として参考になる。LiDAR から camera への蒸留はマルチモーダル前提のデータセットを活かす一般的な手法設計として、地図生成・認識の他タスクにも転用しやすい。

- Paper: https://arxiv.org/abs/2503.12369
- Code: -

### Manboformer: Learning Gaussian Representations via Spatial-temporal Attention Mechanism

arXiv 2025 / Occupancy

**概要**

3D semantic occupancy predictionにおいて、スパースな3D Gaussianでシーンを表現するGaussianFormerは省メモリだが、必要なGaussian数が密なgridベース手法のクエリ解像度より多くなり性能が劣化する問題がある。本研究は、従来のgridベースoccupancyネットワークで使われていた時間情報を活用していなかった点に着目し、Spatial-Temporal Self-attention機構を導入してGaussianFormerを拡張する。NuScenesデータセットで実験を実施中(進行中の研究)。

**新規性**

GaussianFormerに未活用だった時間軸の情報を、grid-based手法で使われるSpatial-Temporal Self-attentionとして組み込み、Gaussian表現の効率と性能のトレードオフを改善しようとする点が新しい。

**読む理由**

Gaussian SplattingベースのoccupancyネットワークとBEV/gridベース手法の時系列処理を融合する試みであり、メモリ効率と時間的一貫性を両立するoccupancy予測の設計動向を把握するうえで参考になる。

- Paper: https://arxiv.org/abs/2503.04863
- Code: -

### QueryOcc: Query-based Self-Supervision for 3D Semantic Occupancy

CVPR 2026 / Occupancy

**概要**

3Dアノテーションが高コストな中、画像やLiDARから3Dセマンティックoccupancyを自己教師ありで学習する手法QueryOccを提案。隣接フレームにまたがる4D時空間クエリを独立にサンプリングし、視覚基盤モデル由来の疑似点群または生LiDARデータから直接教師信号を得る。遠方領域を滑らかに圧縮しつつ近傍の詳細を保つ収縮型シーン表現により、一定メモリでの長距離supervisionと推論を可能にした。

**新規性**

2Dレンダリング一貫性による暗黙的な3D構造獲得や、蓄積LiDAR点群を離散ボクセル化する従来手法と異なり、連続的な3D occupancyを4Dクエリで直接学習する点が新しい。

**読む理由**

自己教師あり設定でのoccupancy予測において、カメラベース手法に対し大幅な性能向上とリアルタイム動作を両立しており、ラベルコストを抑えた環境認識手法の動向として重要。

- Paper: https://arxiv.org/abs/2511.17221
- Code: -

### Sparsity-Aware Voxel Attention and Foreground Modulation for 3D Semantic Scene Completion

CVPR 2026 / Occupancy

**概要**

単眼RGB画像から3D意味シーンを完成させるSSCタスクにおいて、ボクセルの93%以上が空でクラスも長尾分布という不均衡問題に着目。空ボクセルをダミーノード経由でスキップしつつ占有ボクセルをdeformable attentionで精緻化するDSFRモジュールと、前景クラスの過学習を抑えつつ関連特徴を強調するForeground Dropout・Text-Guided Image Filterから成るVoxSAMNetを提案している。

**新規性**

空ボクセルへの冗長な計算を避ける疎性認識設計と、テキスト誘導によるクラス関連特徴の強調を組み合わせた点が従来の均一的なボクセル処理手法と異なる。

**読む理由**

単眼カメラのみでOccupancy/SSCを高精度化する試みであり、コスト効率の良い環境認識手法としてOccupancy Prediction分野の最新動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2604.05780
- Code: -

### An Instance-Centric Panoptic Occupancy Prediction Benchmark for Autonomous Driving

CVPR 2026 / Occupancy

**概要**

自動運転向けpanoptic occupancy予測は、高品質な3Dメッシュ資源とインスタンス単位の物理的整合性のあるデータセットが不足しており進展が阻害されているとして、著者らはADMeshという15K以上の高品質3DモデルからなるCG資産ライブラリと、CARLAシミュレータで生成したインスタンス単位のoccupancy正解を持つ大規模データセットCarlaOccを構築した。あわせて既存occupancyデータセットの品質を測る標準評価指標も提案し、代表的手法のベンチマークを行っている。

**新規性**

既存ベンチマークが低解像度・インスタンス注釈欠如の不完全な幾何情報しか提供しない点に対し、0.05m解像度のインスタンス単位occupancy正解と専用3Dメッシュライブラリを組み合わせて提供する点が新しい。

**読む理由**

occupancy予測研究の評価基盤として、インスタンスレベルの精緻な正解データと標準化指標を提供しており、今後の手法比較・再現性確保の動向を追ううえで参照価値が高い。

- Paper: https://arxiv.org/abs/2603.27238
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

### GaussianFormer-2: Probabilistic Gaussian Superposition for Efficient 3D Occupancy Prediction

CVPR 2025 / Occupancy

**概要**

vision-centricな自動運転向けの3D semantic occupancy predictionにおいて、既存のdense grid表現が持つ計算冗長性と、object-centricな3D Gaussian表現でも空領域を非効率に記述してしまう問題を解く論文。各Gaussianを近傍が占有される確率分布として解釈し、確率的な重ね合わせ(multiplication)で全体形状を導出するprobabilistic Gaussian superpositionモデルを提案する。semantics計算にはexact Gaussian mixture modelを用い、Gaussian同士の不要な重複を避けている。

**新規性**

従来のGaussianベース手法が占有・非占有を決定的に扱っていたのに対し、Gaussianを確率分布として扱い確率演算で統合する点、および深度ではなくpixel-alignedなoccupancy分布を学習する初期化モジュールを導入した点が新規性。

**読む理由**

dense gridでもobject-centric Gaussianでもない、確率的Gaussian表現によるoccupancy predictionの効率化アプローチであり、GaussianFormer系列の発展として3D occupancy分野の効率化トレンドを追ううえで参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Huang_GaussianFormer-2_Probabilistic_Gaussian_Superposition_for_Efficient_3D_Occupancy_Prediction_CVPR_2025_paper.html
- Code: -

### EvOcc: Accurate Semantic Occupancy for Automated Driving Using Evidence Theory

CVPR 2025 / Occupancy

**概要**

LiDAR点群のノイズや未観測領域による不確実性を明示的にモデル化するevidential theoryベースの手法で、正解となる3D semantic occupancyマップの生成と、画像ベースoccupancy推定モデルの学習用損失関数を提案する。

**新規性**

従来のsemantic occupancyマップが不確実性を扱わないのに対し、evidence theoryにより矛盾する観測や未観測空間の不確実性を明示的に表現する点が異なる。

**読む理由**

occupancy推定の精度向上に加え、不確実性を考慮した安全な環境認識という観点で今後のoccupancy研究の方向性を示す論文である。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Kalble_EvOcc_Accurate_Semantic_Occupancy_for_Automated_Driving_Using_Evidence_Theory_CVPR_2025_paper.html
- Code: -

### ALOcc: Adaptive Lifting-Based 3D Semantic Occupancy and Cost Volume-Based Flow Predictions

ICCV 2025 / Occupancy

**概要**

ALOccは画像入力から3Dセマンティックオキュパンシーと物体のフロー(動き)を同時に予測する手法。2D特徴を3Dに持ち上げる際の遮蔽対応・深度ノイズ除去、3D-2D間の意味的整合性を取るプロトタイプ学習、BEV上でのコストボリュームによるセマンティクスとフローの明示的な相関付けという3つの改善を導入している。

**新規性**

深度事前分布への依存を抑えた遮蔽考慮型のadaptive lifting、long-tailクラス対策の信頼度・カテゴリ考慮サンプリング、分類と回帰を組み合わせたコストボリュームによる多様な運動スケールへの対応が特徴で、純畳み込みアーキテクチャで実時間性と精度を両立させている。

**読む理由**

occupancyとflowの同時予測は動的シーン理解の中核課題であり、実時間動作可能なSOTA手法として今後のベースライン比較に有用。

- Paper: https://arxiv.org/abs/2411.07725
- Code: -

## HD Map

### PseudoMapLabeler: Confidence-Aware Pseudo-Label Generation for Semi-Supervised Online Mapping

ECCV 2026 / HD Map

**概要**

オンラインHDマップ構築ではラベル付きデータの不足が汎化性能を制限する課題があり、本論文はteacher-student型の半教師あり学習で解決を図る。教師モデルをラベルデータで学習した後、時間方向の観測に対してBeta分布に基づく信頼度マップで地図要素ごとの信頼性を評価する。信頼度の低い領域だけを空間的に切り取って除去し、要素全体を捨てる従来手法より情報を多く残す。精緻化された地図をpriorとして教師モデルの予測を改善し、それを擬似ラベルとして生徒モデルを学習後、元のラベルデータでfine-tuningする。

**新規性**

要素単位で予測を採否する従来のフィルタリングと異なり、信頼度マップに基づく空間クリッピングで部分的に低信頼な領域だけを除去する点、および精緻化した予測を地図priorとして再利用する2段階構成が特徴。

**読む理由**

ラベル不足という実運用上のボトルネックに対する半教師あり学習アプローチであり、オンラインHDマップ構築の実用化に直結する知見を提供する。

- Paper: https://arxiv.org/abs/2608.12600
- Code: -

### MapTCL: Temporal Consistency Learning via Bidirectional Alignment for Vectorized HD Map Construction

IROS 2026 / HD Map

**概要**

オンラインHD Map構築において、動く物体やオクルージョンにより連続フレーム間で地図形状が幾何学的にぶれる問題を扱う。既存手法はフレームごとのGTのみで教師しており、時間的な一貫性を直接罰する損失がない点に着目し、過去フレームと現在フレームのベクトルインスタンスを双方向に対応付けて幾何・意味的な差異を補助損失として与えるMapTCLを提案する。BEV特徴を安定化するラスターマップ一貫性損失も併用し、追加の推論コストなしに既存ベースラインの精度を向上させる。

**新規性**

フレーム単位のGT教師のみに頼る従来手法と異なり、過去・現在のベクトルインスタンス間の双方向整合性(BVCL)とラスター表現での一貫性(RCL)を明示的な補助損失として導入した点が新規性。

**読む理由**

時間的ジッタの抑制はオンラインHD Map生成の実用化に直結する課題であり、プラグアンドプレイで既存手法に適用できる点で地図生成研究の動向を追ううえで有用。

- Paper: https://arxiv.org/abs/2608.05209
- Code: -

### TwinIR: Coordinated Invisible Dual-Point Attacks on Online HD Map Construction

arXiv 2026 / HD Map

**概要**

オンラインHDマップ構築モデルに対する物理的敵対攻撃を研究する論文。既存の単一境界への攻撃は反対側の視認可能な境界線が幾何的手がかりを補ってしまい効果が限定される「クロスバウンダリ補償効果」を発見し、これを打ち消すTwinIRという攻撃手法を提案している。攻撃点数を最小化しつつ周囲の補償的な幾何情報も抑制するよう最適化し、近赤外照明に対するカメラ応答をモデル化して可視光では目立たない物理的な攻撃点配置を生成する。

**新規性**

単一境界のみを狙う従来攻撃と異なり、複数境界間の幾何的補償を考慮して攻撃点配置を最適化する点、および近赤外光を利用してカメラには写るが人間の目には見えにくい攻撃を実現する点が新しい。

**読む理由**

オンラインHDマップ構築モデルの脆弱性と、実車実験も含めた計画への影響(到達不能率・危険軌道率の増加)を定量的に示しており、地図生成モデルの頑健性評価という観点で重要。

- Paper: https://arxiv.org/abs/2608.04453
- Code: -

### Driver2Map: Imitating Human Driving for Online High-Definition Map Construction

arXiv 2026 / HD Map

**概要**

カメラ画像・標準地図・衛星画像の3モダリティを統合してオンラインでHDマップを構築する手法。モダリティ間の視点・空間ずれにより既存手法が2種の情報源しか使えず整合や融合に苦労している課題に対応する。2段階アライメントでずれを補正し、カメラ姿勢を使ってBEV特徴の重み付けを行うPose-Guided BEV Fusionと、地図構造の事前知識で予測を精緻化するモジュールを組み合わせる。

**新規性**

従来の2モダリティ手法に対し3モダリティ(カメラ・SDマップ・衛星画像)を同時活用し、姿勢情報によるBEV融合とマップ構造の事前学習による精緻化を導入した点が異なる。

**読む理由**

動的遮蔽下でのHDマップ精度向上とマルチモーダル融合の設計事例として、オンラインHDマップ構築の最新動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2608.01338
- Code: -

### GaussianMap: Learning Gaussian Representation for Multi-Sensor Online HD Map Construction

arXiv 2026 / HD Map

**概要**

オンラインHDマップ構築では中間表現として固定解像度の密なBEVグリッドが使われるのが一般的だが、地図要素は空間的に疎で一方で細かい幾何精度が要求されるため、一様なBEV表現は冗長で非効率という問題がある。本論文はBEV平面上のGaussian primitiveの集合でシーンを表現するGaussianMapを提案する。各primitiveは幾何的属性と特徴ベクトルを持ち柔軟な局所領域を担うため、地図に関係する領域へ表現能力を集中的に配分できる。feed-forwardなGaussian encoderがGaussian同士の相互作用モデリングとマルチセンサ特徴集約を通じてprimitiveを段階的に精緻化し、それをsplattingしてBEV特徴マップに変換した後、ベクタマップとしてデコードする。

**新規性**

密な一様BEVグリッドの代わりに、適応的に配置されるBEV上のGaussian primitive集合を中間表現として学習し、splattingを介してベクタマップ予測につなぐ点が従来手法と異なる。カメラ単独とカメラ+LiDAR融合の双方に対応する点も特徴である。

**読む理由**

Gaussian表現をオンラインHDマップ構築の中間表現として使う流れを示す例で、BEVグリッド中心だった地図生成の設計が疎・適応的な表現へ移行しうることを確認できる。nuScenesとArgoverse 2でcamera-onlyおよびcamera-LiDAR fusion設定のstate-of-the-artを報告しており、ベンチマーク動向の把握にも有用である。

- Paper: https://arxiv.org/abs/2606.31177
- Code: -

### AerialFusionMapNet: Online HD Map Construction with Aerial-Onboard BEV Fusion

arXiv 2026 / HD Map

**概要**

航空画像とオンボードセンサのBEV特徴を融合してオンラインHDマップを構築する手法。従来の航空-オンボード融合は航空特徴の構造情報を十分に活かせていない点を課題とし、2段階の学習戦略で航空特徴の寄与を明示的に強化するAerialFusionMapNetを提案する。nuScenesのgeographic splitで最大54.7 mAPを達成し、既存の航空-オンボード融合ベースライン(48.8 mAP)を上回った。

**新規性**

アーキテクチャを複雑化するのではなく、構造化された2段階学習スキームによって航空画像の構造的事前情報をより効果的に統合する点が従来手法との違い。

**読む理由**

航空画像という補助モダリティをオンラインHDマップ構築にどう組み込むかという設計判断(モデル構造 vs 学習戦略)に示唆があり、マルチモーダル地図生成の研究動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2606.24784
- Code: https://github.com/DriverlessMobility/AerialFusionMapNet

### D2HDMap: Non-visible Driveline Map Prior for Online Vectorized HD Map Prediction

arXiv 2026 / HD Map

**概要**

自動運転車が使う道路構造(車線境界・道路境界・横断歩道)のオンライン推定に、車両が実際に走行した経路(driveline)という軽量な非可視priorを注入する手法D2HDMapを提案。フルHDマップpriorに比べ作成・更新コストが低い点を利点とし、nuScenesとArgoverse 2で評価している。地理的に分離した(未知の地域を想定した)split上で、priorがある場合とない場合の双方で性能を検証している。

**新規性**

従来の地図prior手法は完成済みのHDマップそのものを入力とするのに対し、本手法は視認できない走行経路情報のみを軽量priorとして与え、さらにprior無し推論時にも性能が落ちにくいよう学習する点、および位置推定誤差を模したnoise-aware trainingでロバスト性を高める点が異なる。

**読む理由**

HDマップ維持コストとオンラインマッピングの限界という地図生成研究の中心的課題に対し、低コストなprior設計と汎化性の両立を示す事例であり、map priorアプローチの設計選択を比較検討する上で参考になる。

- Paper: https://arxiv.org/abs/2606.20725
- Code: -

### HRDX: A Large-Scale Vector HD-Map Dataset

arXiv 2026 / HD Map

**概要**

既存の公開HD地図データセットが規模・属性の豊富さ・モダリティの点で不十分であることを課題とし、6台のサラウンドカメラ・128chLiDAR・RTK GNSS/IMUに加え高精度航空写真を組み合わせた約1,400km・40時間規模のvector HD-mapデータセットHRDXを提案している。10クラスの地図要素と20以上の意味的・トポロジカルな属性を付与し、幾何精度と属性正解性を統合評価するComposite Score (CS)も導入している。

**新規性**

従来データセットにない航空オルソ画像を精密に位置合わせして提供し、学習時・推論時の補助情報として活用できる点、および属性を含めた評価指標CSを新たに定義した点が特徴。

**読む理由**

オンラインHD地図構築のスケール依存性や、航空写真を特権情報として使うteacher-student転移など、地図生成研究の今後のベンチマーク設計に直結する知見を含む。

- Paper: https://arxiv.org/abs/2606.17080
- Code: https://github.com/honda-research-institute/HRDX

### The Road Ahead in Autonomous Driving: The KITScenes Multimodal Dataset

arXiv 2026 / HD Map

**概要**

既存の自動運転データセットがセンサ精度・地図完全性・地理的多様性のいずれかで不足している課題に対し、KITScenes Multimodalという欧州都市で収録した高精度センサ・地図データセットを提示している。高解像度グローバルシャッターカメラ、400m超のロングレンジLiDAR、4Dイメージングレーダー、冗長GNSS/INSを同期させ、交通信号などの交通要素を3Dで再投影精度かつトポロジー接続情報付きで地図化した点が特徴。online HD map construction、長距離深度推定、novel view synthesis、end-to-end drivingの4つのベンチマークを新設している。

**新規性**

従来データセットに比べ地図の完全性とトポロジー情報の精度が高く、不規則な street layoutを持つ欧州都市を対象とすることで地理的多様性を拡張している点が新規性。

**読む理由**

online HD map constructionとGaussian Splattingベースのnovel view synthesisを同一データセットでベンチマーク化しており、地図生成・環境認識分野の評価基盤として動向を追う上で参照価値が高い。

- Paper: https://arxiv.org/abs/2606.02956
- Code: -

### Systematic Discovery of Semantic Attacks in Online Map Construction through Conditional Diffusion

arXiv 2026 / HD Map

**概要**

オンラインHDマップ構築モデルに対して、拡散モデルの潜在多様体上で意味的に自然な環境変動(影、濡れた路面など)を探索し、既存の敵対的防御を回避しながら車線境界の検出を破壊または偽の境界を注入するMIRAGEという攻撃フレームワークを提案している。nuScenesでの評価により、境界除去攻撃で検出の57.7%を抑制し計画軌道の96%を破壊、境界注入攻撃ではピクセル単位の攻撃(PGD, AdvPatch)が失敗する中で唯一成功することを示した。

**新規性**

従来のピクセル摂動攻撃が標準的な敵対的防御で無効化されるのに対し、拡散モデルを用いて同じ道路トポロジーを保ちながら現実的な環境変化として現れる意味レベルの攻撃を系統的に発見する点が新しい。

**読む理由**

オンラインHDマップ構築モデルの安全性・頑健性を評価する上で、既存防御が見落としている意味レベルの脆弱性を明らかにしており、地図生成モデルの信頼性評価の観点で参考になる。

- Paper: https://arxiv.org/abs/2605.14396
- Code: -

### Learning Ego-Centric BEV Representations from a Perspective-Privileged View: Cross-View Supervision for Online HD Map Construction

ECCV 2026 / HD Map

**概要**

マルチカメラ入力からのオンラインHDマップ構築において、自車視点のみの教師信号では遠方や遮蔽領域で構造推論が不安定になる課題に対し、俯瞰(overhead)画像から幾何・トポロジ的な事前知識をBEVエンコーダに転移するCross-View Supervision (CVS)を提案する。推論時はカメラ画像のみを使用し、俯瞰入力は学習時のみ利用する。

**新規性**

補助的な意味論的損失を追加するのではなく、BEV特徴空間上で自車視点モデルと俯瞰視点の教師モデルの表現を直接整合させる蒸留的アプローチをとる点が既存手法と異なる。

**読む理由**

推論アーキテクチャや入力を変えずに遠方領域のHDマップ精度を大きく改善する学習パラダイムであり、BEV表現学習・地図構築の性能向上手法として動向把握に有用。

- Paper: https://arxiv.org/abs/2605.12218
- Code: -

### Uncertainty Matters: Structured Probabilistic Online Mapping for Motion Prediction in Autonomous Driving

arXiv 2026 / HD Map

**概要**

オンラインでベクトルマップを推定するモデルは通常決定論的に点座標を出力し、構造的な不確実性を捨てている。本研究は各マップ要素内の点間の空間相関を捉えるため、低ランク成分と対角成分からなる共分散(LRPD)で不確実性を明示的にモデル化する確率的マッピング手法を提案する。nuScenesでの評価により、決定論的手法よりマップ生成品質が向上し、マップベースの軌道予測でも最先端性能を達成したことを示している。

**新規性**

従来の確率的マッピングが点間独立を仮定する対角共分散に限られていたのに対し、低ランク+対角分解によって計算コストを抑えつつ点間の空間相関を表現できる点が新しい。

**読む理由**

地図生成における不確実性推定は下流の予測・計画タスクの信頼性に直結するため、オンラインマッピング研究の実用化に向けた重要な方向性を示している。

- Paper: https://arxiv.org/abs/2603.20076
- Code: -

### MapGCLR: Geospatial Contrastive Learning of Representations for Online Vectorized HD Map Construction

arXiv 2026 / HD Map

**概要**

オフラインHDマップの作成・維持コストを削減するため、オンラインでベクトル化HDマップを構築するモデルを対象に、BEV特徴グリッド間の地理的一貫性をcontrastive lossとして課すことで表現学習を改善する研究。同一エリアを複数回走行(multi-traversal)したデータのオーバーラップを解析し、対応するデータセット分割を自動生成する手法も提案している。少量のラベル付き単一走行データで教師あり学習しつつ、広範な未ラベルの複数走行データで自己教師あり学習を組み合わせる半教師ありアプローチを構築している。

**新規性**

地図アノテーションのある単一走行データのみに頼らず、走行間の地理的重なりを明示的に検出してcontrastive pairを作る点が従来の教師ありオンラインHDマップ構築と異なる。

**読む理由**

アノテーションコストを抑えつつオンラインHDマップ構築の性能を上げる半教師あり手法として、地図生成分野の自己教師あり学習トレンドを把握する上で参考になる。

- Paper: https://arxiv.org/abs/2603.10688
- Code: -

### Impact of Localization Errors on Label Quality for Online HD Map Construction

arXiv 2026 / HD Map

**概要**

実運用車両のセンサデータをオンラインHDマップ構築の教師データとして使う際、GPS等の自車位置推定誤差がマップラベルを歪める問題を扱う。Ramp・Gaussian・Perlinの3種の位置誤差を人工的に付与し、Argoverse 2上でMapTRv2を学習して性能劣化を定量評価している。遠方ラベルほど誤差の影響が大きい一方、走行への寄与は小さい点を踏まえ、距離に応じた評価指標も提案する。

**新規性**

位置誤差の大きさだけでなく方位角誤差の影響を分離して評価し、角度誤差が距離とともに誤差を増幅させ位置誤差より深刻であることを示した点、ノイズ量に対する性能劣化が線形以上であることを実験的に明らかにした点が新規性。

**読む理由**

実車フリートデータを使ったオンラインHDマップ学習のスケール化には局所化精度が本質的制約になることを示しており、データ収集・アノテーション設計の指針として参考になる。

- Paper: https://arxiv.org/abs/2603.03452
- Code: -

### FlexMap: Robust HD Map Construction under Flexible Camera Configurations

arXiv 2026 / HD Map

**概要**

既存のHD Map構築手法はキャリブレーション済みマルチカメラと明示的な2D-to-BEV変換を前提とするため、カメラ視点の欠落や姿勢推定誤差に弱く、車両ごとに異なるカメラ構成のフリートに展開しづらい。FlexMapは、カメラパラメータをモデル入力とせず、幾何学的投影の代わりにcross-view 3D構造を捉えるgeometry foundation modelを用いてこの制約を取り除くベクトル化HD Mapフレームワークを提案する。空間推論と時間集約を分離するspatial-temporal enhancementモジュールと、各視点のトークンから姿勢情報なしに注意を適応させるcamera-aware decoderを組み合わせる。

**新規性**

カメラ姿勢や台数構成に依存する既存手法と異なり、幾何学基盤モデルとcamera-awareなトークン処理によって、アーキテクチャ変更や再学習なしに多様なカメラ構成・視点欠落に対応できる点が新しい。

**読む理由**

異種センサー構成のフリート展開という実運用上の課題に正面から取り組んでおり、HD Map生成のロバスト性・汎用性を高める方向性として注目に値する。

- Paper: https://arxiv.org/abs/2601.22376
- Code: -

### SatMap: Revisiting Satellite Maps as Prior for Online HD Map Construction

arXiv 2026 / HD Map

**概要**

オンボードカメラのみでは深度推定が曖昇で遮蔽の影響も受けやすく、オンラインHDマップ推定の精度が低下する。SatMapは事前に取得した衛星画像（BEV視点のレーン級のセマンティクスとテクスチャ）をグローバルプライアとして多視点カメラ観測と統合し、ベクトル化HDマップを直接予測する手法を提案する。

**新規性**

カメラ単体やカメラ・LiDAR融合とは異なり、地上走行時には利用できない広域一貫性を持つ衛星マップを外部プライアとして導入し、深度曖昧性と遮蔽問題を緩和する点が従来手法との違い。

**読む理由**

地図生成におけるオンボードセンサ以外の情報源（衛星画像）の活用例として、長距離・悪天候時のロバスト性向上のアプローチを把握するうえで参考になる。

- Paper: https://arxiv.org/abs/2601.10512
- Code: -

### AMap: Distilling Future Priors for Ahead-Aware Online HD Map Construction

arXiv 2025 / HD Map

**概要**

オンラインHDマップ構築において、既存の時間的融合手法が「空間的に後ろ向き」であり、走行済み領域の精度は向上させるが未走行の前方領域の改善に乏しいという安全上の課題を指摘。前方領域の誤差は危険な運転挙動に直結するため、AMapは未来フレームにアクセスできる教師モデルから現在フレームのみを扱う軽量な生徒モデルへ知識蒸留する「distill-from-future」パラダイムを提案する。

**新規性**

Multi-Level BEV Distillationによる空間マスキングとAsymmetric Query Adaptationモジュールにより、推論時コストをかけずに未来情報を静的クエリへ圧縮転写する点が従来の時間的融合手法と異なる。

**読む理由**

時間的融合の恩恵が前方領域に及ばないという盲点を指摘し、推論効率を保ったまま前方認識精度を上げる設計は、実運用でのHDマップ構築手法の評価軸を見直す上で参考になる。

- Paper: https://arxiv.org/abs/2512.19150
- Code: -

### SATMapTR: Satellite Image Enhanced Online HD Map Construction

arXiv 2025 / HD Map

**概要**

オンボードセンサのみに依存するHDマップ構築は、遮蔽や視野限界により入力品質が低く精度が低下する問題がある。本論文は衛星画像を補助入力として活用し、ゲート付き特徴refinementモジュールで影・遮蔽ノイズを抑えつつ地図関連特徴を抽出し、geometry-aware fusionモジュールで衛星特徴とBEV特徴をグリッド単位で整合的に融合するSATMapTRを提案する。nuScenesで既存の衛星画像併用手法を大きく上回るmAPを達成した。

**新規性**

従来の衛星画像併用手法が単純な特徴抽出・融合に留まっていたのに対し、低品質な衛星画像の雑音を適応的に除去するゲート機構と、grid-to-grid単位で位置整合を取るfusion機構を導入した点が新規性。

**読む理由**

車載視点のみでは遮蔽や範囲限界に弱いオンラインHDマップ構築を、広域かつ安定な衛星画像でどう補完・融合するかという、地図生成研究の重要な方向性を示す一例。

- Paper: https://arxiv.org/abs/2512.11319
- Code: -

### MapRF: Weakly Supervised Online HD Map Construction via NeRF-Guided Self-Training

arXiv 2025 / HD Map

**概要**

オンラインHD地図構築は従来3Dアノテーションのコストが汎化性・拡張性を妨げてきた。MapRFは2D画像ラベルのみで学習する弱教師あり手法で、地図予測条件付きのNeRFモジュールで視点整合的な3D幾何・意味の疑似ラベルを生成し、自己学習でマップネットワークを反復的に改善する。誤差蓄積を抑えるMap-to-Ray Matchingにより2Dラベル由来のカメラ光線と地図予測を整合させる。

**新規性**

3D地図アノテーションを一切使わず、NeRFで生成した疑似ラベルによる自己学習とレイマッチングで誤差蓄積を抑える点が既存の完全教師あり/弱教師あり手法との違い。

**読む理由**

HD地図構築のアノテーションコスト削減という実運用上の重要課題に対し、NeRF由来の疑似ラベル生成という具体的解法を示しており、地図生成のスケーラビリティ動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2511.19527
- Code: -

### Learning Global Representation from Queries for Vectorized HD Map Construction

arXiv 2025 / HD Map

**概要**

DETRベースのオンラインHDマップ構築手法は各クエリが独立学習されるため局所視点に偏り、マップ全体の大域的構造を捉えにくいという課題がある。本研究はMapGRを提案し、全クエリの分布を地図全体のsegmentationタスクと整合させるGlobal Representation Learning(GRL)モジュールと、各クエリに大域的な文脈情報を明示的に与えるGlobal Representation Guidance(GRG)モジュールを組み合わせて解決する。

**新規性**

個々のクエリの独立最適化に頼る従来のDETR系手法と異なり、holistic segmentationを介してクエリ集合全体を大域マップ表現に整合させ、その情報を個々のクエリの最適化に還元する点が新しい。

**読む理由**

クエリベースのベクトルHDマップ構築におけるクエリ間の大域的整合性という共通課題への対処法として、他の同系統手法にも応用可能な知見を提供する。

- Paper: https://arxiv.org/abs/2510.06969
- Code: -

### Mapping like a Skeptic: Probabilistic BEV Projection for Online HD Mapping

BMVC 2025 / HD Map

**概要**

カメラ画像からBEV空間へ道路要素を射影する際の誤差がベクトルHDマップの品質を左右するという課題に対し、カメラパラメータに基づく幾何的射影を出発点として、確信度スコア付きの確率的射影機構でシーンに適応的に補正し、無関係な要素を除去する手法を提案している。さらに確信度スコアを用いて時系列情報を選択的に蓄積することで時間方向の処理も改善している。

**新規性**

既存手法がAttentionベースの学習的射影に全面依存し汎化性能が低くハルシネーションを起こしやすいのに対し、本手法はカメラ幾何に基づく射影を起点として確信度で補正・フィルタする点が異なる。

**読む理由**

nuScenes・Argoverse2での長距離知覚における汎化性能向上を示しており、オンラインHDマップ構築の射影手法設計における参考になる。

- Paper: https://arxiv.org/abs/2508.21689
- Code: https://github.com/Fatih-Erdogan/mapping-like-skeptic

### MapKD: Unlocking Prior Knowledge with Cross-Modal Distillation for Efficient Online HD Map Construction

arXiv 2025 / HD Map

**概要**

オンラインHDマップ構築において、SD/HDマップ事前知識やLiDARなどのマルチモーダル情報を推論時に使わずに済ませたいという課題に対し、Teacher-Coach-Studentという3段階の知識蒸留フレームワークMapKDを提案している。カメラ+LiDAR+地図事前知識を持つteacherから、地図事前知識と疑似LiDARを持つcoachを経て、視覚のみの軽量studentモデルへ知識を伝達する。

**新規性**

単純な2段階蒸留ではなくcoachモデルを挟むことでモーダル間のギャップを埋め、さらにBEV特徴用のToken-Guided 2D Patch DistillationとセマンティクスガイダンスのMasked Semantic Response Distillationという2種類の蒸留手法を導入している点が新しい。

**読む理由**

オフライン地図やマルチモーダルセンサ依存を減らしつつ性能を落とさない設計は、低コストなオンラインHDマップ構築の実運用に向けた重要な方向性であり、蒸留戦略の設計は他タスクにも応用が利く。

- Paper: https://arxiv.org/abs/2508.15653
- Code: https://github.com/2004yan/MapKD2026

### An Initial Study of Bird's-Eye View Generation for Autonomous Vehicles using Cross-View Transformers

arXiv 2025 / HD Map

**概要**

自動運転シミュレータ上で、複数カメラ画像からCross-View Transformer (CVT)を用いて道路・車線区画・計画軌道の3チャンネルからなるBEVマップを推定する手法を検討している。未知の街への汎化性、カメラ配置の違い、focal損失とL1損失の比較を実験的に評価した。単一の街のデータのみで学習しても、4カメラ構成かつL1損失を用いたCVTが未知の街で最も頑健な性能を示したと報告している。

**新規性**

新規アーキテクチャの提案ではなく、既存のCVTをBEVマップ生成タスクに適用した上で、カメラ台数構成や損失関数の選択が汎化性能に与える影響を初期的に検証した点が特徴。

**読む理由**

Online HD Map生成におけるカメラ配置・損失設計といった実装選択の効果に関する初期的な知見が得られ、BEVマップ推定の基礎検討として参考になる。

- Paper: https://arxiv.org/abs/2508.12520
- Code: -

### RelMap: Enhancing Online Map Construction with Class-Aware Spatial Relation and Semantic Priors

arXiv 2025 / HD Map

**概要**

オンラインHDマップ構築において、既存のTransformer手法がマップ要素間の空間的依存関係や意味的関係を無視している点を課題とし、RelMapという手法でこれを明示的にモデル化する。クラス認識型の空間関係とMixture-of-Expertsによる意味的事前知識をエンコーダ・デコーダに組み込み、要素間の相対位置関係とクラス固有の特徴表現を強化する。

**新規性**

従来手法が見落としていたマップ要素間の空間的関係とクラスごとの意味的特性を、学習可能な関係エンコーダとMoEベースの専門家ルーティングで明示的に扱う点が新しい。

**読む理由**

マップ要素間の構造的関係をどう表現に組み込むかは、Transformerベースのオンラインマップ構築の精度向上における重要な設計軸であり、nuScenes・Argoverse 2両方でSOTAを達成している点で参照価値が高い。

- Paper: https://arxiv.org/abs/2507.21567
- Code: -

### MapDiffusion: Generative Diffusion for Vectorized Online HD Map Construction and Uncertainty Estimation in Autonomous Driving

IROS 2025 / HD Map

**概要**

オンラインHDマップ構築において、従来のクエリベース手法が単一の決定論的なベクトルマップしか出力できず、occlusionや車線標示欠損による曖昧さを表現できない点を課題とする。MapDiffusionはdiffusionモデルによりBEV潜在特徴量を条件としてクエリを反復的に精緻化し、複数の妥当なマップサンプルを生成することでマップ分布全体を学習する。nuScenesでの実験により、単一サンプルでもベースラインを上回る性能を示し、複数サンプルの集約でさらに精度が向上することを確認している。

**新規性**

決定論的な点推定ではなく、diffusionによりベクトルマップの分布そのものをモデル化し、サンプル集約による精度向上とocclusion領域に対応する不確実性推定を同時に実現する点が従来手法との違い。

**読む理由**

オンラインHDマップ構築の性能向上に加え、センサー入力が曖昧な領域を不確実性として定量化できる点は、自動運転の意思決定の安全性・信頼性を扱ううえで重要な知見となる。

- Paper: https://arxiv.org/abs/2507.21423
- Code: -

### MambaMap: Online Vectorized HD Map Construction using State Space Model

arXiv 2025 / HD Map

**概要**

オンラインでのベクトル化HDマップ構築において、時系列情報を十分に活用できない問題や長時間シーケンス処理時の計算コスト増大という課題に対し、状態空間モデル(SSM)ベースのMambaMapを提案している。メモリバンクに過去フレームの情報を蓄積し、BEV特徴とインスタンスクエリを動的に更新することでオクルージョンやノイズへの頑健性を高める。

**新規性**

状態空間モデルにゲーティング機構を導入して地図要素間の依存関係を低計算コストで選択的に統合し、さらにBEVレベル・インスタンスレベル双方で多方向・時空間スキャン戦略を組み合わせる点が既存の時系列融合手法との違いである。

**読む理由**

長時間の時系列情報融合を計算効率良く扱う手法として、オンラインHDマップ構築における時間モデリングの新しい設計選択肢を示している。

- Paper: https://arxiv.org/abs/2507.20224
- Code: https://github.com/ZiziAmy/MambaMap

### MapFM: Foundation Model-Driven HD Mapping with Multi-Task Contextual Learning

arXiv 2025 / HD Map

**概要**

自動運転向けにカメラ画像からベクトル化HDマップをオンライン生成するEnd-to-Endモデル「MapFM」を提案。強力な基盤モデルを画像エンコーダとして組み込み、特徴表現の質を高めている。さらにBEV表現上でのセマンティックセグメンテーションを補助タスクとして統合し、マルチタスク学習によりシーン理解を強化してマップ予測精度を向上させる。

**新規性**

既存のオンラインHDマップ生成手法に対し、foundation modelによる画像エンコーディングとBEVセマンティックセグメンテーションの補助ヘッドを組み合わせたマルチタスク学習で文脈情報を強化した点が新しい。

**読む理由**

foundation modelを画像エンコーダに使う設計や補助タスクによる文脈学習は、オンラインHDマップ生成の精度向上手法として今後の研究動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2506.15313
- Code: https://github.com/LIvanoff/MapFM

### SDTagNet: Leveraging Text-Annotated Navigation Maps for Online HD Map Construction

NEURIPS 2025 / HD Map

**概要**

オンラインHDマップ構築はセンサ搭載範囲に限られ遠方の精度が低いという課題に対し、容易に整備できるSD map(OpenStreetMapなど)を事前情報として活用するSDTagNetを提案。ポリラインだけでなく地図上のテキスト注釈もNLP由来特徴として取り込み、点単位のSDマップエンコーダと直交的な要素識別子で多様な地図要素を統一的に扱う。Argoverse 2とnuScenesで評価している。

**新規性**

従来のSD map priorを使う手法が手動で選んだクラスのポリラインのみを使うのに対し、テキスト注釈まで意味情報として取り込みクラス体系への依存を排した点、および点レベルのエンコーダで全種類の地図要素を統一表現した点が新規性。

**読む理由**

SDマップ事前情報を用いたオンラインHDマップ構築の性能向上手法であり、地図生成・遠方検出精度の研究動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2506.08997
- Code: https://github.com/immel-f/SDTagNet

### SuperMapNet for Long-Range and High-Accuracy Vectorized HD Map Construction

arXiv 2025 / HD Map

**概要**

自動運転向けのベクトル化HDマップ構築において、単一モダリティやカメラ・LiDARの単純結合ではBEV特徴に穴や不整合が生じる問題、点情報のみで要素間関係を無視するため形状誤りや要素混同が起きる問題を扱う。SuperMapNetはカメラとLiDAR両方を入力とし、クロスアテンションによるモダリティ融合とフロー整合により長距離BEV特徴を生成し、点クエリと要素クエリの3階層の相互作用により高精度な分類・位置推定を行う。

**新規性**

モダリティ間のシナジー強化と視差整合を行うモジュールでBEV特徴を生成する点、および点同士・要素同士・点と要素間の3種類の相互作用を明示的に設計して局所幾何情報と大域意味情報を統合する点が従来手法との違い。

**読む理由**

マルチモーダル融合とグラフ的な要素間関係モデリングを組み合わせたHDマップ構築の設計は、他のオンラインマップ生成手法の特徴融合・トポロジー推定部分にも応用可能な知見を含む。

- Paper: https://arxiv.org/abs/2505.13856
- Code: -

### SparseMeXT Unlocking the Potential of Sparse Representations for HD Map Construction

arXiv 2025 / HD Map

**概要**

オンラインHD地図構築において、計算コストの高い密なBEV表現に依存せずスパース表現で高精度を達成することを目指した論文。スパース特徴抽出に特化したネットワーク構造、スパース-デンスのセグメンテーション補助タスク、物理的事前知識に基づくデノイジングモジュールを導入し、地図構築とセンターライン検出の性能を底上げしている。

**新規性**

従来のスパース手法は専用設計の不足からデンス手法に性能で劣っていたが、本手法はアーキテクチャとアルゴリズムの両面を作り込むことでデンス手法を上回る精度を達成した点が新しい。

**読む理由**

スパース表現でもデンスBEVベースの手法を凌駕できることを示し、効率と精度のトレードオフの前提を覆す結果であるため、HD地図構築のアーキテクチャ選定の観点で重要。

- Paper: https://arxiv.org/abs/2505.08808
- Code: -

### Uni-PrevPredMap: Extending PrevPredMap to a Unified Framework of Prior-Informed Modeling for Online Vectorized HD Map Construction

arXiv 2025 / HD Map

**概要**

自動運転の地図構築において、過去の予測結果と(欠損・誤りを含む)HDマップという2種類の事前情報を統合する統一フレームワークUni-PrevPredMapを提案。マップが使えない場合と劣化したマップしかない場合の両方に対応するtri-modeパラダイムを導入し、タイル単位で索引付けした3Dベクトルグローバルマップ処理により効率的な更新・保存・検索を実現している。

**新規性**

従来手法が理想的なHDマップの存在を前提としがちなのに対し、non-prior/temporal-prior/temporal-map-fusionの3モードを単一モデルで一貫運用することでマップ有無への依存を切り離し、劣化マップと時系列予測の相補性を実証した点が新しい。

**読む理由**

オンラインHDマップ構築において事前地図情報の破損・欠損への頑健性は実運用上の重要課題であり、時系列情報と地図情報の融合設計は今後のオンラインマッピング研究の方向性を占ううえで参考になる。

- Paper: https://arxiv.org/abs/2504.06647
- Code: https://github.com/pnnnnnnn/Uni-PrevPredMap

### AugMapNet: Improving Spatial Latent Structure via BEV Grid Augmentation for Enhanced Vectorized Online HD Map Construction

WACV 2026 / HD Map

**概要**

カメラ画像群をBEV潜在空間に統合し、そこからレーンや横断歩道などの地図要素をベクトル形式で推定するオンラインHDマップ構築において、BEV潜在特徴の質を高める手法AugMapNetを提案する。従来はラスタマップ予測による密な空間教示か、ベクトルデコーダによるインスタンス単位の予測のいずれかに寄っていたが、本研究はBEV grid augmentationという新機構でこの両者を組み合わせる。nuScenesとArgoverse2でStreamMapNetベースラインに対し60mレンジで最大13.3%の性能向上を確認し、より長距離ではさらに改善する。

**新規性**

既存のハイブリッド手法より統合が容易な形で、密な空間教示とベクトルデコードを同時に活かすBEV grid augmentationという新技術を導入し、潜在空間自体をより構造化した点が従来との違い。

**読む理由**

BEV潜在表現の質がベクトルマップ精度に直結するという知見と、既存ベースラインへの転用可能性（SQD-MapNetでも効果を確認）は、HDマップ構築アーキテクチャ選定の参考になる。

- Paper: https://arxiv.org/abs/2503.13430
- Code: https://github.com/tmonnin/augmapnet

### FastMap: Fast Queries Initialization Based Vectorized HD Map Reconstruction Framework

arXiv 2025 / HD Map

**概要**

DETRベースのベクトルHDマップ再構成手法はデコーダの冗長性から6層ものデコーダ層を積む必要があり計算効率が低い。FastMapは単層・2段階のTransformerデコーダとヒートマップ誘導によるクエリ生成モジュールで、ランダム初期化に頼らず画像特徴を構造化クエリへ変換する。さらに点対点損失では区別しにくい同質的特徴に対応するため、幾何制約付きの点対線損失を導入している。

**新規性**

6層デコーダを積む代わりに単層2段階構成で多段階の表現能力を実現し、ランダムクエリ初期化をヒートマップ誘導生成に置き換えた点が従来のDETR系マップ再構成手法との違い。

**読む理由**

オンラインHDマップ推定はデコーダ層数削減によるリアルタイム性向上が課題であり、nuScenes/Argoverse2でSOTAかつ3.2倍高速というデコーダ設計は実装コスト低減の観点で参照価値が高い。

- Paper: https://arxiv.org/abs/2503.05492
- Code: https://github.com/hht1996ok/FastMap

### RAVE: End-to-end Hierarchical Visual Localization with Rasterized and Vectorized HD map

arXiv 2025 / HD Map

**概要**

自動運転の自己位置推定を、従来のルールベースな多段パイプラインではなくEnd-to-Endで解く手法RAVEを提案。周囲画像とHD mapデータを対応付けてポーズを推定する枠組みで、地図と知覚特徴のずれを補正するFLORAモジュールにより、ズレのある地図priorをBEV特徴に統合する。さらにラスタ化HD mapを用いたBEVマッチングによる粗いポーズ推定(DEMA)と、ベクトル化HD mapを用いたTransformerベースの回帰(POET)による精緻化という階層構造で、効率・解釈性・精度のバランスを取っている。

**新規性**

ラスタ化と ベクトル化という異なる表現のHD mapを、粗い推定と精緻化という役割分担で階層的に組み合わせ、地図priorのミスアラインメントを吸収する専用融合モジュール(FLORA)を導入した点が従来のルールベース・単一表現手法と異なる。

**読む理由**

HD mapを単なる地図生成対象ではなく知覚・自己位置推定の入力として活用する設計は、マップ生成と自動運転知覚の接点を考える上で参考になる。

- Paper: https://arxiv.org/abs/2503.00862
- Code: -

### OptiMVMap: Offline Vectorized Map Construction via Optimal Multi-vehicle Perspectives

CVPR 2026 / HD Map

**概要**

単一車両軌跡のみに依存する従来のオフラインベクトルマップ構築では死角領域の観測が不十分になる課題に対し、周辺車両の視点を活用するOptiMVMapを提案。Optimal Vehicle Selection (OVS)で不確実性低減に寄与する少数の補助車両を選び、Cross-Vehicle Attention (CVA)とSemantic-aware Noise Filter (SNF)でポーズ誤差や遮蔽由来のノイズを抑えつつBEV上で融合する。

**新規性**

全視点を無差別に集約する既存のメモリベース手法と異なり、不確実性を指標に少数の補助車両を選択してから融合する select-then-fuse アプローチを取ることで、計算コストと視点冗長性を抑えつつ精度を高めている。

**読む理由**

マルチエージェント視点統合によるHDマップ精度向上の方向性を示し、単一車両ベースの地図生成の限界を補う具体的な設計(選択・融合の分離)を提示している点で、地図生成研究の動向として参照価値が高い。

- Paper: https://arxiv.org/abs/2604.17135
- Code: https://github.com/DanZeDong/OptiMVMap

### Driving by the Rules: A Benchmark for Integrating Traffic Sign Regulations into Vectorized HD Map

CVPR 2025 / HD Map

**概要**

オンラインHDマップ構築が幾何・接続性層に偏り、交通標識由来の走行規則層を欠いている課題に対し、標識から抽出した規則をローカルなベクトルHDマップの車線と対応付けるデータセットMapDR(10,000本以上の動画クリップ)を構築した論文。あわせて規則統合タスクを新たに定義し、モジュール型のVLE-MEEとエンドツーエンドのRuleVLMという2種のベースライン手法を提示している。

**新規性**

従来の走行規則抽出研究が標識単体の認識に留まるのに対し、標識規則を車線単位のベクトルHDマップ要素に紐付けるタスク・データセットとして定式化した点が新しい。

**読む理由**

幾何・トポロジ中心だったオンラインHDマップ研究に交通規則層という新たな次元を加える提案であり、地図生成の実用性・法規遵守を議論する上で参照価値が高い。

- Paper: https://arxiv.org/abs/2410.23780
- Code: -

## 3D Detection

### Accuracy- and Real-Time-Aware 4D Radar Preprocessing for Autonomous Driving Perception Systems

arXiv 2026 / 3D Detection

**概要**

4Dレーダーを組み込み環境で自動運転の3D物体検出に用いる際、精度・リアルタイム性・計算量をどう両立させるかという課題に対し、レーダー点群の前処理フレームワークを提案している。パーセンタイルに基づく形状保持手法でノイズや誤検出を抑えつつ物体形状情報を残し、複数フレームのカーネル密度推定でスパースな点群の密度と信頼性を改善し、埋め込み向け適合度を評価する指標も導入している。

**新規性**

単一の精度指標だけでなく、悪天候ロバスト性・実時間性・モデル複雑度を統合したEmbedded & NetScoreで埋め込み適合性を評価する点、および複数フレーム情報を用いたKDEベースのノイズ点判別を組み合わせている点が従来手法との違い。

**読む理由**

4Dレーダーは悪天候下でも安定動作するセンサとして注目されており、組み込み実装を見据えた前処理設計は自動運転認識システムの実用化に直結する知見となる。

- Paper: https://arxiv.org/abs/2609.18542
- Code: -

### Learning from Distributed Eyes: Leveraging Collaborative Perception for Automated Model Adaptation

arXiv 2026 / 3D Detection

**概要**

自動運転の3D物体検出モデルは新環境へのドメインシフトに弱く、単一車両のデータのみに頼る教師なし適応は疑似ラベルの質が低いという課題がある。本論文はLDEという手法を提案し、複数エージェントの協調認識(CP)結果を高品質な教師信号として使うことでモデル適応を行う。通信帯域制約、CP視点と学習対象車両の視野(FoV)のずれ、CP由来ラベル自体の不確実性という3つの課題に対し、適応志向の特徴共有、FoVフィルタリング、カリキュラム学習を組み合わせて対処する。

**新規性**

自車のみのデータに依存する従来の教師なし適応と異なり、協調認識由来の疑似ラベルを教師信号として積極的に活用し、通信・視野不一致・ラベル不確実性を専用機構で解決している点が新しい。

**読む理由**

協調認識(V2X的なマルチエージェント認識)をラベル取得コスト削減や環境認識モデルの継続適応に応用する事例として、3D検出の汎化性能向上の研究動向を把握するうえで参考になる。

- Paper: https://arxiv.org/abs/2609.18511
- Code: -

### Bi-Level Routing and Sparse Spatial Attention based Multi-View BEV 3D Object Detection for Autonomous Driving

arXiv 2026 / 3D Detection

**概要**

マルチビュー画像からBEV空間で3D物体検出を行う際の計算コスト・マルチスケール特徴抽出・密な2D-to-BEV変換の効率の課題を解決するため、Sparse-BEVNetを提案する論文。バックボーンにBi-Level Routing Attention、特徴融合にCascaded Group Attentionを導入し、view transformationには密な射影の代わりにSparse Spatial Cross-Attentionを用いる。

**新規性**

従来の密なBEV view transformationパイプラインを疎な(Sparse)Spatial Cross-Attentionに置き換え、バックボーンと特徴融合部にも軽量な注意機構を組み合わせて計算負荷を抑えている点が特徴。

**読む理由**

BEVベース3D検出における計算効率化のアプローチとして、view transformationの疎化手法の実装・性能トレードオフを把握するのに参考になる。

- Paper: https://arxiv.org/abs/2609.14185
- Code: -

### NCGR: Noise-Conditional Gated Rectification for Camera Extrinsic Perturbations in BEV 3D Object Detection

arXiv 2026 / 3D Detection

**概要**

カメラのextrinsic(外部パラメータ)が実際にはずれることでBEV 3D検出のspatial cross-attentionにおける画像平面への投影がずれ、性能が劣化する問題を扱う。NCGRは6DoFの補正を陽に推定せず、query-camera対ごとに2Dの補正オフセットを予測しカメラ単位のゲートで調整することで、deformable samplingの前に投影を補正する。学習時はノイズ由来の条件量を、カメラ特徴から予測した補助スカラーに段階的に置き換えることで、推論時にはノイズのメタ情報なしで動作できるようにしている。

**新規性**

外部パラメータの完全な6DoF補正を明示的に推定するのではなく、query単位の軽量な2D補正+ゲート機構とclean-teacher/perturbed-studentのBEV一致損失で暗黙的に誤差を吸収する点が従来と異なる。

**読む理由**

実運用ではカメラの取り付け誤差やキャリブレーションずれが常に存在するため、BEV検出のロバスト性を上げる手法は地図生成・環境認識パイプライン全体の信頼性向上に直結する。

- Paper: https://arxiv.org/abs/2608.03895
- Code: -

### DeGuNet: Depth-Guided Ultra-Compact Backbones for Efficient LiDAR-Camera 3D Detection

ECCV 2026 / 3D Detection

**概要**

LiDARとカメラを融合する3D物体検出において、2D事前学習済みの巨大な画像バックボーンがLiDAR投影の疎な構造と整合しない問題を指摘し、深度情報を活用した超小型バックボーンDeGuNetを提案する。スパース性を考慮した特徴抽出により、マルチビュー画像を非構造的なLiDAR深度に整合させつつ無効領域の混入を防ぐ。nuScenesでの実験により、既存手法へのplug-and-play導入でメモリ削減と高速化、精度向上を確認している。

**新規性**

既存の汎用2D事前学習バックボーンをそのまま流用するのではなく、LiDAR深度に特化した超軽量・スパース性考慮型のバックボーンを設計し、パラメータ冗長性と構造的ミスアライメントを直接解消する点が従来と異なる。

**読む理由**

マルチモーダル3D検出における画像バックボーン設計の効率化アプローチとして、BEV型認識パイプラインの計算コスト削減の動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2607.12419
- Code: -

### Distortion-Aware PETR for BEV Object Detection with Mixed Pinhole-Fisheye Cameras

ICRA 2026 / 3D Detection

**概要**

魚眼カメラの強い放射歪みがBEV検出器の一様サンプリング前提を崩す問題に対し、pinhole/fisheye混在カメラ向けの投影フリー検出器DAPETRを提案。歪みを考慮した位置エンコーディングと、画像特徴と3D位置埋め込みを相互適応させるco-modulationモジュールを導入し、KITTI-360を魚眼用に変換したベンチマークで検証している。

**新規性**

画像の歪み補正(rectification)に頼らず、学習ベースの歪み適応(位置埋め込み・特徴の相互変調)とPolarPETRのような明示的な幾何学的再パラメータ化を比較し、両者を組み合わせると性能が悪化するという相互作用を明らかにした点が新規。

**読む理由**

低コスト・広視野のfisheyeカメラをBEV検出に活かす設計指針を示しており、マルチカメラ構成でのAD知覚・地図生成の入力品質向上を検討する上で参考になる。

- Paper: https://arxiv.org/abs/2606.08680
- Code: -

### STELLAR: Scaling 3D Perception Large Models for Autonomous Driving

arXiv 2026 / 3D Detection

**概要**

自動運転の知覚モデルにモデルスケーリングが有効かを検証した研究。Sparse Window Transformerを基盤にLiDAR・radar・camera・map priorを入力に統合したSTELLARモデルを構築し、5000万件の走行データと最大5億パラメータで学習してモデルサイズ・データ量・計算量と性能の関係を分析している。

**新規性**

異種センサ融合と3D空間理解という自動運転特有の課題下でスケーリング則を実証的に検証した点が新規で、Waymo Open Datasetで従来手法を大きく上回る性能を達成した。

**読む理由**

LLM分野で確立されたスケーリング則が自動運転知覚にも適用可能かを示す実証研究であり、大規模データ・モデルによる知覚性能向上の今後の方向性を把握するうえで重要。

- Paper: https://arxiv.org/abs/2605.20390
- Code: -

### Generative Texture Diversification of 3D Pedestrians for Robust Autonomous Driving Perception

CVPR 2026 / 3D Detection

**概要**

自動運転における歩行者検出向けの学習データ不足を補うため、単一の3D歩行者アセットからStyleGAN2で顔テクスチャや外見バリエーションを生成し3Dメッシュにマッピングすることで、低コストに多様な合成歩行者インスタンスを量産する手法を提案している。生成したアセットで合成データセットを構築し、実データと合成データを混合した際のRGBベース物体検出への影響、および点群ベース3D検出における幾何学的ドメインギャップの感度を分析している。

**新規性**

新規ジオメトリを個別に設計せず、テクスチャ・外見レベルの多様化のみでアセットスケーリングを行う点が従来のアセット作成コストの高いアプローチと異なる。

**読む理由**

合成データによるアセット多様化がRGB検出とLiDAR/点群検出で異なる感度を示す点は、シミュレーションデータを用いた3D検出モデルの頑健性評価・学習戦略を検討する上で参考になる。

- Paper: https://arxiv.org/abs/2605.13755
- Code: -

### Benchmarking Multi-View BEV Object Detection with Mixed Pinhole and Fisheye Cameras

ICRA 2026 / 3D Detection

**概要**

自動運転で普及しつつあるpinhole+fisheye混在カメラ構成において、既存のBEV 3D物体検出モデルが魚眼歪みで性能劣化する問題を扱う。KITTI-360をnuScenes形式に変換した実データベンチマークを構築し、rectification、MEIカメラモデルに基づく歪み対応View Transformation Module、極座標表現という3種類の適応手法をBEVFormer・BEVDet・PETRの3アーキテクチャに適用して系統的に評価する。

**新規性**

従来はpinhole前提のBEV検出モデルを合成データや個別工夫で魚眼に適用する例はあったが、本研究は実データによる魚眼+pinhole混在の3D検出ベンチマークを初めて整備し、複数の適応戦略とアーキテクチャを横断的に比較している。

**読む理由**

マルチカメラ構成が多様化する中で、fisheye歪みに対するBEV検出手法のロバスト性と設計指針を把握できる点で、実運用を見据えた3D検出・AD知覚の研究動向として参考になる。

- Paper: https://arxiv.org/abs/2603.27818
- Code: https://github.com/CesarLiu/FishBEVOD.git

### StereoMV2D: A Sparse Temporal Stereo-Enhanced Framework for Robust Multi-View 3D Object Detection

arXiv 2025 / 3D Detection

**概要**

MV2Dの2D検出結果を用いたクエリ初期化手法をベースに、単一フレームの2D検出では深度が曖昧になる問題を解決する。隣接フレーム間の時間的ステレオ視差を利用してクエリの深度精度を高める枠組みStereoMV2Dを提案する。2D RoI内で計算を行うことで効率を保ちつつ、動的信頼度ゲーティング機構でフレーム間マッチングと見た目の一致度から時間的ステレオ手がかりの信頼性を評価する。

**新規性**

単一フレーム2D検出の深度曖昧性を、時間的ステレオ視差と動的信頼度ゲーティングにより2D RoI内で効率的に補正する点が従来のクエリベース検出器との違い。

**読む理由**

スパースクエリ型マルチビュー3D検出における深度推定精度と計算効率のトレードオフ改善の一事例として、AD Perception領域の手法動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2512.17620
- Code: https://github.com/Uddd821/StereoMV2D

### DGFusion: Dual-guided Fusion for Robust Multi-Modal 3D Object Detection

arXiv 2025 / 3D Detection

**概要**

自動運転の3D物体検出において、遠方・小型・遮蔽物体などhard instanceの検出精度が課題であることを指摘し、既存のマルチモーダル融合手法が単一方向(Point-guide-ImageまたはImage-guide-Point)のガイドしか使わずモダリティ間の情報密度差に対応できていない点を問題視する。DGFusionでは両方向のガイドを組み合わせたDual-guidedパラダイムを提案し、Difficulty-aware Instance Pair Matcher(DIPM)でインスタンスを難易度別にペアリングした上で、それぞれに適したDual-guided Moduleで融合する。

**新規性**

単一方向ガイドに依存していた従来のPoint-guide-ImageまたはImage-guide-Point手法を統合し、インスタンスの難易度(easy/hard)に応じて異なる融合戦略を適用する点が新しい。

**読む理由**

hard instance(遠方・小型・遮蔽物体)への対応は自動運転認識の安全性に直結する重要課題であり、マルチモーダル融合の設計指針として参考になる。

- Paper: https://arxiv.org/abs/2511.10035
- Code: -

### BEVUDA++: Geometric-aware Unsupervised Domain Adaptation for Multi-View 3D Object Detection

arXiv 2025 / 3D Detection

**概要**

視点ベースのBEV 3D物体検出はドメインシフトにより性能が大きく劣化する問題を扱い、複数の幾何空間(2D/Voxel/BEV)でシフトが蓄積することに着目してドメイン適応を試みた研究。信頼できる深度予測とターゲットLiDARを組み合わせるReliable Depth Teacherと、複数空間の特徴を統一埋め込み空間に写像するGeometric Consistent Studentからなるteacher-studentフレームワークBEVUDA++を提案している。

**新規性**

単一空間での適応にとどまらず、2D・Voxel・BEVという複数の幾何空間にまたがるドメインシフトを統一的に縮小する点、および不確実性に基づくExponential Moving Average(UEMA)で誤差蓄積を抑える点が従来手法と異なる。

**読む理由**

BEV 3D検出の実運用では天候・昼夜・地域差によるドメインシフトが避けられず、Day-Night適応でNDS/mAPを大きく改善した本手法は環境認識のロバスト性向上の観点で参考になる。

- Paper: https://arxiv.org/abs/2509.14151
- Code: -

### Decoupled Functional Evaluation of Autonomous Driving Models via Feature Map Quality Scoring

arXiv 2025 / 3D Detection

**概要**

End-to-endの自動運転モデルでは中間の機能モジュール(特徴マップ)に対する明示的な教師信号がなく、動作が不透明で個別評価・学習が難しいという課題がある。本研究はGT表現との類似度に基づくFeature Map Convergence Score(FMCS)と、Dual-Granularity Dynamic Weighted Scoring Systemによる統合指標Feature Map Quality Scoreを提案し、CLIPベースのネットワークで特徴マップ品質をリアルタイムに予測・評価する。NuScenesでの実験では、この評価モジュールを学習に組み込むことで3D物体検出のNDSが3.89ポイント向上した。

**新規性**

最終出力の精度指標だけでなく、中間特徴マップ自体の品質をGTとの表現類似度で定量化し、それを学習にフィードバックする点が従来のend-to-end評価と異なる。

**読む理由**

end-to-end知覚モデルの中間表現を可視化・評価する仕組みは、モデルの解釈性向上や学習効率化につながる知見として地図生成・知覚研究全体に応用が期待できる。

- Paper: https://arxiv.org/abs/2508.07552
- Code: -

### Collaborative Perceiver: Elevating Vision-based 3D Object Detection via Local Density-Aware Spatial Occupancy

arXiv 2025 / 3D Detection

**概要**

vision-based BEV 3D物体検出において、既存手法が道路や路面などの環境コンテキストを捨象している問題に着目し、occupancy予測を補助タスクとして併用するマルチタスク学習フレームワークCollaborative Perceiverを提案している。局所密度情報を含む密なoccupancy正解データを生成するパイプライン、voxel高さに基づくサンプリング戦略、検出とoccupancyの特徴を統合するグローバル・ローカル協調融合モジュールから構成される。

**新規性**

BEV特徴を単純に潰して物体特徴のみで構成する従来手法と異なり、occupancy予測との構造的・概念的な類似性を利用して空間表現とfeature refinementのギャップを埋める点が新しい。

**読む理由**

3D検出とoccupancy予測というテーマの垣根を越えたマルチタスク統合の設計例として、両者の特徴融合手法の参考になる。

- Paper: https://arxiv.org/abs/2507.21358
- Code: https://github.com/jichengyuan/Collaborative-Perceiver

### Revisiting Radar Camera Alignment by Contrastive Learning for 3D Object Detection

arXiv 2025 / 3D Detection

**概要**

レーダーとカメラの特徴をBEV空間で融合する際に生じるモダリティ間のドメインギャップ・空間的な位置ずれを解消することを課題とし、対照学習に基づくDual-Route Alignmentモジュールで両モダリティの特徴を位置整合させつつ相互作用させ、さらにレーダーBEV特徴の疎性を蒸留損失付きのRadar Feature Enhancementモジュールで補う手法RCAlignを提案している。nuScenesベンチマークでレーダー・カメラ融合3D検出のSOTAを達成した。

**新規性**

従来手法がアライメント時のモダリティ間相互作用を無視するか、同一空間位置での特徴整合に失敗していたのに対し、対照学習による整合と蒸留による特徴densificationを組み合わせている点が異なる。

**読む理由**

レーダー・カメラ融合3D検出における特徴アライメントの課題設定と解決アプローチは、他のマルチモーダルBEV認識・地図生成タスクの特徴融合設計にも応用できる知見となる。

- Paper: https://arxiv.org/abs/2504.16368
- Code: -

### Resilient Sensor Fusion under Adverse Sensor Failures via Multi-Modal Expert Fusion

CVPR 2025 / 3D Detection

**概要**

LiDARビーム削減、LiDARドロップ、視野制限、カメラドロップ、遮蔽といった深刻なセンサ故障下で性能が大きく劣化する既存のマルチモーダル融合手法の課題に対し、モダリティ間の依存を排したMixture-of-Expertsベースの3D物体検出器MoMEを提案している。カメラ専用・LiDAR専用・両方併用の3つの並列エキスパートデコーダでクエリをデコードし、Adaptive Query Routerが特徴品質に応じて各クエリに最適なエキスパートを選択する構成になっている。

**新規性**

既存融合アーキテクチャがモダリティ間依存により故障時に弱いのに対し、Multi-Expert Decoding枠組みでクエリごとに専用デコーダを選択的に用いることでモダリティ依存を完全に切り離している点が異なる。

**読む理由**

悪天候・センサ故障時の頑健性はAD Perceptionの実運用上の重要課題であり、マルチモーダル融合の設計指針として参照価値が高い。

- Paper: https://arxiv.org/abs/2503.19776
- Code: -

### SToRe3D: Sparse Token Relevance in ViTs for Efficient Multi-View 3D Object Detection

CVPR 2026 / 3D Detection

**概要**

マルチビュー3D物体検出向けViTは高精度だが、複数視点・広範な3D領域のトークンとクエリを密に処理するため推論遅延が大きい。既存の2D向けスパース化手法は画像トークンの削減にとどまり、3Dオブジェクトクエリやモデル全体のスパース化には対応できていない。本論文はSToRe3Dという、2D画像トークンと3Dオブジェクトクエリを関連度に基づいて同時選択し、除外した特徴を後で再活性化できる形で保持するフレームワークを提案する。

**新規性**

2D-3D相互関連度ヘッドにより走行判断上重要な領域へ計算資源を配分しつつ、他の特徴は破棄せず保存・再利用可能にする点が、画像トークンのみを扱う既存の2Dスパース化手法との違い。

**読む理由**

nuScenesで3倍の推論高速化と精度維持を両立させており、リアルタイム性が求められる車載3D検出の効率化トレンドを追ううえで参考になる。

- Paper: https://arxiv.org/abs/2605.14110
- Code: -

### Scene Reconstruction as Mapping Priors for 3D Detection

CVPR 2026 / 3D Detection

**概要**

自動運転の3D物体検出において、地図情報が持つ静的環境の構造的事前知識が十分に活用されていない点に着目し、センサデータを人手ラベルなしで集約・再構成して密な地図事前情報(mapping priors)を自動生成するパイプラインを提案している。さらにこの事前情報を異なるセンサモダリティの検出器と統合するMPA3Dというフレームワークを設計し、遠方物体や悪天候など点群が疎・ノイジーになる状況での検出精度低下を補う。

**新規性**

従来のHDマップは人手による作成・維持コストが高く大規模展開が難しいのに対し、本手法は集約センサデータから自動的に密な地図事前情報を再構成する点、およびそれを3D検出器にモダリティを跨いで統合する点が新しい。

**読む理由**

HDマップ生成コストの問題を、地図生成そのものではなく認識タスク(3D検出)への再構成事前情報という形で回避しつつ精度向上を狙うアプローチであり、Map ReconstructionとPerceptionの接点を考える上で参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Fu_Scene_Reconstruction_as_Mapping_Priors_for_3D_Detection_CVPR_2026_paper.html
- Code: -

### RaGS: Unleashing 3D Gaussian Splatting from 4D Radar and Monocular Cue for 3D Object Detection

CVPR 2026 / 3D Detection

**概要**

4D millimeter-wave radarと単眼画像を用いた3D物体検出において、既存のinstance proposalベースやBEVグリッドベースの融合手法が持つ表現の硬直性を解消するため、シーンをGaussianの連続場としてモデル化するRaGSを提案する。Frustum-based Localization Initiationで画素をunprojectしてGaussian中心を初期化し、Iterative Multimodal AggregationでRoI内のGaussianを画像意味情報とradarの速度・幾何情報で refinementし、Multi-level Gaussian Fusionで階層的BEV特徴に変換して検出する。View-of-Delft、TJ4DRadSet、OmniHD-Scenesで検証している。

**新規性**

固定的なinstance proposalや剛直なBEVグリッド構造に依存せず、前景領域に動的にリソースを割り当てられるGaussian場としてシーンを表現する点が従来手法との違い。

**読む理由**

Gaussian SplattingをBEV特徴生成・3D検出のバックボーンとして応用する設計は、occupancyやシーン表現の柔軟化を狙う地図生成・環境認識研究の潮流と直結しており参考になる。

- Paper: https://arxiv.org/abs/2507.19856
- Code: https://github.com/shawnnnkb/RaGS

### OcRFDet: Object-Centric Radiance Fields for Multi-View 3D Object Detection in Autonomous Driving

ICCV 2025 / 3D Detection

**概要**

マルチビュー3D物体検出において、2D特徴を3D空間へ変換する際の暗黙的な学習に限界があるとし、放射輝度場(radiance field)を補助タスクとして導入することで幾何推定能力を強化する手法を提案している。単純にシーン全体をレンダリングすると背景の強い応答が検出性能を低下させることを分析で示し、前景物体のみをモデル化するobject-centric radiance fields(OcRF)を導入して問題を解決している。

**新規性**

背景ノイズを除外し前景物体に限定したradiance fieldsで3D voxel特徴を強化する点、およびレンダリングの副産物であるopacityを用いた高さ方向認識のattention機構(HOA)で2D BEV特徴を強化する点が従来手法と異なる。

**読む理由**

radiance field/NeRF的表現を検出器の補助タスクとして統合するアプローチであり、3D検出とreconstruction技術の融合という観点で地図生成・環境認識研究の技術トレンドを把握するのに有用。

- Paper: https://arxiv.org/abs/2506.23565
- Code: -

### FreqPDE: Rethinking Positional Depth Embedding for Multi-View 3D Object Detection Transformers

ICCV 2025 / 3D Detection

**概要**

マルチビュー2D画像からの3D物体検出において、深度予測の質が物体境界での不連続や小物体の見落としを招く問題に取り組む。高周波エッジ情報と低周波意味情報を組み合わせた特徴ピラミッド、クロスビューでスケール不変な深度推定、位置埋め込みと深度特徴を融合するモジュールから成るFreqPDEを提案する。metricとdistributionの両面から深度を教師するhybrid supervisionも導入している。

**新規性**

既存手法が高レベル特徴のみで疎な点群教師に頼っていたのに対し、周波数帯域を分離した特徴抽出とクロスビュー一貫性・スケール不変性を明示的に扱う点が異なる。

**読む理由**

カメラのみのBEV/3D検出におけるdepth-aware query decodingの改良方向性を把握するうえで参考になる。

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Su_FreqPDE_Rethinking_Positional_Depth_Embedding_for_Multi-View_3D_Object_Detection_ICCV_2025_paper.html
- Code: -

### Leveraging Temporal Cues for Semi-Supervised Multi-View 3D Object Detection

CVPR 2025 / 3D Detection

**概要**

カメラのみのマルチビュー3D物体検出において大量の人手アノテーションが必要な問題に対し、ラベルなしRGB走行シーケンスを活用する半教師あり学習フレームワークを提案。前向き・後向き両方向の時系列を扱う単一検出器を訓練し、両方向の疑似ラベルをアンサンブルすることで3D位置精度の低さを解消する。さらに3Dトラッキングによる検出漏れの補完、2D検出ヘッドを用いたフィルタリング、物体クエリ条件付きマスク再構成という自己教師あり目的も導入している。

**新規性**

従来の単純な信頼度閾値による疑似ラベリングが時系列カメラ設定では3D位置推定精度不足で機能しない点を指摘し、双方向時系列アンサンブルとトラッキング補完・2D補助ヘッドによる疑似ラベル品質向上を組み合わせた点が新しい。

**読む理由**

アノテーションコストを抑えつつ時系列カメラ3D検出を改善する半教師あり手法として、大規模実運用データセットでの検出性能向上手法の動向を把握するうえで参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Park_Leveraging_Temporal_Cues_for_Semi-Supervised_Multi-View_3D_Object_Detection_CVPR_2025_paper.html
- Code: -

### UniMamba: Unified Spatial-Channel Representation Learning with Group-Efficient Mamba for LiDAR-based 3D Object Detection

CVPR 2025 / 3D Detection

**概要**

点群のTransformer系手法はシリアライズで空間構造が壊れ、グループ化により受容野も制限される問題を指摘。UniMambaは3D submanifold convolutionによる局所空間モデリングとZ-orderシリアライズ、チャネルグループ化したmulti-head SSM(Mamba)による大域集約を組み合わせ、局所・大域の文脈を効率的に同時学習する。encoder-decoder構造でUniMambaブロックを積み重ね、マルチスケール学習を行う。

**新規性**

3D convolutionとState Space Model(Mamba)を統一し、チャネルグループ化とZ-orderシリアライズにより局所・大域の空間依存性を単一ブロックで扱う点がTransformer系やシングルスケールSSM手法との違い。

**読む理由**

点群のシリアライズ手法とSSMベースの効率的な大域文脈モデリングは、LiDAR 3D検出の受容野・計算効率トレードオフを改善する動向として地図生成・認識研究にも波及しうる。

- Paper: https://arxiv.org/abs/2503.12009
- Code: -

### CorrBEV: Multi-View 3D Object Detection by Correlation Learning with Multi-modal Prototypes

CVPR 2025 / 3D Detection

**概要**

マルチビューカメラのみによる3D物体検出において、遮蔽(occlusion)により物体特徴が劣化する問題を扱う。人間のamodal知覚に着想を得て、視覚・言語の補助プロトタイプを導入し、Siamese物体追跡的な深さ方向correlationでベースラインの特徴と融合することで、遮蔽物体のクエリ学習を強化する。学習時にはランダム画素ドロップで遮蔽を模擬し、異なる遮蔽度合いの特徴を揃えるマルチモーダル対照損失を用いる。

**新規性**

遮蔽対策として外部の視覚・言語プロトタイプ知識をSiamese追跡由来のcorrelation学習で融合する点が新規で、従来のBEV検出改善が主に構造改良に留まっていたのに対し人間の補完的知覚メカニズムを模した設計になっている。

**読む理由**

遮蔽という3D検出の中核課題に対する解法であり、BEVFormerやSparseBEVなど既存手法へ適用可能な汎用モジュールとして悪天候等の頑健性向上にも波及する点で、自動運転認識の性能改善動向を追う上で参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Xue_CorrBEV_Multi-View_3D_Object_Detection_by_Correlation_Learning_with_Multi-modal_CVPR_2025_paper.html
- Code: -

### DriveGEN: Generalized and Robust 3D Detection in Driving via Controllable Text-to-Image Diffusion Generation

CVPR 2025 / 3D Detection

**概要**

自動運転の視覚ベース3D検出は学習データの収集コストが高く、分布外(OOD)シーンで性能が劣化しやすい。DriveGENは追加学習なしのテキスト画像拡散モデルを用い、レイアウトから抽出した自己プロトタイプで3D物体の幾何情報を保持しつつ、多様なOODシーン画像を生成して学習データを拡張する手法を提案している。

**新規性**

既存の制御可能なT2I手法は学習データ規模に制約されるか全ての注釈付き3D物体を保持できないのに対し、DriveGENは拡散モデルを追加学習せず、自己注意特徴からのプロトタイプ抽出とプロトタイプ誘導型のデノイジングにより3D物体の幾何を各生成で維持する。

**読む理由**

分布外データへの頑健性はAD知覚全般の実運用課題であり、拡散生成によるデータ拡張は環境認識モデルの評価・学習パイプライン設計を検討する上で参考になる。

- Paper: https://arxiv.org/abs/2503.11122
- Code: -

### GBlobs: Explicit Local Structure via Gaussian Blobs for Improved Cross-Domain LiDAR-based 3D Object Detection

CVPR 2025 / 3D Detection

**概要**

LiDARベースの3D物体検出器はドメインシフトに弱く、既存のドメイン汎化手法は点群のグローバルな座標情報のみを入力特徴として使うため、物体の絶対位置に過度に依存し汎化性能が低下する問題がある。本研究は各点の近傍局所構造をガウス分布(GBlobs)として明示的にエンコードすることでこれを解決する。追加パラメータなしで既存検出器に組み込むだけで、Waymo→KITTIなど複数のシングルソース・マルチソースのドメイン汎化ベンチマークで大幅な性能向上を達成した。

**新規性**

従来のグローバルな点群座標特徴に頼る手法と異なり、点近傍の局所幾何構造をガウスブロブとして明示的に表現することでドメイン不変性を高めている点が新しい。

**読む理由**

実運用では取得LiDARやシーンが変わるたびに検出精度が落ちる問題が常につきまとうため、パラメータ追加なしで既存検出器のクロスドメイン性能を底上げできる本手法は実装コストが低く注目に値する。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Malic_GBlobs_Explicit_Local_Structure_via_Gaussian_Blobs_for_Improved_Cross-Domain_CVPR_2025_paper.html
- Code: -

### Towards Accurate and Efficient 3D Object Detection for Autonomous Driving: A Mixture of Experts Computing System on Edge

ICCV 2025 / 3D Detection

**概要**

自動運転車のエッジデバイス上でLiDAR点群とカメラ画像を融合し、低遅延かつ高精度な3D物体検出を実現するMoEベースの計算システムEMC2を提案する研究。物体の可視性や距離に応じて特徴量を適切なエキスパートに動的にルーティングするシナリオ認識型アーキテクチャと、Jetson等の資源制約デバイス向けのハードウェア・ソフトウェア協調最適化を組み合わせている。

**新規性**

従来のマルチモーダル融合手法と異なり、シーンごとの物体可視性・距離に応じてスパースな点群とデンスな画像特徴を切り替えるscenario-aware MoEルーティングを導入し、計算グラフ簡略化などのハードウェア最適化までエンドツーエンドで統合している点が新しい。

**読む理由**

エッジ実装での実時間性と精度のトレードオフをMoEアーキテクチャで解く事例として、車載向け3D検出システムの設計動向を追う上で参考になる。

- Paper: https://arxiv.org/abs/2507.04123
- Code: -

### JiSAM: Alleviate Labeling Burden and Corner Case Problems in Autonomous Driving via Minimal Real-World Data

CVPR 2025 / 3D Detection

**概要**

LiDARベースの自動運転認識は実データのラベル付けコストが高く、レアなコーナーケースが不足しがちである。本研究はCARLA等のシミュレータで生成した合成点群を活用し、jitter augmentation、domain-aware backbone、memory-based Sectorized AlignMentの3手法(JiSAM)を組み合わせることで、この課題に取り組む。NuScenesでの実験では、実データの2.5%のラベルのみで全実データ学習に匹敵する性能を達成している。

**新規性**

単純なsim-to-real転移ではなく、augmentation・ドメイン適応backbone・sector単位のアライメントを組み合わせたplug-and-play手法により、サンプル効率とsim-real gapの両課題を同時に解決している点が従来と異なる。

**読む理由**

実データ依存を大幅に減らしつつコーナーケース性能を向上させるアプローチであり、アノテーションコストが課題となる3D検出研究の効率化動向を把握する上で参考になる。

- Paper: https://arxiv.org/abs/2503.08422
- Code: -

### V2X-R: Cooperative LiDAR-4D Radar Fusion with Denoising Diffusion for 3D Object Detection

CVPR 2025 / 3D Detection

**概要**

悪天候下でV2X協調型3D物体検出の性能が低下する課題に対し、LiDAR・カメラ・4Dレーダーを含む初のシミュレーションV2Xデータセット「V2X-R」を構築し、4DレーダーとLiDARを融合する検出パイプラインを提案している。さらに4Dレーダー特徴を条件としてLiDAR特徴のノイズを除去するMulti-modal Denoising Diffusion(MDD)モジュールを導入し、悪天候時の頑健性を高めている。

**新規性**

従来のLiDAR・カメラ中心のV2X検出と異なり、Doppler速度情報を持つ耐候性の高い4Dレーダーを協調融合に組み込み、拡散モデルによるマルチモーダルデノイジングで悪天候ノイズに対処する点が新しい。

**読む理由**

V2X協調認識と悪天候ロバスト性という自動運転認識の重要課題に対し、新規マルチモーダルデータセットと融合・デノイジング手法を同時に提示しており、センサー融合ベースの3D検出動向を追ううえで参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Huang_V2X-R_Cooperative_LiDAR-4D_Radar_Fusion_with_Denoising_Diffusion_for_3D_CVPR_2025_paper.html
- Code: -

## AD Perception

### Geometry-Grounded Unified 3D Perception for Autonomous Driving

BMVC 2026 / AD Perception

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

**概要**

中国農村部の複雑な交通環境ではデータ不足と汎化性の課題があるとして、Unreal Engineで生成した合成画像と河南省尉氏県で撮影した実画像を組み合わせた14クラスの物体検出データセットを構築した論文。電動三輪車や低速車両、露店など地域特有の物体クラスを定義し、YOLOv5/v8/11/26シリーズとRT-DETR-Lの計13モデルを、実データのみ・実:合成=1:0.5・1:1の3条件で比較評価している。

**新規性**

既存研究が都市部・欧米中心のデータセットに偏る中、農村特有の物体カテゴリと実画像・合成画像の混合比率を体系的に変えて検出性能への影響を定量評価した点が新しい。

**読む理由**

合成データ混合比率が検出性能に与える影響とlong-tail物体での限界を実証しており、データ戦略設計の知見として環境認識研究の参考になる。

- Paper: https://arxiv.org/abs/2607.27058
- Code: -

### ASTAD: Asymmetric Style Transfer for Synthetic-to-Real Adaptation in Autonomous Driving

ECCV 2026 / AD Perception

**概要**

自動運転向け合成データと実データ間のドメインギャップを埋めるスタイル変換タスクASTADを提案。合成データには完全なピクセルレベル注釈があるが実世界の参照画像には注釈がないという非対称性に着目し、この制約下で意味的整合性を保ったスタイル変換を実現する手法ASTModelを開発している。

**新規性**

従来の対称的な意味的guidanceに依存する手法と異なり、ラベルなし実データからの粗い意味的priorを動的に精緻化し、拡散モデルのdenoising過程でクラス整合的なスタイル注入を行う学習不要の2段階フレームワークを採用している。

**読む理由**

合成データ活用によるアノテーションコスト削減は知覚モデル開発の重要課題であり、非対称な注釈制約下でのdomain adaptation手法は実運用データパイプライン設計に直接応用できる。

- Paper: https://arxiv.org/abs/2606.29286
- Code: https://github.com/Dingyi-Yao/ASTAD

### Towards Compact Autonomous Driving Perception with Balanced Learning and Multi-sensor Fusion

arXiv 2026 / AD Perception

**概要**

自動運転向けに、セマンティックセグメンテーション・深度推定・LiDARセグメンテーション・BEV投影を1回の推論で同時に行うコンパクトなマルチタスクモデルを提案。タスク間の学習不均衡を解消する適応的な損失重み付け手法を導入し、RGBカメラ・DVS・LiDARを車両複数箇所に配置して中間段階で融合する。

**新規性**

多数タスクの同時学習で生じる不均衡を適応的損失重み付けで解消しつつ、少パラメータ・低GPUメモリで高速推論を実現している点が従来の大型マルチタスクモデルとの違い。

**読む理由**

複数センサ融合とマルチタスク学習を軽量に両立させる設計は、実車搭載を想定した知覚パイプラインの効率化を検討する際の参考になる。

- Paper: https://arxiv.org/abs/2606.02979
- Code: https://github.com/oskarnatan/compact-perception

### ATLAS: A Large-Scale Evaluation Benchmark for Adversarial LiDAR Perception

arXiv 2026 / AD Perception

**概要**

自動運転向けLiDAR知覚モデルが、点の注入や除去といった物理的に模擬可能なブラックボックス攻撃に対してどれだけ脆弱かを大規模かつ体系的に評価するベンチマークATLASを提案する。実際の走行シーケンスを用い、注入・除去という2種類の主要な攻撃モードをシミュレートして、現行の最先端LiDAR検出モデル群を横断的に評価している。

**新規性**

従来の敵対的LiDAR研究が攻撃ハードウェアや初期世代の検出器、幾何的・アルゴリズム的防御に留まっていたのに対し、本研究は現代の知覚モデルを対象に物理的根拠のある大規模評価を初めて行い、標準ベンチマークでの性能が高いモデルほど点除去には強いが点注入には弱いという非対称な脆弱性を発見した点が新しい。

**読む理由**

クリーンなベンチマーク評価だけでは見えないLiDAR知覚モデルの実運用時のロバスト性リスクを可視化しており、データベースサンプリング拡張という一般的な学習慣行が引き起こすアーキテクチャ非依存の脆弱性を指摘している点で、3D検出・知覚モデルの評価設計を考える上で参考になる。

- Paper: https://arxiv.org/abs/2606.02924
- Code: -

### Towards Trustworthy and Explainable AI for Perception Models: From Concept to Prototype Vehicle Deployment

arXiv 2026 / AD Perception

**概要**

自動運転の3Dシーン理解に使われるTransformerベース検出器を対象に、注意機構から忠実な説明(saliency)を導出し、摂動ベースの一貫性テストで検証する。さらに不確実性の推定・較正モジュールと頑健性向上の学習手法を統合し、実車プロトタイプに実装してリアルタイムで可視化するXAIインターフェースまで構築している。

**新規性**

理論的なXAI/Trustworthy AIの枠組みにとどまらず、説明性・較正済み不確実性・頑健性を単一の知覚モジュールに統合し、実車搭載まで実証した点が従来研究との違い。

**読む理由**

知覚モデルの信頼性・説明可能性の実装例は少なく、実車デプロイまで踏み込んだ事例として安全性保証やHMI設計の参考になる。

- Paper: https://arxiv.org/abs/2605.16087
- Code: -

### WILD SAM: A Simulated-and-Real Data Augmentation for Autonomous Driving Perception under Challenging Weather

arXiv 2026 / AD Perception

**概要**

悪天候による自動運転向け物体検出器の性能劣化に対し、実データから生成した疑似ラベルのノイズをフィルタするWILDフレームワークと、それをシミュレーションデータ学習と組み合わせるWILD SAMを提案。Four Seasonsデータセットの雨・雪シーンで検証している。

**新規性**

従来の合成データ依存型手法と異なり、悪天候下の実データから得た疑似ラベルのノイズを除去する仕組みを導入し、シミュレーションと実データ双方を活用するハイブリッド学習を実現した点が新しい。

**読む理由**

天候変動によるドメインシフト対策は自動運転認識の頑健性向上に直結するテーマであり、疑似ラベル denoising という具体的アプローチは他の認識・地図生成タスクへの応用も見込める。

- Paper: https://arxiv.org/abs/2605.01081
- Code: https://github.com/Kh-Hamed/WILD-SAM

### Object-Centric Stereo Ranging for Autonomous Driving: From Dense Disparity to Census-Based Template Matching

arXiv 2026 / AD Perception

**概要**

自動運転における長距離車両検知向けの奥行き推定を扱う論文。従来の密なブロックマッチング/SGMは計算コストが高く遠距離で視差が小さいため精度が低下する課題に対し、密ステレオ視差・物体中心のCensusベーステンプレートマッチング・単眼幾何プライアを統合した検知-測距-追跡パイプラインを提案している。

**新規性**

検出されたバウンディングボックス内でGPU上の疎なステレオマッチングを行う物体中心Censusテンプレートマッチング(遠近分割統治、前後方検証、遮蔽考慮サンプリング、頑健なマルチブロック集約を含む)と、レーダー・ステレオ連携によるオンライン外部パラメータ較正補正を組み合わせている点が従来の密ステレオ手法と異なる。

**読む理由**

カメラ単体に頼らないステレオ+レーダー融合による実用的な測距システムの設計例であり、実車搭載の認識パイプラインにおける精度とリアルタイム性の両立の工夫を学べる。

- Paper: https://arxiv.org/abs/2604.07980
- Code: -

### BEVPredFormer: Spatio-temporal Attention for BEV Instance Prediction in Autonomous Driving

arXiv 2026 / AD Perception

**概要**

自動運転における動的物体のBEVセグメンテーションと将来動作予測を、モジュール型パイプラインの誤差蓄積・遅延を避けて単一モデルで行う手法を提案。カメラ入力のみから3D空間への注意機構ベース投影と、時空間attentionによる特徴処理でシーンの時間発展を捉える。差分ガイド付き特徴抽出モジュールで時間方向の表現も強化している。

**新規性**

再帰(RNN)構造を使わず、gated transformer層と時空間分離attentionによりBEVインスタンス予測を行う点が従来の再帰的時系列処理と異なる。

**読む理由**

BEVベースの統合認識・予測アーキテクチャの最新設計パターンとして、地図生成や占有予測系研究のバックボーン選定の参考になる。

- Paper: https://arxiv.org/abs/2604.02930
- Code: -

### AurigaNet: A Real-Time Multi-Task Network for Enhanced Urban Driving Perception

arXiv 2026 / AD Perception

**概要**

本論文は自動運転向けのリアルタイムマルチタスク認識ネットワークAurigaNetを提案する。物体検出・車線検出・走行可能領域のインスタンスセグメンテーションを単一ネットワークで統合し、BDD100Kで学習・評価している。単一モデルで複数タスクを処理することで計算効率とリアルタイム性を両立させることを狙っている。

**新規性**

走行可能領域検出をend-to-endのインスタンスセグメンテーションとして扱う点が既存のマルチタスク認識モデルとの違いであり、経路推定の精度と効率を同時に高めている。

**読む理由**

マルチタスク学習による認識の効率化とエッジデバイス(Jetson Orin NX)での実時間動作の両立事例として、車載認識システムの実用化動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2602.10660
- Code: https://github.com/KiaRational/AurigaNet

### A Style-Based Profiling Framework for Quantifying the Synthetic-to-Real Gap in Autonomous Driving Datasets

arXiv 2025 / AD Perception

**概要**

自動運転の知覚モデル評価には環境試験が必要だが実車走行によるテストは困難なため、合成データセットの活用が進んでいる。しかし合成データと実データの間にはスタイル面でのドメインギャップがあり、モデル汎化性能を損なう要因となる。本研究はGram行列ベースのスタイル抽出とmetric learningを組み合わせ、両ドメインの画像からスタイル埋め込みを取得し、その分布差を定量化するフレームワークを提案する。

**新規性**

従来のsim-to-real評価が主にタスク性能(検出精度等)で間接的にギャップを測るのに対し、本研究はStyle Embedding Distribution Discrepancy (SEDD)という新指標を導入し、画像スタイルそのものの分布差を直接定量化する点が異なる。

**読む理由**

合成データを用いた自動運転データセット拡充が今後も進む中、データの質を体系的に診断・改善するための標準的な評価軸を提供しており、データセット設計や評価基盤の研究動向として押さえておく価値がある。

- Paper: https://arxiv.org/abs/2510.10203
- Code: -

### From Filters to VLMs: Benchmarking Defogging Methods through Object Detection and Segmentation Performance

WACV 2026 / AD Perception

**概要**

濃霧環境下での自動運転知覚性能低下に対し、古典的フィルタから学習型デフォギングネットワーク、それらの連結、さらにVLMベースの画像編集まで幅広いデフォギング手法を比較したベンチマーク研究。合成データ(Foggy Cityscapes)と実データ(ACDC)の両方で評価し、画像復元品質と下流タスク(検出mAP・パノプティックセグメンテーション品質)の相関を検証している。

**新規性**

画像品質の改善が必ずしも下流の検出・セグメンテーション性能向上につながらない点を実証的に示し、さらに人間およびVLM判定によるルーブリック評価と下流タスク指標との整合性まで分析している点が従来のデフォギング評価と異なる。

**読む理由**

悪天候下での知覚頑健性は自動運転知覚の前提条件であり、前処理としてのデフォギングがいつ有効かを整理した知見は実運用のパイプライン設計判断に直結する。

- Paper: https://arxiv.org/abs/2510.03906
- Code: -

### Seg2Track-SAM2: SAM2-based Multi-object Tracking and Segmentation

arXiv 2025 / AD Perception

**概要**

自動運転における物体追跡(MOT/MOTS)を、SAM2のようなプロンプト可能な動画セグメンテーション基盤モデル上に構築しようとする研究。SAM2単体ではID管理機構がなく、追跡が長くなるほどメモリ消費が増える課題があるため、既存の物体検出器とSAM2を組み合わせ、Seg2Trackモジュールでトラックの初期化・データアソシエーション・トラック修正を担わせるフレームワークSeg2Track-SAM2を提案している。

**新規性**

データセット固有のfine-tuningを行わず検出器非依存という条件を保ったまま、SAM2にID管理機構を追加し、さらにスライディングウィンドウ方式のメモリ管理でメモリ使用量を最大75%削減している点が従来のSAM2応用と異なる。

**読む理由**

基盤セグメンテーションモデルを追跡タスクに転用する際のID管理・メモリ効率という実装上の課題への対処例として、動的シーン認識全般の設計に参考になる。

- Paper: https://arxiv.org/abs/2509.11772
- Code: https://github.com/hcmr-lab/Seg2Track-SAM2

### Foundation Models for Autonomous Driving Perception: A Survey Through Core Capabilities

arXiv 2025 / AD Perception

**概要**

自動運転の知覚タスクを、個別タスクごとの深層学習モデルから汎用的な基盤モデルへ移行させる動きを整理したサーベイ。汎化性・スケーラビリティ・分布シフトへの頑健性という課題に対し、基盤モデルがどう対応するかを論じている。generalized knowledge、spatial understanding、multi-sensor robustness、temporal reasoningという4つの能力軸で手法を分類し、各能力の重要性と代表的アプローチを整理している。

**新規性**

手法名やアーキテクチャで分類する従来型サーベイと異なり、動的運転環境で求められる能力を起点とした分類軸を導入し、モデル設計の指針となる視点を提供している。

**読む理由**

Open-world知覚や基盤モデル活用が地図生成・環境認識分野でも重要になりつつあり、能力軸での整理は今後の技術動向を俯瞰する上で参考になる。

- Paper: https://arxiv.org/abs/2509.08302
- Code: -

### Adverse Weather-Independent Framework Towards Autonomous Driving Perception through Temporal Correlation and Unfolded Regularization

arXiv 2025 / AD Perception

**概要**

霧や雨などの複合的な悪天候下で自動運転認識タスク(意味セグメンテーション等)の性能が劣化する問題に対し、晴天画像を参照とせず、単一の天候条件にも限定されない汎用フレームワークAdventを提案している。時系列的に隣接するフレーム間の均質性を利用し、天候条件に依存しない特徴抽出を実現する。

**新規性**

従来のdomain adaptationが晴天画像を参照として要求し単一天候にしか対応できなかったのに対し、Locally Sequential MechanismとGlobally Shuffled Mechanism、Unfolded Regularizersにより参照フリーかつ任意の悪天候条件に汎化できる点が異なる。

**読む理由**

悪天候下での認識性能劣化は自動運転パーセプションの実運用における重要課題であり、参照画像不要かつマルチ天候対応という設計思想は環境認識のロバスト性研究の動向として注目に値する。

- Paper: https://arxiv.org/abs/2508.01583
- Code: -

### S2R-Bench: A Sim-to-Real Evaluation Benchmark for Autonomous Driving

arXiv 2025 / AD Perception

**概要**

自動運転の知覚アルゴリズムは主にシミュレーションベースのベンチマークで評価されており、悪天候やセンサ異常など実世界特有の劣化条件との乖離が課題となっている。本研究はS2R-Bench(Sim-to-Real Evaluation Benchmark)を提案し、様々な道路状況・天候・照度・時間帯における実世界のセンサ異常データを収集した。実データとシミュレーションデータを比較することで、収集データが実応用にとって信頼性・実用性を持つことを示している。

**新規性**

従来の破損頑健性ベンチマークが全てシミュレーション生成のデータに依存していたのに対し、実世界で収集したセンサ異常データに基づく初のベンチマークである点が新規性。

**読む理由**

知覚モデルの頑健性評価がシミュレーションに偏りがちな現状に対し、実世界データとの乖離を定量的に示す試みであり、モデル評価手法の妥当性を検討する上で参考になる。

- Paper: https://arxiv.org/abs/2505.18631
- Code: https://github.com/adept-thu/S2R-Bench

### JarvisIR: Elevating Autonomous Driving Perception with Intelligent Image Restoration

CVPR 2025 / AD Perception

**概要**

自動運転の視覚中心認識は現実世界の予測不能かつ複合的な悪天候による画質劣化に弱く、既存手法は特定の劣化事前知識に依存するかドメインギャップが大きいという課題がある。本研究はVLM(Llava-Llama3等)をコントローラとして複数の専門修復モデルを管理するエージェントJarvisIRを提案し、教師あり微調整と人間フィードバック整合の2段階学習で頑健性とハルシネーション抑制、汎化性を高める。学習・評価用に合成15万件・実世界8万件の指示応答対からなるデータセットCleanBenchも構築した。

**新規性**

特定劣化に特化した単一モデルではなく、VLMが状況を判断して複数の修復エキスパートを選択・制御する点、および実世界のペアデータ不足を人間フィードバックによる教師なし微調整で補う点が従来手法と異なる。

**読む理由**

悪天候などの実運用条件下での認識頑健性は、地図生成や3D検出など下流タスクの入力品質を左右するため、認識パイプライン全体の信頼性向上の観点で参考になる。

- Paper: https://arxiv.org/abs/2504.04158
- Code: -

### DynRsl-VLM: Enhancing Autonomous Driving Perception with Dynamic Resolution Vision-Language Models

arXiv 2025 / AD Perception

**概要**

VQA系のvision-language modelは画像入力を複数回ダウンサンプリングするため、遠方の歩行者・標識・障害物などの細部情報が失われ、自動運転の環境認識精度を損なう。本研究はDynRsl-VLMという動的解像度画像処理手法を提案し、ViTの計算量を抑えつつ画像内の全エンティティの特徴情報を保持する。あわせてQ-Formerに代わる新たなimage-text alignmentモジュールを導入し、動的解像度入力とテキストとのシンプルで効率的な整合を実現する。

**新規性**

固定的なダウンサンプリングに依存する従来のVLMと異なり、動的解像度入力によって詳細情報の欠落を防ぎつつ、Q-Formerを置き換える新規alignmentモジュールで計算コストを抑える点が特徴。

**読む理由**

end-to-end自動運転におけるVLMベース知覚での解像度・情報損失問題への対処法として、Open-world/AD Perception分野の設計指針の参考になる。

- Paper: https://arxiv.org/abs/2503.11265
- Code: -

### RecEdit-Drive: 3D Reconstruction-Guided Spatiotemporal Video Editing for Autonomous Driving Scenes

CVPR 2026 / AD Perception

**概要**

自動運転シーンの動画において、動的3Dオブジェクトを精密に制御しつつ時空間的な一貫性を保つ編集手法を提案している。Spatial Feature Warpingで前景3Dオブジェクトの空間変化を制御し、Spatiotemporal Collaborative Modelingで編集後の前景を背景に自然に統合する。加えて、denoising初期段階で背景構造をノイズ操作により再構成し、前景編集の参照として利用する推論戦略を設計している。

**新規性**

テキストプロンプトや2D構造的事前情報に依存する既存の動画編集手法と異なり、3D再構成に基づく空間特徴のワーピングで動的3Dオブジェクトの変化を直接制御する点が特徴。

**読む理由**

自動運転向けデータ生成・拡張の観点で、3D再構成を活用した動画編集は知覚モデルの学習データ整備やシミュレーションに応用できるため、地図生成・環境認識研究の周辺動向として押さえておく価値がある。

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Wu_RecEdit-Drive_3D_Reconstruction-Guided_Spatiotemporal_Video_Editing_for_Autonomous_Driving_Scenes_CVPR_2026_paper.html
- Code: -

### Toward Real-world BEV Perception: Depth Uncertainty Estimation via Gaussian Splatting

CVPR 2025 / AD Perception

**概要**

マルチカメラ画像から BEV 表現を作る際、近年主流の projection ベース(クエリ学習で明示的な depth 推定を回避する方式)は不確実性のモデル化がなく計算コストも高い、という問題を扱っている。本論文は Lift-Splat-Shoot 系の unprojection ベースを再検討し、depth 分布の soft mean と分散を学習することで空間的な広がり(=物体のスケール)を暗黙的に捉える GaussianLSS を提案する。得られた depth 分布を 3D Gaussian に変換し、rasterize することで不確実性を織り込んだ BEV feature を構成する。nuScenes で評価し、unprojection 系の中で最高性能を報告している。

**新規性**

LSS の離散的な depth bin ではなく depth 分布の平均と分散を明示的に扱い、それを 3D Gaussian の rasterization として BEV に落とし込む点が従来と異なる。結果として projection ベース手法に対し 2 倍の速度と 0.3 倍のメモリで、IoU 差 0.7% の同等性能を達成している。

**読む理由**

BEV 知覚の主流が projection ベースに寄るなかで、depth の不確実性を明示的に持たせた unprojection 系の再評価という逆張りの方向性を示しており、実車適用を意識した速度・メモリ面の議論も含む。Gaussian Splatting の rasterization を生成ではなく知覚の特徴構成に使う応用例としても参考になる。

- Paper: https://arxiv.org/abs/2504.01957
- Code: -

## Gaussian Splatting

### Immediate 3D Gaussian Splat Reconstruction of Unordered Input with Global Consistency

arXiv 2026 / Gaussian Splatting

**概要**

無順序かつ大量の入力画像から3D Gaussian Splattingシーンを即時かつグローバルに一貫した形で再構成する手法を提案している。従来のStructure from Motionは全画像取得後でないと動作せず計算コストも高く、SLAM系の逐次再構成手法は順序通りの撮影しか扱えないという課題に対応する。視覚的場所認識モデルとcovisibilityグラフを用いた高速マッチング、クラスタベースのループクロージャ、大規模シーン対応の階層構造を組み合わせ、数千枚規模の画像でも即時フィードバック可能な再構成を実現している。

**新規性**

順序に依存しないout-of-order撮影に対しても即時フィードバックとグローバル整合性を両立させる点が新規であり、covisibilityグラフベースのマッチングとクラスタ型ループクロージャ、進行的階層構造によりスケーラビリティも確保している。

**読む理由**

大規模かつ動的・非順序な取得データからの高速3DGS再構成技術は、自動運転向けの地図・シーン再構成やオンラインHDマップ生成技術の基盤要素として応用可能であり、Gaussian Splattingの実運用化に向けた重要な進展として参照価値が高い。

- Paper: https://arxiv.org/abs/2607.14481
- Code: -

### 360-GeoGS: Geometrically Consistent Feed-Forward 3D Gaussian Splatting Reconstruction for 360 Images

arXiv 2026 / Gaussian Splatting

**概要**

360度画像から幾何的に一貫した3D Gaussian Splattingをfeed-forward方式で生成する手法を提案。従来のfeed-forward 3DGSは見た目の品質を重視し幾何的整合性が犠牲になっていた課題に対し、Depth-Normal幾何正則化によりレンダリング深度勾配と法線情報を結びつけ、Gaussianの回転・スケール・位置を教師信号として補正する。これにより点雲・表面再構成の精度向上を図る。

**新規性**

レンダリング品質重視だった既存のfeed-forward 3DGSに対し、深度勾配と法線を連動させるDepth-Normal正則化でGaussianパラメータを直接教師付けし、幾何的一貫性を明示的に強化した点が新規性。

**読む理由**

feed-forward型3DGSの幾何精度向上手法は、大規模屋外シーンの高速3D/4D再構成やマップ生成への応用可能性があり、地図生成・環境認識の技術動向として参考になる。

- Paper: https://arxiv.org/abs/2601.02102
- Code: -

### Vision-Only Gaussian Splatting for Collaborative Semantic Occupancy Prediction

AAAI 2026 / Gaussian Splatting

**概要**

複数の連結車両が情報を共有して遮蔽や単一車両のセンシング範囲の限界を克服する協調認識において、既存の視覚のみによる3D semantic occupancy予測手法は高通信コストな密な3Dボクセルか、深度推定精度に依存する2D平面特徴に頼らざるを得ない課題があった。本研究はスパースな3D semantic Gaussian splattingを中間表現として車両間で共有・融合する初の手法を提案し、近傍ベースのクロスエージェント融合で重複除去とノイズ抑制を行い、幾何と意味を同一プリミティブに統合することで深度教師信号への依存を減らし剛体アライメントを可能にしている。

**新規性**

密なボクセルや2D平面特徴に依存する従来の協調occupancy予測と異なり、スパースでオブジェクト中心のGaussianプリミティブを共有メッセージとして用いることで通信量を抑えつつ構造情報を保持する点が新しい。

**読む理由**

Gaussian Splattingを協調的な3D occupancy予測へ応用した事例であり、通信効率と精度の両立という自動運転マルチエージェント認識の実用課題に直結するため参考になる。

- Paper: https://arxiv.org/abs/2508.10936
- Code: -

### OnlinePG: Online Open-Vocabulary Panoptic Mapping with 3D Gaussian Splatting

CVPR 2026 / Gaussian Splatting

**概要**

オンラインでの3D Gaussian Splattingによるopen-vocabulary panoptic mappingを提案する論文。従来手法がオフライン処理かインスタンスレベル理解を欠く点を課題とし、スライディングウィンドウでローカルに3Dセグメントをクラスタリングして一貫したインスタンスを構築し、それをbidirectionalなGaussianインスタンスマッチングでグローバルマップに逐次統合する仕組みを提示している。最終的にVLM特徴を空間グリッドに埋め込み、open-vocabularyなシーン理解を実現する。

**新規性**

オフライン処理が主流だったopen-vocabulary panoptic mappingを、local-to-globalのスライディングウィンドウ方式と3D Gaussianインスタンスの明示的な空間属性グリッドによるマッチング・融合でオンライン化した点が従来との違い。

**読む理由**

3D Gaussian Splattingをリアルタイム制約のあるオンライン設定でシーン理解に応用する事例であり、自動運転向けのOccupancy/Scene Understanding手法の設計に転用できる知見を含む。

- Paper: https://arxiv.org/abs/2603.18510
- Code: -

### SplatFlow: Self-Supervised Dynamic Gaussian Splatting in Neural Motion Flow Field for Autonomous Driving

CVPR 2025 / Gaussian Splatting

**概要**

動的な市街地シーンをDynamic Gaussian Splattingで再構成する際、従来は追跡済み3Dバウンディングボックスなど高コストな物体レベルの教師情報が必要で、スケールしないという課題があった。SplatFlowは、LiDAR点群とGaussianの時間的な動きを連続的なmotion flow fieldとして陰関数で表すNeural Motion Flow Field (NMFF)を導入し、これを4D Gaussian表現と統合することで、3Dボックスの教師なし(自己教師的)に4D時空間表現を学習する。静的背景を3D Gaussian、動的物体を4D Gaussianとして分離表現し、NMFFが各4D Gaussianの時間対応を与えることで時系列特徴を集約し、動的部分のcross-view一貫性を高める。さらに2D foundation modelの特徴を4D表現へ蒸留して動的物体の識別を改善し、RGB/depth/flowのnovel view synthesisを行う。

**新規性**

追跡済み3Dバウンディングボックスによる物体レベル教師を前提とせず、motion flow fieldを陰関数でモデル化するNMFFの中に4D Gaussianを組み込むことで静的/動的分解と時間対応付けを同時に扱う点が従来手法との違いである。また2D foundation modelの特徴蒸留を4D時空間表現に組み合わせ、動的物体の識別を教師ラベルに頼らず補強している。

**読む理由**

アノテーションコストを避けつつ動的な走行シーンの4D再構成を行う方向性は、大規模な走行ログからの地図・シーン表現構築やデータ生成に直結する。Waymo/KITTIでの再構成・novel view synthesisにおける最新手法として、Gaussian Splattingベースの自動運転向けシーン表現の動向を押さえるうえで参考になる。

- Paper: https://arxiv.org/abs/2411.15482
- Code: -

### VoteSplat: Hough Voting Gaussian Splatting for 3D Scene Understanding

ICCV 2025 / Gaussian Splatting

**概要**

3DGSは高品質・リアルタイムなnovel view synthesisを実現している一方で、幾何と外観のモデリングに偏っており、シーンの意味的な理解が弱いという課題がある。本論文は、Hough votingの考え方を3DGSに統合したVoteSplatを提案する。SAMでinstance segmentationを行って2Dのvote mapを作り、Gaussian primitiveに空間オフセットベクトルを埋め込むことで、2Dの投票を3D空間の投票へ結び付けて物体中心を推定する。さらにdepth distortion制約で奥行き方向の定位を精緻化し、2Dの意味情報をvoting pointsを介して3D点群へ写す構成とする。

**新規性**

高次元CLIP特徴を各Gaussianに直接埋め込む従来のsemantic 3DGSとは異なり、Hough votingによる物体中心への投票を介して2D意味を3Dへ橋渡しし、学習コストを抑えつつ意味の曖昧さを回避している点が新しい。open-vocabulary localizationやclickベースの物体定位、hierarchical segmentationを同一枠組みで扱える。

**読む理由**

Gaussian Splattingを単なる再構成表現から「物体単位で問い合わせ可能な表現」へ拡張する流れを示す一例であり、地図・環境認識側で3DGS表現に意味やinstance情報を持たせる設計の参考になる。voting経由で2D基盤モデルの意味を3Dへ持ち上げる手法は、コスト制約のある車載側の意味付き再構成にも波及しうる。

- Paper: https://arxiv.org/abs/2506.22799
- Code: -

### Event-boosted Deformable 3D Gaussians for Dynamic Scene Reconstruction

ICCV 2025 / Gaussian Splatting

**概要**

RGBカメラの時間分解能不足によりdeformable 3D-GSが動きの中間情報を取得できない問題に対し、高時間分解能なイベントカメラの情報を組み合わせて動的シーン再構成を改善する手法を提案している。イベントの閾値モデリングと3D再構成を相互に強化するGS-Threshold Joint Modelingと、動的・静的領域を分離するDynamic-Static Decomposition戦略を導入している。

**新規性**

イベントカメラをdeformable 3D-GSに組み込んだ初めての手法であり、閾値モデリングと再構成を同時最適化する点、静的領域の不要な変形を避けて動的領域に計算を集中させる分解戦略が従来手法と異なる。

**読む理由**

動的シーンの高精度・高効率な3D-GS再構成手法であり、車載カメラ映像における動体を含む4D再構成やシーン理解の高度化に応用できる可能性がある。

- Paper: https://arxiv.org/abs/2411.16180
- Code: -

### CoDa-4DGS: Dynamic Gaussian Splatting with Context and Deformation Awareness for Autonomous Driving

ICCV 2025 / Gaussian Splatting

**概要**

自動運転のクローズドループシミュレーション用にフォトリアルな動的シーンを再現することを目指した論文。交通環境の複雑な動きを正確にレンダリングする難しさに対し、4D Gaussian Splatting (4DGS) にコンテキスト情報と時間的変形の認識を組み込む手法CoDa-4DGSを提案している。2D意味分割の基盤モデルで各Gaussianの4D意味特徴を自己教師的に学習させ、さらに隣接フレーム間でのGaussianの時間的変形を追跡する。

**新規性**

既存の4DGSが幾何や色の再構成に留まるのに対し、意味的特徴と時間変形特徴を集約・符号化してGaussianに変形補正の手がかりを与える点が新規性。

**読む理由**

動的シーンのGaussian Splatting表現に意味情報を組み込む設計は、occupancyやシーン理解タスクへの応用可能性があり、自動運転向け3D/4D再構成の技術動向として参考になる。

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Song_CoDa-4DGS_Dynamic_Gaussian_Splatting_with_Context_and_Deformation_Awareness_for_ICCV_2025_paper.html
- Code: -

### SplatAD: Real-Time Lidar and Camera Rendering with 3D Gaussian Splatting for Autonomous Driving

CVPR 2025 / Gaussian Splatting

**概要**

自動運転車のテストには多様な走行シナリオでの検証が必要だが、既存のNeRFベースのセンサーレンダリング手法はレンダリング速度が遅く大規模テストへの適用が難しい。SplatADは3D Gaussian Splattingを用いてカメラとlidarの両方を動的シーンでリアルタイムかつセンサーリアルにレンダリングする初の手法として、この速度の課題を解決する。ローリングシャッター効果、lidar強度、lidarのドロップアウトといったセンサー固有の現象を専用アルゴリズムでモデル化している。

**新規性**

従来の3DGS手法がカメラ画像のみに限定されていたのに対し、lidarデータも同時にレンダリングできる点が新規性であり、NeRFベース手法に比べて1桁高速なレンダリングを達成する。

**読む理由**

ログデータからのシミュレーション環境構築という文脈でGaussian Splattingを動的な走行シーン・マルチセンサーに拡張した事例であり、World Modelやシミュレーションベースのテスト・データ拡張の動向を追ううえで参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Hess_SplatAD_Real-Time_Lidar_and_Camera_Rendering_with_3D_Gaussian_Splatting_CVPR_2025_paper.html
- Code: -

### BezierGS: Dynamic Urban Scene Reconstruction with Bezier Curve Gaussian Splatting

ICCV 2025 / Gaussian Splatting

**概要**

自動運転シミュレータ向けに、街路シーンの静的・動的要素を分離して再構成する手法BezierGSを提案。従来手法は物体の姿勢アノテーションに依存していたが、動的物体の移動軌跡を学習可能なBezier曲線で表現することで大規模シーンへの適用を可能にした。Waymo Open DatasetとnuPlanベンチマークで、動的・静的シーン再構成と新規視点合成の両方で最先端手法を上回る性能を示した。

**新規性**

物体姿勢の高精度アノテーションに頼らず、学習可能なBezier曲線で動的物体の軌跡をモデル化し、姿勢誤差を自動補正する点が従来手法との違い。

**読む理由**

動的物体を含む大規模都市シーンのGaussian Splatting再構成は自動運転シミュレータや4D再構成研究の中核テーマであり、姿勢アノテーション依存を減らす設計は実応用へのスケーラビリティに直結する。

- Paper: https://arxiv.org/abs/2506.22099
- Code: -

### DeGauss: Dynamic-Static Decomposition with Gaussian Splatting for Distractor-free 3D Reconstruction

ICCV 2025 / Gaussian Splatting

**概要**

実世界のegocentric動画など動きの多い雑然としたシーンから、歩行者や手など動的な要素(distractor)を含まないクリーンな3Dシーンを復元することが難しいという課題に取り組んだ論文。DeGaussは3D Gaussian Splattingを前景(動的)用と背景(静的)用に分離し、確率的マスクで両者の合成を制御しながら独立に最適化する自己教師あり手法を提案する。NeRF-on-the-go、ADT、AEA、Hot3D、EPIC-Fieldsなど複数のベンチマークで既存手法を上回る性能を示している。

**新規性**

複雑なヒューリスティックや大量の教師信号に頼らず、前景・背景のGaussianを確率的マスクで疎結合に協調最適化する点が既存のdistractor除去手法との違い。

**読む理由**

動的物体と静的地図要素の分離は自動運転のシーン再構成・地図更新でも共通課題であり、Gaussian Splattingベースの動的静的分解技術の動向として参考になる。

- Paper: https://arxiv.org/abs/2503.13176
- Code: -

### RadarSplat: Radar Gaussian Splatting for High-Fidelity Data Synthesis and 3D Reconstruction of Autonomous Driving Scenes

ICCV 2025 / Gaussian Splatting

**概要**

自動運転向けレーダーセンサーのデータ合成と3D再構成を課題とし、受信機飽和やマルチパス反射といったレーダー特有のノイズをモデル化した上でGaussian Splattingと統合する手法RadarSplatを提案している。既存のレーダー向けニューラル表現がノイズ環境で性能劣化し、前処理済みのノイズ除去画像しか合成できない点を解決する。

**新規性**

レーダーノイズを明示的にモデル化してGaussian Splattingに組み込むことで、ノイズ込みの実写的なレーダー画像合成と幾何再構成の両立を実現している点が従来手法との違い。

**読む理由**

カメラ・LiDAR中心だったGaussian Splattingベースのシーン再構成を悪天候に強いレーダーへ拡張する事例であり、マルチモーダルなAD向け3D/4D再構成の動向を追う上で参考になる。

- Paper: https://arxiv.org/abs/2506.01379
- Code: -

### Robust and Efficient 3D Gaussian Splatting for Urban Scene Reconstruction

ICCV 2025 / Gaussian Splatting

**概要**

都市スケールのシーンを対象に、高速な再構成とリアルタイムレンダリングを実現する3D Gaussian Splattingフレームワークを提案している。シーン分割による並列学習、可視性ベースの画像選択、密度を予算制御するLOD戦略、マルチビュー間の見た目のばらつきを補正する外観変換モジュールを組み合わせている。さらに深度・スケール正則化やアンチエイリアシングで再構成品質を高めている。

**新規性**

従来手法に対し、Gaussian密度をユーザー指定予算で明示的に制御できるLOD機構と、多視点間の外観不整合を吸収する変換モジュールを統合した点が特徴。

**読む理由**

都市規模の大規模シーンを効率的かつ頑健に再構成する手法であり、自動運転向けの3Dシーン表現やマップ生成技術の動向として参照価値が高い。

- Paper: https://arxiv.org/abs/2507.23006
- Code: -

### AD-GS: Object-Aware B-Spline Gaussian Splatting for Self-Supervised Autonomous Driving

ICCV 2025 / Gaussian Splatting

**概要**

自動運転シミュレーション向けに、単一ログから動的都市シーンを高品質にフリービューポイントレンダリングする自己教師あり手法AD-GSを提案。手動の物体トラックレットアノテーションに頼らず、擬似2Dセグメンテーションでシーンを物体と背景に自動分解し、各物体を動的Gaussianと双方向時間可視性マスクで表現する。

**新規性**

局所的なB-splineカーブと大域的な三角関数を組み合わせた学習可能なモーションモデルにより、アノテーションなしで柔軟かつ精密な動的物体モデリングを実現し、可視性推論と物理的剛性正則化でロバスト性を高めている点が従来のアノテーション依存手法と異なる。

**読む理由**

アノテーションコストを排した動的シーンのGaussian Splatting再構成は、自動運転シミュレーション・データ生成の効率化に直結する重要な技術動向である。

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Xu_AD-GS_Object-Aware_B-Spline_Gaussian_Splatting_for_Self-Supervised_Autonomous_Driving_ICCV_2025_paper.html
- Code: -

## World Model

### Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models

arXiv 2026 / World Model

**概要**

ストリーミング型の自己回帰ビデオ拡散モデルは局所フレーム予測しか最適化しないため、長時間ロールアウトで幾何的なドリフトが蓄積し、静止または不自然な動きに劣化する問題がある。既存の3D Gaussian Splatting再構成に基づく報酬は静的シーンしか扱えず、実際の物体運動を再構成誤差とみなして罰してしまい、映像を静止させる方向にモデルを誘導してしまう。本研究Stream4Dは、この静的critic をシーンダイナミクスを明示的にモデル化するfeed-forwardな4D再構成報酬に置き換え、さらに自然なscene-flow量を促しジッターや非剛体アーティファクトを抑えるmotion priorを追加することで、この問題を解決する。

**新規性**

単一の剛体3D再構成に基づく静的一貫性報酬を、動的シーンを扱える4D再構成報酬とmotion priorの組み合わせに置き換えた点が従来との違い。

**読む理由**

自己回帰的な長時間ビデオ生成における4D一貫性の確保手法は、動的環境を扱うworld modelや将来のシーン予測(occupancy forecasting等)の設計にも応用しうるため。

- Paper: https://arxiv.org/abs/2608.19556
- Code: -

### DrivingGen: A Comprehensive Benchmark for Generative Video World Models in Autonomous Driving

ICLR 2026 / World Model

**概要**

自動運転向け動画生成world modelを評価する統一ベンチマークDrivingGenを提案。既存評価は視覚品質偏重で安全上重要な軌道妥当性・時間的一貫性・ego条件制御性を欠いており、多様な気象・地域・運転行動を含むデータセットと新指標群でこれらを同時評価する。14種のSOTAモデルを比較し、汎用モデルは見た目が良いが物理法則を破り、運転特化モデルは動きは自然だが視覚品質で劣るというトレードオフを明らかにした。

**新規性**

汎用動画品質指標に加え、軌道妥当性・エージェント一貫性・ego条件への制御性を統合的に測る点、および多様な収集源からの評価データセットを新規構築した点が従来のベンチマークと異なる。

**読む理由**

driving world modelの評価軸が乱立する中で標準化されたベンチマークを提示しており、今後この分野の研究比較や進捗判断の基準として参照される可能性が高い。

- Paper: https://arxiv.org/abs/2601.01528
- Code: -

### GaussianDWM: 3D Gaussian Driving World Model for Unified Scene Understanding and Multi-Modal Generation

CVPR 2026 / World Model

**概要**

既存の driving world model は入力条件付きの生成に特化していて、走行環境そのものを3Dで理解・推論する能力を欠いているという課題に取り組んだ論文。point cloud や BEV 特徴では言語情報と3D空間の対応付けが不正確になる点を問題視し、3D Gaussian をシーン表現の基盤に据えた統一フレームワークを提案している。各 Gaussian primitive に言語特徴を埋め込むことで、3Dシーン理解とマルチモーダル生成の両方を1つの枠組みで扱う。nuScenes と NuInteract で評価し、state-of-the-art を達成したと報告している。

**新規性**

言語特徴を Gaussian primitive の段階で埋め込む early modality alignment と、タスクに応じて冗長な Gaussian を削って LLM へコンパクトな3Dトークンを渡す language-guided sampling を導入した点が従来と異なる。さらに vision-language model が捉えた高レベルの言語条件と低レベルの画像条件を組み合わせる dual-condition 生成モデルを設計している。

**読む理由**

world model を単なる生成器ではなく3Dシーン理解の器として再定義する流れを示しており、Gaussian Splatting 表現が認識と生成を橋渡しする基盤になりうることを具体的に示している。地図生成・環境認識側でも、3D表現と言語・LLM の結合をどう設計するかの参考になる。

- Paper: https://arxiv.org/abs/2512.23180
- Code: -

### GenieDrive: Towards Physics-Aware Driving World Model with 4D Occupancy Guided Video Generation

CVPR 2026 / World Model

**概要**

自動運転向けの物理整合的なdriving world modelを提案。行動から直接動画を生成する従来手法は学習が難しく物理的に不整合な出力になりやすいため、まず4D occupancyを生成し、それを物理情報の基盤として動画生成に利用する2段階構成をとる。occupancyをtri-plane潜在表現に圧縮するVAEと、制御信号のoccupancy遷移への影響を捉えるMutual Control Attention (MCA)を導入し、VAEと予測モジュールをend-to-endで共同学習する。

**新規性**

単一の拡散モデルで行動から映像を直接生成する従来手法と異なり、4D occupancyを中間の物理表現として明示的に生成・活用する点、および高圧縮なtri-plane VAEとMCAによる制御信号のモデリング、Normalized Multi-View Attentionによるマルチビュー一貫性の確保が特徴。

**読む理由**

occupancy予測とマルチビュー動画生成を統合したworld model設計であり、closed-loop評価やOOD合成データ生成のための自動運転world model研究の最新動向を把握する上で参考になる。

- Paper: https://arxiv.org/abs/2512.12751
- Code: -

### GaussianWorld: Gaussian World Model for Streaming 3D Occupancy Prediction

CVPR 2025 / World Model

**概要**

カメラ入力からの3D occupancy prediction において、既存手法は過去フレームの特徴を単純に融合するだけで、走行シーンが連続的に変化するという事前知識を活かせていない点を問題視している。本論文はこのタスクを「現在のセンサ入力を条件とした4D occupancy forecasting」として捉え直し、シーンの時間変化を(1) 自車運動による静的シーンの整合、(2) 動的物体の局所的な移動、(3) 新たに観測された領域の補完、の3要素に分解する。これらの事前知識を3D Gaussian 表現の空間上で明示的に扱う Gaussian world model を構築し、現在のRGB観測を条件に次時刻のシーン状態を推論する。nuScenes で評価し、単一フレーム版に対して追加計算なしで mIoU を2%以上改善したと報告している。

**新規性**

過去フレーム特徴の融合ではなく、シーンの進化そのものを予測対象とする world model として occupancy prediction を定式化した点が従来と異なる。さらに、その進化を自車運動・動的物体の移動・新規観測領域の補完という解釈可能な3要素に分解し、3D Gaussian という疎な物体中心表現の空間上で扱っている。

**読む理由**

occupancy prediction と world model、そして 3D Gaussian 表現という近年の主要な流れが一本に統合された代表例であり、ストリーミング入力を前提とした環境認識の設計思想を把握するのに適している。静的・動的の分離という考え方は地図生成や逐次的な地図更新の枠組みにも通じる。

- Paper: https://arxiv.org/abs/2412.10373
- Code: -

### HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation

ICCV 2025 / World Model

**概要**

従来のDriving World Modelがシーン生成に特化し環境理解を欠いていた課題に対し、HERMESはBEV表現とLLMのcausal attentionを用いたworld queryを導入し、3Dシーン理解と未来シーン生成を単一フレームワークで同時に扱う手法を提案している。nuScenesおよびOmniDrive-nuScenesで有効性を検証している。

**新規性**

生成のみを対象としてきた既存DWMに対し、world queryによってBEV特徴にLLMの世界知識を注入し、理解タスクと生成タスクを一つのモデルで統一的に扱う点が従来との違いである。

**読む理由**

BEVベースの環境認識とWorld Modelの統合という潮流を示す代表例であり、シーン理解と予測生成を両立させる設計思想は今後のAD Perception研究の方向性を掴む上で参考になる。

- Paper: https://arxiv.org/abs/2501.14729
- Code: https://github.com/LMD0311/HERMES

### MaskGWM: A Generalizable Driving World Model with Video Mask Reconstruction

CVPR 2025 / World Model

**概要**

行動から環境変化を予測するdriving world modelにおいて、既存のpixel-level拡散生成モデルは予測時間や汎化性に限界があるという課題を扱う。本研究はDiTベースの拡散生成にMAE的なマスク再構成によるfeature-level学習を組み合わせ、拡散用マスクトークンと時空間方向へ拡張した行毎マスク・行毎cross-view moduleを設計してMaskGWMを提案する。長期予測用のMaskGWM-longとマルチビュー生成用のMaskGWM-mviewの2種を用意し、nuScenes・OpenDV-2K・Waymo(zero-shot)で評価している。

**新規性**

単純なpixel-level生成損失のみに頼らず、MAEスタイルのマスク再構成タスクを拡散過程・時空間・マルチビューに合わせて再設計し、DiT構造に統合した点が従来のdriving world modelと異なる。

**読む理由**

world modelは環境認識・シーン理解と連続する将来予測の要であり、長期予測・マルチビュー生成・zero-shot汎化への対応方針は他のAD perception手法の設計にも参考になる。

- Paper: https://arxiv.org/abs/2502.11663
- Code: -

### End-to-End Driving with Online Trajectory Evaluation via BEV World Model

ICCV 2025 / World Model

**概要**

end-to-end自動運転において生成された走行軌道の安全性をどう評価するかが課題。本研究はBEV空間の world model(WoTE)で将来のBEV状態を予測し、その予測結果を用いて複数の候補軌道を評価・選択するフレームワークを提案する。NAVSIMおよびCARLAベースのBench2Driveで検証している。

**新規性**

画像レベルのworld modelに比べ計算コストの低いBEV空間でのworld modelを採用し、既存のBEV空間交通シミュレータの出力をそのまま教師信号として使える点が従来との違い。

**読む理由**

軌道評価にworld modelを組み込む設計は、occupancy forecastingとplanningを繋ぐ実装例として地図・環境認識研究の応用先を考える上で参考になる。

- Paper: https://arxiv.org/abs/2504.01941
- Code: https://github.com/liyingyanUCAS/WoTE

### World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model

ICCV 2025 / World Model

**概要**

本研究は、コストの高い知覚アノテーションに依存しないend-to-end自動運転を目指し、視覚基盤モデルから得たシーン特徴と運転意図を用いてlatent world modelを構築する。現在のシーン特徴と意図に基づき複数の候補軌道と将来のlatent状態を予測し、実際の将来観測との自己教師あり整合によって知覚ラベルなしで学習する。生成した複数軌道はworld model selectorモジュールで評価・選択される。

**新規性**

従来のend-to-end手法が手作業の知覚アノテーションに強く依存するのに対し、視覚基盤モデルの空間・意味的事前情報を用いたlatent world modelと自己教師あり将来予測により、アノテーションフリーで軌道生成・評価を行う点が異なる。

**読む理由**

知覚アノテーションへの依存を減らしつつ計画性能を高めるworld model駆動のend-to-end設計は、occupancy/BEV系の知覚から計画までを繋ぐ潮流の代表例であり、World Modelとplanningの統合動向を追う上で参考になる。

- Paper: https://arxiv.org/abs/2507.00603
- Code: https://github.com/ucaszyp/World4Drive

### Epona: Autoregressive Diffusion World Model for Autonomous Driving

ICCV 2025 / World Model

**概要**

動画拡散モデルは固定長フレーム列の同時分布を学習するため可変長・長時間の未来予測や経路計画との統合が難しい。Eponaは時空間を分離し自己回帰的に局所分布を逐次生成することで、高解像度かつ長時間の未来映像生成と軌道予測を単一のエンドツーエンド枠組みで実現する。自己回帰ループ特有の誤差蓄積を抑えるchain-of-forward学習も導入している。

**新規性**

時間方向のダイナミクスと空間的な将来生成を切り離すdecoupled spatiotemporal factorizationと、軌道予測と映像予測をモジュール化して統合した点が既存のグローバル同時分布モデリング型video diffusion world modelとの違い。

**読む理由**

映像生成ベースのworld modelを実時間の経路計画器として使う設計であり、occupancyやBEV予測とは異なるアプローチでのAD向けworld model研究の方向性を把握する上で参考になる。

- Paper: https://arxiv.org/abs/2506.24113
- Code: -

### DriveArena: A Closed-loop Generative Simulation Platform for Autonomous Driving

ICCV 2025 / World Model

**概要**

実世界の道路網上で走行エージェントを評価するためのクローズドループシミュレータDriveArenaを提案。任意の都市の道路地図から現実的な交通流を生成するTraffic Managerと、無限に自己回帰生成できる条件付き生成モデルWorld Dreamerの2要素で構成される。実画像を処理できる任意の運転エージェントがこの中で走行・評価できるモジュール構成を持つ。

**新規性**

従来のルールベース・記録再生型シミュレータと異なり、生成モデルによる無限自己回帰で多様な交通シナリオ画像をクローズドループに生成し、世界中の道路網を条件として使える点が特徴。

**読む理由**

生成モデルベースのクローズドループ評価基盤は、World Model系研究や自動運転エージェントのベンチマーク動向を追う上で重要な参照点となる。

- Paper: https://arxiv.org/abs/2408.00415
- Code: -

## Scene Understanding

### Distill, Diffuse, Segment: Unsupervised 3D Semantic Segmentation for Autonomous Driving Based on Multi-Level Distillation and Graph Diffusion

arXiv 2026 / Scene Understanding

**概要**

点群の密なアノテーションコストとロングテール環境下での小物体検出困難という課題に対し、教師なし3Dセマンティックセグメンテーション手法DDSを提案。粗density→細粒度のマスクカスケードで多様なスケールの物体を捉え、リージョン単位の多段蒸留で自己教師あり視覚知識を点/マスク/プロトタイプの各レベルで転移し、リスタート型グラフ拡散でsuperpoint間の文脈情報を効率的に伝播する。

**新規性**

既存手法が抱えるスケール変動への弱さ・領域内一貫性/領域間識別性の欠如・グラフ固有値分解を要する非効率な伝播という3課題を、マルチ粒度マスク・多段蒸留・restartベース拡散でそれぞれ個別に解決している点が新しい。

**読む理由**

アノテーション不要で3Dシーン理解を進める手法は地図生成・環境認識のデータ効率化に直結し、実路データでの性能改善が報告されている点でトレンド把握に有用。

- Paper: https://arxiv.org/abs/2605.08293
- Code: -

### PanDA: Unsupervised Domain Adaptation for Multimodal 3D Panoptic Segmentation in Autonomous Driving

CVPR 2026 / Scene Understanding

**概要**

本論文は、天候・時間帯・場所・センサ構成などのドメインシフト下で性能が劣化する、自動運転向けマルチモーダル3Dパノプティックセグメンテーション(mm-3DPS)の教師なしドメイン適応(UDA)を扱う。既存の疑似ラベル手法は高信頼領域のみを残すため、パノプティック分割に不可欠なマスクの完全性が損なわれる問題を指摘し、PanDAという専用UDAフレームワークを提案する。

**新規性**

片方のモダリティが劣化する状況を模した非対称マルチモーダル拡張と、2D/3D両モダリティからドメイン不変な事前情報を抽出するdual-expert疑似ラベル精緻化モジュールにより、単一モダリティ劣化への頑健性と疑似ラベルの完全性を同時に高めている点が従来の3Dセマンティックセグメンテーション向けUDA手法との違い。

**読む理由**

実運用で避けられないドメインシフト(天候・照明・センサ差異)への頑健性は、環境認識モデルを実車展開する際の重要課題であり、マルチモーダル融合とパノプティック分割の両面を扱う本研究は最新動向を把握する上で参考になる。

- Paper: https://arxiv.org/abs/2604.19379
- Code: -

### HiLoTs: High-Low Temporal Sensitive Representation Learning for Semi-Supervised LiDAR Segmentation in Autonomous Driving

CVPR 2025 / Scene Understanding

**概要**

自動運転向けLiDAR点群セマンティックセグメンテーションにおいて、アノテーションコストを抑えるための半教師あり学習手法を提案。近い物体は時間的に安定し遠い物体は変化しやすいという観察から、連続フレームから高時間感度・低時間感度の2種の表現を学習し、cross-attentionで融合する。さらにteacher-studentフレームワークでラベルあり/なしブランチの表現を揃え、大量の未ラベルデータを活用する。

**新規性**

隣接2フレームなど短期的な時間情報のみを使う従来手法と異なり、距離に応じた時間感度の違いに着目した長期的な時間表現を明示的に分離・融合する点が新しい。

**読む理由**

LiDARベースのシーン理解において時間的文脈をどう設計に組み込むかは、Occupancy予測やマップ更新など他の時系列タスクにも応用可能な視点を提供する。

- Paper: https://arxiv.org/abs/2503.17752
- Code: -

### D^3CTTA: Domain-Dependent Decorrelation for Continual Test-Time Adaption of 3D LiDAR Segmentation

CVPR 2025 / Scene Understanding

**概要**

走行中に観測ドメインが変化し続ける状況で、事前学習済みLiDARセグメンテーションモデルをオンラインかつバックプロパゲーションなしで適応させる手法を提案している。点群の距離依存的な密度差とドメイン間の特徴分布差、特徴間の高い相関がセグメンテーション精度を下げる要因であるとし、それぞれに対応するモジュールを設計している。

**新規性**

距離に応じたプロトタイプ学習でLiDAR特有の幾何的事前分布を取り込み、ドメイン依存のデコリレーションでドメイン間・カテゴリ間の特徴相関を低減する点が、逆伝播や大バッチに依存する既存のcontinual test-time adaptation手法との違いである。

**読む理由**

実運用で避けられないドメインシフト下でのLiDARセグメンテーションの頑健性は自動運転の認識信頼性に直結するため、CTTA手法の動向を把握する上で参考になる。

- Paper: https://openaccess.thecvf.com/content/CVPR2025/html/Zhao_D3CTTA_Domain-Dependent_Decorrelation_for_Continual_Test-Time_Adaption_of_3D_LiDAR_CVPR_2025_paper.html
- Code: -

### Distilling Diffusion Models to Efficient 3D LiDAR Scene Completion

ICCV 2025 / Scene Understanding

**概要**

拡散モデルベースの3D LiDARシーン補完は品質が高い一方サンプリングが遅く、自動運転の実時間認識に不向きという課題がある。本論文はScoreLiDARという蒸留手法を提案し、拡散モデルを少ないステップで動作する軽量モデルに変換する。さらに幾何構造を保持するためのStructural Loss(シーン全体項と点単位項)を導入し補完品質を維持する。

**新規性**

既存の拡散モデルによるLiDARシーン補完がステップ数に依存して低速だったのに対し、蒸留により推論ステップ数を削減しつつ、構造保持のための専用損失で品質劣化を抑える点が新しい。

**読む理由**

LiDARシーン補完はOccupancy予測やマップ生成の前段処理として重要であり、推論速度と品質のトレードオフ改善は実車搭載を見据えた認識パイプライン設計の参考になる。

- Paper: https://arxiv.org/abs/2412.03515
- Code: https://github.com/happyw1nd/ScoreLiDAR

## Reconstruction

### RoadVGGT: Road-Structure-Aware Feed-Forward Road Surface Reconstruction

arXiv 2026 / Reconstruction

**概要**

大規模道路サーフェス再構成を、シーンごとの最適化なしにfeed-forwardで行う手法RoadVGGTを提案。幾何学的foundation modelでマルチビュー画像・pose・depthからGaussian属性を予測し、metric座標系に整合させたうえでroad平面上でconfidence-weightedなgrid fusionにより冗長Gaussianを統合する。歩道との境界などの脆弱な道路構造はcategory-aware groupingとjunction保護で扱う。

**新規性**

従来の道路特化最適化手法がシーンごとの学習と軌道依存のカバレッジ設計を必要とするのに対し、test-time最適化なしのfeed-forward推論でコンパクトなGaussian道路表現を生成する点が異なる。

**読む理由**

HD Map生成やGaussian Splattingを用いた大規模屋外シーン再構成のスケーラビリティ向上という観点で、地図生成研究の動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2607.23758
- Code: -

### LiDAR Prompted Spatio-Temporal Multi-View Stereo for Autonomous Driving

arXiv 2026 / Reconstruction

**概要**

自動運転で高精度なメートル単位の深度を得るための多視点ステレオ手法DriveMVSを提案。疎なLiDAR点をコスト volumeへのハードな幾何プライアと、特徴融合によるソフトなガイダンスの両方として活用し、空間・時間方向の一貫性を持つ深度推定を実現する。空間・時間デコーダにより隣接フレーム間の整合性も確保している。

**新規性**

LiDARを単純な補助入力としてではなく、コスト volume上の絶対スケール固定と特徴レベルの融合という二重の形で組み込む点、および複数手がかりを統合するtriple-cue combinerと時空間デコーダを組み合わせている点が従来のMVS手法と異なる。

**読む理由**

占有予測やシーン再構成の入力として使われるメトリック深度の精度・時間的一貫性・領域汎化を同時に扱っており、認識・地図生成パイプラインの前段技術として動向を追う価値がある。

- Paper: https://arxiv.org/abs/2603.03765
- Code: -

### DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving

CVPR 2026 / Reconstruction

**概要**

自動運転における動的シーン再構成では移動物体や時間変化の扱いが課題となる。本研究はVGGTを静的3D復元から動的4D復元へ拡張したDynamicVGGTを提案し、現在と将来の点群マップを共通の参照座標系で同時予測することで時間的対応を通じた動的点表現の学習を行う。Motion-aware Temporal Attentionで時間依存性を捉え、Dynamic 3D Gaussian Splatting Headでシーンフロー教師あり学習によりGaussian速度を予測し幾何を精緻化する。

**新規性**

静的復元に強い既存のfeed-forward 3Dモデル(VGGT)を、明示的なGaussian速度予測と時間的注意機構により動的4D復元へ拡張した点が新規性。

**読む理由**

feed-forwardな4D動的シーン復元は地図生成・環境認識における動的物体表現の基盤技術であり、Gaussian Splattingベースの手法動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2603.08254
- Code: -

### Ov3R: Open-Vocabulary Semantic 3D Reconstruction from RGB Videos

CVPR 2026 / Reconstruction

**概要**

Ov3Rは、RGB動画ストリームからオープン語彙の意味的3D再構成を行うフレームワークである。重なり合うクリップから密な点群マップと物体レベルの意味情報を同時に予測するCLIP3Rと、2D特徴を空間・幾何・意味情報を統合した記述子として3Dへ持ち上げる2D-3D OVSモジュールから構成される。

**新規性**

従来手法とは異なり、CLIPによる意味情報を再構成プロセス自体に組み込むことで、大域的に一貫した幾何形状と細粒度の意味的整合を同時に達成している点が新しい。

**読む理由**

RGB動画のみからの密な3D再構成とオープン語彙セグメンテーションを統合するアプローチは、地図生成やシーン理解におけるオープンボキャブラリ対応の潮流を把握するうえで参考になる。

- Paper: https://arxiv.org/abs/2507.22052
- Code: -

## Occupancy Forecasting

### TGRIP: A Text-Guided Approach to Vehicle Instance Prediction in Autonomous Driving

arXiv 2026 / Occupancy Forecasting

**概要**

BEV上でのend-to-endな将来インスタンス予測(周辺車両の位置・挙動予測)を扱う研究。既存手法がoccupancy回帰やoptical flowなど幾何的教師信号のみに頼り、物体固有の意味的挙動(追い越しや交差点での振る舞いなど)を捉えられない点を課題とする。Vision-Language Foundation Modelsを用いてマルチカメラ画像から意味情報を付加したBEVマップを生成し、teacher-student構成でこれを補助教師信号として学習に組み込むTGRIPを提案している。

**新規性**

幾何的教師信号のみだった従来のBEV instance predictionに対し、VLMベースの意味的BEVマップを補助教師として初めて統合し、意味理解と時系列予測タスクを結びつけた点が新規性。

**読む理由**

occupancy/BEVベースの将来予測に意味的priorを組み込むアプローチであり、幾何情報偏重の従来手法からの発展方向として地図生成・動的シーン理解の研究動向を追う上で参考になる。

- Paper: https://arxiv.org/abs/2607.04812
- Code: https://github.com/miguelag99/TGRIP

### SelfOccFlow: Towards end-to-end self-supervised 3D Occupancy Flow prediction

arXiv 2026 / Occupancy Forecasting

**概要**

自動運転における3D occupancyとその動きの推定には従来occupancy/flowの人手アノテーションやbounding boxからの速度ラベル、事前学習済みoptical flowモデルが必要だった。本研究はこれらの外部教師を一切使わない自己教師あり手法を提案する。シーンを静的・動的なsigned distance fieldに分離し、時間方向の特徴集約により動きを暗黙的に学習する。加えて特徴のcosine類似度から得られる自己教師ありのflow手がかりを導入する。

**新規性**

occupancy/flowアノテーション・速度ラベル・外部flowモデルのいずれにも依存せず、静的/動的SDFの分離と特徴類似度ベースのflow手がかりのみでend-to-endに学習する点が従来手法との違い。

**読む理由**

occupancy forecasting研究はアノテーションコストの高さが導入のボトルネックであり、完全自己教師あり化のアプローチは今後のスケーラブルな環境認識の方向性を示す好例。

- Paper: https://arxiv.org/abs/2602.23894
- Code: -

### UniOcc: A Unified Benchmark for Occupancy Forecasting and Prediction in Autonomous Driving

ICCV 2025 / Occupancy Forecasting

**概要**

自動運転向けのoccupancy predictionとoccupancy forecastingを統一的に評価するベンチマークUniOccを提案。nuScenes・Waymoの実データとCARLA・OpenCOODのシミュレータデータを統合し、2D/3D occupancyラベルとper-voxel flowを付与している。既存研究がground truthに依存した疑似ラベル評価に頼っていた問題に対し、ラベル非依存の新規評価指標を導入し、頑健な評価を可能にしている。

**新規性**

複数の実データ・シミュレータデータセットを統合した点と、ground truthを必要としない新しい評価指標を導入した点が従来のoccupancyベンチマークとの違い。

**読む理由**

occupancy prediction/forecasting分野で標準的な評価基盤となりうるベンチマークであり、今後の手法比較や評価指標選定の参考になる。

- Paper: https://arxiv.org/abs/2503.24381
- Code: -

## Open-world

### Contrastive Learning-Driven Traffic Sign Perception: Multi-Modal Fusion of Text and Vision

arXiv 2025 / Open-world

**概要**

交通標識認識において、ロングテール分布と小物体・多スケールという2つの課題に対処する2段階手法を提案。検出にはRepVL-PANとSPD-Convを組み込んだNanoVerse YOLOを、分類にはViT視覚特徴とルールベースBERTの意味特徴を対照学習させるTSR-MCLを用い、頻度に依存しない頑健な表現を学習する。TT100Kデータセットでロングテール全クラス検出において高い性能を達成した。

**新規性**

オープン語彙検出と視覚-言語のマルチモーダル対照学習を組み合わせ、従来のCNNベース手法が苦手とする低頻度・分布外クラスの認識精度を、クラス不均衡に頑健な表現学習で改善している点が新しい。

**読む理由**

小物体検出とロングテール分布への対処は自動運転の知覚全般（標識に限らず稀少物体検出）に共通する課題であり、open-vocabulary検出と対照学習の組み合わせ方が参考になる。

- Paper: https://arxiv.org/abs/2507.23331
- Code: -

### Learning to Identify Out-of-Distribution Objects for 3D LiDAR Anomaly Segmentation

CVPR 2026 / Open-world

**概要**

自動運転向けのLiDARベース3D意味セグメンテーションにおいて、既知クラスに含まれない未知物体(anomaly)を検出する課題を扱う論文。既存手法の多くが2D画像処理の後処理手法を3Dに流用しているのに対し、特徴空間で直接inlierクラスの分布をモデル化し異常サンプルを制約する新手法を提案する。あわせて、既存の3D LiDAR anomaly segmentationデータセットが単純すぎる点を補うため、既存の意味セグメンテーションベンチマークを基にした実データと合成データを混合した新データセット群も提示する。

**新規性**

2D由来の後処理的アプローチではなく、特徴空間でinlierクラス分布を直接モデル化して異常を検出する点、および複雑・多様な環境と多数の異常物体を含む新規データセットを提供する点が従来との違い。

**読む理由**

自動運転の3D認識において未知物体検出はOpen-world Perceptionの中核課題であり、LiDARベースの手法とデータセット整備の動向を追ううえで参考になる。

- Paper: https://arxiv.org/abs/2604.23604
- Code: -

### OV-SCAN: Semantically Consistent Alignment for Novel Object Discovery in Open-Vocabulary 3D Object Detection

ICCV 2025 / Open-world

**概要**

自動運転向けのopen-vocabulary 3D物体検出において、3D検出器とVLMを組み合わせる際に3D特徴と2D特徴の対応付けが意味的に食い違い、未知クラスの認識精度が落ちるという課題を扱う。OV-SCANは、正確な3Dアノテーションの発見と、遮蔽・解像度・アノテーション由来のノイズで質の低い3D-2D対応ペアを除去する2つの戦略で、意味的に一貫したクロスモーダル整合を実現する。

**新規性**

既存手法が3D-2D特徴ペアの生成品質を問わずに整合を取っていたのに対し、ノイズを含む対応ペアを明示的にフィルタリングして整合の意味的一貫性を担保する点が異なる。

**読む理由**

open-vocabulary 3D検出はクローズドセットの物体検出を超えて未知物体を扱うopen-world知覚の中核課題であり、クロスモーダル整合の質を上げる工夫は今後の類似手法設計の参考になる。

- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Chow_OV-SCAN_Semantically_Consistent_Alignment_for_Novel_Object_Discovery_in_Open-Vocabulary_ICCV_2025_paper.html
- Code: -

## Topology

### HGeo-TopoMap: Boosting Topological Mapping with Hierarchical Geometric Priors

arXiv 2026 / Topology

**概要**

実世界に明示的な標示がないセンターラインの検出が困難であるという課題に対し、HGeo-TopoMapは事前地図(IPMで得た道路構造マップ)から抽出した幾何・意味特徴への注意機構と、センターライン間の幾何的な向きの一致を利用した特徴整合の2段階で、トポロジカルマッピングの精度を高める。OpenLane-V2のcenterline・lane segment・robustnessベンチマークで評価している。

**新規性**

明示的な事前地図由来の特徴に対するprior-mask attentionと、センターライン instance 間の幾何的整合性を強制するgeometry-aware decoderを組み合わせ、階層的に事前知識を活用する点が従来手法との違い。

**読む理由**

センターライン検出はオンラインHDマップ・トポロジー推定の中心的な難所であり、事前地図の活用と幾何的整合性による頑健性向上のアプローチは同分野の手法設計の参考になる。

- Paper: https://arxiv.org/abs/2607.21281
- Code: https://github.com/lynn-yu/HGeo-TopoMap

### TopoHR: Hierarchical Centerline Representation for Cyclic Topology Reasoning in Driving Scenes with Point-to-Instance Relations

CVPR 2026 / Topology

**概要**

自動運転シーンにおけるcenterline検出とtopology推論を統合的に扱う論文。従来手法はcenterlineをインスタンス単位で検出した後、簡易なMLPでtopologyを推論しており、点とインスタンス間(P2I)の関係性を軽視していた。TopoHRはpoint query・instance query・semantic representationからなる階層的centerline表現を導入し、検出とtopology推論が相互に反復強化し合うend-to-endフレームワークを提案する。

**新規性**

point-to-instance関係とinstance-to-instance関係を単一アーキテクチャ内で同時に捉える階層的topology推論モジュールを導入し、検出とtopology推論を循環的(cyclic)に相互作用させる点が従来の逐次パイプラインと異なる。

**読む理由**

OpenLane-V2ベンチマークでDET_lとTOP_llを大幅に更新しており、lane topology推論の最新SOTA動向を把握する上で参照価値が高い。

- Paper: https://openaccess.thecvf.com/content/CVPR2026/html/Bai_TopoHR_Hierarchical_Centerline_Representation_for_Cyclic_Topology_Reasoning_in_Driving_CVPR_2026_paper.html
- Code: -

### T2SG: Traffic Topology Scene Graph for Topology Reasoning in Autonomous Driving

CVPR 2025 / Topology

**概要**

自動運転のHDマップ生成において、レーン同士やレーンと交通標識(右折等)の関係性を明示的にモデル化したTraffic Topology Scene Graph(T2SG)を新たに定義し、それを生成する一段階のTransformerであるTopoFormerを提案している。TopoFormerはレーン中心線間の幾何距離を利用して大域情報を集約するLane Aggregation Layerと、交差点や直進などの妥当な道路構造を反実仮想的介入でモデル化するCounterfactual Intervention Layerから構成される。

**新規性**

従来のHDマップ手法が見落としていた、道路標識に制御・誘導されるレーン間トポロジー関係を明示的なシーングラフとして定式化し、反実仮想介入層により道路構造の妥当性を学習させる点が新しい。

**読む理由**

OpenLane-V2ベンチマークでSOTA(46.3 OLS)を達成しており、topology reasoningを介したオンラインHDマップ生成研究の最新動向を把握する上で参照価値が高い。

- Paper: https://arxiv.org/abs/2411.18894
- Code: https://github.com/MICLAB-BUPT/T2SG

## Map Update

### NavMapFusion: Diffusion-based Fusion of Navigation Maps for Online Vectorized HD Map Construction

WACV 2026 / Map Update

**概要**

オンラインでベクトル化HDマップを構築する際、車載センサからの高精度だが局所的な情報と、OpenStreetMapのような粗い/古いおそれのあるナビゲーション用SDマップを融合する課題を扱う。提案手法NavMapFusionは拡散モデルを用い、SDマップとセンサ由来の推定結果の食い違いをノイズとみなして段階的にデノイズすることで、両者を統合したマップ表現を生成する。

**新規性**

SDマップとセンサ観測の不整合を拡散過程のノイズとして扱う点が新しく、整合する領域を強化し古くなった/誤った区間を抑制する仕組みをdiffusionのフレームワークに組み込んでいる。

**読む理由**

SDマップなどの低精度事前情報を高精度センサ情報と融合してオンラインHDマップ構築の精度・範囲を伸ばすアプローチであり、地図生成分野でのprior活用手法の動向として参考になる。

- Paper: https://arxiv.org/abs/2512.03317
- Code: https://github.com/tmonnin/navmapfusion
