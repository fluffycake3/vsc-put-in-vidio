import streamlit as st
import tempfile
import cv2
from PIL import Image

def save_frame_from_video(video_path, frame_number, output_path):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    cap.release()

uploaded_video = st.file_uploader("Upload video thinkerbelle nyaa", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    # Simpan video yang diupload ke file sementara
    with tempfile.NamedTemporaryFile(delete=False) as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    # Tampilkan video yang diupload
    st.video(uploaded_video)

    # Jumlah total frame dan durasi video
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = total_frames / fps
    st.write(f'Jumlah semua frame dalam 1 video: {total_frames}')
    st.write(f'FPS: {fps}')
    st.write(f'Durasi: {duration:.2f} detik')

    # Input untuk memilih nomor frame
    frame_number = st.number_input("Frame ke berapa untuk di cek atau di extract", min_value=0, max_value=total_frames-1, step=1)

    if st.button('Cek Frame'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            output_path = f"frame_{frame_number}.jpg"
            cv2.imwrite(output_path, frame)
            img = Image.open(output_path)
            st.image(img, caption=f'Frame {frame_number}', use_column_width=True)
        cap.release()

    if st.button('Extract Frame'):
        output_path = f"frame_{frame_number}.jpg"
        save_frame_from_video(video_path, frame_number, output_path)
        st.success(f'Frame {frame_number} berhasil diextract dan disimpan sebagai {output_path}')

        # Tampilkan frame yang diextract sebagai gambar
        img = Image.open(output_path)
        st.image(img, caption=f'Extracted Frame {frame_number}', use_column_width=True)