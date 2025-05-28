import cv2

def crop_to_3_4(image):
    h, w = image.shape[:2]
    target_ratio = 3 / 4
    current_ratio = w / h

    if abs(current_ratio - target_ratio) < 0.01:
        return image  # Already 3:4

    if current_ratio > target_ratio:
        # Too wide: crop width
        new_width = int(h * target_ratio)
        start_x = (w - new_width) // 2
        return image[:, start_x:start_x + new_width]
    else:
        # Too tall: crop height
        new_height = int(w / target_ratio)
        start_y = (h - new_height) // 2
        return image[start_y:start_y + new_height, :]

# === File paths ===
source_path = r"Silent-Face-Anti-Spoofing/images/sample/Kerim.jpg"    # Image you want to crop
target_path = r"Silent-Face-Anti-Spoofing/images/sample/image_F2.jpg"     # Image whose size you want to match
output_path = r"Silent-Face-Anti-Spoofing/images/sample/cropped.jpg"     # Final saved image

# === Load images ===
source_img = cv2.imread(source_path)
target_img = cv2.imread(target_path)

if source_img is None or target_img is None:
    print("Error: Could not load one or both images.")
    exit()

# === Crop and Resize ===
cropped = crop_to_3_4(source_img)
target_h, target_w = target_img.shape[:2]
resized = cv2.resize(cropped, (target_w, target_h))

# === Save the result ===
cv2.imwrite(output_path, resized)
print(f"Saved cropped and resized image as {output_path}")
