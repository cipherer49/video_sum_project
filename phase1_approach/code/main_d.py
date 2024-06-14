import json
import numpy as np
from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.preprocessing import OneHotEncoder

# Step 1: Load SURF features from the existing JSON file
def load_surf_features(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

# Step 2: Perform dictionary learning on the SURF features
def perform_dictionary_learning(features, n_components=100, alpha=1, n_iter=1000, batch_size=10, verbose=1):
    # Extract descriptors from the features
    descriptors = [frame['descriptors'] for frame in features]

    # Flatten the list of descriptors into a single list
    flat_descriptors = [descriptor for sublist in descriptors for descriptor in sublist]

    # Transform the descriptors into a suitable format for MiniBatchDictionaryLearning
    X = np.array(flat_descriptors)

    # Perform dictionary learning
    dl = MiniBatchDictionaryLearning(n_components=n_components, alpha=alpha, n_iter=n_iter, batch_size=batch_size, verbose=verbose)
    dl.fit(X)

    return dl.components_

# Step 3: Reconstruct the SURF features using the learned dictionary
def reconstruct_features(features, dictionary):
    reconstructed_features = []
    for frame in features:
        X = np.zeros((1, len(dictionary)))
        for kp in frame['keypoints']:
            index = int(kp['x'])
            if index < len(dictionary):
                X[0, index] = 1
        reconstructed_features.append(X.dot(dictionary))
    return reconstructed_features

# Step 4: Select key frames based on the reconstructed features
def select_key_frames(reconstructed_features, threshold=0.5, summary_percentage=0.15):
    num_frames = len(reconstructed_features)
    num_summary_frames = int(num_frames * summary_percentage)
    
    sorted_indices = np.argsort([np.max(feature) for feature in reconstructed_features])
    selected_indices = sorted_indices[-num_summary_frames:]
    selected_indices.sort()  # Sort the selected indices
    
    return selected_indices


# Step 5: Print the frame numbers of the summarised frames
def print_summarised_frames(key_frames):
    print("Summarised Frame Numbers:")
    print(key_frames)

def write_summary_frames_to_txt(summary_frames, output_txt):
    with open(output_txt, 'w') as f:
        for frame_number in summary_frames:
            f.write(f"Frame number: {frame_number}\n")


json_file = 'code/dictionary_summarison/SURF_JSON/cooking.json'
features = load_surf_features(json_file)

n_components = 100
dictionary = perform_dictionary_learning(features, n_components=n_components)

reconstructed_features = reconstruct_features(features, dictionary)
key_frames = select_key_frames(reconstructed_features)
print_summarised_frames(key_frames)
summary_frames = select_key_frames(reconstructed_features, threshold=0.5, summary_percentage=0.15)
output_txt = 'code/dictionary_summarison/summary/cooking.txt'
write_summary_frames_to_txt(summary_frames, output_txt)