import pandas as pd
import torch

from inference_single import get_videofact_model, load_single_video, process_single_video
from utils import *


#display videos on react 

#values given in demo.py
VideoFACT_xfer = None
VideoFACT_df = None

videofact_df_threshold = 0.33
videofact_xfer_threshold = 0.4

output_root_dir = "output"

#model
@torch.no_grad()
def video_forgery_detection(video_path: str) -> Tuple[List[str], List[Tuple[int, float]], str, str]:
    global VideoFACT_xfer
    if VideoFACT_xfer is None:
        VideoFACT_xfer = get_videofact_model("xfer")

    #load in video 
    dataloader = load_single_video(video_path, shuffle=True, max_num_samples=100, sample_every=5, batch_size=1, num_workers=8)
    results = process_single_video(VideoFACT_xfer, dataloader, progress=None)
    result_frame_paths, idxs, scores = list(zip(*results))
    decision = "Forged" if scores[0] > videofact_xfer_threshold else "Authentic"
    return result_frame_paths, list(zip(idxs, scores)), f"Frame: {idxs[0]}, Score: {scores[0]:.5f}", decision


if __name__ == "__main__":
    video_path = "/home/cropthecoder/Documents/Disinfo/videofact-wacv-2024/examples/df/zella-rena_deepfake.mp4"  #test video path for now can change to whatever, idk maybe command line arguments 
    result_frame_paths, idxs_scores, first_result, decision = video_forgery_detection(video_path)

    #Save the results to a text file, can also change to whatever 
    output_file_path = "output_results.txt"
    with open(output_file_path, "w") as file:
        file.write("Results:\n")
        file.write(f"First Result: {first_result}\n")
        file.write(f"Decision: {decision}\n")
        file.write("Frame Index\tScore\n")
        for idx, score in idxs_scores:
            file.write(f"{idx}\t{score}\n")

    print(f"Results saved to {output_file_path}")
