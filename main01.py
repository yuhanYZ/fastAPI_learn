import time
from pynput import keyboard

# 定义判定连击的毫秒阈值（通常机械轴体抖动连击在 5ms - 60ms 之间）
CHATTER_THRESHOLD_MS = 80

last_press_time = None
chatter_count = 0
total_backspace_count = 0

print("=" * 60)
print(" 键盘退格键 (Backspace) 连击监控工具已启动...")
print(f" 当前连击判定阈值: < {CHATTER_THRESHOLD_MS} ms")
print(" 请将此窗口挂在后台，正常打字/写代码即可。按下 Ctrl+C 可退出。")
print("=" * 60)

def on_press(key):
    global last_press_time, chatter_count, total_backspace_count

    if key == keyboard.Key.backspace:
        current_time = time.time() * 1000  # 转为毫秒
        total_backspace_count += 1
        
        timestamp_str = time.strftime("%H:%M:%S")

        if last_press_time is not None:
            interval = current_time - last_press_time
            
            # 如果触发间隔小于设定阈值，认定为硬件连击 (Chatter)
            if interval < CHATTER_THRESHOLD_MS:
                chatter_count += 1
                # ANSI 转义序列：红色高亮输出
                print(f"\032[31m[{timestamp_str}] ⚠️ 检测到连击! 间隔: {interval:.2f} ms (累计连击: {chatter_count} 次)\033[0m")
            else:
                print(f"[{timestamp_str}] 正常退格 | 间隔: {interval:.1f} ms")
        else:
            print(f"[{timestamp_str}] 正常退格 | 首次按压")

        last_press_time = current_time

try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print(f"监控结束。共记录退格 {total_backspace_count} 次，捕获异常连击 {chatter_count} 次。")
    print("=" * 60)