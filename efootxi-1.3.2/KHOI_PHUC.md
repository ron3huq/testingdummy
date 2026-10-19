# Khôi phục sau màn hình đen

Người dùng đã xác nhận khôi phục dt200 gốc giúp game mở lại bình thường.

Ưu tiên lấy `assets/dt200_mobile_all.cpk` từ bản sao APK trước khi thử. Không xóa dữ liệu hoặc gỡ ứng dụng.

Nếu cần dùng file trong `restore/`, SHA-256 của dt200 gốc phát hành 1.3.2 là:

```
088bb2e661cfcd8a1110c40402a461dac0c37eecdbce72ce692d505a77050954
```

Trong bản sao APK hiện tại, thay đúng `assets/dt200_mobile_all.cpk` bằng file gốc. Cập nhật với chữ ký tương thích bản đã cài, rồi đóng hẳn game và mở lại. Nếu báo chữ ký không khớp, dừng và giữ nguyên app/save.

Không áp dụng lại bản thử có SHA-256 `dd22d6cc3a0870efb12350023de8793ef786c72c19467ec500eb9aac533d2a8e`. Không sửa thêm DEX, libUE4 hoặc save để chữa lỗi này.
