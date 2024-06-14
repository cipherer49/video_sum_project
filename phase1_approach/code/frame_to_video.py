import cv2

def read_summary_frames_from_txt(txt_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        summary_frames = []
        for line in lines:
            try:
                frame_number = int(line.split(':')[1].strip())
                summary_frames.append(frame_number)
            except (ValueError, IndexError):
                print(f"Ignoring line: {line.strip()}")
    return summary_frames

def generate_summarised_video_from_frames(video_path, summary_frames, output_video):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    for frame_number in summary_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            out.write(frame)

    cap.release()
    out.release()

# Example usage
video_path = 'code/videos/Saving_dolphines.mp4'
summary_frames_file = 'code/dictionary_summarison/summary/saving_sum.txt'
output_video = 'code/dictionary_summarison/summary/saving_dolph_sum.mp4'

summary_frames = read_summary_frames_from_txt(summary_frames_file)
generate_summarised_video_from_frames(video_path, summary_frames, output_video)
