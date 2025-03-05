"""
===============================================================
ŠIS KODS:
    Šis ir grafiskā lietotāja saskarnes (GUI) kods spēlei "Akmentu spēle", 
    kas izstrādāta kā praktiskais darbs kursā "Mākslīgā intelekta pamati".
    
SPĒLES APRAKSTS UN NOTEIKUMI:
    Spēles sākumā tiek uz galda novietots noteikts akmeņu skaits (no 50 līdz 70).
    Spēlētāji (cilvēks un dators) veic gājienus pa kārtām. Katra gājiena laikā 
    spēlētājs var paņemt vai nu 2, vai 3 akmeņus. Pēc akmeņu paņemšanas:
        - Ja uz galda atlikušais akmeņu skaits ir pāra skaitlis, spēlētājam tiek 
          pieskaitīti 2 punkti.
        - Ja atlikušais akmeņu skaits ir nepāra, spēlētāja punktu skaitlis tiek samazināts par 2.
    Spēle beidzas, kad uz galda ir mazāk par 2 akmeņiem (t.i., vairs nevar veikt gājienu).
    Galīgo rezultātu aprēķina, saskaitot spēlētāja punktus un savākto akmeņu skaitu.
    Uzvar tas spēlētājs, kuram galīgais rezultāts ir lielāks; ja rezultāti sakrīt, spēle ir neizšķirta.

PRASĪBAS UZ PROJEKTU:
    - Spēlei jābūt izstrādātai ar pilnvērtīgu grafisko lietotāja saskarni (nav komandrindas versijas).
    - Jāizmanto datu struktūras, lai attēlotu spēles stāvokļus un (vai) spēles koku.
    - Jāsavieno minimaks algoritms un tā uzlabotā versija – alfa-beta atgriešana, lai izvēlētos labāko gājienu.
    - Projekta gaitā ir jāveic eksperimentāli mērījumi (piemēram, cik virsotņu tiek apmeklēts, cik ātri darbojas algoritms utt.).
    - Komandas dalībniekiem ir jāspēj izskaidrot katru koda daļu.
===============================================================
"""
# Importējam nepieciešamās bibliotēkas
import tkinter as tk            # GUI izveidei (Grafiskā lietotāja saskarne)
from tkinter import messagebox  # Logu ar kļūdu paziņojumiem attēlošanai
import copy                     # Objekta kopēšanai (lai nemainītu sākotnējo stāvokli)
import time                     # Laika mērīšanai (algoritmu ātruma noteikšanai)
import random                   # Nejaušu skaitļu ģenerēšanai

# Globālais mainīgais apmeklēto virsotņu skaitīšanai (eksperimentiem)
apmekleto_virsotnu_skaits = 0

# Meklēšanas dziļums (cik dziļi algoritms pārbauda nākotnes gājienus)
DZILUMS = 6

# ============================================================================
# Klase: SpelesStavoklis
# Apraksts: Glabā spēles datus – cik akmeņu ir uz galda, cik akmeņu un punktu
#     ir iegūti abiem spēlētājiem un kurš spēlētājs veic gājienu.
# ============================================================================
class SpelesStavoklis:
    def __init__(self, akmeni, cilveka_akmeni=0, cilveka_punkti=0, datora_akmeni=0, datora_punkti=0, gaji="cilveks"):
        # 'akmeni' – sākotnējais akmeņu skaits uz galda
        # 'cilveka_akmeni' un 'cilveka_punkti' – cilvēka savākto akmeņu un punktu skaits
        # 'datora_akmeni' un 'datora_punkti' – datora savākto akmeņu un punktu skaits
        # 'gaji' – kurš veic gājienu: "cilveks" vai "dators"
        self.akmeni = akmeni
        self.cilveka_akmeni = cilveka_akmeni
        self.cilveka_punkti = cilveka_punkti
        self.datora_akmeni = datora_akmeni
        self.datora_punkti = datora_punkti
        self.gaji = gaji

    def ir_beidzies(self):
        # Spēle beidzas, ja uz galda ir mazāk par 2 akmeņiem (t.i., nevar paņemt 2 vai 3)
        return self.akmeni < 2

    def iespējamie_gajieni(self):
        # Atgriež sarakstu ar gājieniem (paņem 2 vai 3 akmeņus), ja to var veikt
        gajieni = []
        if self.akmeni >= 2:
            gajieni.append(2)
        if self.akmeni >= 3:
            gajieni.append(3)
        return gajieni

    def izpildi_gajienu(self, gajiens):
        # Izveido jaunu spēles stāvokli, kurā tiek piemērots dots gājiens
        jaunais_stavoklis = copy.deepcopy(self)
        jaunais_stavoklis.akmeni -= gajiens
        if jaunais_stavoklis.gaji == "cilveks":
            jaunais_stavoklis.cilveka_akmeni += gajiens
            # Ja atlikušais akmeņu skaits ir pāra, pievieno 2 punktus, citādi atņem 2
            if jaunais_stavoklis.akmeni % 2 == 0:
                jaunais_stavoklis.cilveka_punkti += 2
            else:
                jaunais_stavoklis.cilveka_punkti -= 2
        else:
            jaunais_stavoklis.datora_akmeni += gajiens
            if jaunais_stavoklis.akmeni % 2 == 0:
                jaunais_stavoklis.datora_punkti += 2
            else:
                jaunais_stavoklis.datora_punkti -= 2
        # Mainām gājiena pusi
        jaunais_stavoklis.gaji = "dators" if jaunais_stavoklis.gaji == "cilveks" else "cilveks"
        return jaunais_stavoklis

    def vertiba(self):
        # Aprēķina spēles stāvokļa vērtību no datora skatpunkta:
        # Vērtība = (datora punkti + datora akmeņi) - (cilveka punkti + cilveka akmeņi)
        cilveka_final = self.cilveka_punkti + self.cilveka_akmeni
        datora_final = self.datora_punkti + self.datora_akmeni
        return datora_final - cilveka_final

# ============================================================================
# Funkcija: minimaks
# Apraksts: Klasisks minimaks algoritms, kas rekursīvi izvēlas labāko gājienu
# ============================================================================
def minimaks(stavoklis, dziļums, vai_maksimizet):
    global apmekleto_virsotnu_skaits
    apmekleto_virsotnu_skaits += 1

    # Ja dziļums ir 0 vai spēle beigusies, atgriež stāvokļa vērtību
    if dziļums == 0 or stavoklis.ir_beidzies():
        return stavoklis.vertiba(), None

    labakais_gajiens = None
    if vai_maksimizet:
        max_vertiba = -float('inf')
        for gajiens in stavoklis.iespējamie_gajieni():
            vert, _ = minimaks(stavoklis.izpildi_gajienu(gajiens), dziļums - 1, False)
            if vert > max_vertiba:
                max_vertiba = vert
                labakais_gajiens = gajiens
        return max_vertiba, labakais_gajiens
    else:
        min_vertiba = float('inf')
        for gajiens in stavoklis.iespējamie_gajieni():
            vert, _ = minimaks(stavoklis.izpildi_gajienu(gajiens), dziļums - 1, True)
            if vert < min_vertiba:
                min_vertiba = vert
                labakais_gajiens = gajiens
        return min_vertiba, labakais_gajiens

# ============================================================================
# Funkcija: alfa_beta
# Apraksts: Uzlabota minimaks versija ar alfa-beta atgriešanu, lai samazinātu pārbaudāmo stāvokļu skaitu
# ============================================================================
def alfa_beta(stavoklis, dziļums, alfa, beta, vai_maksimizet):
    global apmekleto_virsotnu_skaits
    apmekleto_virsotnu_skaits += 1

    if dziļums == 0 or stavoklis.ir_beidzies():
        return stavoklis.vertiba(), None

    labakais_gajiens = None
    if vai_maksimizet:
        max_vertiba = -float('inf')
        for gajiens in stavoklis.iespējamie_gajieni():
            vert, _ = alfa_beta(stavoklis.izpildi_gajienu(gajiens), dziļums - 1, alfa, beta, False)
            if vert > max_vertiba:
                max_vertiba = vert
                labakais_gajiens = gajiens
            alfa = max(alfa, max_vertiba)
            if alfa >= beta:
                break  # Atgriešana, ja turpmāka pārbaude nav nepieciešama
        return max_vertiba, labakais_gajiens
    else:
        min_vertiba = float('inf')
        for gajiens in stavoklis.iespējamie_gajieni():
            vert, _ = alfa_beta(stavoklis.izpildi_gajienu(gajiens), dziļums - 1, alfa, beta, True)
            if vert < min_vertiba:
                min_vertiba = vert
                labakais_gajiens = gajiens
            beta = min(beta, min_vertiba)
            if beta <= alfa:
                break
        return min_vertiba, labakais_gajiens

# ============================================================================
# Klase: SpelesGUI
# Apraksts: Veido grafisko lietotāja saskarni (GUI) spēlei, kur lietotājs var izvēlēties
# sākotnējos parametrus un veikt gājienus.
# ============================================================================
class SpelesGUI:
    def __init__(self, logs):
        self.logs = logs
        self.logs.title("Akmentu spēle")
        self.stavoklis = None  # Spēles stāvoklis vēl nav izveidots

        # Rāmis iestatījumiem
        self.iestatijumi_ramis = tk.Frame(self.logs)
        self.iestatijumi_ramis.pack(pady=10)

        # Iestatījums akmeņu skaitam
        tk.Label(self.iestatijumi_ramis, text="Izvēlies sākuma akmentu skaitu (50-70):").grid(row=0, column=0)
        self.akmenu_lauks = tk.Entry(self.iestatijumi_ramis)
        self.akmenu_lauks.grid(row=0, column=1)
        self.akmenu_lauks.insert(0, "50")
        # Čekboks nejaušam akmeņu skaitam
        self.nejauss_akmenu = tk.BooleanVar(value=False)
        tk.Checkbutton(self.iestatijumi_ramis, text="Nejaušs skaits", variable=self.nejauss_akmenu).grid(row=0, column=2)

        # Iestatījums, kurš sāks spēli
        tk.Label(self.iestatijumi_ramis, text="Kurš sāk:").grid(row=1, column=0)
        self.sakuma_speletajs = tk.StringVar()
        self.sakuma_speletajs.set("cilveks")
        tk.Radiobutton(self.iestatijumi_ramis, text="Cilvēks", variable=self.sakuma_speletajs, value="cilveks").grid(row=1, column=1)
        tk.Radiobutton(self.iestatijumi_ramis, text="Dators", variable=self.sakuma_speletajs, value="dators").grid(row=1, column=2)
        tk.Radiobutton(self.iestatijumi_ramis, text="Nejauši", variable=self.sakuma_speletajs, value="nejauši").grid(row=1, column=3)

        # Iestatījums algoritmam
        tk.Label(self.iestatijumi_ramis, text="Izvēlies algoritmu:").grid(row=2, column=0)
        self.algoritms = tk.StringVar()
        self.algoritms.set("minimaksa")
        tk.Radiobutton(self.iestatijumi_ramis, text="Minimaksa", variable=self.algoritms, value="minimaksa").grid(row=2, column=1)
        tk.Radiobutton(self.iestatijumi_ramis, text="Alfa-beta", variable=self.algoritms, value="alfa_beta").grid(row=2, column=2)

        # Poga spēles sākšanai
        self.sakt_poga = tk.Button(self.iestatijumi_ramis, text="Sākt spēli", command=self.sakt_speli)
        self.sakt_poga.grid(row=3, column=0, columnspan=4, pady=5)

        # Rāmis spēles stāvokļa attēlošanai
        self.speles_ramis = tk.Frame(self.logs)
        # Šis rāmis parādīsies pēc spēles sākuma

        # Paziņojumu etiķete
        self.pazinojums = tk.Label(self.logs, text="", font=("Helvetica", 12))
        self.pazinojums.pack(pady=5)

        # Poga spēles restartēšanai (parādās, kad spēle beidzas)
        self.restart_poga = tk.Button(self.logs, text="Sākt jaunu spēli", command=self.restartet)

        # Rāmis cilvēka gājienu pogām
        self.gajiena_ramis = tk.Frame(self.logs)
        self.poga_2 = tk.Button(self.gajiena_ramis, text="Paņemt 2", command=lambda: self.cilveka_gajens(2))
        self.poga_3 = tk.Button(self.gajiena_ramis, text="Paņemt 3", command=lambda: self.cilveka_gajens(3))

    # ============================================================================
    # Funkcija: sakt_speli
    # Apraksts: Lasīt iestatījumus, inicializēt spēles stāvokli un uzsākt spēli.
    # ============================================================================
    def sakt_speli(self):
        # Ja nejauša akmeņu skaita opcija ir aktivizēta, ģenerē nejaušu skaitu
        if self.nejauss_akmenu.get():
            sakuma_akmeni = random.randint(50, 70)
        else:
            try:
                sakuma_akmeni = int(self.akmenu_lauks.get())
                if sakuma_akmeni < 50 or sakuma_akmeni > 70:
                    messagebox.showerror("Kļūda", "Akmeņu skaitam jābūt no 50 līdz 70!")
                    return
            except ValueError:
                messagebox.showerror("Kļūda", "Lūdzu, ievadi skaitli!")
                return

        # Ja nejauša sākuma opcija ir izvēlēta, izlasa nejauši starp "cilveks" un "dators"
        sakums = self.sakuma_speletajs.get()
        if sakums == "nejauši":
            sakums = random.choice(["cilveks", "dators"])

        # Inicializē spēles stāvokli ar nolasītajiem parametriem
        self.stavoklis = SpelesStavoklis(sakuma_akmeni, gaji=sakums)

        # Paslēpj iestatījumu rāmi un parādi spēles stāvokļa rāmi un gājiena pogas
        self.iestatijumi_ramis.pack_forget()
        self.speles_ramis.pack(pady=10)
        self.gajiena_ramis.pack(pady=10)
        self.atjaunot_speles_ekranu()

        # Ja sāk gāji datora kārtā, palaiž datora gājens ar nelielu aizturi
        if self.stavoklis.gaji == "dators":
            self.logs.after(500, self.datora_gajens)

    # ============================================================================
    # Funkcija: atjaunot_speles_ekranu
    # Apraksts: Parāda pašreizējo spēles stāvokli – cik akmeņu uz galda, spēlētāju rezultātus,
    # un kuru spēlētājs veic gājienu.
    # ============================================================================
    def atjaunot_speles_ekranu(self):
        # Notīra veco informāciju
        for elem in self.speles_ramis.winfo_children():
            elem.destroy()

        # Parāda spēles datus
        tk.Label(self.speles_ramis, text=f"Akmeņu skaits: {self.stavoklis.akmeni}").pack()
        tk.Label(self.speles_ramis, text=f"Cilvēka akmeņi: {self.stavoklis.cilveka_akmeni}, punkti: {self.stavoklis.cilveka_punkti}").pack()
        tk.Label(self.speles_ramis, text=f"Datora akmeņi: {self.stavoklis.datora_akmeni}, punkti: {self.stavoklis.datora_punkti}").pack()
        tk.Label(self.speles_ramis, text=f"Kurš gāji: {self.stavoklis.gaji}").pack()

        # Ja ir cilvēka kārta, parāda gājiena pogas
        if self.stavoklis.gaji == "cilveks":
            self.poga_2.pack(side=tk.LEFT, padx=5)
            self.poga_3.pack(side=tk.LEFT, padx=5)
        else:
            self.poga_2.pack_forget()
            self.poga_3.pack_forget()

    # ============================================================================
    # Funkcija: cilveka_gajens
    # Apraksts: Izpilda cilvēka gājienu, ja izvēlēts paņemt 2 vai 3 akmeņus.
    # ============================================================================
    def cilveka_gajens(self, gajiens):
        if gajiens not in self.stavoklis.iespējamie_gajieni():
            messagebox.showerror("Kļūda", "Šis gājiens nav iespējams!")
            return
        self.stavoklis = self.stavoklis.izpildi_gajienu(gajiens)
        self.atjaunot_speles_ekranu()
        if self.stavoklis.ir_beidzies():
            self.beigt_speli()
        elif self.stavoklis.gaji == "dators":
            self.logs.after(500, self.datora_gajens)

    # ============================================================================
    # Funkcija: datora_gajens
    # Apraksts: Datora gājiena funkcija, kas izvēlas labāko gājienu, izmantojot izvēlēto algoritmu.
    # ============================================================================
    def datora_gajens(self):
        # Atspējo cilvēka pogas, kamēr dators veic gājienu
        self.poga_2.config(state=tk.DISABLED)
        self.poga_3.config(state=tk.DISABLED)

        start = time.time()
        global apmekleto_virsotnu_skaits
        apmekleto_virsotnu_skaits = 0

        # Izvēlas algoritmu pēc iestatījumiem
        if self.algoritms.get() == "minimaksa":
            _, lab_gajiens = minimaks(self.stavoklis, DZILUMS, True)
        else:
            _, lab_gajiens = alfa_beta(self.stavoklis, DZILUMS, -float('inf'), float('inf'), True)
        ilgums = time.time() - start

        # Izvade eksperimentu rezultātu konsolē (var redzēt, cik ātri algoritms strādāja)
        print(f"Datora gājiens: {lab_gajiens}, Apmeklēti: {apmekleto_virsotnu_skaits}, Laiks: {ilgums:.4f} s")

        if lab_gajiens is None:
            self.beigt_speli()
            return

        self.stavoklis = self.stavoklis.izpildi_gajienu(lab_gajiens)
        self.atjaunot_speles_ekranu()
        if self.stavoklis.ir_beidzies():
            self.beigt_speli()
        else:
            self.poga_2.config(state=tk.NORMAL)
            self.poga_3.config(state=tk.NORMAL)

    # ============================================================================
    # Funkcija: beigt_speli
    # Apraksts: Aprēķina galīgo rezultātu un parāda paziņojumu, ka spēle ir beigusies.
    # ============================================================================
    def beigt_speli(self):
        cilveka_final = self.stavoklis.cilveka_punkti + self.stavoklis.cilveka_akmeni
        datora_final = self.stavoklis.datora_punkti + self.stavoklis.datora_akmeni
        if cilveka_final > datora_final:
            rezultats = "Cilvēks uzvar!"
        elif datora_final > cilveka_final:
            rezultats = "Dators uzvar!"
        else:
            rezultats = "Neizšķirts!"
        self.pazinojums.config(text=f"Spēle beigusies! {rezultats}\nCilvēks: {cilveka_final}, Dators: {datora_final}")
        self.gajiena_ramis.pack_forget()
        self.restart_poga.pack(pady=10)

    # ============================================================================
    # Funkcija: restartet
    # Apraksts: Atgriežas sākotnējā iestatījumu ekrānā, lai varētu sākt jaunu spēli.
    # ============================================================================
    def restartet(self):
        # Atiestatām cilvēka gājiena pogu stāvokli uz NORMAL
        self.poga_2.config(state=tk.NORMAL)
        self.poga_3.config(state=tk.NORMAL)
        self.speles_ramis.pack_forget()
        self.gajiena_ramis.pack_forget()
        self.restart_poga.pack_forget()
        self.pazinojums.config(text="")
        self.iestatijumi_ramis.pack(pady=10)

# ============================================================================
# Funkcija: main
# Apraksts: Spēles loga inicializācija un palaišana.
# ============================================================================
def main():
    logs = tk.Tk()         # Izveido jaunu logu
    app = SpelesGUI(logs)  # Inicializē spēles GUI objektu
    logs.mainloop()        # Palaiž loga cilpu

# Programmas izpilde sākas šeit
if __name__ == "__main__":
    main()
