import h5py

def print_file_info(h5_file_path):
    """Prints information about datasets and groups in an HDF5 file.

    Args:
        h5_file_path (str): Path to the HDF5 file.
    """

    with h5py.File(h5_file_path, 'r') as hdf5_file:
        def print_dataset_info(name, obj):
            print(f"  Dataset: {name}")
            print(f"    Shape: {obj.shape}")
            print(f"    Datatype: {obj.dtype}")

        def print_group_info(name, obj):
            print(f"  Group: {name}")
            for child_name, child_obj in obj.items():
                print_info(child_name, child_obj)  # Recursive call

        def print_info(name, obj):
            if isinstance(obj, h5py.Dataset):
                print_dataset_info(name, obj)
            elif isinstance(obj, h5py.Group):
                print_group_info(name, obj)
            else:
                print(f"  Other object: {name} (type: {type(obj)})")

        print("HDF5 File Information:")
        print_info("/", hdf5_file)  # Start at the root group

# Example usage (replace with your actual file path)
h5_file_path = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/datasets/datasets/eccv16_dataset_summe_google_pool5.h5"
#h5_file_path = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/merge3_features.h5"
print_file_info(h5_file_path)
