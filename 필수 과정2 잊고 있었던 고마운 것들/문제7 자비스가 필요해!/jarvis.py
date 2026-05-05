import datetime
import os
import wave

try:
    import pyaudio  # type: ignore[import-not-found]
except ImportError:
    pyaudio = None


class JarvisRecorder:
    def __init__(self, records_dir='records'):
        self.records_dir = records_dir
        os.makedirs(self.records_dir, exist_ok=True)

    def _build_filename(self):
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S.wav')

    def record_voice(self, duration_seconds=5):
        if pyaudio is None:
            raise RuntimeError(
                'pyaudio가 설치되어 있지 않습니다. pip install pyaudio 후 실행해 주세요.'
            )

        sample_rate = 44100
        chunk_size = 1024
        channels = 1
        sample_format = pyaudio.paInt16

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=sample_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
        )

        total_chunks = int(sample_rate / chunk_size * duration_seconds)
        frames = []
        print(f'녹음 시작: {duration_seconds}초')

        try:
            for _ in range(total_chunks):
                frames.append(stream.read(chunk_size, exception_on_overflow=False))
        finally:
            stream.stop_stream()
            stream.close()

        filename = self._build_filename()
        output_path = os.path.join(self.records_dir, filename)

        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(audio.get_sample_size(sample_format))
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))

        audio.terminate()
        print(f'녹음 완료: {output_path}')
        return output_path


def main():
    recorder = JarvisRecorder()
    recorder.record_voice(duration_seconds=5)


if __name__ == '__main__':
    main()
