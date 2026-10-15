import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from PIL import Image, ImageTk
from models import ItemGame

class AplikasiInventarisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ Epic Game Inventory System ⚔️")
        self.root.geometry("950x620")
        self.root.minsize(850, 550)
        
        # Color Palette: Modern Dark RPG Theme (Smooth & Sleek)
        self.bg_main = "#0f1016"       # Latar belakang utama sangat gelap
        self.bg_card = "#181a24"       # Kartu / Panel section
        self.bg_hover = "#252838"      # Efek hover / seleksi
        self.accent_gold = "#f39c12"   # Aksen Emas RPG
        self.accent_cyan = "#00d2d3"   # Aksen Neon
        self.text_main = "#ffffff"     # Teks putih terang
        self.text_muted = "#8c92a4"    # Teks pudar
        
        self.root.configure(bg=self.bg_main)
        
        # Styling ttk Custom untuk tampilan tabel yang lebih bersih dan smooth
        style = ttk.Style()
        style.theme_use("clam")
        
        # Konfigurasi Treeview (Tabel Item)
        style.configure("Treeview", 
                        background=self.bg_card, 
                        foreground=self.text_main, 
                        fieldbackground=self.bg_card,
                        borderwidth=0,
                        font=("Segoe UI", 10),
                        rowheight=32)
        style.configure("Treeview.Heading", 
                        background="#222534", 
                        foreground=self.accent_gold, 
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Treeview", 
                  background=[('selected', '#2d334a')], 
                  foreground=[('selected', '#ffffff')])

        self.buat_widget()
        self.muat_data_tabel()

    def buat_widget(self):
        # --- HEADER UTAMA ---
        header_frame = tk.Frame(self.root, bg=self.bg_main)
        header_frame.pack(fill=tk.X, padx=25, pady=20)
        
        lbl_judul = tk.Label(header_frame, text="⚡ LEGENDARY INVENTORY VAULT ⚡", 
                             font=("Segoe UI", 18, "bold"), bg=self.bg_main, fg=self.accent_gold)
        lbl_judul.pack(side=tk.LEFT)

        lbl_sub = tk.Label(header_frame, text="Manage Your Gear & Stats", 
                           font=("Segoe UI", 10, "italic"), bg=self.bg_main, fg=self.text_muted)
        lbl_sub.pack(side=tk.RIGHT, anchor="s")

        # --- CONTAINER UTAMA (DUA KOLOM) ---
        main_content = tk.Frame(self.root, bg=self.bg_main)
        main_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))

        # ----------------------------------------------------
        # KOLOM KIRI: TABEL & TOMBOL AKSI
        # ----------------------------------------------------
        left_container = tk.Frame(main_container_wrapper := main_content, bg=self.bg_main) # Trick pembungkus
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Hapus variabel sementara di atas, langsung gunakan main_content
        
        left_frame = tk.Frame(main_content, bg=self.bg_card, highlightbackground="#2a2e43", highlightthickness=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # Label Header Tabel
        lbl_tabel_title = tk.Label(left_frame, text="📦 DAFTAR ITEM TERSEDIA", font=("Segoe UI", 11, "bold"),
                                   bg=self.bg_card, fg=self.accent_cyan, anchor="w")
        lbl_tabel_title.pack(fill=tk.X, padx=15, pady=(15, 10))

        # Tabel Treeview
        columns = ("Nama Item", "Tipe", "HP", "Damage")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=tk.W)
        self.tree.column("HP", width=70, anchor=tk.CENTER)
        self.tree.column("Damage", width=70, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Panel Tombol Aksi Bawah Kiri
        btn_frame = tk.Frame(left_frame, bg=self.bg_card)
        btn_frame.pack(fill=tk.X, padx=15, pady=15)

        self.buahkan_tombol(btn_frame, "➕ Tambah Item", "#2ed573", "#26af5d", self.buka_jendela_tambah, side=tk.LEFT, padx_right=10)
        self.buahkan_tombol(btn_frame, "🔄 Refresh", "#1e90ff", "#1873cc", self.muat_data_tabel, side=tk.LEFT, padx_right=0)
        self.buahkan_tombol(btn_frame, "❌ Keluar / Exit", "#ff4757", "#d63031", self.root.quit, side=tk.RIGHT, padx_right=0)

        # ----------------------------------------------------
        # KOLOM KANAN: PANEL DETAIL & STATS VISUAL BAR
        # ----------------------------------------------------
        right_frame = tk.Frame(main_content, bg=self.bg_card, width=320, highlightbackground="#2a2e43", highlightthickness=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        right_frame.pack_propagate(False) # Kunci lebar agar tetap rapi

        lbl_detail_title = tk.Label(right_frame, text="🔍 INSPEKSI ITEM", font=("Segoe UI", 11, "bold"), 
                                    bg=self.bg_card, fg=self.accent_gold)
        lbl_detail_title.pack(pady=(15, 10))

        # Kotak Gambar Item yang Stylist
        self.lbl_gambar = tk.Label(right_frame, text="[ Pilih Item ]", bg="#12131b", fg=self.text_muted,
                                   font=("Segoe UI", 9), width=20, height=9, relief=tk.FLAT)
        self.lbl_gambar.pack(pady=5)

        # Informasi Teks Detail
        self.lbl_nama_detail = tk.Label(right_frame, text="Nama: -", font=("Segoe UI", 12, "bold"), bg=self.bg_card, fg=self.text_main)
        self.lbl_nama_detail.pack(anchor="w", padx=20, pady=(10, 2))

        self.lbl_tipe_detail = tk.Label(right_frame, text="Tipe: -", font=("Segoe UI", 9), bg=self.bg_card, fg=self.text_muted)
        self.lbl_tipe_detail.pack(anchor="w", padx=20, pady=(0, 15))

        # --- STATS BAR VISUAL (HP & DAMAGE) ---
        stats_box = tk.Frame(right_frame, bg=self.bg_card)
        stats_box.pack(fill=tk.X, padx=20, pady=5)

        # HP Bar Widget
        tk.Label(stats_box, text="❤️ HP Stats", font=("Segoe UI", 9, "bold"), bg=self.bg_card, fg="#ff6b81").pack(anchor="w")
        self.canvas_hp = tk.Canvas(stats_box, bg="#12131b", height=12, highlightthickness=0)
        self.canvas_hp.pack(fill=tk.X, pady=(2, 8))
        self.hp_bar_fill = self.canvas_hp.create_rectangle(0, 0, 0, 12, fill="#ff4757", width=0)

        # Damage Bar Widget
        tk.Label(stats_box, text="⚔️ Damage Power", font=("Segoe UI", 9, "bold"), bg=self.bg_card, fg="#ffa502").pack(anchor="w")
        self.canvas_dmg = tk.Canvas(stats_box, bg="#12131b", height=12, highlightthickness=0)
        self.canvas_dmg.pack(fill=tk.X, pady=(2, 5))
        self.dmg_bar_fill = self.canvas_dmg.create_rectangle(0, 0, 0, 12, fill="#ffa502", width=0)

        self.lbl_stat_angka = tk.Label(right_frame, text="HP: 0 | DMG: 0", font=("Segoe UI", 9), bg=self.bg_card, fg=self.text_muted)
        self.lbl_stat_angka.pack(anchor="w", padx=20, pady=(5, 0))

    def buahkan_tombol(self, parent, text, bg_color, hover_color, command, side, padx_right):
        """Fungsi helper untuk membuat tombol kustom yang mulus dan interaktif"""
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                        font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0,
                        activebackground=hover_color, activeforeground="white",
                        padx=12, pady=6, cursor="hand2", command=command)
        btn.pack(side=side, padx=(0, padx_right))
        
        # Efek hover lembut
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    def muat_data_tabel(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.daftar_item_obj = []
        if not os.path.exists("item.csv"):
            return

        with open("item.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Lewati header
            for row in reader:
                if row:
                    nama = row[0]
                    tipe = row[1]
                    hp = row[2]
                    dmg = row[3]
                    gambar = row[4] if len(row) > 4 else ""
                    
                    item = ItemGame(nama, tipe, hp, dmg, gambar)
                    self.daftar_item_obj.append(item)
                    self.tree.insert("", tk.END, values=(item.nama_item, item.tipe, item.hp, item.damage))

    def on_item_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        index = self.tree.index(selected_item[0])
        item = self.daftar_item_obj[index]

        # Update teks detail
        self.lbl_nama_detail.config(text=f"Nama: {item.nama_item}")
        self.lbl_tipe_detail.config(text=f"Tipe: {item.tipe.upper()}")
        self.lbl_stat_angka.config(text=f"HP Value: {item.hp}  |  DMG Value: {item.damage}")

        # Update Animasi Bar Statistik (Dihitung proporsional max 500 sebagai acuan visual penuh)
        max_stat = 500
        
        # Update HP Bar
        hp_width = min(max(int((item.hp / max_stat) * 260), 2), 260)
        self.canvas_hp.coords(self.hp_bar_fill, 0, 0, hp_width, 12)

        # Update Damage Bar
        dmg_width = min(max(int((item.damage / max_stat) * 260), 2), 260)
        self.canvas_dmg.coords(self.dmg_bar_fill, 0, 0, dmg_width, 12)

        # Update Gambar Item
        if item.gambar and os.path.exists(item.gambar):
            try:
                img = Image.open(item.gambar)
                img = img.resize((150, 130), Image.Resampling.LANCZOS)
                self.img_tk = ImageTk.PhotoImage(img)
                self.lbl_gambar.config(image=self.img_tk, text="")
            except Exception:
                self.lbl_gambar.config(image="", text="[ Gagal Memuat Gambar ]")
        else:
            self.img_tk = None
            self.lbl_gambar.config(image="", text="[ Tanpa Gambar / WIP ]")

    def buka_jendela_tambah(self):
        # Jendela Popup Tambah Item Modern
        tambah_win = tk.Toplevel(self.root)
        tambah_win.title("Tambah Item Baru")
        tambah_win.geometry("400x480")
        tambah_win.configure(bg=self.bg_main)
        tambah_win.grab_set()

        tk.Label(tambah_win, text="✨ BUAT ITEM GAME BARU ✨", font=("Segoe UI", 12, "bold"), 
                 bg=self.bg_main, fg=self.accent_cyan).pack(pady=15)

        form_frame = tk.Frame(tambah_win, bg=self.bg_main)
        form_frame.pack(fill=tk.BOTH, padx=30, pady=5)

        def buat_input(label_text):
            tk.Label(form_frame, text=label_text, bg=self.bg_main, fg=self.text_main, 
                     font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(fill=tk.X, pady=(5, 2))
            entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text_main, 
                             insertbackground="white", relief=tk.FLAT)
            entry.pack(fill=tk.X, ipady=5, pady=(0, 8))
            return entry

        entry_nama = buat_input("Nama Item:")
        entry_tipe = buat_input("Tipe (Weapon / Armor / Consumable):")
        entry_hp = buat_input("Stats HP (Angka):")
        entry_dmg = buat_input("Damage (Angka):")

        path_gambar_var = tk.StringVar()

        def pilih_gambar():
            file_path = filedialog.askopenfilename(title="Pilih Gambar Item", 
                                                   filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            if file_path:
                path_gambar_var.set(file_path)
                lbl_path_info.config(text=f"📁 {os.path.basename(file_path)}", fg="#2ed573")

        btn_img = tk.Button(form_frame, text="Pilih Berkas Gambar (Opsional)", command=pilih_gambar, 
                            bg="#252838", fg=self.text_main, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2", pady=5)
        btn_img.pack(fill=tk.X, pady=5)

        lbl_path_info = tk.Label(form_frame, text="Belum ada gambar dipilih", bg=self.bg_main, fg=self.text_muted, font=("Segoe UI", 8))
        lbl_path_info.pack(anchor=tk.W, pady=(0, 10))

        def simpan():
            nama = entry_nama.get().strip()
            tipe = entry_tipe.get().strip()
            hp = entry_hp.get().strip()
            dmg = entry_dmg.get().strip()
            gambar = path_gambar_var.get().strip()

            if not nama or not tipe or not hp or not dmg:
                messagebox.showerror("Peringatan", "Semua kolom teks wajib diisi!", parent=tambah_win)
                return

            try:
                hp_val = int(hp)
                dmg_val = int(dmg)
            except ValueError:
                messagebox.showerror("Peringatan", "HP dan Damage harus berupa angka!", parent=tambah_win)
                return

            item_baru = ItemGame(nama, tipe, hp_val, dmg_val, gambar)
            file_exists = os.path.exists("item.csv")
            
            with open("item.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["NamaItem", "Tipe", "HP", "Damage", "Gambar"])
                writer.writerow(item_baru.to_list())

            messagebox.showinfo("Sukses", "Item berhasil ditambahkan ke vault!", parent=tambah_win)
            tambah_win.destroy()
            self.muat_data_tabel()

        btn_simpan = tk.Button(tambah_win, text="Simpan Item", bg="#2ed573", fg="white", 
                               font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", command=simpan, pady=8)
        btn_simpan.pack(fill=tk.X, padx=30, pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiInventarisGame(root)
    root.mainloop()