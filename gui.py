import customtkinter as ctk
from tkinter import ttk
from PIL import Image

class AppGUI(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("QUẢN LÝ ĐỒ ÁN MÔN HỌC - Đại học Đồng Tháp")
        self.geometry("1800x900")

        self.create_header()
        self.create_dashboard()

    def create_header(self):
        header = ctk.CTkFrame(self, height=125, fg_color="#1e40af")
        header.pack(fill="x", padx=15, pady=(15, 8))
        header.pack_propagate(False)

        frame = ctk.CTkFrame(header, fg_color="#1e40af")
        frame.pack(expand=True)

        try:
            logo_img = ctk.CTkImage(light_image=Image.open("logo_dhdt.png"), size=(90, 90))
            logo = ctk.CTkLabel(frame, image=logo_img, text="")
            logo.image = logo_img
            logo.pack(side="left", padx=(0, 30))
        except:
            ctk.CTkLabel(frame, text="🏛️", font=ctk.CTkFont(size=65)).pack(side="left", padx=(0, 30))

        title_frame = ctk.CTkFrame(frame, fg_color="#1e40af")
        title_frame.pack(side="left")

        ctk.CTkLabel(title_frame, text="QUẢN LÝ ĐỒ ÁN MÔN HỌC",
                     font=ctk.CTkFont(size=34, weight="bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Đại học Đồng Tháp",
                     font=ctk.CTkFont(size=18), text_color="#bae6fd").pack(anchor="w")

    def create_toolbar(self):
        toolbar = ctk.CTkFrame(self, height=55)
        toolbar.pack(fill="x", padx=15, pady=10)

        btn_style = {"width": 145, "height": 36, "font": ctk.CTkFont(size=14, weight="bold"), "corner_radius": 10}

        ctk.CTkButton(toolbar, text="➕ Thêm mới", fg_color="#1e40af", **btn_style, command=self.controller.them_moi).pack(side="left", padx=6)
        ctk.CTkButton(toolbar, text="🛠 Sửa", fg_color="#1e40af", **btn_style, command=self.controller.sua).pack(side="left", padx=6)
        ctk.CTkButton(toolbar, text="❌ Xóa", fg_color="#1e40af", **btn_style, command=self.controller.xoa).pack(side="left", padx=6)
        
        ctk.CTkButton(toolbar, text="Xuất Excel", fg_color="#1e40af", **btn_style, command=self.controller.xuat_excel).pack(side="left", padx=6)
        ctk.CTkButton(toolbar, text="Nhập Excel", fg_color="#1e40af", **btn_style, command=self.controller.nhap_excel).pack(side="left", padx=6)

        ctk.CTkButton(toolbar, text="Dashboard", fg_color="#1e40af", **btn_style, command=self.show_dashboard).pack(side="left", padx=6)
        
        self.sort_combo = ctk.CTkComboBox(toolbar, 
            values=["Mã đề tài", "MSSV", "Tên đề tài", "Họ tên SV", "Lớp", "GVHD", 
                    "Điểm cao → thấp", "Điểm thấp → cao", "Trạng thái"],
            command=self.controller.sap_xep, width=160, height=36)
        self.sort_combo.set("Sắp xếp theo...")
        self.sort_combo.pack(side="left", padx=20)

        self.search_entry = ctk.CTkEntry(toolbar, 
                                         placeholder_text="🔍 Tìm kiếm theo mã, tên đề tài, sinh viên, lớp...", 
                                         width=460, height=36, font=ctk.CTkFont(size=14))
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", self.controller.tim_kiem)

    def create_table(self):
        columns = ("stt", "ma", "ten", "mssv", "hoten", "lop", "gvhd", "namhoc", "trangthai", "diem")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=28)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview", 
                        background="#f8fafc",
                        foreground="#1e2937",
                        rowheight=48,
                        font=("Segoe UI", 12, "bold"))

        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 13, "bold"),
                        background="#1e40af",
                        foreground="white",
                        padding=10)

        style.map("Treeview", background=[("selected", "#bae6fd")])

        headers = ["STT", "Mã Đề Tài", "Tên Đề Tài", "MSSV", "Sinh Viên", "Lớp", "GVHD", "Năm Học", "Trạng Thái", "Điểm"]
        widths = [60, 130, 450, 130, 250, 100, 220, 120, 190, 90]

        for col, text, w in zip(columns, headers, widths):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["stt", "diem"] else "w")

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree.pack(fill="both", expand=True)
     
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")

        self.tree.configure(xscrollcommand=h_scrollbar.set)

        self.tree.bind("<Double-1>", lambda e: self.controller.sua())
    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        items = data or self.controller.get_all()

        for i, da in enumerate(items):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                i + 1,
                da.ma,
                da.ten,
                da.mssv,
                da.hoten,
                da.lop,         
                da.gvhd,
                da.namhoc,
                da.trangthai,
                f"{da.diem:.1f}"
            ), tags=(tag,))

        self.tree.tag_configure("even", background="#f8fafc")
        self.tree.tag_configure("odd",  background="#e0f2fe")
    def create_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_header()

        dash_frame = ctk.CTkFrame(self, fg_color="#f8fafc")
        dash_frame.pack(fill="both", expand=True, padx=30, pady=20)

        dash_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        dash_frame.grid_rowconfigure((0, 1), weight=1)

        lst = self.controller.get_all()
        total = len(lst)
        dang_thuc_hien = sum(1 for x in lst if x.trangthai == "Đang thực hiện")
        da_bao_cao = sum(1 for x in lst if x.trangthai == "Đã báo cáo")
        da_hoan_thanh = sum(1 for x in lst if x.trangthai == "Đã hoàn thành")

        diem_list = [x.diem for x in lst if x.trangthai == "Đã báo cáo" and x.diem > 0]
        diem_tb = round(sum(diem_list) / len(diem_list), 2) if diem_list else 0.0
        ty_le = round((da_bao_cao / total * 100), 1) if total > 0 else 0

        self.create_stat_card(dash_frame, "TỔNG SỐ ĐỀ TÀI", str(total), "#1e40af", 0, 0)
        self.create_stat_card(dash_frame, "ĐANG THỰC HIỆN", str(dang_thuc_hien), "#d97706", 1, 0)
        self.create_stat_card(dash_frame, "ĐÃ HOÀN THÀNH", str(da_hoan_thanh), "#15803d", 2, 0)

        self.create_stat_card(dash_frame, "ĐÃ BÁO CÁO", str(da_bao_cao), "#0f766e", 0, 1)
        self.create_gauge_card(dash_frame, "TỶ LỆ BÁO CÁO", f"{ty_le}%", "Đã báo cáo / Tổng đề tài", "#14b8a6", 1, 1)
        self.create_gauge_card(dash_frame, "ĐIỂM TRUNG BÌNH", f"{diem_tb}", "Trung bình các đề tài đã báo cáo", "#1e40af", 2, 1)

        btn_frame = ctk.CTkFrame(dash_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=2, padx=25, pady=40, sticky="se")

        ctk.CTkButton(btn_frame, text="📋 XEM TOÀN BỘ DANH SÁCH ĐỀ TÀI", 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     height=55, width=340, fg_color="#1e40af", hover_color="#1e3a8a",
                     corner_radius=12,
                     command=self.show_table_view).pack()

    def create_stat_card(self, parent, title, value, color, col, row):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=16, 
                           border_width=3, border_color=color, height=180)
        card.grid(row=row, column=col, padx=16, pady=16, sticky="nsew")
        card.grid_propagate(False) 


        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(28, 6))
        

        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=58, weight="bold"), 
                    text_color=color).pack(pady=4)
        

        ctk.CTkLabel(card, text="Tổng số đề tài hiện có", 
                    font=ctk.CTkFont(size=12), text_color="#64748b").pack()

    def create_gauge_card(self, parent, title, value, subtitle, color, col, row):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=16, 
                           border_width=3, border_color=color, height=180)
        card.grid(row=row, column=col, padx=16, pady=16, sticky="nsew")
        card.grid_propagate(False)

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(28, 8))
        
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=58, weight="bold"), 
                    text_color=color).pack(pady=6)
        
        ctk.CTkLabel(card, text=subtitle, font=ctk.CTkFont(size=13), 
                    text_color="#64748b").pack(pady=4)

    def show_table_view(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_header()
        self.create_toolbar()
        self.create_table()
        self.refresh_table()
    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_header()
        self.create_dashboard()
