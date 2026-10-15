import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from PIL import Image, ImageTk
from models import ItemGame

class AplikasiInventarisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Inventaris Item Game")
        self.root.geometry("850x550")
        self.root.minsize(750, 500)
        
        # Styling warna ala Game / RPG
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.accent_color = "#4e73df"
        self.btn_exit_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Konfigurasi style ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#2d2d44", 
                        foreground="white", 
                        fieldbackground="#2d2d44",
                        rowheight=25)
        style.configure("Treeview.Heading", 
                        background="#3f3f5f", 
                        foreground="white", 
                        font=("Arial", 10, "bold"))
        style.map("Treeview", background=[('selected', self.accent_color)])

        self.buat_widget()
        self.muat_data_tabel()

    def buat_widget(self):
        # Header Judul
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        lbl_judul = tk.Label(header_frame, text="⚔️ SISTEM INVENTARIS ITEM GAME ⚔️", 
                             font=("Arial", 16, "bold"), bg=self.bg_color, fg="#f1c40f")
        lbl_judul.pack()

        # Frame Utama (Dibagi jadi 2: Kiri (Tabel & Aksi), Kanan (Detail & Gambar))
        main_content = tk.Frame(self.root, bg=self.bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # --- BAGIAN KIRI (Tabel & Tombol Navigasi) ---
        left_frame = tk.Frame(main_content, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tabel Item (Treeview)
        columns = ("Nama Item", "Tipe", "HP", "Damage")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=tk.W)
        self.tree.column("HP", width=70, anchor=tk.CENTER)
        self.tree.column("Damage", width=70, anchor=tk.CENTER)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Panel Tombol Aksi di Kiri
        btn_frame = tk.Frame(left_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=5)

        btn_tambah = tk.Button(btn_frame, text="➕ Tambah Item Baru", bg="#2ecc71", fg="white",
                               font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5,
                               command=self.buka_jendela_tambah)
        btn_tambah.pack(side=tk.LEFT, padx=(0, 5))

        btn_refresh = tk.Button(btn_frame, bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                                relief=tk.FLAT, padx=10, pady=5, text="🔄 Refresh", command=self.muat_data_tabel)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        btn_keluar = tk.Button(btn_frame, text="❌ Keluar / Stop", bg=self.btn_exit_color, fg="white",
                               font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5,
                               command=self.root.quit)
        btn_keluar.pack(side=tk.RIGHT, padx=(5, 0))

        # --- BAGIAN KANAN (Preview Detail & Gambar Item) ---
        right_frame = tk.Frame(main_content, bg="#2d2d44", bd=2, relief=tk.GROOVE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0), ipadx=10, ipady=10)

        lbl_detail_title = tk.Label(right_frame, text="Detail Item", font=("Arial", 12, "bold"), 
                                    bg="#2d2d44", fg="#f1c40f")
        lbl_detail_title.pack(pady=10)

        # Area Gambar Item
        self.lbl_gambar = tk.Label(right_frame, text="[ Tidak Ada Gambar ]", bg="#1e1e2f", fg="#aaaaaa",
                                   width=22, height=10, relief=tk.SUNKEN)
        self.lbl_gambar.pack(pady=5)

        # Label Informasi Teks
        self.lbl_info = tk.Label(right_frame, text="Pilih item di tabel\nuntuk melihat detail.", 
                                 font=("Arial", 10), bg="#2d2d44", fg="white", justify=tk.LEFT)
        self.lbl_info.pack(pady=15, anchor=tk.W)

    def muat_data_tabel(self):
        # Bersihkan isi tabel lama
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.daftar_item_obj = []
        if not os.path.exists("item.csv"):
            return

        with open("item.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Lewati header
            for row in reader:
                if row:
                    # Menangani kompatibilitas jika file lama hanya punya 4 kolom
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

        # Update teks info detail
        info_text = (f"Nama : {item.nama_item}\n"
                     f"Tipe : {item.tipe}\n"
                     f"HP   : {item.hp}\n"
                     f"DMG  : {item.damage}")
        self.lbl_info.config(text=info_text)

        # Update gambar item (jika ada path file valid)
        if item.gambar and os.path.exists(item.gambar):
            try:
                img = Image.open(item.gambar)
                img = img.resize((140, 140), Image.Resampling.LANCZOS)
                self.img_tk = ImageTk.PhotoImage(img)
                self.lbl_gambar.config(image=self.img_tk, text="")
            except Exception:
                self.lbl_gambar.config(image="", text="[ Gagal Muat Gambar ]")
        else:
            self.img_tk = None
            self.lbl_gambar.config(image="", text="[ Tidak Ada Gambar ]")

    def buka_jendela_tambah(self):
        # Jendela Popup (Toplevel) untuk Form Tambah Item (WIP/Bisa isi gambar atau tidak)
        tambah_win = tk.Toplevel(self.root)
        tambah_win.title("Tambah Item Game Baru")
        tambah_win.geometry("380x440")
        tambah_win.configure(bg=self.bg_color)
        tambah_win.grab_set()  # Fokus ke jendela popup

        tk.Label(tambah_win, text="TAMBAH ITEM BARU", font=("Arial", 12, "bold"), 
                 bg=self.bg_color, fg="#2ecc71").pack(pady=10)

        form_frame = tk.Frame(tambah_win, bg=self.bg_color)
        form_frame.pack(fill=tk.BOTH, padx=20, pady=5)

        # Input Nama Item
        tk.Label(form_frame, text="Nama Item:", bg=self.bg_color, fg="white", anchor=tk.W).pack(fill=tk.X)
        entry_nama = tk.Entry(form_frame, font=("Arial", 10))
        entry_nama.pack(fill=tk.X, pady=(0, 8))

        # Input Tipe Item
        tk.Label(form_frame, text="Tipe (Weapon/Armor/Consumable):", bg=self.bg_color, fg="white", anchor=tk.W).pack(fill=tk.X)
        entry_tipe = tk.Entry(form_frame, font=("Arial", 10))
        entry_tipe.pack(fill=tk.X, pady=(0, 8))

        # Input HP
        tk.Label(form_frame, text="Stats HP:", bg=self.bg_color, fg="white", anchor=tk.W).pack(fill=tk.X)
        entry_hp = tk.Entry(form_frame, font=("Arial", 10))
        entry_hp.pack(fill=tk.X, pady=(0, 8))

        # Input Damage
        tk.Label(form_frame, text="Damage:", bg=self.bg_color, fg="white", anchor=tk.W).pack(fill=tk.X)
        entry_dmg = tk.Entry(form_frame, font=("Arial", 10))
        entry_dmg.pack(fill=tk.X, pady=(0, 8))

        # Pilih Gambar (Opsional / WIP)
        path_gambar_var = tk.StringVar()
        
        def pilih_gambar():
            file_path = filedialog.askopenfilename(title="Pilih Gambar Item", 
                                                   filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
            if file_path:
                path_gambar_var.set(file_path)
                lbl_path_info.config(text=os.path.basename(file_path), fg="#2ecc71")

        btn_img = tk.Button(form_frame, text="📁 Pilih Gambar (Opsional)", command=pilih_gambar, 
                            bg="#34495e", fg="white", font=("Arial", 9))
        btn_img.pack(fill=tk.X, pady=2)

        lbl_path_info = tk.Label(form_frame, text="Belum ada gambar dipilih", bg=self.bg_color, fg="#888888", font=("Arial", 8))
        lbl_path_info.pack(anchor=tk.W, pady=(0, 10))

        def simpan():
            nama = entry_nama.get().strip()
            tipe = entry_tipe.get().strip()
            hp = entry_hp.get().strip()
            dmg = entry_dmg.get().strip()
            gambar = path_gambar_var.get().strip()

            if not nama or not tipe or not hp or not dmg:
                messagebox.showerror("Peringatan", "Semua kolom teks (Nama, Tipe, HP, Damage) wajib diisi!", parent=tambah_win)
                return

            try:
                hp_val = int(hp)
                dmg_val = int(dmg)
            except ValueError:
                messagebox.showerror("Peringatan", "HP dan Damage harus berupa angka (integer)!", parent=tambah_win)
                return

            # Simpan ke CSV
            item_baru = ItemGame(nama, tipe, hp_val, dmg_val, gambar)
            file_exists = os.path.exists("item.csv")
            
            with open("item.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["NamaItem", "Tipe", "HP", "Damage", "Gambar"])
                writer.writerow(item_baru.to_list())

            messagebox.showinfo("Sukses", "Item game berhasil ditambahkan!", parent=tambah_win)
            tambah_win.destroy()
            self.muat_data_tabel()

        btn_simpan = tk.Button(tambah_win, text="Simpan Item", bg="#2ecc71", fg="white", 
                               font=("Arial", 10, "bold"), relief=tk.FLAT, command=simpan)
        btn_simpan.pack(fill=tk.X, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiInventarisGame(root)
    root.mainloop()