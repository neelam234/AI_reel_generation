import requests
import time
import os

BASE_URL = "http://localhost:8001/api/projects"

def test_full_workflow():
    # 1. Create Project
    print("Step 1: Creating project...")
    resp = requests.post(f"{BASE_URL}/", json={"title": "Test Reel Project"})
    project = resp.json()
    project_id = project['id']
    print(f"Project created: {project_id}")

    # 2. Upload Reference (using the one from POC)
    print("Step 2: Uploading reference video...")
    with open("ref_video.mp4", "rb") as f:
        resp = requests.post(f"{BASE_URL}/{project_id}/upload-reference", files={"file": f})
    print(resp.json())

    # 3. Upload Images (using the ones from POC)
    print("Step 3: Uploading product images...")
    files = []
    for img in ["red.jpg", "green.jpg", "blue.jpg"]:
        files.append(("files", open(f"demo_images/{img}", "rb")))
    resp = requests.post(f"{BASE_URL}/{project_id}/upload-images", files=files)
    print(resp.json())

    # 4. Generate Reel
    print("Step 4: Triggering reel generation...")
    resp = requests.post(f"{BASE_URL}/{project_id}/generate")
    print(resp.json())

    # 5. Poll for completion
    print("Step 5: Polling for completion...")
    for _ in range(30):
        resp = requests.get(f"{BASE_URL}/{project_id}")
        status = resp.json()['status']
        print(f"Current status: {status}")
        if status == "completed":
            print("Success! Reel generated.")
            print(f"Output path: {resp.json()['output_video']}")
            break
        time.sleep(2)
    else:
        print("Timeout waiting for reel generation.")

if __name__ == "__main__":
    test_full_workflow()
