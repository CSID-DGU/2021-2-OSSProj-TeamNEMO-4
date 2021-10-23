import pygame

# 메인 함수 정의
def main():
    # 파이게임 모듈 초기화
    pygame.init()

    # 240 x 180 사이즈의 스크린 표면을 만듦
    screen = pygame.display.set_mode((1000, 500))
    # 메인 루프를 제어할 변수 정의
    running = True

    # 메인 루프
    while running:
        # 이벤트 핸들러, 이벤트 큐로부터 모든 이벤트를 얻는다.
        for event in pygame.event.get():
            # QUIT 타입의 이벤트라면 다음 코딩을 실행
            if event.type == pygame.QUIT:
                # 메인 루프를 탈출하기 위해 변수를 False 로 바꾼다.
                running = False


# 현재 모듈이 메인 스크립트라면 메인 함수 실행
# (이 모듈을 임포트하면 아무것도 실행하지 않는다)
if __name__ == "__main__":
    # call the main function
    main()

print("test2")
print("test3")
