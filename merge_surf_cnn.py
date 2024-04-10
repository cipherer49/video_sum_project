import h5py
import logging

logging.basicConfig(level=logging.INFO)

def merge_feature_files(surf_h5_file, googlenet_h5_file, output_h5_file):
    """Merges SURF features from one HDF5 file into GoogleNet features in another based on matching video names.

    Args:
        surf_h5_file (str): Path to the HDF5 file containing SURF features.
        googlenet_h5_file (str): Path to the HDF5 file containing GoogleNet features.
        output_h5_file (str): Path to the output HDF5 file containing merged features.
    """

    try:
        with h5py.File(surf_h5_file, 'r') as surf_file, \
             h5py.File(googlenet_h5_file, 'r') as googlenet_file, \
             h5py.File(output_h5_file, 'w') as output_file:

            for video_name in surf_file.keys():
                if video_name in googlenet_file:
                    surf_group = surf_file[video_name]
                    googlenet_group = googlenet_file[video_name]

                    # Create a group in the output file
                    output_group = output_file.create_group(video_name)

                    # Copy datasets from GoogleNet group (except video_name)
                    for dataset_name, dataset in googlenet_group.items():
                        if dataset_name != 'video_name':
                            output_group.create_dataset(dataset_name, data=dataset)

                    # Copy 'surf_features' dataset from SURF group if it exists
                    if 'surf_features' in surf_group:
                        surf_features_dataset = surf_group['surf_features']
                        output_group.create_dataset('surf_features', data=surf_features_dataset)
                    else:
                        logging.warning(f"No 'surf_features' dataset found for video '{video_name}' in SURF features.")

                    # Copy 'video_name' dataset if it doesn't already exist
                    if 'video_name' not in output_group:
                        output_group.create_dataset('video_name', data=surf_group['video_name'][()])
                else:
                    logging.warning(f"Video '{video_name}' found in SURF features but not GoogleNet features.")

        logging.info("Merging completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during merging: {str(e)}")


if __name__ == "__main__":
    surf_h5_file = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/surf_features.h5"  # Replace with your SURF feature file
    googlenet_h5_file = "D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/datasets/datasets/eccv16_dataset_summe_google_pool5.h5"   # Replace with your GoogleNet feature file
    output_h5_file = "merge3_features.h5"  # Specify the output filename

    merge_feature_files(surf_h5_file, googlenet_h5_file, output_h5_file)
