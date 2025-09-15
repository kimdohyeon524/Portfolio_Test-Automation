# Portfolio_Test-Automation
해당 파일은 자동화 테스트 포트폴리오로 제작한 단일 파일입니다.
테스트 구동 조건은 다음과 같습니다.

1. 테스트 환경
- Python 3.9.13
- Selenium 4.35.0
- Appium-Python-Client 5.2.2
- Appium Server 3.0.2 (APPIUM_URL 기본값 = http://127.0.0.1:4723)
- Android SDK & ADB 설치 및 테스트 단말 연결 (테스트 단말명 ADB로 확인 후 변경 필요)

2. 테스트 대상
- my-demo-app-android (Version 2.2.0)
- URL : https://github.com/saucelabs/my-demo-app-android/releases/tag/2.2.0

3. 테스트 내용
- 로그인
- 로그아웃
- 로그인 실패 (ID 미입력)
- 로그인 실패 (Password 미입력)
- 로그인 실패 (Locked out 계정 사용)
- 상품 목록 내 첫 상품을 장바구니에 담기
  (테스트 실패 시 테스트 실행 파일과 동일 경로에 스크린샷 저장)
