from audio_capture import AudioCapture


def main():
    audio_capture = AudioCapture()
    try:
        if audio_capture.available_mics:
            audio_capture.set_active_mics([1])
            audio_capture.capture()
            audio_capture.save_to_wav()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        audio_capture.close()


if __name__ == "__main__":
    main()