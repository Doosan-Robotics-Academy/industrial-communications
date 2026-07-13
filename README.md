# Doosan Robotics DRL 산업용 통신 예제

Doosan Robotics **DRL(Doosan Robot Language)** 기반 산업용 통신 교육 예제 모음입니다.
Modbus TCP 및 TCP/IP Socket 통신의 Master/Slave, Client/Server 구조를 학습용으로 구성했습니다.

## 구성

```
doosan-drl-comm/
├── examples/
│   ├── modbus_tcp/
│   │   ├── modbus_tcp_master.drl   # 로봇이 Master(Client): 외부 PLC/IO 읽기·쓰기
│   │   └── modbus_tcp_slave.drl    # 로봇이 Slave(Server): 상위 SCADA/HMI가 접근
│   └── socket/
│       ├── socket_client.drl       # 로봇이 Client: 비전/상위 PC에 접속
│       └── socket_server.drl       # 로봇이 Server: 클라이언트 명령 수신·처리
├── tools/
│   └── test_socket_server.py       # 하드웨어 없이 socket_client.drl 테스트용 PC 서버
└── docs/
    └── protocol.md                 # 예제에서 사용한 통신 규약 정리
```

## 예제 요약

| 파일 | 로봇 역할 | 상대 | 용도 |
|------|-----------|------|------|
| `modbus_tcp_master.drl` | Master(Client) | PLC, I/O 모듈 | 외부 레지스터/코일 읽기·쓰기, 생산 카운트 폴링 |
| `modbus_tcp_slave.drl`  | Slave(Server)  | SCADA, HMI, 상위 PLC | 로봇 상태 게시 + 상위 명령 수신 |
| `socket_client.drl`     | Client         | 비전 시스템, 상위 PC | 좌표 요청·수신·이동·완료 통보 |
| `socket_server.drl`     | Server         | 상위 PC, HMI | HOME/MOVE/STATE/QUIT 명령 처리 |

## 사용 방법

1. Doosan **DART-Studio / Teach Pendant**에서 `.drl` 파일을 프로젝트로 불러옵니다.
2. 각 파일 상단의 접속 파라미터(IP, Port, 슬레이브 주소)를 실제 설비에 맞게 수정합니다.
3. Modbus 예제는 슬레이브 장비 또는 시뮬레이터(예: ModbusPal, pymodbus)와 연동합니다.
4. Socket Client 예제는 `tools/test_socket_server.py`로 PC에서 바로 테스트할 수 있습니다.

```bash
# PC에서 테스트 서버 실행 (socket_client.drl과 페어)
python tools/test_socket_server.py --host 0.0.0.0 --port 20002
```

## ⚠️ 중요 (교육 진행 시 반드시 안내)

DRL 통신 함수(`add_modbus_signal`, `client_socket_read`, `server_socket_open` 등)의
**인자 구성·반환 형식·지원 여부는 컨트롤러 SW 버전(M/A/H 시리즈, DART-Platform)에
따라 다릅니다.** 실제 장비 적용 전 **반드시 해당 버전의 공식 프로그래밍 매뉴얼로
함수 시그니처를 검증**하세요. 본 예제의 좌표·주소·프로토콜은 학습용 임의값입니다.

## 라이선스

MIT License — 자유롭게 교육에 활용·수정하세요.
