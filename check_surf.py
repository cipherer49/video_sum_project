import h5py

def check_surf_features(h5_file_path):
    """Checks if an HDF5 file contains SURF features.

    Args:
        h5_file_path (str): Path to the HDF5 file.

    Returns:
        bool: True if SURF features are found, False otherwise.
    """

    with h5py.File(h5_file_path, 'r') as hdf5_file:
        # Check for datasets or groups containing 'surf' or 'sift' keywords
        for name, obj in hdf5_file.items():
            if isinstance(obj, h5py.Group) and ('surf' in name.lower() or 'sift' in name.lower()):
                return True
            elif isinstance(obj, h5py.Dataset) and ('surf' in name.lower() or 'sift' in name.lower()):
                # Check if the dataset has appropriate dimensions for features
                data_shape = obj.shape
                if len(data_shape) >= 2 and data_shape[1] >= 4:  # Assuming at least 4 values per feature
                    return True

    return False

# Example usage (replace with your actual file path)
h5_file_path = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/eccv16_dataset_tvsum_google_pool5.h5"
has_surf_features = check_surf_features(h5_file_path)

if has_surf_features:
    print("SURF features found in the HDF5 file.")
else:
    print("SURF features not found in the HDF5 file.")