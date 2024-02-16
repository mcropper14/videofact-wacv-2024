from flask import Flask, request, jsonify
from flask_cors import CORS
from demo_app import video_forgery_detection
from inference_single import get_videofact_model, load_single_video, process_single_video



app = Flask(__name__)
CORS(app)

@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    video_file = request.files['video']
    # Call your model function to perform analysis
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
