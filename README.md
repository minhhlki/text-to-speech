# 🎙️ Công Cụ Chuyển Văn Bản Thành Giọng Nói Tiếng Việt

Tool chuyển văn bản thành giọng nói (Text-to-Speech) hỗ trợ tiếng Việt với giao diện đơn giản, dễ sử dụng.

## ✨ Tính Năng

- ✅ Hỗ trợ tiếng Việt với giọng đọc tự nhiên
- 🎤 Nhiều lựa chọn giọng đọc (Nam/Nữ, Miền Bắc/Miền Nam)
- 🔊 Phát âm thanh trực tiếp
- 💾 Lưu file MP3
- 🖥️ Giao diện đẹp mắt, dễ sử dụng
- ⚡ Chạy hoàn toàn offline sau khi tải giọng đọc

## 📋 Yêu Cầu Hệ Thống

- Windows 7 trở lên
- Python 3.7 trở lên
- Kết nối Internet (chỉ khi sử dụng lần đầu để tải giọng đọc)

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Cài đặt Python

1. Tải Python từ: https://www.python.org/downloads/
2. Chạy file cài đặt
3. **QUAN TRỌNG**: Tick vào ô "Add Python to PATH" trước khi cài đặt
4. Click "Install Now"

### Bước 2: Cài đặt thư viện

Double-click vào file `install.bat` và đợi quá trình cài đặt hoàn tất.

## 🎯 Cách Sử Dụng

### Khởi chạy chương trình

Double-click vào file `run.bat` để mở ứng dụng.

### Sử dụng giao diện

1. **Nhập văn bản**: Gõ hoặc dán văn bản cần đọc vào ô text
2. **Chọn giọng đọc**: Chọn giọng Nam/Nữ, Miền Bắc/Miền Nam từ dropdown
3. **Phát âm thanh**: Click nút "▶️ Phát Âm Thanh" để nghe
4. **Dừng**: Click nút "⏹️ Dừng" để dừng phát
5. **Lưu file**: Click nút "💾 Lưu File MP3" để lưu thành file

## 🎤 Các Giọng Đọc Có Sẵn

- **Nữ Miền Bắc (HoaiMy)**: Giọng nữ tự nhiên, giọng Miền Bắc
- **Nam Miền Bắc (NamMinh)**: Giọng nam trầm ấm, giọng Miền Bắc

## 📁 Cấu Trúc Thư Mục

```
text-to-speech/
├── tts_gui.py          # File chương trình chính
├── requirements.txt    # Danh sách thư viện cần thiết
├── install.bat         # Script cài đặt
├── run.bat            # Script khởi chạy (double-click để mở)
└── README.md          # Hướng dẫn sử dụng
```

## ❓ Xử Lý Lỗi

### Lỗi: "Python chưa được cài đặt"

- Cài đặt Python từ https://www.python.org/downloads/
- Nhớ tick "Add Python to PATH" khi cài đặt

### Lỗi: "No module named 'edge_tts'" hoặc "No module named 'pygame'"

- Chạy lại file `install.bat`
- Hoặc mở Command Prompt và chạy: `pip install -r requirements.txt`

### Lỗi: "Không thể phát âm thanh"

- Kiểm tra kết nối Internet (lần đầu sử dụng)
- Kiểm tra loa/tai nghe đã bật chưa
- Thử chọn giọng đọc khác

### Lỗi: "Permission denied" khi lưu file

- Chọn vị trí lưu file khác (không phải thư mục System)
- Chạy chương trình với quyền Administrator

## 🔧 Chạy Từ Command Line (Nâng Cao)

```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Chạy chương trình
python tts_gui.py
```

## 📝 Ghi Chú

- Tool sử dụng Microsoft Edge TTS API (miễn phí)
- Chất lượng giọng đọc phụ thuộc vào Microsoft Edge TTS
- Lần đầu sử dụng cần Internet để tải giọng đọc
- Sau khi tải xong, có thể sử dụng offline

## 🤝 Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra lại hướng dẫn cài đặt
2. Đảm bảo đã cài đặt Python đúng cách
3. Chạy lại file `install.bat`

## 📜 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

---

**Chúc bạn sử dụng vui vẻ! 🎉**
