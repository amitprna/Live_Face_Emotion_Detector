import cv2
from deepface import DeepFace
import streamlit as st
from streamlit_webrtc import (AudioProcessorBase,RTCConfiguration,VideoProcessorBase,WebRtcMode,webrtc_streamer)
import av

#inp_image = st.camera_input('say cheese.......')
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoTransformer(VideoProcessorBase):
    result_queue: "queue.Queue[List[Detection]]"
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        predictions = DeepFace.analyze(img)
        result = [*predictions]
        faceCascade = cv2.CascadeClassifier('harcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,1.1,4)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w, y+h),(0,255,0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText( img, predictions['dominant_emotion'], (0,50), font, 1, (255,255,128), 2, cv2.LINE_4 ); 
        cv2.putText( img, str(predictions['age']), (10,50), font, 1, (255,255,128), 2, cv2.LINE_AA ); 
        cv2.putText( img, predictions['gender'], (20,50), font, 1, (255,255,128), 2, cv2.LINE_4 );
        
        self.result_queue.put(result)
        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_ctx = webrtc_streamer(key="example",mode=WebRtcMode.SENDRECV,rtc_configuration=RTC_CONFIGURATION, video_processor_factory=VideoTransformer,media_stream_constraints={"video": True, "audio": False},async_processing=True)

if st.checkbox("Show the detected labels", value=True):
    if webrtc_ctx.state.playing:
        labels_placeholder = st.empty()
        while True:
            if webrtc_ctx.video_processor:
                try:
                    result = webrtc_ctx.video_processor.result_queue.get(
                        timeout=1.0
                    )
                except:
                    queue.Empty
                    result = None
                labels_placeholder.table(result)
            else:
                break

