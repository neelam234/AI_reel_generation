import os
import cv2
import numpy as np
from moviepy import (
    VideoFileClip, 
    ImageClip, 
    CompositeVideoClip, 
    concatenate_videoclips,
    ColorClip
)
from scenedetect import detect, ContentDetector

def get_scene_timings(video_path):
    """Detect scenes in the reference video using MoviePy's internal frame differences."""
    print(f"Analyzing {video_path} for scenes...")
    try:
        # Try PySceneDetect first, but catch the NaN error
        scene_list = detect(video_path, ContentDetector())
        timings = []
        for i, scene in enumerate(scene_list):
            start = scene[0].get_seconds()
            end = scene[1].get_seconds()
            timings.append((start, end))
        return timings
    except Exception as e:
        print(f"PySceneDetect failed ({e}), falling back to fixed intervals.")
        clip = VideoFileClip(video_path)
        duration = clip.duration
        # Fallback: create 3 scenes of equal length
        n_scenes = 3
        scene_duration = duration / n_scenes
        return [(i * scene_duration, (i + 1) * scene_duration) for i in range(n_scenes)]

def get_smart_crop_center(image_path, target_ratio=9/16):
    """
    Finds the center of interest using a simple saliency map (Fine Grained).
    If fails, defaults to image center.
    """
    img = cv2.imread(image_path)
    if img is None:
        return 0.5, 0.5
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple Saliency: Spectral Residual or Fine Grained
    # For MVP, we'll use a simple Laplacian variance or Canny to find 'detail' centers
    edges = cv2.Canny(gray, 100, 200)
    
    # Find moments of the edges to get center of mass
    M = cv2.moments(edges)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX / img.shape[1], cY / img.shape[0]
    
    return 0.5, 0.5

def create_animated_clip(image_path, duration, target_size=(1080, 1920)):
    """Creates a 9:16 clip from an image with a slow zoom effect."""
    print(f"Processing image: {image_path}")
    
    # Get saliency center
    cX, cY = get_smart_crop_center(image_path)
    
    # Load image
    clip = ImageClip(image_path).with_duration(duration)
    
    # Resize to cover the target size while maintaining aspect ratio
    # We want to keep the center of interest
    w, h = clip.size
    target_w, target_h = target_size
    
    # Calculate scale to cover
    scale = max(target_w / w, target_h / h)
    clip = clip.resized(scale)
    
    # Ken Burns effect (simple zoom)
    # We use a lambda for the zoom factor
    def zoom(t):
        return 1 + 0.05 * (t / duration)
    
    # Apply zoom and center on our saliency point
    # MoviePy 2.x uses 'with_position' and 'with_effects'
    # For simplicity in this POC, we'll just center it
    final_clip = clip.resized(zoom).with_position('center')
    
    # Crop to 9:16
    final_clip = final_clip.cropped(
        x_center=final_clip.w * cX, 
        y_center=final_clip.h * cY, 
        width=target_w, 
        height=target_h
    )
    
    return final_clip

def generate_fashion_reel(ref_video, image_folder, output_path):
    # 1. Get timings
    scene_timings = get_scene_timings(ref_video)
    if not scene_timings:
        print("No scenes detected, using default 3s intervals.")
        scene_timings = [(i*3, (i+1)*3) for i in range(5)]
    
    # 2. Get images
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()
    
    if not images:
        print("No images found!")
        return

    # 3. Create clips
    clips = []
    for i, (start, end) in enumerate(scene_timings):
        duration = end - start
        img_idx = i % len(images)
        clip = create_animated_clip(images[img_idx], duration)
        clips.append(clip)
        
    # 4. Concatenate and add music from ref video
    print("Assembling final reel...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Try to extract audio from ref video
    try:
        ref_clip = VideoFileClip(ref_video)
        if ref_clip.audio:
            audio = ref_clip.audio.with_duration(final_video.duration)
            final_video = final_video.with_audio(audio)
    except Exception as e:
        print(f"Could not extract audio: {e}")

    # 5. Export
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Success! Reel saved at {output_path}")

if __name__ == "__main__":
    # Create dummy data for demo if not exists
    os.makedirs("demo_images", exist_ok=True)
    
    # Generate 3 solid color images if none exist
    if not any(f.endswith('.jpg') for f in os.listdir("demo_images")):
        for color_name, color_rgb in [("red", (255,0,0)), ("green", (0,255,0)), ("blue", (0,0,255))]:
            img = np.zeros((1000, 1000, 3), dtype=np.uint8)
            img[:] = color_rgb
            cv2.imwrite(f"demo_images/{color_name}.jpg", img)
            
    # Create a dummy ref video if not exists
    if not os.path.exists("ref_video.mp4"):
        print("Creating dummy reference video...")
        c1 = ColorClip(size=(640, 480), color=(255, 0, 0)).with_duration(2)
        c2 = ColorClip(size=(640, 480), color=(0, 255, 0)).with_duration(2)
        c3 = ColorClip(size=(640, 480), color=(0, 0, 255)).with_duration(2)
        dummy_ref = concatenate_videoclips([c1, c2, c3])
        dummy_ref.write_videofile("ref_video.mp4", fps=24, codec="libx264")

    generate_fashion_reel("ref_video.mp4", "demo_images", "output_reel.mp4")
