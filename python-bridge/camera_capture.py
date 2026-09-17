"""Chup 1 frame tu webcam laptop (qua OpenCV) de gui kem canh bao Telegram."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def capture_photo(camera_index: int = 0) -> bytes | None:
    try:
        import cv2
    except ImportError:
        logger.warning("Chua cai opencv-python (pip install opencv-python) - bo qua chup anh.")
        return None

    cap = cv2.VideoCapture(camera_index)
    try:
        if not cap.isOpened():
            logger.warning("Khong mo duoc camera index=%s - bo qua chup anh.", camera_index)
            return None
        ok, frame = cap.read()
        if not ok:
            logger.warning("Khong doc duoc frame tu camera - bo qua chup anh.")
            return None
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            logger.warning("Khong encode duoc anh JPEG - bo qua chup anh.")
            return None
        return buffer.tobytes()
    finally:
        cap.release()
