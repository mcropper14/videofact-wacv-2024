import pandas as pd
import torch
from flask import Flask, render_template, jsonify

from inference_single import get_videofact_model, load_single_video, process_single_video
from utils import *

"""
app = Flask(__name__)
CORS(app)

#@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    video_file = request.files['video']
    #model function
    result_frame_paths, idxs_scores, first_result, decision = video_forgery_detection(video_file)
    return jsonify({
        'result_frame_paths': result_frame_paths,
        'idxs_scores': idxs_scores,
        'first_result': first_result,
        'decision': decision
    })
    #results = video_forgery_detection(video_file)
    #return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
"""
app = Flask(__name__)

# values given in demo.py
VideoFACT_xfer = None
VideoFACT_df = None

videofact_df_threshold = 0.33
videofact_xfer_threshold = 0.4

output_root_dir = "output"

# model
@torch.no_grad()
def video_forgery_detection(video_path: str) -> Tuple[List[str], List[Tuple[int, float]], str, str]:
    global VideoFACT_xfer
    if VideoFACT_xfer is None:
        VideoFACT_xfer = get_videofact_model("xfer")

    # load in video
    dataloader = load_single_video(video_path, shuffle=True, max_num_samples=100, sample_every=5, batch_size=1,
                                   num_workers=8)
    results = process_single_video(VideoFACT_xfer, dataloader, progress=None)
    result_frame_paths, idxs, scores = list(zip(*results))
    decision = "Forged" if scores[0] > videofact_xfer_threshold else "Authentic"
    return result_frame_paths, list(zip(idxs, scores)), f"Frame: {idxs[0]}, Score: {scores[0]:.5f}", decision


@app.route('/')
def index():
    # Provide the path to your video
    print("Got to here")
    video_path = "/home/cropthecoder/Documents/Disinfo/videofact-wacv-2024/examples/df/zella-rena_deepfake.mp4"
    result_frame_paths, idxs_scores, first_result, decision = video_forgery_detection(video_path)
    return jsonify({
        'result_frame_paths': result_frame_paths,
        'idxs_scores': idxs_scores,
        'first_result': first_result,
        'decision': decision
    })
    #results = video_forgery_detection(video_file)
    #return jsonify(results)
   


if __name__ == "__main__":
    app.run(debug=True)
