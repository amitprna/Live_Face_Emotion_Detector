import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title('Emotion Detection')

run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
cam = cv2.VideoCapture(0)

while run:
  ret, frame = cam.read()
  FRAME_WINDOW.image(frame)
  if cv2.waitkey(2) & 0xFF == ord('q'):
     break
else:
  st.write('stopped')
