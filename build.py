import PyInstaller.__main__
import os
import shutil

# 스크립트가 있는 디렉토리로 작업 경로 변경 (파일을 못 찾는 문제 해결)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 빌드할 메인 파이썬 스크립트 파일 이름
SCRIPT_NAME = 'github_tagger.py'

# 생성될 실행 파일의 이름
EXE_NAME = 'GitHubTagger'

def build():
    """PyInstaller를 사용하여 실행 파일을 빌드합니다."""
    print(f"'{SCRIPT_NAME}' 빌드를 시작합니다...")

    PyInstaller.__main__.run([
        '--name=%s' % EXE_NAME,
        '--onefile',      # 하나의 실행 파일로 만듭니다.
        '--windowed',     # 실행 시 콘솔 창을 숨깁니다.
        SCRIPT_NAME
    ])

    print("\n빌드가 완료되었습니다!")
    print(f"실행 파일은 'dist' 폴더에서 찾을 수 있습니다: {os.path.join(os.getcwd(), 'dist', EXE_NAME + '.exe')}")

    # 빌드 과정에서 생성된 불필요한 파일/폴더 정리
    shutil.rmtree('build', ignore_errors=True)
    if os.path.exists(f'{EXE_NAME}.spec'):
        os.remove(f'{EXE_NAME}.spec')

if __name__ == '__main__':
    build()