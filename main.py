import os
import sys
import cv2
from data_pre import crop_to_3_4

## Add Silent-Face-Anti-Spoofing to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
spoof_dir = os.path.join(current_dir, "Silent-Face-Anti-Spoofing")
sys.path.insert(0, spoof_dir)

def process_and_test_image(input_image_path):
    """
    Process an input image and perform liveness detection.
    """
    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(base_dir, "Silent-Face-Anti-Spoofing", "images", "sample")
    model_dir = os.path.join(base_dir, "Silent-Face-Anti-Spoofing", "resources", "anti_spoof_models")
    cropped_path = os.path.join(sample_dir, "cropped.jpg")
    
    # Step 1: Preprocess the image
   # print("\nStep 1: Preprocessing image...")
    
    # Load input image
    source_img = cv2.imread(input_image_path)
    if source_img is None:
        print(f"Error: Could not load input image from {input_image_path}")
        return False
    
    # Load reference image for dimensions
    reference_path = os.path.join(sample_dir, "image_F2.jpg")
    reference_img = cv2.imread(reference_path)
    if reference_img is None:
        print("Error: Could not load reference image for dimensions")
        return False
    
    # Process image
    try:
        cropped = crop_to_3_4(source_img)
        target_h, target_w = reference_img.shape[:2]
        resized = cv2.resize(cropped, (target_w, target_h))
        cv2.imwrite(cropped_path, resized)
        #print("Image preprocessed successfully!")
    except Exception as e:
        print(f"Error during image preprocessing: {str(e)}")
        return False    # Step 2: Perform liveness detection
    #print("\nStep 2: Performing liveness detection...")
    try:
        # Import and run test function
        import test
        test.test("cropped.jpg", model_dir, 0)
        #print("Liveness detection completed!")
        return True
        
    except Exception as e:
        print(f"Error during liveness detection: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Face Liveness Detection System")
    parser.add_argument("--image", type=str, required=True,
                      help="Path to the input image file")
    
    args = parser.parse_args()
    
    # Run the processing pipeline
    #print("Starting face liveness detection process...")
    if process_and_test_image(args.image):
        print("\nProcess completed successfully!")
    else:
        print("\nProcess failed. Please check the error messages above.")