from audio_capture import AudioCapture
from logger_module import setup_logger, log_message
from performance_module import start_monitoring
import threading


def main():
    setup_logger(logger_name='main')
    
    monitoring_thread = threading.Thread(target=start_monitoring, args=(10, 'main'))
    monitoring_thread.daemon = True
    monitoring_thread.start()

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