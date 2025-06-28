import os
import time
import psutil
import tkinter as tk
from tkinter import messagebox

def turn_off_monitor():
    os.system(
        'powershell -Command "(Add-Type \'[DllImport(\\"user32.dll\\")]public static extern int SendMessage(int hWnd,int hMsg,int wParam,int lParam);\' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)"'
    )

def shutdown_pc():
    os.system("shutdown /s /t 0")

def get_net_bytes_recv():
    net_io = psutil.net_io_counters()
    return net_io.bytes_recv

def show_popup():
    root = tk.Tk()
    root.title("Загрузка завершена")
    root.geometry("300x100")
    root.eval('tk::PlaceWindow . center')

    label = tk.Label(root, text="Загрузка завершена!", font=("Arial", 14))
    label.pack(pady=20)

    root.mainloop()

def main():
    try:
        size_gb = float(input("Введите размер игры в ГБ: "))
        if size_gb <= 0:
            print("Размер должен быть положительным числом!")
            return
    except ValueError:
        print("Пожалуйста, введите число.")
        return

    answer_mon = input("Выключить монитор сразу? (да/нет): ").strip().lower()
    answer_shutdown = input("Выключить ПК после загрузки? (да/нет): ").strip().lower()

    if answer_mon in ['да', 'д']:
        turn_off_monitor()
        print("Монитор выключен.")

    speed_mbps = 80  # можно изменить
    speed_MBps = speed_mbps / 8
    size_mb = size_gb * 1024
    est_time = int(size_mb / speed_MBps)

    print(f"Ожидаемая длительность загрузки: {est_time // 60} мин {est_time % 60} сек.")
    print("Ждем завершения скачивания...")

    zero_speed_count = 0
    prev_bytes = get_net_bytes_recv()
    idle_threshold = 10  # секунд с почти нулевым трафиком

    while True:
        time.sleep(1)
        current_bytes = get_net_bytes_recv()
        speed = (current_bytes - prev_bytes) / (1024 * 1024)  # MB/s
        prev_bytes = current_bytes

        if speed < 2:  # МБ/с — нижче цієї швидкості вважаємо, що гра не качається
            zero_speed_count += 1
        else:
            zero_speed_count = 0

        if zero_speed_count >= idle_threshold:
            print("Загрузка завершена.")
            if answer_shutdown in ['да', 'д']:
                shutdown_pc()
            else:
                show_popup()
            break

if __name__ == "__main__":
    main()
