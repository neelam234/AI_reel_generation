import os
import cv2
import numpy as np
from pathlib import Path
from moviepy import (
    VideoFileClip, 
    ImageClip, 
    concatenate_videoclips
)
from scenedetect import detect, ContentDetector

class VideoEngine:
    def __init__(self, target_size=(1080, 1920)):
        self.target_size = target_size

    def get_scene_timings(self, video_path: str):
        print(f"Analyzing {video_path} for scenes...")
        try:
            scene_list = detect(video_path, ContentDetector())
            timings = []
            for scene in scene_list:
                start = scene[0].get_seconds()
                end = scene[1].get_seconds()
                timings.append((start, end))
            return timings
        except Exception as e:
            print(f"PySceneDetect failed ({e}), using fallback.")
            n_scenes = 3
            sd = 2.0 # Assume 2s per scene for dummy data
            return [(i * sd, (i + 1) * sd) for i in range(n_scenes)]

    def get_smart_crop_center(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None: return 0.5, 0.5
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        M = cv2.moments(edges)
        if M["m00"] != 0:
            return int(M["m10"]/M["m00"])/img.shape[1], int(M["m01"]/M["m00"])/img.shape[0]
        return 0.5, 0.5

    def create_clip(self, image_path: str, duration: float):
        cX, cY = self.get_smart_crop_center(image_path)
        clip = ImageClip(image_path).with_duration(duration)
        w, h = clip.size
        tw, th = self.target_size
        scale = max(tw/w, th/h)
        clip = clip.resized(scale)
        
        # Simple Ken Burns (Zoom)
        def zoom(t): return 1 + 0.05 * (t / duration)
        final_clip = clip.resized(zoom).with_position('center')
        
        return final_clip.cropped(
            x_center=final_clip.w * cX, 
            y_center=final_clip.h * cY, 
            width=tw, 
            height=th
        )

    def generate_reel(self, ref_video: str, images: list, output_path: str):
        timings = self.get_scene_timings(ref_video)
        clips = []
        for i, (start, end) in enumerate(timings):
            img_path = images[i % len(images)]
            clips.append(self.create_clip(img_path, end - start))
        
        final_video = concatenate_videoclips(clips, method="compose")
        
        try:
            ref_clip = VideoFileClip(ref_video)
            if ref_clip.audio:
                final_video = final_video.with_audio(ref_clip.audio.with_duration(final_video.duration))
        except: pass

        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path

video_engine = VideoEngine()
