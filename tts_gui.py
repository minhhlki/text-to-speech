#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese Text-to-Speech GUI Application
Công cụ chuyển văn bản thành giọng nói tiếng Việt
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import edge_tts
import asyncio
import pygame
import os
import tempfile
import threading
import time

class VietnameseTTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chuyển Văn Bản Thành Giọng Nói - Vietnamese TTS")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Màu sắc giao diện
        self.bg_color = "#f0f4f8"
        self.primary_color = "#4a90e2"
        self.secondary_color = "#50c878"
        self.text_color = "#2c3e50"

        self.root.configure(bg=self.bg_color)

        # Khởi tạo pygame mixer cho phát âm thanh
        pygame.mixer.init()

        # Danh sách giọng đọc tiếng Việt
        self.voices = {
            "Nữ Miền Bắc (HoaiMy)": "vi-VN-HoaiMyNeural",
            "Nam Miền Bắc (NamMinh)": "vi-VN-NamMinhNeural"
        }

        self.temp_files = []  # Danh sách các file tạm để cleanup sau
        self.is_playing = False

        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện người dùng"""

        # Tiêu đề
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(
            title_frame,
            text="🎙️ Chuyển Văn Bản Thành Giọng Nói",
            font=("Segoe UI", 20, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)

        # Frame chính
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Khung nhập văn bản
        text_label = tk.Label(
            main_frame,
            text="📝 Nhập văn bản cần đọc:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        text_label.pack(anchor=tk.W, pady=(0, 5))

        # Text box với scrollbar
        self.text_input = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.primary_color
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.text_input.insert("1.0", "Xin chào! Đây là công cụ chuyển văn bản thành giọng nói tiếng Việt.")

        # Khung chọn giọng đọc
        voice_frame = tk.Frame(main_frame, bg=self.bg_color)
        voice_frame.pack(fill=tk.X, pady=(0, 15))

        voice_label = tk.Label(
            voice_frame,
            text="🎤 Chọn giọng đọc:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        voice_label.pack(side=tk.LEFT, padx=(0, 10))

        style = ttk.Style()
        style.configure("TCombobox", font=("Segoe UI", 10))

        self.voice_var = tk.StringVar(value=list(self.voices.keys())[0])
        self.voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=list(self.voices.keys()),
            state="readonly",
            font=("Segoe UI", 10),
            width=30
        )
        self.voice_combo.pack(side=tk.LEFT)

        # Khung nút điều khiển
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=(0, 15))

        # Nút phát âm thanh
        self.play_button = tk.Button(
            button_frame,
            text="▶️  Phát Âm Thanh",
            font=("Segoe UI", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.play_audio
        )
        self.play_button.pack(side=tk.LEFT, padx=5)

        # Nút dừng
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️  Dừng",
            font=("Segoe UI", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.stop_audio,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Nút lưu file
        self.save_button = tk.Button(
            button_frame,
            text="💾  Lưu File MP3",
            font=("Segoe UI", 11, "bold"),
            bg=self.secondary_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.save_audio
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Thanh trạng thái
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#7f8c8d",
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, pady=(10, 0))

    def get_text(self):
        """Lấy văn bản từ text box"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần đọc!")
            return None
        return text

    def get_selected_voice(self):
        """Lấy giọng đọc được chọn"""
        return self.voices[self.voice_var.get()]

    async def generate_speech_async(self, text, voice, output_file):
        """Tạo file âm thanh từ văn bản (async)"""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    def generate_speech(self, text, voice, output_file):
        """Tạo file âm thanh từ văn bản"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.generate_speech_async(text, voice, output_file))
            loop.close()
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo âm thanh: {str(e)}")
            return False

    def play_audio(self):
        """Phát âm thanh"""
        text = self.get_text()
        if not text:
            return

        # Vô hiệu hóa nút trong khi xử lý
        self.play_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.status_var.set("Đang tạo âm thanh...")

        def play_thread():
            try:
                # Dừng âm thanh đang phát (nếu có) để giải phóng file
                pygame.mixer.music.stop()

                # Tạo file tạm mới
                temp_file = tempfile.mktemp(suffix=".mp3")
                self.temp_files.append(temp_file)

                voice = self.get_selected_voice()

                if self.generate_speech(text, voice, temp_file):
                    self.status_var.set("Đang phát âm thanh...")

                    # Phát âm thanh
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()

                    self.is_playing = True
                    self.stop_button.config(state=tk.NORMAL)

                    # Đợi phát xong
                    while pygame.mixer.music.get_busy() and self.is_playing:
                        pygame.time.Clock().tick(10)

                    self.status_var.set("Hoàn thành!")
                else:
                    self.status_var.set("Lỗi khi tạo âm thanh")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể phát âm thanh: {str(e)}")
                self.status_var.set("Lỗi")
            finally:
                self.is_playing = False
                self.play_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

        # Chạy trong thread riêng để không block UI
        thread = threading.Thread(target=play_thread, daemon=True)
        thread.start()

    def stop_audio(self):
        """Dừng phát âm thanh"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.status_var.set("Đã dừng")
            self.stop_button.config(state=tk.DISABLED)

    def save_audio(self):
        """Lưu file âm thanh"""
        text = self.get_text()
        if not text:
            return

        # Chọn vị trí lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")],
            title="Lưu file âm thanh"
        )

        if not file_path:
            return

        # Vô hiệu hóa nút trong khi xử lý
        self.play_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.status_var.set("Đang tạo và lưu file...")

        def save_thread():
            try:
                voice = self.get_selected_voice()

                if self.generate_speech(text, voice, file_path):
                    self.status_var.set(f"Đã lưu: {os.path.basename(file_path)}")
                    messagebox.showinfo("Thành công", f"Đã lưu file:\n{file_path}")
                else:
                    self.status_var.set("Lỗi khi lưu file")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
                self.status_var.set("Lỗi")
            finally:
                self.play_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.NORMAL)

        # Chạy trong thread riêng
        thread = threading.Thread(target=save_thread, daemon=True)
        thread.start()

    def on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        if self.is_playing:
            pygame.mixer.music.stop()

        # Dừng mixer và giải phóng tất cả file
        try:
            pygame.mixer.music.unload()
        except:
            # Nếu không có method unload, dùng stop
            pygame.mixer.music.stop()

        # Đợi một chút để đảm bảo file được giải phóng
        time.sleep(0.2)

        # Xóa tất cả file tạm
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

        self.root.destroy()


def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = VietnameseTTSApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Căn giữa cửa sổ
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
