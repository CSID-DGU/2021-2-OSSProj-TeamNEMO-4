# 오픈소스 소프트웨어 프로젝트 4조 TEAM NEMO

<hr>

## PC 로 즐기는 오징어게임

[![GitHub license](https://img.shields.io/badge/license-LGPL-lightgrey.svg)](https://github.com/CSID-DGU/2021-2-OSSProj-TeamNEMO-4/blob/master/LICENSE)
[![OS](https://img.shields.io/badge/OS-ubuntu-red)](https://ubuntu.com)
[![Python version](https://img.shields.io/badge/python-3.9.0-brightgreen.svg)](https://www.python.org)
[![Pygame version](https://img.shields.io/badge/pygame-2.0.2-yellow.svg)](http://pygame.org)

**Team Leader**: [오한음](https://github.com/0hhanum)
**Team Member**: [이준영](https://github.com/JunYoung3682), [윤종연](https://github.com/YJY189)

<hr>
추후 정리 필요

[10.28]

- 게임별 디렉토리 나누어 청사진 작성
- 폰트 사용. SIL 오픈폰트 프리텐다드 폰트. (https://noonnu.cc/font_page/694)
- "무궁화 꽃이 피었습니다" 게임 베이스코드 찾아 업로드. (https://github.com/AidenBurgess/CrossGame)

[10.29]

- 무궁화게임 NPC 개수 추가, 속도 및 크기 조절정
- 무궁화게임 타이머 추가 & 무궁화 타이머 추가
- 무궁화게임 로직 완성
- 게임 재시작시 타이머 리셋 안되는 버그 수
- 진행요원 이미지 추가 출처: https://pixabay.com
- 게임 요소 이미지 출처 :https://opengameart.org [오픈소스 게임 이미지 공유 사이트]

[10.30]

- 달고나게임 플레이 방식 수정 (경계선에 올려진 버튼을 클릭해 달고나를 뽑는 방식으로)
- 공통 구성요소 추가 (색상, 메세지 작성 etc)

[10.31]

- 글로벌 타이머 추가
- 달고나게임 기본 설계
- 구슬홀짝 기본 설계

[11.1]

- 달고나게임 초안 완성
- 글로벌 타이머 연결

[11.3]

- 달고나 모양 추가
- 게임 방식 변경

[11.4]

- 공통 타이머 reset 기능 수정
- 무궁화 영희 이미지 변경
- 무궁화 술래 사운드에 맞춰 플레이하는 방식으로 변경
- 무궁화 NPC 가 상하좌우로 랜덤하게 돌아다님
- 공통 리셋 타이머 수정
- 달고나 플레이 도중 진행요원이 돌아다님(드라마 반영)
- 달고나 사운드작업

[11.5]

- 달고나 Wrong point 추가
- 핀 아트워크 추가 cleanPNG 오픈아트워크 사이트
- 무궁화 finding effect pngALL

[11.11]

- 통합 작업 완료.
- [x] T사운드 삽입 요원 상하좌우 이동. ODO IN THIS WEEK

- NPC move 4way after level 3.
- Fix reset timer
- Add sound effect
- Dalgona broke when click wrong point
- Change doll image
- Screen filck red
- NPC move around while Dalgona playing
- ** Code cleaning
- Add pin artwork

TODO

- [ ] 메세지 출력부분 간소화. => 따로 파일 만들어도 좋을듯? => \n 이용해서 함수 한번에 어떻게 안되나 보기
- [ ] 두번째 라운드부터는 시작화면 안보여야함
- [ ] Main 클린코드
- [ ] 무궁화 시작화면 없애기. 자막으로 사운드를 키워 주세요만 나타나도록.
- [ ] 스코어 화면 npc 돌아다니게
- [ ] 사운드파일 try-catch
- [x] 인트로, 패배, 승리화면 정리
- [x] 레벨 연동 시스템 => 레벨 연동해서 난이도 증가해야함f
- [x] 스코어 화면에 띄우기
- [x] 볼륨 통일
- [x] 각 게임 패배했을 때 pygame.quit() 하면 안됨. 점수 렌더화면으로 못넘어감
- [x] 달고나 랜덤
- [x] 중간에 탈락하면 게임 꺼져야함 => 총 이미지 렌더링
- [x] Main 에서 나가기 누르면 나가져야함
- [x] 스코어 화면 버그픽스 ( 화면 멈춰버림 )
- [x] 게임 종료 시 스코어 출력
- [x] 달고나 npc 무궁화에서 가져와서 사용.
- [x] 스코어 받아오기 FINISHED
- Npc aim 클래스 구분
- 통합작업 위해 모두 절대경로로 변경
- 사운드 깃허브 내리기 => try - catch 문
- 클린코드 최대로 ( 따로 상수 저장해놓은 파일로 정리하라는 피드백 반영해 만들었음. 방식이 맞는지는 모르겠음.)
- 팀원 모두 주석작업 열심히
- 사운드 볼륨 통일.
- Npc / aim 클래스 구분
- 게임 이었음
- 스코어 연결
-

[11.12]
버튼 이미지 cleanPNG 버튼 이미지 365PSD.com

업다운 이미지 clipartmax.com
