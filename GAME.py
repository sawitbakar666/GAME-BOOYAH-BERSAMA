import time
import random

# ===== KELAS PEMAIN =====
class Pemain:
    def __init__(self, nama):
        self.nama = nama
        self.hp = 100
        self.max_hp = 100
        self.mana = 50
        self.max_mana = 50
        self.level = 1
        self.exp = 0
        self.exp_max = 100
        self.emas = 100
        self.inventori = {"Pistol": 1, "Peluru": 30, "Obat HP": 3}
        self.artefak = []
        self.lokasi = "Gerbang Kota"
        self.quest_aktif = None
        self.quest_selesai = []
        self.game_selesai = False
        
    def tampilkan_status(self):
        print(f"\n╔════════════════════════════════════════╗")
        print(f"║ NAMA: {self.nama:<34} ║")
        print(f"║ Level: {self.level:<32} ║")
        print(f"║ HP: {self.hp}/{self.max_hp:<33} ║")
        print(f"║ Mana: {self.mana}/{self.max_mana:<31} ║")
        print(f"║ EXP: {self.exp}/{self.exp_max:<33} ║")
        print(f"║ Emas: {self.emas:<34} ║")
        print(f"║ Lokasi: {self.lokasi:<31} ║")
        print(f"╚════════════════════════════════════════╝")
        
    def tampilkan_inventori(self):
        print(f"\n📦 INVENTORI:")
        if self.inventori:
            for item, jumlah in self.inventori.items():
                print(f"  • {item}: {jumlah}")
        else:
            print("  (Inventori kosong)")

# ===== KELAS ZOMBIE =====
class Zombie:
    def __init__(self, nama, hp, atk, exp_drop):
        self.nama = nama
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.exp_drop = exp_drop
        
    def tampilkan_status(self):
        print(f"\n👹 {self.nama}")
        print(f"   HP: {self.hp}/{self.max_hp}")

# ===== KELAS LOKASI =====
class Lokasi:
    def __init__(self, nama, deskripsi, zombie_spawn=None):
        self.nama = nama
        self.deskripsi = deskripsi
        self.zombie_spawn = zombie_spawn if zombie_spawn else []
        
    def tampilkan_info(self):
        print(f"\n🏘️ {self.nama}")
        print(f"   {self.deskripsi}")

# ===== INISIALISASI KOTA =====
lokasi_kota = {
    "Gerbang Kota": Lokasi(
        "Gerbang Kota",
        "Pintu masuk kota SERLOK TAK PARANI. Udara terasa dingin dan mencekam."
    ),
    "Pasar Utama": Lokasi(
        "Pasar Utama",
        "Pasar yang dulu ramai, kini penuh dengan zombie. Suara desisan terdengar di mana-mana.",
        ["Zombie Biasa", "Zombie Biasa"]
    ),
    "Rumah Sakit": Lokasi(
        "Rumah Sakit",
        "Rumah sakit tertua di kota. Mungkin ada jadwal penelitian virus zombie di sini.",
        ["Zombie Mutan", "Zombie Biasa", "Zombie Biasa"]
    ),
    "Laboratorium": Lokasi(
        "Laboratorium",
        "Pusat penelitian biologis. Sumber virus zombie berasal dari sini!",
        ["Zombie Mutan", "Zombie Mutan"]
    ),
    "Persimpangan Jalan": Lokasi(
        "Persimpangan Jalan",
        "Jalan utama yang menghubungkan berbagai lokasi. Ada zombie berpatroli.",
        ["Zombie Biasa"]
    ),
    "Gedung Pemerintah": Lokasi(
        "Gedung Pemerintah",
        "Kantor pusat pemerintahan kota. Di sini mungkin tersimpan dokumen penting.",
        ["Zombie Biasa", "Zombie Biasa", "Zombie Mutan"]
    ),
    "Kamar Tua": Lokasi(
        "Kamar Tua",
        "Sebuah ruangan kuno yang misterius, penuh dengan artefak bersejarah yang bersinar aneh. Di sini terpancar energi gelap... AGUNG SUNDAKI ada di sini!",
        ["AGUNG SUNDAKI"]
    )
}

# ===== SISTEM PERTARUNGAN =====
def pertarungan(pemain, musuh):
    print(f"\n⚔️ PERTARUNGAN DIMULAI!")
    print(f"Vs {musuh.nama}\n")
    
    # Cek apakah ini AGUNG SUNDAKI
    if musuh.nama == "AGUNG SUNDAKI" and pemain.level < 67:
        print(f"\n⚠️ {musuh.nama} adalah boss yang sangat kuat!")
        print(f"📊 Level mu: {pemain.level}")
        print(f"⚡ Level yang dibutuhkan: 67")
        print(f"\n😱 Aura gelap memancar dari {musuh.nama}!")
        print(f"💀 Kamu terlalu lemah untuk melawan musuh ini!")
        print(f"⚔️ Setiap serangan mu TIDAK BERHASIL merugikan {musuh.nama}!\n")
    
    while pemain.hp > 0 and musuh.hp > 0:
        pemain.tampilkan_status()
        musuh.tampilkan_status()
        
        print("\n🎮 PILIHAN AKSI:")
        print("1. Serang")
        print("2. Gunakan Obat")
        print("3. Lari")
        
        pilihan = input("\nPilih aksi (1-3): ").strip()
        
        if pilihan == "1":
            # Serangan pemain
            # Cek apakah pemain bisa menyerang AGUNG SUNDAKI
            if musuh.nama == "AGUNG SUNDAKI" and pemain.level < 67:
                damage = 0
                print(f"\n💥 Kamu menyerang {musuh.nama}!")
                print(f"❌ Serangan mu TIDAK BERHASIL! Level mu terlalu rendah!")
                print(f"📊 Butuh level 67 untuk melukai {musuh.nama}!")
            else:
                damage = random.randint(15, 35)
                musuh.hp -= damage
                print(f"\n💥 Kamu menyerang! Damage: {damage}")
            
            if musuh.hp <= 0:
                print(f"\n✨ {musuh.nama} berhasil dikalahkan!")
                pemain.exp += musuh.exp_drop
                pemain.emas += random.randint(20, 50)
                print(f"📊 +{musuh.exp_drop} EXP, +{20}-50 Emas")
                cek_level_up(pemain)
                return True
            
            # Serangan balik zombie
            damage_musuh = random.randint(10, musuh.atk)
            pemain.hp -= damage_musuh
            print(f"👹 {musuh.nama} menyerangmu! Damage: {damage_musuh}")
            
        elif pilihan == "2":
            if "Obat HP" in pemain.inventori and pemain.inventori["Obat HP"] > 0:
                heal = 50
                pemain.hp = min(pemain.hp + heal, pemain.max_hp)
                pemain.inventori["Obat HP"] -= 1
                print(f"\n💊 Kamu menggunakan Obat HP! +{heal} HP")
                
                damage_musuh = random.randint(10, musuh.atk)
                pemain.hp -= damage_musuh
                print(f"👹 {musuh.nama} menyerangmu! Damage: {damage_musuh}")
            else:
                print("\n❌ Tidak ada obat!")
                
        elif pilihan == "3":
            if random.random() > 0.5:
                print("\n💨 Kamu berhasil lari!")
                return False
            else:
                print("\n❌ Lari gagal!")
                damage_musuh = random.randint(10, musuh.atk)
                pemain.hp -= damage_musuh
                print(f"👹 {musuh.nama} menyerangmu! Damage: {damage_musuh}")
        
        if pemain.hp <= 0:
            print(f"\n💀 Kamu kalah! Pertarungan berakhir.")
            pemain.hp = 1
            return False
        
        print("\n" + "="*40)
        time.sleep(1)

def cek_level_up(pemain):
    if pemain.exp >= pemain.exp_max:
        pemain.level += 1
        pemain.exp = 0
        pemain.exp_max += 50
        pemain.max_hp += 20
        pemain.hp = pemain.max_hp
        pemain.max_mana += 15
        pemain.mana = pemain.max_mana
        print(f"\n⭐ LEVEL UP! Kamu sekarang level {pemain.level}!")

# ===== SISTEM QUEST =====
def tampilkan_quest(pemain):
    print(f"\n📜 QUEST")
    print("="*40)
    
    quests = {
        "Membersihkan Pasar": {
            "deskripsi": "Bersihkan Pasar Utama dari zombies",
            "lokasi": "Pasar Utama",
            "target": 2,
            "reward_exp": 150,
            "reward_emas": 100
        },
        "Investigasi Rumah Sakit": {
            "deskripsi": "Cari informasi tentang virus di Rumah Sakit",
            "lokasi": "Rumah Sakit",
            "target": 3,
            "reward_exp": 200,
            "reward_emas": 150
        },
        "Serang Laboratorium": {
            "deskripsi": "Musnahkan pusat virus di Laboratorium",
            "lokasi": "Laboratorium",
            "target": 2,
            "reward_exp": 300,
            "reward_emas": 250
        }
    }
    
    num = 1
    for nama_quest, detail in quests.items():
        status = "✓" if nama_quest in pemain.quest_selesai else " "
        print(f"[{status}] {num}. {nama_quest}")
        print(f"    {detail['deskripsi']}")
        num += 1
    
    return quests

# ===== SISTEM ARTEFAK KUNO =====
def tampilkan_artefak_kamar(pemain):
    print("\n" + "="*60)
    print("🏛️ ARTEFAK KUNO DI KAMAR TUA")
    print("="*60)
    print("""
    Kamu memasuki ruangan yang penuh dengan artefak bersejarah.
    Di sini tersimpan kekuatan kuno yang legendaris!
    
    Pilih salah satu artefak untuk meningkatkan kekuatanmu:
    """)
    
    artefak_tersedia = {
        "1": {
            "nama": "Pedang Cahaya Kuno",
            "deskripsi": "Pedang yang bersinar dengan cahaya spiritual. Meningkatkan ATK 30!",
            "efek": "attack",
            "nilai": 30
        },
        "2": {
            "nama": "Baju Zirah Pelindung",
            "deskripsi": "Zirah dari zaman dahulu dengan mantra perlindungan. Menambah HP 100!",
            "efek": "health",
            "nilai": 100
        },
        "3": {
            "nama": "Mahkota Kebijaksanaan",
            "deskripsi": "Mahkota yang memberikan nalar tinggi. Meningkatkan Level 5!",
            "efek": "level",
            "nilai": 5
        }
    }
    
    for kode, artefak in artefak_tersedia.items():
        print(f"\n{kode}. {artefak['nama']}")
        print(f"   {artefak['deskripsi']}")
    
    pilihan = input("\nPilih artefak (1-3): ").strip()
    
    if pilihan in artefak_tersedia:
        artefak = artefak_tersedia[pilihan]
        pemain.artefak.append(artefak['nama'])
        
        print(f"\n✨ Kamu mengambil {artefak['nama']}!")
        print(f"💫 Kekuatan legendaris mengalir melalui tubuhmu!\n")
        time.sleep(1.5)
        
        if artefak['efek'] == "attack":
            print(f"🔥 Seranganmu akan 30% lebih kuat!\n")
        elif artefak['efek'] == "health":
            pemain.max_hp += artefak['nilai']
            pemain.hp = pemain.max_hp
            print(f"❤️ HP maksimum mu meningkat menjadi {pemain.max_hp}!\n")
        elif artefak['efek'] == "level":
            pemain.level += artefak['nilai']
            print(f"⭐ Levelmu meningkat drastis menjadi level {pemain.level}!\n")
        
        time.sleep(2)
    else:
        print("\n❌ Pilihan tidak valid!")
# ===== GAME OVER =====
def tampilkan_game_over(pemain):
    print("\n" + "="*70)
    print("💀 GAME OVER - KEKALAHAN")
    print("="*70)
    
    print(f"""
    
    Sadar atau tidak, dalam sekejap mata, nyawa {pemain.nama} melayang.
    Sesuatu yang terlalu kuat, terlalu berbahaya, tergantian persisnya...
    
    😵 Dalam kondisi terbaring yang lemah, pandangan {pemain.nama} mulai
       gelap. Suara-suara zombie terdengar mendekat, semakin keras, semakin
       menakutkan...
    
    💀 Kota SERLOK TAK PARANI tetap dalam kegelapan.
    
    """)
    
    time.sleep(2)
    
    print("="*70)
    print("📖 KISAH KEGAGALAN")
    print("="*70)
    
    cerita_gagal = [
        f"""
    {pemain.nama} yang pemberani mencoba menyelamatkan kota dari wabah zombie.
    Namun nasib tidak berpihak. Kamu terlalu terburu-buru, tidak cukup kuat,
    dan tidak siap menghadapi ancaman yang begitu besar.
    
    Zombie-zombie ganas terus bertambah dan menyebar. Tanpa pahlawan sejati
    untuk menghentikan mereka, wabah terus berkembang. Kota mayat ini semakin
    penuh dengan korban-korban baru setiap hari.
    
    Penduduk yang selamat kehilangan harapan. Mereka menunggu seorang pahlawan
    yang tidak pernah datang. Mereka menunggu penyelamat yang telah gagal.
        """,
        f"""
    Ledakan energi zombie overwhelm {pemain.nama}. Kekuatan yang dilepaskan
    oleh monster kota ini jauh melampaui imajinasi. Tidak ada artefak yang
    cukup kuat. Tidak ada obat yang bisa menyembuhkan.
    
    Dalam keputusasaan terakhir, {pemain.nama} menyadari bahwa mereka
    seharusnya telah berlatih lebih lama, mencapai level yang lebih tinggi,
    atau mengumpulkan lebih banyak artefak kuno.
    
    Kota SERLOK TAK PARANI akan tetap menjadi tempat horor selamanya.
    Legenda tentang pahlawan yang gagal akan diceritakan dari mulut ke mulut
    sebagai peringatan bagi generasi mendatang.
        """,
        f"""
    Hanya ada keheningan setelah napas terakhir {pemain.nama} berhenti.
    
    Monster gelap terus merampok nyawa di setiap jalan, di setiap sudut kota.
    Wabah yang dimulai dari Laboratorium kini menguasai seluruh wilayah.
    
    Tidak ada yang tahu siapa saja para korban yang tersisa. Kota yang dulunya
    penuh kehidupan kini menjadi makam besar untuk jutaan orang yang tidak
    berdosa.
    
    Kegagalan {pemain.nama} akan menjadi dosa yang tidak terlunasi selamanya.
        """
    ]
    
    print(random.choice(cerita_gagal))
    
    time.sleep(3)
    
    print("\\n" + "="*70)
    print("📊 STATISTIK AKHIR (KEGAGALAN)")
    print("="*70)
    
    print(f"""
    👤 Nama Pemberani       : {pemain.nama}
    📈 Level Akhir          : {pemain.level}
    💰 Total Emas Terkumpul : {pemain.emas}
    ❤️  HP                   : {pemain.hp}/{pemain.max_hp}
    🏆 Quest Selesai        : {len(pemain.quest_selesai)}
    🎁 Artefak Dikumpulkan  : {len(pemain.artefak)}
    
    Mohon coba lagi dengan strategi yang lebih baik...
    """)
    
    print("\\n" + "="*70)

def restart_atau_keluar():
    while True:
        print(f"\\n{'='*40}")
        print("🎮 PILIHAN AKHIR")
        print(f"{'='*40}")
        print("1. Mulai Ulang dari Awal")
        print("2. Keluar dari Game")
        
        pilihan = input("\\nPilih opsi (1-2): ").strip()
        
        if pilihan == "1":
            print("\\n⏳ Mempersiapkan petualangan baru...\\n")
            time.sleep(2)
            return True
        elif pilihan == "2":
            print("\\n👋 Terima kasih telah bermain BOOYAH BERSAMA!")
            print("Semoga kali berikutnya Anda akan berhasil menyelamatkan kota!\\n")
            return False
        else:
            print("\\n❌ Pilihan tidak valid!")

# ===== ENDING GAME =====
def tampilkan_ending(pemain):
    print("\n" + "="*70)
    print("🎬 ENDING - KEMENANGAN TERAKHIR")
    print("="*70)
    
    print("""
    
    💀 AGUNG SUNDAKI, monster zombie yang telah merajalela di kota
       SERLOK TAK PARANI selama berbulan-bulan, akhirnya tergoyahkan!
    
    ⚔️ Dengan kemenangan berguncang, jasad AGUNG SUNDAKI terjatuh
       ke tanah, dan energi gelap yang menyelubungi kota mulai surut.
    
    ✨ Virus zombie yang telah menginfeksi ribuan penduduk kota
       perlahan-lahan memudar, hilang seiring dengan hilangnya sang
       penyebab wabah.
    
    """)
    
    time.sleep(3)
    
    print("="*70)
    print("📜 EPILOG - TIGA BULAN SETELAH KEMENANGAN")
    print("="*70)
    
    print(f"""
    
    Kota SERLOK TAK PARANI telah mulai pulih dengan pesat. Penduduk yang
    selamat kembali membangun hidup mereka dari puing-puing kehancuran.
    
    {pemain.nama}, sang pahlawan penyelamat, diterima dengan sambutan
    meriah di seluruh kota. Patung emas didirikan di Pasar Utama sebagai
    tanda terima kasih atas keberanian dan pengorbanannya yang luar biasa.
    
    Laboratorium telah ditutup dan dijadikan makam untuk para korban wabah.
    Kamar Tua, tempat di mana keputusan akhir terjadi, kini menjadi tempat
    suci yang dilindungi. Artefak-artefak kuno disimpan dengan baik untuk
    peringatan generasi mendatang.
    
    💪 {pemain.nama} diangkat sebagai PELINDUNG KOTA seumur hidup!
    
    Malam hari, ketika langit berbintang, {pemain.nama} menatap kota yang
    telah diselamatkan, menyadari bahwa perjalanan berbahaya, kerja keras,
    dan pengorbanan telah menghasilkan kedamaian dan harapan baru.
    
    Kota SERLOK TAK PARANI aman lagi... Berkat seorang pahlawan sejati!
    
    ═══════════════════════════════════════════════════════════════════════
    
    📊 STATISTIK AKHIR PERMAINAN:
    ═══════════════════════════════════════════════════════════════════════
    
    👤 Nama Pahlawan        : {pemain.nama}
    📈 Level Akhir          : {pemain.level}
    💰 Total Emas           : {pemain.emas}
    ❤️  HP Maksimum          : {pemain.max_hp}
    🏆 Quest Selesai        : {len(pemain.quest_selesai)}
    🎁 Artefak Dikumpulkan  : {len(pemain.artefak)}
    """)
    
    if pemain.artefak:
        print("\n🏛️ Artefak Legendaris yang Digunakan:")
        for artefak in pemain.artefak:
            print(f"   ✓ {artefak}")
    
    print("\n" + "="*70)
    print("🎮 TERIMA KASIH TELAH BERMAIN BOOYAH BERSAMA!")
    print("="*70)
    print(f"\n👋 Game berakhir... Legenda {pemain.nama} akan dikenang selamanya!\n")
    
    pemain.game_selesai = True

# ===== PENJELAJAHAN KOTA =====
def jelajahi_kota(pemain):
    print(f"\n🗺️ PETA KOTA SERLOK TAK PARANI")
    print("="*40)
    
    lokasi_list = list(lokasi_kota.keys())
    for i, loc in enumerate(lokasi_list, 1):
        print(f"{i}. {loc}")
    print(f"{len(lokasi_list)+1}. Kembali ke Menu Utama")
    
    pilihan = input("\nKemana kamu ingin pergi? (1-{}): ".format(len(lokasi_list)+1)).strip()
    
    try:
        idx = int(pilihan) - 1
        if idx == len(lokasi_list):
            return
        
        if 0 <= idx < len(lokasi_list):
            loc_name = lokasi_list[idx]
            lokasi = lokasi_kota[loc_name]
            pemain.lokasi = loc_name
            
            lokasi.tampilkan_info()
            
            if lokasi.zombie_spawn:
                print(f"\n👹 Ada {len(lokasi.zombie_spawn)} zombie di sini!")
                opsi = input("Lawan mereka? (y/t): ").lower()
                
                if opsi == 'y':
                    # Jika ini Kamar Tua, tawarkan artefak terlebih dahulu
                    if loc_name == "Kamar Tua":
                        tampilkan_artefak_kamar(pemain)
                    
                    zombies_di_lokasi = {
                        "Zombie Biasa": Zombie("Zombie Biasa", 30, 15, 50),
                        "Zombie Mutan": Zombie("Zombie Mutan", 60, 25, 100),
                        "AGUNG SUNDAKI": Zombie("AGUNG SUNDAKI", 500, 50, 1000)
                    }
                    
                    for zombie_type in lokasi.zombie_spawn:
                        musuh = zombies_di_lokasi[zombie_type]
                        menang = pertarungan(pemain, musuh)
                        if not menang:
                            # Jika kalah, return untuk trigger game over
                            return
                        # Jika berhasil mengalahkan AGUNG SUNDAKI, tampilkan ending
                        elif musuh.nama == "AGUNG SUNDAKI" and menang:
                            tampilkan_ending(pemain)
                            return
            else:
                print("\n✨ Lokasi ini aman dari zombie.")
    except ValueError:
        print("\n❌ Pilihan tidak valid!")

# ===== MENU UTAMA =====
def menu_utama(pemain):
    while True:
        print(f"\n{'='*40}")
        print(f"🎮 BOOYAH BERSAMA - Zombie Apocalypse")
        print(f"{'='*40}")
        print(f"1. Lihat Status")
        print(f"2. Jelajahi Kota")
        print(f"3. Lihat Quest")
        print(f"4. Lihat Inventori")
        print(f"5. Istirahat & Selamatkan Game")
        print(f"6. Keluar Game")
        
        pilihan = input("\nPilih menu (1-6): ").strip()
        
        if pilihan == "1":
            pemain.tampilkan_status()
            
        elif pilihan == "2":
            jelajahi_kota(pemain)
            # Jika game selesai atau pemain mati, keluar dari menu
            if pemain.game_selesai or pemain.hp == 1:
                break
            
        elif pilihan == "3":
            tampilkan_quest(pemain)
            
        elif pilihan == "4":
            pemain.tampilkan_inventori()
            
        elif pilihan == "5":
            print(f"\n💤 {pemain.nama} istirahat di tempat aman...")
            pemain.hp = pemain.max_hp
            pemain.mana = pemain.max_mana
            print(f"✨ Kesehatan dan Mana pulih kembali!")
            print(f"💾 Game disimpan!")
            time.sleep(1)
            
        elif pilihan == "6":
            print(f"\n👋 Terima kasih telah bermain!")
            print(f"📊 Statistik Akhir:")
            print(f"   Level: {pemain.level}")
            print(f"   Total Emas: {pemain.emas}")
            print(f"   Quest Selesai: {len(pemain.quest_selesai)}")
            break
        
        else:
            print("\n❌ Pilihan tidak valid!")

# ===== INTRO GAME =====
def intro_game():
    print("\n" + "="*50)
    print("🎮 SELAMAT DATANG DI GAME BOOYAH BERSAMA")
    print("="*50)
    print("\n📖 CERITA:")
    print("""
Kota SERLOK TAK PARANI yang dulunya ramai kini telah berubah
menjadi kota mayat. Wabah zombie apocalypse telah melanda
seluruh wilayah kota. Tidak ada yang tahu bagaimana virus ini
menyebar, hanya ada satu hal yang jelas...

SESEORANG HARUS MENGHENTIKANNYA!

Kamu adalah satu-satunya harapan. Bersenjata dengan keyakinan
dan keberanian, kamu harus menjelajahi kota yang berbahaya ini,
mengungkap misteri virus, dan menghentikan wabah sebelum semuanya
terlambat.

Apakah kamu siap untuk menyelamatkan Kota Serlok Tak Parani?
    """)
    print("="*50)

def game_utama():
    while True:
        intro_game()
        
        nama = input("\n👤 Siapa namamu, Pahlawan? ")
        pemain = Pemain(nama)
        
        print(f"\n✨ Selamat datang, {pemain.nama}!")
        print(f"   Petualanganmu dimulai di {pemain.lokasi}...")
        time.sleep(2)
        
        menu_utama(pemain)
        
        # Jika game selesai (menang), tanyakan apakah ingin bermain lagi
        if pemain.game_selesai:
            if not restart_atau_keluar():
                break
        # Jika HP = 1 (mati), tampilkan game over
        elif pemain.hp == 1:
            tampilkan_game_over(pemain)
            if not restart_atau_keluar():
                break
    
if __name__ == "__main__":
    game_utama()