"""Gate S2a checks for the official AprilTag v3.4.5 build (see docs/gates/S2a.md)."""

import json
import os
from pathlib import Path

import cv2
import numpy as np
import pytest

apriltag = pytest.importorskip("apriltag")
REPO = Path(__file__).resolve().parents[1]
KW = {"threads": 1, "maxhamming": 0, "decimate": 1.0, "blur": 0.0, "refine_edges": True}


def tag_image(tag_id: int, size: int = 300, margin: int = 150) -> tuple[np.ndarray, np.ndarray]:
    """Independent generator: OpenCV's AprilTag 36h11 dictionary, white border, returns image and true outer corners."""
    d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    m = cv2.aruco.generateImageMarker(
        d, tag_id, size, borderBits=1
    )  # 10x10 cells incl. 1-cell black border
    img = np.full((size + 2 * margin, size + 2 * margin), 255, np.uint8)
    img[margin : margin + size, margin : margin + size] = m
    c = np.array(
        [
            [margin, margin],
            [margin + size, margin],
            [margin + size, margin + size],
            [margin, margin + size],
        ],
        float,
    )
    return img, c


def detector():
    return apriltag.apriltag("tag36h11", **KW)


def test_provenance_commit():
    p = json.loads((REPO / "config/apriltag_build.json").read_text())
    assert p["commit"].startswith("94be783") and p["release"] == "v3.4.5"


def test_no_ld_library_path_needed():
    assert "LD_LIBRARY_PATH" not in os.environ or "apriltag" not in os.environ["LD_LIBRARY_PATH"]
    detector()


@pytest.mark.parametrize("tag_id", [0, 1, 7, 35])
def test_detects_own_id(tag_id):
    img, truth = tag_image(tag_id)
    det = detector().detect(img)
    assert len(det) == 1 and det[0]["id"] == tag_id and det[0]["hamming"] == 0
    # corners lie on the outer edge of the black border; their ORDER follows the AprilTag frame (a 180-degree
    # rotation of OpenCV's rendering), so compare as sets
    lb = np.array(det[0]["lb-rb-rt-lt"])
    d = max(min(np.linalg.norm(t - lb, axis=1)) for t in truth)
    assert d < 0.5, d
    assert np.linalg.norm(np.array(det[0]["center"]) - truth.mean(axis=0)) < 0.05


def test_no_tag_no_detection():
    assert len(detector().detect(np.full((400, 400), 128, np.uint8))) == 0


def test_determinism():
    img, _ = tag_image(0)
    a = detector().detect(img)[0]["lb-rb-rt-lt"]
    b = detector().detect(img)[0]["lb-rb-rt-lt"]
    assert np.array_equal(a, b)
