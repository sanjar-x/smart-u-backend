import os
from typing import List

import cv2
from insightface.app.common import Face
from insightface.app import FaceAnalysis
from fastapi import HTTPException, status

UPLOAD_DIR = "static/users"


async def check_face(image_file_path: str) -> bool:
    class FaceAnalysisContext:
        def __init__(self, providers):
            self.providers = providers
            self.app = None

        def __enter__(self):
            self.app = FaceAnalysis(providers=self.providers)
            self.app.prepare(ctx_id=0, det_thresh=0.7, det_size=(640, 640))
            return self.app

        def __exit__(self, exc_type, exc_val, exc_tb):
            del self.app

    with FaceAnalysisContext(providers=["CPUExecutionProvider"]) as app:
        img = cv2.imread(image_file_path)
        faces: List[Face] = app.get(img)
        if len(faces) != 1:
            os.remove(image_file_path)
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"{len(faces)} face(s) in the provided image. Please provide an image with a single face.",
            )
        return True
