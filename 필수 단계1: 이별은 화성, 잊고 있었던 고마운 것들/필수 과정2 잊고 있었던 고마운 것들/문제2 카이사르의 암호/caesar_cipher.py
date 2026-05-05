import string
from pathlib import Path


DICTIONARY_WORDS = {
    'mars',
    'base',
    'emergency',
    'storage',
    'password',
    'key',
    'door',
    'oxygen',
}


def caesar_cipher_decode(target_text):
    results = []

    for shift in range(26):
        decoded_chars = []
        for ch in target_text:
            if ch.islower():
                idx = string.ascii_lowercase.index(ch)
                decoded_chars.append(string.ascii_lowercase[(idx - shift) % 26])
            elif ch.isupper():
                idx = string.ascii_uppercase.index(ch)
                decoded_chars.append(string.ascii_uppercase[(idx - shift) % 26])
            else:
                decoded_chars.append(ch)

        decoded = ''.join(decoded_chars)
        results.append(decoded)
        print(f'[{shift:02}] {decoded}')

        lowered = decoded.lower()
        if any(word in lowered for word in DICTIONARY_WORDS):
            print(f'보너스 감지: 사전 키워드 발견 (shift={shift})')
            break

    return results


def load_password(path='password.txt'):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f'파일을 찾을 수 없습니다: {file_path}')

    content = file_path.read_text(encoding='utf-8').strip()
    if not content:
        raise ValueError('password.txt 파일이 비어 있습니다.')
    return content


def choose_result(results):
    while True:
        choice = input('저장할 해독 결과 번호를 입력하세요: ').strip()
        if not choice.isdigit():
            print('숫자만 입력해 주세요.')
            continue

        idx = int(choice)
        if 0 <= idx < len(results):
            return idx

        print(f'0부터 {len(results) - 1} 사이 번호를 입력해 주세요.')


def save_result(decoded_text, path='result.txt'):
    file_path = Path(path)
    file_path.write_text(decoded_text, encoding='utf-8')
    print(f'해독 결과를 저장했습니다: {file_path}')


def main():
    try:
        target_text = load_password()
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return

    print(f'암호문: {target_text}')
    results = caesar_cipher_decode(target_text)

    selected_idx = choose_result(results)
    final_text = results[selected_idx]
    print(f'선택된 결과[{selected_idx:02}]: {final_text}')
    save_result(final_text)


if __name__ == '__main__':
    main()
