# 통신 규약 (교육용)

본 예제에서 사용한 애플리케이션 프로토콜을 정리합니다. **모두 학습용 임의 규약**이며,
실제 현장에서는 설비/상위 시스템 규격에 맞춰 재정의해야 합니다.

## 1. Modbus TCP

표준 Modbus TCP를 사용합니다. 포트 502, Unit ID로 슬레이브를 구분합니다.

### Master 예제 (`modbus_tcp_master.drl`)

| 심볼 | 레지스터 타입 | 주소 | 방향 | 의미 |
|------|---------------|------|------|------|
| start_button   | Discrete Input   | 0   | 읽기 | 외부 시작 버튼 |
| conveyor_cmd   | Coil             | 0   | 쓰기 | 컨베이어 가동 명령 |
| part_count     | Input Register   | 100 | 읽기 | 생산 수량 |
| target_position| Holding Register | 200 | 쓰기 | 목표 위치/레시피 |

### Slave 예제 (`modbus_tcp_slave.drl`)

| 주소 | 타입 | 방향 | 의미 |
|------|------|------|------|
| 0   | Holding | 상위→로봇 | 명령 모드 (0 대기 / 1 홈 / 2 작업 / 9 정지) |
| 1   | Holding | 상위→로봇 | 속도 비율 (%) |
| 100 | Input   | 로봇→상위 | 상태 코드 |
| 101 | Input   | 로봇→상위 | 현재 TCP X (mm) |
| 102 | Input   | 로봇→상위 | 완료 사이클 수 |

## 2. TCP/IP Socket (텍스트 프로토콜)

라인 단위(`\n` 종료), 콤마 구분 문자열.

### Client 예제 (`socket_client.drl`)

| 방향 | 메시지 | 의미 |
|------|--------|------|
| 로봇→서버 | `REQ,POSE`               | 물체 좌표 요청 |
| 서버→로봇 | `POSE,x,y,z,rx,ry,rz`    | 좌표 회신 |
| 로봇→서버 | `DONE`                   | 작업 완료 통보 |

### Server 예제 (`socket_server.drl`)

| 방향 | 메시지 | 의미 |
|------|--------|------|
| 클라→로봇 | `HOME`                    | 홈 위치 이동 |
| 클라→로봇 | `MOVE,x,y,z,rx,ry,rz`     | 지정 좌표 이동 |
| 클라→로봇 | `STATE`                   | 현재 상태 요청 |
| 클라→로봇 | `QUIT`                    | 서버 종료 |
| 로봇→클라 | `OK` / `STATE,...` / `ERR,<사유>` | 응답 |
