import csv
import datetime
from pathlib import Path

try:
    import speech_recognition as sr  # type: ignore[import-not-found]
except ImportError:
    sr = None


class JarvisStt:
    def __init__(self, records_dir='records'):
        self.records_dir = Path(records_dir)
        self.records_dir.mkdir(exist_ok=True)

    def list_audio_files(self):
        audio_files = sorted(self.records_dir.glob('*.wav'))
        print('녹음 파일 목록:')
        if not audio_files:
            print('- (없음)')
            return []

        for file_path in audio_files:
            print(f'- {file_path.name}')
        return audio_files

    @staticmethod
    def stt_from_audio(audio_path):
        if sr is None:
            raise RuntimeError(
                'speech_recognition이 설치되어 있지 않습니다. '
                'pip install SpeechRecognition 후 실행해 주세요.'
            )

        recognizer = sr.Recognizer()
        with sr.AudioFile(str(audio_path)) as source:
            audio_data = recognizer.record(source)

        try:
            return recognizer.recognize_google(audio_data, language='ko-KR')
        except sr.UnknownValueError:
            return ''
        except sr.RequestError:
            return ''

    @staticmethod
    def save_to_csv(audio_path, recognized_text):
        csv_path = audio_path.with_suffix('.csv')
        now_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['time', 'recognized_text'])
            writer.writerow([now_text, recognized_text])

        print(f'CSV 저장: {csv_path.name}')
        return csv_path

    def convert_all_audio_to_csv(self):
        audio_files = self.list_audio_files()
        if not audio_files:
            return []

        csv_files = []
        for audio_path in audio_files:
            print(f'\nSTT 처리 중: {audio_path.name}')
            try:
                text = self.stt_from_audio(audio_path)
            except Exception as error:  # pylint: disable=broad-except
                print(f'오류: {error}')
                text = ''

            print(f'인식 결과: {text}')
            csv_files.append(self.save_to_csv(audio_path, text))
        return csv_files

    @staticmethod
    def find_keyword_in_csv(csv_files, keyword):
        if not keyword:
            return

        print(f"\n키워드 검색: '{keyword}'")
        found = False
        for csv_path in csv_files:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    text = row.get('recognized_text', '')
                    if keyword in text:
                        found = True
                        print(f'- 발견 파일: {csv_path.name}')
                        print(f'  시간: {row.get("time", "")}')
                        print(f'  내용: {text}')

        if not found:
            print('- 키워드를 포함한 내용이 없습니다.')


def main():
    jarvis_stt = JarvisStt(records_dir='records')
    csv_files = jarvis_stt.convert_all_audio_to_csv()

    if not csv_files:
        return

    keyword = input('\n(보너스) 검색할 키워드를 입력하세요 (건너뛰기: Enter): ').strip()
    jarvis_stt.find_keyword_in_csv(csv_files, keyword)


if __name__ == '__main__':
    main()
