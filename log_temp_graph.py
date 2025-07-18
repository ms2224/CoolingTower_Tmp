import serial
import datetime
import time
import matplotlib.pyplot as plt
import os
from serial.tools import list_ports

# --- 設定項目 ---
BAUD_RATE = 115200
OUTPUT_DIR = './logs'
# ----------------

def find_arduino_port():
    """Arduino公式・互換ボードを自動的に検索して返す"""
    ports = list_ports.comports()
    for port in ports:
        if 'VID:PID=2341' in port.hwid or 'CH340' in port.description:
            print(f"Arduinoまたは互換デバイスを発見しました: {port.device}")
            return port.device
    return None

# --- メイン処理 ---
SERIAL_PORT = find_arduino_port()

if not SERIAL_PORT:
    print("エラー: Arduinoが見つかりませんでした。接続を確認してください。")
    exit()

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"temperature_log_{timestamp}.dat")

print(f"データ記録およびグラフ表示プログラムを開始します。")
print(f"ポート: {SERIAL_PORT}, ログファイル: {OUTPUT_FILE}")
print("終了するにはグラフウィンドウを閉じるか Ctrl + C を押してください。")

timestamps = []
temperatures = []
start_time = time.time()

# --- グラフの初期設定 ---
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(timestamps, temperatures, 'r-') 

ax.set_ylim(20, 30)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.grid(True)

temp_text = ax.text(0.95, 0.95, '', transform=ax.transAxes,
                    fontsize=12, color='black',
                    ha='right', va='top',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7))


try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Relative Time(s) Temperature(C)\n")

        while plt.fignum_exists(fig.number):
            try:
                line_from_arduino = ser.readline().decode('utf-8').strip()
                if line_from_arduino:
                    try:
                        temperature = float(line_from_arduino)
                        relative_time = time.time() - start_time
                        timestamps.append(relative_time)
                        temperatures.append(temperature)
                        log_entry = f"{int(relative_time)} {temperature:.2f}\n"
                        f.write(log_entry)
                        f.flush()

                        line.set_xdata(timestamps)
                        line.set_ydata(temperatures)

                        ax.relim()
                        ax.autoscale_view(scalex=True, scaley=False)

                        temp_text.set_text(f'Recentry: {temperature:.2f} ℃')

                        fig.canvas.draw()
                        fig.canvas.flush_events()

                    except ValueError:
                        print(f"Arduinoから無効なデータを受信: {line_from_arduino}")

            except serial.SerialException as e:
                print(f"シリアルポートエラー: {e}")
                break
            except KeyboardInterrupt:
                print("プログラムを終了します。")
                break

except serial.SerialException as e:
    print(f"エラー: {SERIAL_PORT}に接続できません。")
    print(e)
finally:
    plt.ioff()
    print("プログラムを終了しました。")
    if 'ser' in locals() and ser.is_open:
        ser.close()