import cv2
import numpy as np
import h5py
import os


def extract_surf_features(video_path):
    """Extracts SURF features from a single video.

    Args:
        video_path (str): Path to the video file.

    Returns:
        tuple: A tuple containing two elements:
            - np.ndarray: A NumPy array containing all SURF descriptors from the video.
            - str: The name of the video file (without extension).
    """

    cap = cv2.VideoCapture(video_path)
    all_descriptors = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create SURF detector (check for xfeatures2d)
        try:
            surf_detector = cv2.SURF_create()
        except AttributeError:
            print("Warning: xfeatures2d module not found. Using cv2.ORB instead.")
            surf_detector = cv2.ORB_create()

        # Find keypoints and descriptors
        _, descriptors = surf_detector.detectAndCompute(gray_frame, None)

        if descriptors is not None:
            all_descriptors.extend(descriptors.tolist())  # Convert to list for appending

    cap.release()
    video_name = os.path.splitext(os.path.basename(video_path))[0]  # Extract filename without extension
    return np.array(all_descriptors), video_name


def process_video_dataset(dataset_folder, label_mapping_file, output_h5_file):
    """Processes all videos in a dataset, extracts features and saves them to an HDF5 file.

    Args:
        dataset_folder (str): Path to the folder containing videos.
        label_mapping_file (str): Path to a file containing video-label mappings (optional).
        output_h5_file (str): Path to the output HDF5 file.
    """

    video_counter = 1  # Start video counter at 1

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.mp4') or filename.endswith('.avi'):  # Check for common video extensions
            video_path = os.path.join(dataset_folder, filename)
            features, video_name = extract_surf_features(video_path)

            # Create video group and datasets within it
            with h5py.File(output_h5_file, 'a') as h5_file:
                video_group = h5_file.create_group(f'video_{video_counter}')
                video_group.create_dataset('surf_features', data=features)
                video_group.create_dataset('video_name', data=video_name.encode('utf-8'))  # Encode for HDF5

            video_counter += 1  # Increment counter for next video


if __name__ == "__main__":
    dataset_folder = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/datasets/datasets/SumMe/videos"  # Replace with your dataset path
    label_mapping_file = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/file.txt"  # Optional, replace with your label file path (if available)
    output_h5_file = "surf_features.h5"  # Specify the output filename

    process_video_dataset(dataset_folder, label_mapping_file, output_h5_file)
