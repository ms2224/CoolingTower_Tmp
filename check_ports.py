from serial.tools import list_ports

print("現在接続されているシリアルポートの一覧:")
print("-" * 40)

ports = list_ports.comports()

if not ports:
    print("シリアルポートが見つかりません。")
else:
    for port in ports:
        print(f"ポート: {port.device}")
        print(f"  説明: {port.description}")
        print(f"  HWID: {port.hwid}")
        print("-" * 20)

print("-" * 40)