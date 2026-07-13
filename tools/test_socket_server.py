#!/usr/bin/env python3
"""
socket_client.drl 테스트용 PC 서버 (교육용)
------------------------------------------------
로봇(클라이언트)이 접속하면:
  - "REQ,POSE" 수신 시  -> "POSE,x,y,z,rx,ry,rz" 회신 (샘플 좌표 순환)
  - "DONE"     수신 시  -> 완료 로그
하드웨어/비전 시스템 없이 통신 흐름을 검증할 수 있습니다.

실행:
    python test_socket_server.py --host 0.0.0.0 --port 20002
"""
import argparse
import socket

# 회신할 샘플 좌표 (교육용): x, y, z, rx, ry, rz
SAMPLE_POSES = [
    (500.0,  100.0, 300.0, 0.0, 180.0, 0.0),
    (500.0,    0.0, 300.0, 0.0, 180.0, 0.0),
    (500.0, -100.0, 300.0, 0.0, 180.0, 0.0),
]


def handle_conn(conn, addr):
    print(f"[SERVER] 접속됨: {addr}")
    idx = 0
    buf = ""
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print("[SERVER] 연결 종료됨")
                break
            buf += data.decode(errors="ignore")

            # 개행 단위로 라인 처리
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                print(f"[SERVER] RX: {line}")

                if line.startswith("REQ,POSE"):
                    p = SAMPLE_POSES[idx % len(SAMPLE_POSES)]
                    idx += 1
                    reply = "POSE,{},{},{},{},{},{}\n".format(*p)
                    conn.sendall(reply.encode())
                    print(f"[SERVER] TX: {reply.strip()}")
                elif line.startswith("DONE"):
                    print("[SERVER] 로봇 작업 완료 통보 수신")
                else:
                    print(f"[SERVER] 알 수 없는 명령: {line}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=20002)
    args = ap.parse_args()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.host, args.port))
    srv.listen(1)
    print(f"[SERVER] 리슨 중: {args.host}:{args.port}  (Ctrl+C 종료)")

    try:
        while True:
            conn, addr = srv.accept()
            handle_conn(conn, addr)
    except KeyboardInterrupt:
        print("\n[SERVER] 종료")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
