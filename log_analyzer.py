import csv
error_count = 0
error_lines = []
by_device = {}
hour_count = {}

log_path = "log1.txt"   # ←必要なら "log.txt" に変更

with open(log_path, encoding="utf-8") as f:
    for line in f:
        if "ERROR" not in line:
            continue

        parts = line.split()
        # 例: ["2026-02-26","10:02:11","ERROR","sensorA","failed"]
        if len(parts) < 4:
            # 形式が想定外のERROR行はスキップ（必要なら保存してもOK）
            continue

        error_count += 1
        error_lines.append(line.strip())

        device = parts[3]
        by_device[device] = by_device.get(device, 0) + 1

        time_part = parts[1]               # "10:02:11"
        hour = time_part.split(":")[0]     # "10"
        hour_count[hour] = hour_count.get(hour, 0) + 1

print("エラー総数:", error_count)

print("----エラー一覧----")
for e in error_lines:
    print(e)

print("----機器別エラー回数----")
for device, cnt in sorted(by_device.items()):
    print(device, cnt)

print("----時間帯エラー回数----")
for h, c in sorted(hour_count.items(), key=lambda x: x[0]):
    print(h, "時", c, "回")

# 機器別をCSV出力
with open("error_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["device", "error_count"])
    for device, cnt in sorted(by_device.items()):
        writer.writerow([device, cnt])

# 時間帯別もCSVにしたい場合（任意）
with open("error_by_hour.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["hour", "error_count"])
    for h, c in sorted(hour_count.items(), key=lambda x: x[0]):
        writer.writerow([h, c])

print("CSV出力完了")