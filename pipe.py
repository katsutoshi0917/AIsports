import cv2
import mediapipe as mp

# MediaPipeの描画ユーティリティとポーズモデルの初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def initialize_pose_estimator():
    """ポーズ検出モデルを初期化して返す"""
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False, smooth_landmarks=True)
    return pose

def evaluate_shooting_form(frame, landmarks):
    """ランドマークデータを使用してシュートフォームを評価し、結果をフレームにテキストで表示する"""
    # 各ランドマークの取得
    left_wrist = landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_elbow = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    right_elbow = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    nose = landmarks.landmark[mp_pose.PoseLandmark.NOSE.value]

    # シュートフォームの条件を評価
    if (left_wrist.y < nose.y or right_wrist.y < nose.y) and \
       (abs(right_elbow.y - right_shoulder.y) < 0.1 or abs(left_elbow.y - left_shoulder.y) < 0.1):
        cv2.putText(frame, 'Good Shooting Form', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'Adjust Shooting Form', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

def process_frame(frame, pose):
    """フレームを処理してポーズを検出し、ランドマークに基づいて評価する"""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        evaluate_shooting_form(frame, results.pose_landmarks)
    cv2.imshow('Frame', frame)

def process_video(video_path):
    """ビデオファイルを開いてフレームごとに処理する"""
    cap = cv2.VideoCapture(video_path)
    pose = initialize_pose_estimator()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        process_frame(frame, pose)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video('7.mov')
