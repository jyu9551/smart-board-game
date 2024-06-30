# 0시작, 겹치는 말 위치, 효과음, LED, 말사진
import pygame
import random  # 주사위 난수
import time
import serial

# 아두이노 통신
ser2 = serial.Serial('COM5',9600)  # 시리얼 포트, 속도
time.sleep(2)  # 아두이노 재부팅, 초기화 대기
dice_go = 'r'  # 전송할 변수

# 라즈베리파이 통신
port = 'COM4'  # 라즈베리 파이의 시리얼 포트 경로
#baudrate = 115200  # 시리얼 통신 속도
baudrate = 9600

# 시리얼 포트 설정
ser = serial.Serial(port, baudrate)
ser.close()

pygame.init()
pygame.mixer.init()

# SCREEN WIDTH AND SCREEN HEIGHT :
screen_w, screen_h = 1200, 675

# CREATING THE PYGAME DISPLAY :
gameWindow = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Snakes and Ladders")

# FONT :
font1 = pygame.font.SysFont("Franklin Gothic Demi Cond", 40)
font2 = pygame.font.SysFont("Franklin Gothic Demi Cond", 35)

# CLOCK AND FPS :
fps = 60
clock = pygame.time.Clock()

# LOADING THE SNAKES AND LADDERS BOARD :
board = pygame.image.load("data/images/board.png")
board = pygame.transform.scale(board, (896, 675)).convert_alpha()

# LOGO :
logo = pygame.image.load("data/images/logo.png").convert_alpha()

# DICE IMAGES :
dice_images = []
for i in range(1, 7):
    dice_i = pygame.image.load("data/images/dice/" + str(i) + ".jpg")
    dice_i = pygame.transform.scale(dice_i, (90, 83)).convert_alpha()
    dice_images.append(dice_i)

roll_dice = []
for i in range(1, 7):
    roll_i = pygame.image.load("data/images/dice/roll/" + str(i) + ".png")
    if i % 2 != 0:
        roll_i = pygame.transform.scale(roll_i, (120, 109)).convert_alpha()
    else:
        roll_i = pygame.transform.scale(roll_i, (90, 83)).convert_alpha()
    roll_dice.append(roll_i)

# SNAKES AND LADDERS LIST IN THE GIVEN BOARD :
ladders = {3: ([[207, 580], [121, 516], [35, 452]], 21),
           8: ([[637, 580], [716, 508], [809, 452]], 30),
           58: ([[207, 260], [247, 187], [293, 132]], 77),
           75: ([[465, 132], [458, 100], [465, 68]], 86),
           80: ([[35, 132], [35, 68], [52, 4]], 100),
           28: ([[637, 452], [565, 362], [485, 272], [410, 182], [335, 92], [293, 68]], 84),
           90: ([[809, 68], [810, 36], [809, 4]], 91)
           }

snakes = {17: (
    [[293, 516], [320, 490], [360, 510], [405, 510], [465, 460], [525, 505], [570, 525], [610, 505], [637, 516]], 13),
    52: (
        [[723, 260], [742, 260], [751, 290], [718, 335], [700, 375], [754, 422], [775, 400], [729, 400], [729, 435],
         [723, 452]], 29),
    57: (
        [[293, 260], [283, 240], [233, 260], [239, 300], [247, 340], [212, 380], [167, 340], [122, 308], [88, 338],
         [68, 358], [35, 388]], 40),
    62: (
        [[121, 196], [121, 206], [136, 236], [138, 266], [103, 286], [128, 311], [148, 351], [111, 381], [131, 421],
         [121, 452]], 22),
    88: (
        [[637, 68], [652, 68], [677, 138], [647, 188], [607, 188], [537, 228], [517, 288], [467, 328], [407, 328],
         [360, 378], [340, 428], [270, 428], [220, 468], [207, 516]], 18),
    95: ([[465, 4], [480, -15], [540, 12], [570, 2], [610, -15], [660, -10], [703, 20], [720, 80], [750, 90],
          [826, 90], [816, 150], [810, 210], [809, 260]], 51),
    97: ([[293, 4], [246, -15], [212, 15], [242, 45], [250, 75], [200, 95], [150, 105], [121, 132]], 79)
}

# STARTING COORDINATES :
starting_coords = {2: [[950, 590], [1090, 590]],
                   3: [[950, 590], [1090, 590], [1020, 460]],
                   4: [[950, 590], [1090, 590], [950, 460], [1090, 460]]}


# PLAYER CLASS
class Player:
    def __init__(self, current_block, coordinates, piece, is_open):
        self.current_block = current_block
        self.coordinates = coordinates
        self.piece = piece
        self.is_open = is_open


# FUNCTION TO WRITE ON THE SCREEN
def text_on_screen(text, color, x, y, font=font1):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# FUNCTION TO ASCEND A PLAYER OVER A LADDER :
def ascend(players, turn):
    ladder = ladders[players[turn].current_block][0]
    index = 0
    players[turn].coordinates = ladder[index]

    change = time.time()
    while index < len(ladder):
        if time.time() - change > 0.2:
            index += 1
            if index == len(ladder):
                break
            players[turn].coordinates = ladder[index]
            change = time.time()

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        sound4 = pygame.mixer.Sound("data/audios/ladder.mp3") ################################################음악4
        sound4.play()
        clock.tick(fps)
        pygame.display.update()

    players[turn].coordinates = ladder[-1].copy()  # .copy() is necessary
    players[turn].current_block = ladders[players[turn].current_block][1]


# FUNCTION TO DESCEND A PLAYER FROM A SNAKE :
def descend(players, turn):
    snake = snakes[players[turn].current_block][0]
    index = 0
    players[turn].coordinates = snake[index]

    change = time.time()
    while index < len(snake):
        if time.time() - change > 0.2:
            index += 1
            if index == len(snake):
                break
            players[turn].coordinates = snake[index]
            change = time.time()

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        sound5 = pygame.mixer.Sound("data/audios/snake.mp3") ################################################음악5
        sound5.play()
        clock.tick(fps)
        pygame.display.update()

    players[turn].coordinates = snake[-1].copy()  # .copy() is necessary
    players[turn].current_block = snakes[players[turn].current_block][1]


# RECURSIVE FUNCTION TO MOVE A PLAYER :
def move_player(players, turn, dice, won):  # 눈금 수에 따라 플레이어 이동
    if players[turn].current_block + dice > 100:  # 100보다 큰 경우, 종료
        return

    if dice == 1:  # BASE CASE, 주사위 1인 경우
        if players[turn].current_block % 10 == 0:  # 10의 배수인 경우, 위로 이동
            players[turn].coordinates[1] -= 64
        else:  # 10의 배수가 아닌 경우 몇 번째 줄인지 확인 후 좌/우 이동
            first_digit = players[turn].current_block // 10
            if first_digit % 2 == 0:
                players[turn].coordinates[0] += 86
            else:
                players[turn].coordinates[0] -= 86
        gameWindow.blit(board, (0, 0))  # 보드 창에 띄움
        gameWindow.blit(logo, (885, -10))  # 로고 창에 띄움
        for player in players:  # 플레이어 위치 창에 띄움
            gameWindow.blit(player.piece, player.coordinates)
        sound2 = pygame.mixer.Sound("data/audios/jump.mp3") ################################################음악2
        sound2.play()

        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트
        players[turn].current_block += 1  # 플레이어 위치 1 증가
        if players[turn].current_block in ladders.keys():  # 사다리를 만났을 때
            ascend(players, turn)
        elif players[turn].current_block in snakes.keys():  # 뱀을 만났을 때
            descend(players, turn)
        if players[turn].current_block == 100:  # 플레이어의 위치가 100일 때,
            won.append(turn)  # 승리한 플레이어 리스트에 추가
            if len(won) == len(players) - 1:  # 승리 자리 꽉찼을 때, 종료
                game_over(won)

    else:  # 주사위 1 아닌 경우
        if players[turn].current_block % 10 == 0:  # 10의 배수인 경우, 위로 이동
            players[turn].coordinates[1] -= 64
        else:  # 10의 배수가 아닌 경우 몇 번째 줄인지 확인 후 좌/우 이동
            first_digit = players[turn].current_block // 10
            if first_digit % 2 == 0:
                players[turn].coordinates[0] += 86
            else:  
                players[turn].coordinates[0] -= 86
        gameWindow.blit(board, (0, 0))  # 보드 창에 띄움
        gameWindow.blit(logo, (885, -10))  # 로고 창에 띄움
        for player in players:  # 플레이어 위치 창에 띄움
            gameWindow.blit(player.piece, player.coordinates)
        sound2 = pygame.mixer.Sound("data/audios/jump.mp3") ################################################음악2
        sound2.play()
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트
        players[turn].current_block += 1  # 플레이어 위치 1 증가
        time.sleep(0.4)  # 0.4초 대기
        # 1일 때는, 실행 X
        move_player(players, turn, dice - 1, won)  # 계속해서 1칸씩 이동


# FUNCTION TO CHANGE THE TURN :
def change_turn(turn, num_players):  # 턴 변경
    if turn < num_players - 1:  # 턴이 플레이어 수보다 작으면, 다음 플레이어
        return turn + 1
    else:  # 같으면 첫 번째 플레이어
        return 0

global cnt
cnt = 0
ser.open()
def read_serial():
    global cnt 
    if cnt > 0:
        time.sleep(15)
    ser.flushInput()
    #ser.open()
    while True:
        #print(ser.in_waiting)
        if ser.in_waiting > 0:  # 수신 데이터가 있는지 확인
            #print("waiting_end")
            received_data = ser.read(1).decode()  # 데이터 수신 및 디코딩
            ser.read_all()
            #ser.close()
            cnt = cnt + 1
            #print(received_data)
            return int(received_data)


# FUNCTION TO ROLL T
# HE DICE :
def dice_roll(players):  # 주사위를 굴려 결과를 화면에 구현
    index = 0  # 현재 이미지 인덱스
    change = time.time()  # 현재 시간 변수 초기화

    dice = read_serial()
    print("Received dice value:", dice)

    sound1 = pygame.mixer.Sound("data/audios/dice.mp3") ################################################음악1
    sound1.play()

    ser2.write(dice_go.encode())
    #print(dice_go)

    while index < len(roll_dice):  # 인덱스가 이미지 리스트의 길이보다 작을 때 루프
        if time.time() - change > 0.2:  # 경과한 시간이 0.2초 일 때
            index += 1  # 다음 이미지
            if index == len(roll_dice):  # 이미지 길이와 같으면
                break  # 루프 종료
            change = time.time()  # 시간  업데이트
        gameWindow.fill((255, 255, 255))  # 게임 창 흰색으로 채움
        if index % 2 == 0:  # 이미지가 홀수일 때
            gameWindow.blit(roll_dice[index], (985, 194))  # 이미지 위치
        else:  # 짝수일 때
            gameWindow.blit(roll_dice[index], (1003, 207))  # 이미지 위치
        gameWindow.blit(board, (0, 0))  # 보드 이미지
        gameWindow.blit(logo, (885, -10))  # 로고 이미지
        for player in players:  # 플레이어 좌표에 그림b 
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트

    gameWindow.blit(dice_images[dice - 1], (1003, 207))  # 최종 주사위 값 그림
    clock.tick(fps)  # 프레임   
    pygame.display.update()  # 창 업데이트
    time.sleep(1)  # 1초 대기
    return dice, dice_images[dice - 1]  # 결과값과 이미지 반환

def random_dice_roll(players):  # 주사위를 굴려 결과를 화면에 구현
    index = 0  # 현재 이미지 인덱스
    change = time.time()  # 현재 시간 변수 초기화
    dice = random.randint(1, 6)  # 주사위 난수 발생
    # dice = read_serial()
    # print("Received dice value:", dice)

    # ser2.write(dice_go.encode())
    # print(dice_go)

    while index < len(roll_dice):  # 인덱스가 이미지 리스트의 길이보다 작을 때 루프
        if time.time() - change > 0.2:  # 경과한 시간이 0.2초 일 때
            index += 1  # 다음 이미지
            if index == len(roll_dice):  # 이미지 길이와 같으면
                break  # 루프 종료
            change = time.time()  # 시간  업데이트
        gameWindow.fill((255, 255, 255))  # 게임 창 흰색으로 채움
        if index % 2 == 0:  # 이미지가 홀수일 때
            gameWindow.blit(roll_dice[index], (985, 194))  # 이미지 위치
        else:  # 짝수일 때
            gameWindow.blit(roll_dice[index], (1003, 207))  # 이미지 위치
        gameWindow.blit(board, (0, 0))  # 보드 이미지
        gameWindow.blit(logo, (885, -10))  # 로고 이미지
        for player in players:  # 플레이어 좌표에 그림b 
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트

    gameWindow.blit(dice_images[dice - 1], (1003, 207))  # 최종 주사위 값 그림
    clock.tick(fps)  # 프레임   
    pygame.display.update()  # 창 업데이트
    time.sleep(1)  # 1초 대기
    return dice, dice_images[dice - 1]  # 결과값과 이미지 반환


# GAME OVER DISPLAY :
def game_over(won):  # 게임 종료 시 결과 화면 구현

    pygame.mixer.music.load("data/audios/25 Course Clear.mp3")  # 음악 파일 로드
    pygame.mixer.music.play()  # 재생

    pedestal_1 = pygame.image.load("data/images/display/pedestal1.png").convert_alpha()  # 이미지 로드
    pedestal_2 = pygame.image.load("data/images/display/pedestal2.png").convert_alpha()  # 이미지 로드

    gogo = 's' #########################################################################################LED
    ser2.write(gogo.encode())

    winners = []  # 승리한 플레이어 이미지 리스트
    for index in won:  # 'won'리스트 반복
        winner_index = pygame.image.load("data/images/pieces/" + str(index + 1) + ".png").convert_alpha()  # 이미지 로드
        winners.append(winner_index)  # 이미지 리스트에 추가

    exit_screen = False  # 종료 화면 플래그
    current_image = pedestal_1  # 현재 화면 이미지
    change = time.time()  # 시간 변수 초기화
    coordinates = [[557, 207], [262, 242], [832, 249]]  # 승리 플레이어 이미지 좌표

    while not exit_screen:  # 종료 화면 나타날 때까지 반복
        for event in pygame.event.get():  # 발생한 이벤트 처리
            if event.type == pygame.QUIT:  # 종료 이벤트 발생, 루프 종료
                exit_screen = True
            elif event.type == pygame.KEYDOWN:  # 키 눌렸을 때, 이벤트 처리
                if event.key == pygame.K_RETURN:  # ENTER키가 눌렸을 때, 배경음악 정지하고 홈화면 돌아감
                    pygame.mixer.music.stop()
                    home_screen()
        if time.time() - change >= 0.2:  # 경과 시간 0.2초 이상일 때, 이미지 변환
            if current_image == pedestal_1:  
                current_image = pedestal_2
            else:
                current_image = pedestal_1
            change = time.time()  # 시간 업데이트

        gameWindow.blit(current_image, (0, 0))  # 현재 이미지 창에 그림
        for j in range(len(winners)):  # 리스트 길이만큼 반복
            gameWindow.blit(winners[j], coordinates[j])  # 승리 플레이어 좌표에 그림
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 게임 창 업데이트

    pygame.quit()  # 게임 종료
    quit()  # 프로그램 종료


# GAME LOOP FUNCTION :
def game_loop(num_players):  # 주어진 플레이어 수에 따라 게임 실행
    dice_screen = 0

    # 플레이어 수에 따라 게임 실행, 플레이어 조작에 따라 진행과 이동, 음악 재생, 화면 업데이트
    pygame.mixer.music.stop()  # 현재 재생 음악 정지
    playlist = ["data/audios/05 Super Mario 64 Main Theme.mp3",  # 음악 리스트 정의
                "data/audios/11 Snow Mountain.mp3",
                "data/audios/07 Inside The Castle Walls.mp3",
                "data/audios/06 Slider.mp3",
                "data/audios/02 Title Theme.mp3"]

    playlist_i = 0  # 현재 재생 음악 인덱스
    pygame.mixer.music.load(playlist[0])  # 현재 재생 음악 인덱스
    pygame.mixer.music.play()  # 음악 재생
    pygame.mixer.music.set_volume(0.4) ##################################################################음악
    change = time.time()  # 음악 변경을 위한 시간 기록

    players = []  # list of all players, 모든 플레이어 저장
    won = []  # 승리한 플레이어 저장
    turn = 0  # variable to decide turn, 턴을 결정
    colors = [(255, 255, 0), (54, 238, 8), (26, 202, 255), (255, 0, 0)]  # 플레이어 색상
    for j in range(num_players):  # 플레이어 수만큼 반복하여 플레이어 생성
        piece = pygame.image.load("data/images/pieces/" + str(j + 1) + ".png")  # 플레이어 이미지 로드
        piece = pygame.transform.scale(piece, (55, 75)).convert_alpha()  # 플레이어 이미지 크기, 알파 채널 변환
        players.append(Player(0, starting_coords[num_players][j].copy(), piece, False))  # 플레이어 클래스의 인스턴스 생성, 플레이어 초기 블록, 좌표, 이미지 및 오픈 여부

    count6 = 0  # variable to count number of sixes, 주사위 6인 횟수 세는 변수
    exit_game = False  # 게임 종료 여부
    dice_image = dice_images[0]  # 주사위 이미지

    while not exit_game:  # 게임 종료 여부에 따라 무한루프
        gameWindow.fill((255, 255, 255))  # 게임 창 배경 -> 흰색
        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:  # 종료 이벤트 발생하면, 게임 종료
                exit_game = True
            elif event.type == pygame.USEREVENT:  # 추가적인 동작
                if playlist_i == 2:  # 인데스 2일 때, 해당 음악 대기열 추가
                    pygame.mixer.music.queue(playlist[2])
                    playlist_i = 0  # 재생목록 끝에 도달한 경우 다시 첫 번째 음악 재생
            elif event.type == pygame.KEYDOWN:  # 키가 눌리면, 다음 동작 수행
                if event.key == pygame.K_SPACE:  # 스페이스바 눌리면, 주사위 굴리고 게임 진행
                    print("space")
                elif event.key == pygame.K_w:  # 'w'를 누르면, 첫 번째 플레이어 98 지점으로 이동
                    players[0].is_open = True
                    players[0].current_block = 98
                    players[0].coordinates = [535 + 2 * 86, 4]
                elif event.key == pygame.K_a:  # 'a'를 누르면, 두 번째 플레이어 98 지점으로 이동
                    players[1].is_open = True
                    players[1].current_block = 98
                    players[1].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_s:  # 's'를 누르면, 세 번째 플레이어 98 지점으로 이동
                    players[2].is_open = True
                    players[2].current_block = 98
                    players[2].coordinates = [35 + 2 * 86, 4]

        if dice_screen > 3:
            ser2.write(str(turn).encode())
            print(str(turn))

            dice, dice_image = dice_roll(players)  # 주사위를 굴림
            if dice == 6:  # 6이면, 횟수를 세고 승리 여부 확인
                sound3 = pygame.mixer.Sound("data/audios/one.mp3") ################################################음악3
                sound3.play()
                count6 += 1  # 6의 횟수 증가
                if players[turn].current_block + count6 * 6 >= 100:  # 100 이상이면, 승리한 플레이어로 처리
                    turn = change_turn(turn, num_players)  # 턴을 변경
                    count6 = 0
                else:
                    if count6 == 3:
                        turn = change_turn(turn, num_players)
                        count6 = 0
            else:    # 6이 아닌 경우
                # 주사위와 6의 횟수에 따라 이동
                if not players[turn].is_open:
                    players[turn].current_block = 1
                    #players[turn].coordinates = [35, 580]#####86###################################겹치는 말 위치
                    if turn == 0:
                        players[turn].coordinates = [20,580]
                    elif turn == 1:
                        players[turn].coordinates = [35,580]
                    elif turn == 2:
                        players[turn].coordinates = [45,580]
                    else:
                        players[turn].coordinates = [55,580]
                    players[turn].is_open = True
                    if count6 == 0:####################################################################0시작
                        if dice != 1:
                            move_player(players, turn, dice - 1, won)
                        turn = change_turn(turn, num_players)
                    else:
                        move_player(players, turn, (count6 * 6) + dice - 1, won)
                        count6 = 0
                        turn = change_turn(turn, num_players)
                else:
                    if count6 == 0:
                        move_player(players, turn, dice, won)
                        turn = change_turn(turn, num_players)
                    else:
                        move_player(players, turn, (count6 * 6) + dice, won)
                        count6 = 0
                        turn = change_turn(turn, num_players)

            while turn in won:  # 승리한 플레이어인 경우, 턴을 변경
                turn = change_turn(turn, num_players)

        gameWindow.blit(board, (0, 0))  # 게임 보드를 표시
        gameWindow.blit(logo, (885, -10))  # 게임 로고 표시
        pygame.draw.rect(gameWindow, colors[turn], [896, 300, 304, 25])  # 턴을 나타내는 바
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 300, 304, 25], 2)  # 바의 외곽선
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])  # 화면에 다른 메시지 표시하는 바
        text_on_screen("PLAYER " + str(turn + 1) + "'S TURN", (255, 0, 0), 915, 345)  # 플레이어 번호
        pygame.draw.rect(gameWindow, colors[turn], [896, 410, 304, 25])  # 또 다른 바
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 410, 304, 25], 2)  # 바의 외곽선

        for player in players:  # 플레이어 화면에 표시
            gameWindow.blit(player.piece, player.coordinates)  # 이미지를 위치에 배치
        gameWindow.blit(dice_image, (1003, 207))  # 주사위 이미지를 표시

        if time.time() - change >= 120:  # 120초 경과한 경우
            if playlist_i == 4:  # 인덱스가 4인 노래의 경우
                playlist_i = 0  # 0으로 설정
            else:  # 인덱스 4가 아닌 경우
                playlist_i += 1 # 다음 노래
            pygame.mixer.music.load(playlist[playlist_i])  # 음악 로드
            pygame.mixer.music.play()  # 음악 재생
            pygame.mixer.music.set_volume(0.4) ##########################################################음악
            change = time.time()  # 시간 업데이트

        clock.tick(fps)  # 프레임
        pygame.display.update()  # 창 업데이트
        dice_screen += 1

    pygame.quit()  # 게임 종료
    quit()  # 파이썬 종료


# GAME LOOP FUNCTION (VS COMPUTER) :
def game_loop_vs_computer(num_players):  # 플레이어와 컴퓨터간의 게임
    dice_screen = 0

    pygame.mixer.music.stop()  # 현재 재생 음악 정지
    playlist = ["data/audios/05 Super Mario 64 Main Theme.mp3",  # 음악 리스트 정의
                "data/audios/11 Snow Mountain.mp3",
                "data/audios/07 Inside The Castle Walls.mp3",
                "data/audios/06 Slider.mp3",
                "data/audios/02 Title Theme.mp3"]

    playlist_i = 0  # 현재 재생 음악 인덱스
    pygame.mixer.music.load(playlist[0])  # 첫 번재 음악 로드
    pygame.mixer.music.play()  # 음악 재생
    change = time.time()  # 음악 변경을 위한 시간 기록

    players = []  # list of all players, 모든 플레이어 저장
    won = []  # 승리한 플레이어 저장
    turn = 0  # variable to decide turn, 턴을 결정
    colors = [(255, 255, 0), (54, 238, 8), (26, 202, 255), (255, 0, 0)]  # 플레이어 색상
    for j in range(num_players):  # 플레이어 수만큼 반복하여 플레이어 생성
        piece = pygame.image.load("data/images/pieces/" + str(j + 1) + ".png")  # 플레이어 이미지 로드
        piece = pygame.transform.scale(piece, (55, 75)).convert_alpha()  # 플레이어 이미지 크기, 알파 채널 변환
        players.append(Player(0, starting_coords[num_players][j].copy(), piece, False))  # 플레이어 클래스의 인스턴스 생성, 플레이어 초기 블록, 좌표, 이미지 및 오픈 여부

    count6 = 0  # variable to count number of sixes, 주사위 6인 횟수 세는 변수
    exit_game = False  # 게임 종료 여부
    dice_image = dice_images[0]  # 주사위 이미지

    while not exit_game:  # 게임 종료 여부에 따라 무한루프
        gameWindow.fill((255, 255, 255))  # 게임 창 배경 -> 흰색
        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:  # 종료 이벤트 발생하면, 게임 종료
                exit_game = True
            elif event.type == pygame.KEYDOWN:  # 키가 눌리면, 다음 동작 수행
                if event.key == pygame.K_SPACE:  # 스페이스바 눌리면, 주사위 굴리고 게임 진행
                    print("space")
                elif event.key == pygame.K_w:  # 'w'를 누르면, 첫 번째 플레이어 98 지점으로 이동
                    players[0].is_open = True
                    players[0].current_block = 98
                    players[0].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_a:  # 'a'를 누르면, 두 번째 플레이어 98 지점으로 이동
                    players[1].is_open = True
                    players[1].current_block = 98
                    players[1].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_s:  # 's'를 누르면, 세 번째 플레이어 98 지점으로 이동
                    players[2].is_open = True
                    players[2].current_block = 98
                    players[2].coordinates = [35 + 2 * 86, 4]

        if dice_screen > 3 and turn == 0:
            ser2.write(str(turn).encode())
            print(str(turn))

            dice, dice_image = dice_roll(players)  # 주사위를 굴림
            if dice == 6:  # 6이면, 횟수를 세고 승리 여부 확인
                count6 += 1  # 6의 횟수 증가
                if players[turn].current_block + count6 * 6 >= 100:  # 100 이상이면, 승리한 플레이어로 처리
                    turn = change_turn(turn, num_players)  # 턴을 변경
                    count6 = 0
                else:
                    if count6 == 3:
                        turn = change_turn(turn, num_players)
                        count6 = 0
            else:    # 6이 아닌 경우
                # 주사위와 6의 횟수에 따라 이동
                if not players[turn].is_open:
                    players[turn].current_block = 1
                    players[turn].coordinates = [35, 580]
                    players[turn].is_open = True

                if count6 == 0:
                    move_player(players, turn, dice, won)
                    turn = change_turn(turn, num_players)
                else:
                    move_player(players, turn, (count6 * 6) + dice, won)
                    count6 = 0
                    turn = change_turn(turn, num_players)

            while turn in won:  # 승리한 플레이어인 경우, 턴을 변경
                turn = change_turn(turn, num_players)

        gameWindow.blit(board, (0, 0))  # 게임 보드를 표시
        gameWindow.blit(logo, (885, -10))  # 게임 로고 표시
        for player in players:  # 플레이어 화면에 표시
            gameWindow.blit(player.piece, player.coordinates)  # 이미지를 위치에 배치
        gameWindow.blit(dice_image, (1003, 207))  # 주사위 이미지를 표시

        # 현재 턴을 확인, 턴에 따라 화면에 메시지를 표시, 주사위를 굴리고 플레이어 이동
        if turn != 0:  # 턴이 0이 아닌 경우 화면에 컴퓨터 턴을 표시
            pygame.draw.rect(gameWindow, colors[turn], [896, 300, 304, 25])  # 턴을 나타내는 바
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 300, 304, 25], 2)  # 바의 외곽선
            pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])  # 화면에 다른 메시지 표시하는 바
            text_on_screen("COMPUTER " + str(turn) + "'S TURN", (255, 0, 0), 905, 347, font2)  # 컴퓨터 번호
            pygame.draw.rect(gameWindow, colors[turn], [896, 410, 304, 25])  # 또 다른 바
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 410, 304, 25], 2)  # 바의 외곽선
            clock.tick(fps)  # 프레임 속도 조절
            pygame.display.update()  # 화면 업데이트
            time.sleep(1)  # 1초 대기
            if dice_screen > 3:
                ser2.write(str(turn).encode())
                print(str(turn))

                dice, dice_image = random_dice_roll(players)  # 주사위를 굴림
                if dice == 6:  # 6이면, 횟수를 세고 승리 여부 확인
                    count6 += 1  # 6의 횟수 증가
                    if players[turn].current_block + count6 * 6 >= 100:  # 100 이상이면, 승리한 플레이어로 처리
                        turn = change_turn(turn, num_players)  # 턴을 변경
                        count6 = 0
                    else:
                        if count6 == 3:
                            turn = change_turn(turn, num_players)
                            count6 = 0
                else:    # 6이 아닌 경우
                    # 주사위와 6의 횟수에 따라 이동
                    if not players[turn].is_open:
                        players[turn].current_block = 1
                        players[turn].coordinates = [35, 580]
                        players[turn].is_open = True

                    if count6 == 0:
                        move_player(players, turn, dice, won)
                        turn = change_turn(turn, num_players)
                    else:
                        move_player(players, turn, (count6 * 6) + dice, won)
                        count6 = 0
                        turn = change_turn(turn, num_players)

                while turn in won:  # 승리한 플레이어인 경우, 턴을 변경
                    turn = change_turn(turn, num_players)

        if turn == 0:  # 플레이어 턴
            pygame.draw.rect(gameWindow, colors[0], [896, 300, 304, 25])  # 플레이어 턴을 나타내는 바
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 300, 304, 25], 2)  # 바의 외곽선
            pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])  # 화면에 다른 메시지 표시
            text_on_screen("PLAYER'S TURN", (255, 0, 0), 929, 345)  # 메시지 화면에 표시
            pygame.draw.rect(gameWindow, colors[0], [896, 410, 304, 25])  # 다른 바 그림
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 410, 304, 25], 2)  # 바의 외곽선

        if time.time() - change >= 120:  # 120초 경과한 경우
            if playlist_i == 4:  # 인덱스가 4인 노래의 경우
                playlist_i = 0  # 0으로 설정
            else:  # 인덱스 4가 아닌 경우
                playlist_i += 1 # 다음 노래
            pygame.mixer.music.load(playlist[playlist_i])  # 음악 로드
            pygame.mixer.music.play()  # 음악 재생
            change = time.time()  # 시간 업데이트

        clock.tick(fps)  # 프레임
        pygame.display.update()  # 창 업데이트
        dice_screen += 1

    pygame.quit()  # 게임 종료
    quit()  # 파이썬 종료


# SELECT NUMBER OF PLAYERS :
def num_of_players(vs_comp):  # 플레이어 수 선택 화면 구현
    # 플레이어 수 선택 화면, 키 이벤트 처리하여 선택된 플레이어 수에 따라 대전 모드 이미지 표시
    vs_2 = pygame.image.load("data/images/display/vs2.png").convert_alpha()  # 2명
    vs_3 = pygame.image.load("data/images/display/vs3.png").convert_alpha()  # 3명
    vs_4 = pygame.image.load("data/images/display/vs4.png").convert_alpha()  # 4명

    vs = [vs_2, vs_3, vs_4]  # 이미지 리스트로 저장
    exit_screen = False  # 화면 종료 여부
    current = 0  # 대전 모드

    while not exit_screen:  # 화면 종료 여부
        for event in pygame.event.get():  # pygame 이벤트 처리
            if event.type == pygame.QUIT:  # 창이 닫히면, 화면 종료
                exit_screen = True
            elif event.type == pygame.KEYDOWN:  # 키가 눌리면, 동작 수행
                if event.key == pygame.K_DOWN:  # DOWN키 눌리면 모드 변경
                    if current == 2:
                        current = 0
                    else:
                        current += 1
                elif event.key == pygame.K_UP:  # UP키 눌리면 모드 변경
                    if current == 0:
                        current = 2
                    else:
                        current -= 1
                elif event.key == pygame.K_RETURN:  # ENTER키 눌리면, 대전 모드에 따라 게임
                    if vs_comp:  # 컴퓨터와 대전 게임 실행
                        game_loop_vs_computer(current + 2)
                    else:  # 친구와 대전 게임 실행
                        game_loop(current + 2)

        gameWindow.blit(vs[current], (0, 0))  # 선택된 대전 모드 이미지 창에 표시
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트

    pygame.quit()  # 게임 종료
    quit()  # 파이썬 종료


# CHOOSE VERSUS :
def choose_versus():  # 게임 상대 선택 화면 구현
    # 상대 선택 화면 구현, 키 이벤트 처리로 모드 변경, 모드에 따라 이미지 표시
    vs_computer = pygame.image.load("data/images/display/vscomputer.png").convert_alpha()  # 컴퓨터 이미지
    vs_friends = pygame.image.load("data/images/display/vsfriends.png").convert_alpha()  # 친구와 대전 이미지

    exit_screen = False  # 화면 종료 여부
    vs_comp = True  # 컴퓨터와 대전하는 모드

    while not exit_screen:  # 화면 종료 여부에 따라 무한루프
        for event in pygame.event.get():  # 게임 이벤트 처리
            if event.type == pygame.QUIT:  # 창이 닫히면, 화면 종료
                exit_screen = True
            elif event.type == pygame.KEYDOWN:  # 키가 눌리면, 동작 수행
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:  # 오/왼 키가 눌리면 모드 전환
                    vs_comp = not vs_comp
                elif event.key == pygame.K_RETURN:  # ENTER가 눌리면, 모드에 따라 다음 화면
                    num_of_players(vs_comp)
        if vs_comp:  # 컴퓨터와 대전이므로 'vs_computer'이미지 표시
            gameWindow.blit(vs_computer, (0, 0))
        else:  # 친구와 대전이므로 'vs_friends'이미지 표시
            gameWindow.blit(vs_friends, (0, 0))

        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트

    pygame.quit()  # 게임 종료
    quit()  # 파이썬 종료


# HOME SCREEN :
def home_screen():  # 홈 화면 구현
    # 게임의 홈 화면 실행
    # 주어진 이미지 전환, 키 이벤트 처리, 게임 창을 업데이트 등의 작업 수행
    background_music = pygame.mixer.music.load("data/audios/27 Stage Boss.mp3")  # 배경 음악 로드
    pygame.mixer.music.play()  # 음악 재생

    home_screen_1 = pygame.image.load("data/images/display/homescreen1.png").convert_alpha()  # 홈 화면 이미지 로드
    home_screen_2 = pygame.image.load("data/images/display/homescreen2.png").convert_alpha()  # 두 번째 홈 로드

    gogo = 's' ##########################################################################################LED
    ser2.write(gogo.encode())

    exit_screen = False  # 화면 종료 여부
    current_image = home_screen_1  # 현재 화면 = 홈 화면
    change = time.time()  # 이미지 전환을 위한 시간 변수

    while not exit_screen:  # 화면 종료 여부가 False이면 무한 루프
        for event in pygame.event.get():  # pygame 이벤트 처리를 위한 루프
            if event.type == pygame.QUIT:  # 창이 닫히면, 화면 종료
                exit_screen = True
            elif event.type == pygame.KEYDOWN:  # 눌린 키 동작
                if event.key == pygame.K_RETURN:  # ENTER가 눌리면 함수 호출하여 다음 화면 이동
                    choose_versus()

        if time.time() - change >= 0.2:  # 일정 시간 0.2마다 이미지 전환
            if current_image == home_screen_1:  # 첫 번째 -> 두 번재 이미지
                current_image = home_screen_2
            else:  # 아니면 첫 번째 이미지
                current_image = home_screen_1
            change = time.time()

        gameWindow.blit(current_image, (-3, -50))  # 현재 이미지의 창 위치 정함
        clock.tick(fps)  # 프레임
        pygame.display.update()  # 화면 업데이트

    pygame.quit()  # game 종료
    quit()  # 파이썬 종료


home_screen()  # 화면 호출
