import os
from linked_list import DoAn

class FileHandler:
    FILE_PATH = "data/doan.txt"

    @staticmethod
    def save(linked_list):
        os.makedirs("data", exist_ok=True)
        with open(FileHandler.FILE_PATH, "w", encoding="utf-8") as f:
            current = linked_list.head
            while current:
                line = (f"{current.ma}|{current.ten}|{current.mssv}|{current.hoten}|"
                        f"{current.gvhd}|{current.lop}|{current.namhoc}|"
                        f"{current.trangthai}|{current.diem}\n")
                f.write(line)
                current = current.next

    @staticmethod
    def load(linked_list):
        if not os.path.exists(FileHandler.FILE_PATH):
            print(f"Không tìm thấy file {FileHandler.FILE_PATH}. Bắt đầu với danh sách trống.")
            return

        try:
            with open(FileHandler.FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            count = 0
            skipped = 0

            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 5:
                    skipped += 1
                    continue

                ma = parts[0]
                ten = parts[1]
                mssv = parts[2]
                hoten = parts[3]
                gvhd = parts[4]
                lop = parts[5] if len(parts) > 5 else ""
                namhoc = parts[6] if len(parts) > 6 else "2025-2026"
                trangthai = parts[7] if len(parts) > 7 else "Đang thực hiện"
                
                diem = 0.0
                if len(parts) > 8:
                    try:
                        diem = float(parts[8])
                    except ValueError:
                        diem = 0.0

                doan = DoAn(ma, ten, mssv, hoten, gvhd, lop, namhoc, trangthai, diem)

                if linked_list.them(doan):
                    count += 1
                else:
                    skipped += 1

            print(f"Hoàn tất load → Thành công: {count} | Bỏ qua: {skipped} | Tổng: {len(linked_list.to_list())} đề tài")

        except Exception as e:
            print(f"Lỗi load file: {e}")
