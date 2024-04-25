import cv2
import json

def extract_surf_features_with_labels(video_path, output_json):
  """Extracts SURF features from a video, converts them to arrays, and saves them as JSON with labels.

  Args:
      video_path (str): Path to the video file.
      output_json (str): Path to the output JSON file.
  """

  # Create SURF object
  surf = cv2.ORB_create()

  # Open video capture
  cap = cv2.VideoCapture(video_path)

  # Check if video opened successfully
  if not cap.isOpened():
    print("Error opening video file:", video_path)
    return

  # Initialize empty list for storing features with labels
  features_list = []

  # Process video frame by frame
  frame_number = 0  # Initialize frame counter
  while True:
    ret, frame = cap.read()

    # Break loop if frame is not read or 'q' key is pressed
    if not ret or cv2.waitKey(1) == ord('q'):
      break

    # Convert frame to grayscale for SURF
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find keypoints and descriptors
    keypoints, descriptors = surf.detectAndCompute(gray, None)

    # Convert keypoints to list of dictionaries for JSON
    keypoints_list = []
    for kp in keypoints:
      keypoints_list.append({
          "x": kp.pt[0],
          "y": kp.pt[1],
          "size": kp.size,
          "angle": kp.angle,
          "response": kp.response,
      })

    # Combine keypoints, descriptors, and frame number into a dictionary
    features = {
        "frame_number": frame_number,
        "keypoints": keypoints_list,
        "descriptors": descriptors.tolist(),  # Convert to list for JSON
    }

    # Append features to the list
    features_list.append(features)

    frame_number += 1  # Increment frame counter

  # Release video capture
  cap.release()

  # Write features to JSON file
  with open(output_json, 'w') as f:
    json.dump(features_list, f, indent=4)

  print(f"SURF features extracted frame-by-frame with labels and saved to: {output_json}")

# Example usage
video_path = 'code/Saving dolphines.mp4'
output_json = 'code/video2_surf.json'

extract_surf_features_with_labels(video_path, output_json)
