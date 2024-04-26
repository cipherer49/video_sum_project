import cv2
import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def load_json_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def extract_frame_numbers(data):
    frame_numbers = [frame['frame_number'] for frame in data]
    return np.array(frame_numbers)

def apply_hierarchical_clustering(frame_numbers, num_clusters):
    hierarchical = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
    hierarchical.fit(frame_numbers.reshape(-1, 1))  # Reshape to fit input format
    return hierarchical.labels_

def calculate_num_clusters(total_frames, summary_percentage):
    return int(total_frames * summary_percentage)

def summarize_video(json_file, num_clusters, total_frames):
    data = load_json_file(json_file)
    frame_numbers = extract_frame_numbers(data)
    
    hierarchical_labels = apply_hierarchical_clustering(frame_numbers, num_clusters)
    
    cluster_frames = {}
    for i, label in enumerate(hierarchical_labels):
        if label not in cluster_frames:
            cluster_frames[label] = []
        cluster_frames[label].append(frame_numbers[i])
    
    summary_length = int(total_frames * 0.15)  # 15% of total frames for summary
    selected_frames = []
    for cluster in range(num_clusters):
        frames_in_cluster = cluster_frames[cluster]
        frames_in_cluster.sort()
        selected_frames.extend(frames_in_cluster[:int(summary_length / num_clusters)])
    
    selected_frames.sort()
    return selected_frames[:summary_length]

def count_total_frames(json_file):
    data = load_json_file(json_file)
    return len(data)

def convert_frames_to_video(summary_frames, video_file, output_file):
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    for frame_number in summary_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    
    cap.release()
    out.release()

# Example usage
json_file = 'code/video2_surf.json'
summary_percentage =15/100
total_frames = count_total_frames(json_file)
num_clusters = calculate_num_clusters(total_frames,summary_percentage)
summary_frames = summarize_video(json_file, num_clusters, total_frames)
print(total_frames)
print(summary_frames)

video_file = 'code/Saving_dolphines.mp4'
output_file = 'code/video2_h_cluster.mp4'
convert_frames_to_video(summary_frames, video_file, output_file)
