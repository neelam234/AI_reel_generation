import pytest
from app.services.video_engine import video_engine
import os
import cv2
import numpy as np

def test_smart_crop_center_white_image(tmp_path):
    # Create a simple white image
    img_path = str(tmp_path / "white.jpg")
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.imwrite(img_path, img)
    
    cX, cY = video_engine.get_smart_crop_center(img_path)
    # For a blank image, it should fallback to center
    assert cX == 0.5
    assert cY == 0.5

def test_smart_crop_center_with_shape(tmp_path):
    # Create an image with a rectangle on the left side
    img_path = str(tmp_path / "shape.jpg")
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(img, (10, 10), (30, 90), (255, 255, 255), -1)
    cv2.imwrite(img_path, img)
    
    cX, cY = video_engine.get_smart_crop_center(img_path)
    # Center should be shifted towards the left (less than 0.5)
    assert cX < 0.5
    assert 0.4 < cY < 0.6

def test_scene_timings_fallback():
    # Test fallback logic with non-existent file
    timings = video_engine.get_scene_timings("non_existent.mp4")
    assert len(timings) == 3 # Default fallback n_scenes
    assert timings[0][0] == 0
