import h5py

# Open the HDF5 file
with h5py.File("D:/project/sem_8_project/video short/Trying_2/v_sum/video_sum_project/merge3_features.h5", 'r') as f:
    # Iterate through the groups
    for group_name in f.keys():
        group = f[group_name]
        print("Group:", group_name)
        
        # Check if the 'video_name' dataset exists in the current group
        if 'video_name' in group:
            # Access the 'video_name' dataset value
            video_name = group['video_name'][()]
            
            # Print the video name
            print("Video Name:", video_name)
        else:
            print("Dataset 'video_name' not found in group:", group_name)