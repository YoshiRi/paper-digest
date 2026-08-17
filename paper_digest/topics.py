"""重点テーマの定義と、キーワードベースの関連度スコアリング。

LLM に投げる前の一次フィルタ。ここで明らかに無関係なものを落として、
残りを LLM が abstract を読んで最終判定する。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Topic:
    name: str                                   # 出力に出る短いトピック名
    strong: list[str] = field(default_factory=list)  # これだけで該当と見なせる語
    weak: list[str] = field(default_factory=list)    # 補助的な語
    queries: list[str] = field(default_factory=list)  # 検索クエリ用フレーズ


TOPICS: list[Topic] = [
    Topic(
        name="HD Map",
        strong=["hd map", "hdmap", "high-definition map", "vectorized map", "vector map",
                "online mapping", "map construction", "maptr", "bevformer map", "lane graph"],
        weak=["map element", "polyline", "bev", "birds-eye-view", "bird's-eye-view"],
        queries=["online HD map construction", "vectorized HD map", "high-definition map perception"],
    ),
    Topic(
        name="Topology",
        strong=["lane topology", "road topology", "topology reasoning", "lane graph",
                "centerline", "road network extraction", "openlane"],
        weak=["lane detection", "traffic element", "connectivity", "graph reasoning"],
        queries=["lane topology reasoning autonomous driving", "road network graph extraction"],
    ),
    Topic(
        name="Map Update",
        strong=["map update", "map maintenance", "map change detection", "map reconstruction",
                "crowdsourced map", "map merging", "map fusion"],
        weak=["change detection", "localization prior", "sd map", "standard definition map"],
        queries=["HD map update change detection", "crowdsourced map construction driving"],
    ),
    Topic(
        name="3D Detection",
        strong=["3d object detection", "3d detection", "monocular 3d detection", "bev detection",
                "lidar detection", "multi-view 3d object"],
        weak=["nuscenes", "waymo", "kitti", "point cloud", "detr3d", "voxel"],
        queries=["3D object detection autonomous driving", "BEV 3D object detection"],
    ),
    Topic(
        name="Scene Understanding",
        strong=["3d scene understanding", "3d semantic segmentation", "panoptic segmentation",
                "scene graph", "lidar segmentation", "semantic occupancy"],
        weak=["point cloud segmentation", "instance segmentation", "scene completion"],
        queries=["3D scene understanding autonomous driving", "LiDAR semantic segmentation outdoor"],
    ),
    Topic(
        name="Occupancy",
        strong=["occupancy prediction", "semantic occupancy", "occupancy network",
                "scene completion", "occ3d", "surroundocc", "occupancy grid learning"],
        weak=["voxel", "occupancy", "tpvformer"],
        queries=["3D semantic occupancy prediction", "occupancy network autonomous driving"],
    ),
    Topic(
        name="Occupancy Forecasting",
        strong=["occupancy forecasting", "4d occupancy", "occupancy flow", "future occupancy",
                "occupancy world model"],
        weak=["forecasting", "future prediction", "temporal occupancy"],
        queries=["4D occupancy forecasting driving", "occupancy flow prediction"],
    ),
    Topic(
        name="Gaussian Splatting",
        strong=["gaussian splatting", "3dgs", "3d gaussians", "4d gaussian"],
        weak=["radiance field", "nerf", "rasterization", "novel view synthesis"],
        queries=["gaussian splatting driving scene", "3D gaussian splatting reconstruction"],
    ),
    Topic(
        name="Reconstruction",
        strong=["3d reconstruction", "4d reconstruction", "dynamic scene reconstruction",
                "neural radiance field", "novel view synthesis", "scene reconstruction"],
        weak=["nerf", "sdf", "photometric", "multi-view stereo", "depth estimation"],
        queries=["dynamic 3D scene reconstruction driving", "4D reconstruction urban scene"],
    ),
    Topic(
        name="Open-world",
        strong=["open-world", "open world perception", "open-vocabulary", "open vocabulary",
                "zero-shot detection", "unknown object", "corner case", "out-of-distribution"],
        weak=["clip", "foundation model", "vision-language", "anomaly"],
        queries=["open-vocabulary 3D perception driving", "open-world detection autonomous driving"],
    ),
    Topic(
        name="World Model",
        strong=["world model", "driving world model", "generative simulation",
                "neural simulator", "future scene generation", "video generation driving"],
        weak=["diffusion", "autoregressive", "rollout", "latent dynamics"],
        queries=["driving world model generation", "world model autonomous driving simulation"],
    ),
    Topic(
        name="AD Perception",
        strong=["autonomous driving perception", "end-to-end driving", "bev perception",
                "multi-modal fusion driving", "camera-lidar fusion", "motion forecasting"],
        weak=["autonomous driving", "self-driving", "ego vehicle", "nuscenes", "planning"],
        queries=["autonomous driving perception", "end-to-end autonomous driving perception"],
    ),
]

TOPIC_NAMES = [t.name for t in TOPICS]

# 分野コンテキスト。これが全く無い論文は、キーワードが当たっても弾く方向に効かせる。
DOMAIN_TERMS = [
    "autonomous driving", "self-driving", "driving", "vehicle", "traffic", "road", "lane",
    "urban scene", "street", "nuscenes", "waymo", "kitti", "argoverse", "lidar", "bev",
    "bird's-eye-view", "birds-eye-view", "3d", "point cloud", "robot", "outdoor scene",
]

STRONG_W, WEAK_W, DOMAIN_W = 3.0, 1.0, 1.5
DEFAULT_THRESHOLD = 4.0


def contains_phrase(text: str, phrase: str) -> bool:
    """語境界を見た部分一致。"bev" が "bevel" に当たらないようにする。"""
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", text) is not None


def score_paper(title: str, abstract: str) -> tuple[float, list[str]]:
    """(関連度スコア, 該当トピック一覧) を返す。

    タイトル中のヒットは abstract 中よりも重く数える。
    """
    t, a = (title or "").lower(), (abstract or "").lower()
    text = f"{t} {a}"

    matched: list[tuple[float, str]] = []
    total = 0.0
    for topic in TOPICS:
        s = 0.0
        for kw in topic.strong:
            if contains_phrase(t, kw):
                s += STRONG_W * 1.5
            elif contains_phrase(a, kw):
                s += STRONG_W
        for kw in topic.weak:
            if contains_phrase(text, kw):
                s += WEAK_W
        if s > 0:
            matched.append((s, topic.name))
            total += s

    domain_hits = sum(1 for d in DOMAIN_TERMS if contains_phrase(text, d))
    if domain_hits:
        total += min(domain_hits, 3) * DOMAIN_W
    else:
        # 自動運転/3D 文脈が皆無ならほぼ対象外
        total *= 0.4

    matched.sort(key=lambda x: -x[0])
    return round(total, 2), [name for _, name in matched]


def default_queries() -> list[str]:
    """--query 未指定時に使う検索フレーズ。"""
    qs: list[str] = []
    for t in TOPICS:
        qs.extend(t.queries)
    return qs


def keywords_for_prefilter() -> list[str]:
    """タイトルだけを見る安価な事前フィルタ用(CVF 一覧など)。"""
    kws: set[str] = set()
    for t in TOPICS:
        kws.update(t.strong)
    kws.update(["occupancy", "hd map", "bev", "3d detection", "gaussian", "driving",
                "lane", "lidar", "world model", "scene understanding", "reconstruction"])
    return sorted(kws)
