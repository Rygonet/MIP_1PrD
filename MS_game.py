import random
import tkinter as tk
from tkinter import messagebox

class AkmenisuSpele:
    def __init__(self, akmentinu_skaits, algoritms):
        self.akmentinu_skaits = akmentinu_skaits
        self.algoritms = algoritms
        self.punkti_cilveks = 0
        self.punkti_dators = 0
        self.cilveks_gajiens = True

    def parbaudi_galu(self, akmentinu_skaits=None):
        if akmentinu_skaits is None:
            akmentinu_skaits = self.akmentinu_skaits
        return akmentinu_skaits <= 0

    def pievieno_punktus(self, parskaitisana=True):
        jaatnem = 2 if self.akmentinu_skaits % 2 == 0 else -2
        if parskaitisana:
            if self.cilveks_gajiens:
                self.punkti_cilveks += self.akmentinu_skaits
            else:
                self.punkti_dators += self.akmentinu_skaits
        else:
            if self.cilveks_gajiens:
                self.punkti_cilveks += jaatnem
            else:
                self.punkti_dators += jaatnem

    def heurisks(self, akmentinu_skaits):
        return akmentinu_skaits if akmentinu_skaits % 2 == 0 else -akmentinu_skaits

    def minimax(self, akmentinu_skaits, ir_maximizing):
        if self.parbaudi_galu(akmentinu_skaits):
            return self.heurisks(akmentinu_skaits)

        if ir_maximizing:
            best_value = -float('inf')
            for gajiens in [2, 3]:
                if gajiens <= akmentinu_skaits:
                    value = self.minimax(akmentinu_skaits - gajiens, False)
                    best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for gajiens in [2, 3]:
                if gajiens <= akmentinu_skaits:
                    value = self.minimax(akmentinu_skaits - gajiens, True)
                    best_value = min(best_value, value)
            return best_value

    def dator_gajiens(self):
        best_value = -float('inf')
        best_move = 2
        for gajiens in [2, 3]:
            if gajiens <= self.akmentinu_skaits:
                value = self.minimax(self.akmentinu_skaits - gajiens, False)
                if value > best_value:
                    best_value = value
                    best_move = gajiens
        return best_move

class GrafiskaSpele(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Akmenīšu spēle")
        self.geometry("400x300")
        self.speles_objekts = None
        self.izveidot_sakuma_saskarni()

    def izveidot_sakuma_saskarni(self):
        self.sakuma_frame = tk.Frame(self)
        self.sakuma_frame.pack(pady=20)

        tk.Label(self.sakuma_frame, text="Izvēlies akmentiņu skaitu (50-70):").pack()
        self.akmentinu_skaits_entry = tk.Entry(self.sakuma_frame)
        self.akmentinu_skaits_entry.pack()

        tk.Label(self.sakuma_frame, text="Izvēlies algoritmu (minimax/alpha-beta):").pack()
        self.algoritms_entry = tk.Entry(self.sakuma_frame)
        self.algoritms_entry.pack()

        tk.Button(self.sakuma_frame, text="Sākt spēli", command=self.sakt_speli).pack(pady=10)

    def sakt_speli(self):
        try:
            akmentinu_skaits = int(self.akmentinu_skaits_entry.get())
            if not (50 <= akmentinu_skaits <= 70):
                raise ValueError("Akmentiņu skaitam jābūt no 50 līdz 70.")
            algoritms = self.algoritms_entry.get().lower()
            if algoritms not in ['minimax', 'alpha-beta']:
                raise ValueError("Nepareizs algoritma veids.")

            self.speles_objekts = AkmenisuSpele(akmentinu_skaits, algoritms)
            self.sakuma_frame.pack_forget()
            self.izveidot_speles_saskarni()
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))

    def izpildit_gajienu(self, gajiens):
        self.speles_objekts.akmentinu_skaits -= gajiens
        self.speles_objekts.pievieno_punktus(parskaitisana=False)

        if not self.speles_objekts.parbaudi_galu():
            dator_gajiens = self.speles_objekts.dator_gajiens()
            self.speles_objekts.akmentinu_skaits -= dator_gajiens
            self.speles_objekts.pievieno_punktus(parskaitisana=False)

        self.atjaunot_spelei()

    def atjaunot_spelei(self):
        if self.speles_objekts.parbaudi_galu():
            cilveks = self.speles_objekts.punkti_cilveks
            dators = self.speles_objekts.punkti_dators
            uzvaretajs = "Cilvēks uzvarēja!" if cilveks > dators else "Dators uzvarēja!" if dators > cilveks else "Rezultāts ir neizšķirts."
            messagebox.showinfo("Spēles beigas", f"Cilvēks: {cilveks}, Dators: {dators}\n{uzvaretajs}")
            self.destroy()
        else:
            self.akmentinu_label.config(text=f"Atlikušie akmentiņi: {self.speles_objekts.akmentinu_skaits}")

    def izveidot_speles_saskarni(self):
        self.speles_frame = tk.Frame(self)
        self.speles_frame.pack(pady=20)
        self.akmentinu_label = tk.Label(self.speles_frame, text="")
        self.akmentinu_label.pack()
        tk.Button(self.speles_frame, text="Paņemt 2 akmentiņus", command=lambda: self.izpildit_gajienu(2)).pack()
        tk.Button(self.speles_frame, text="Paņemt 3 akmentiņus", command=lambda: self.izpildit_gajienu(3)).pack()
        self.atjaunot_spelei()

if __name__ == '__main__':
    app = GrafiskaSpele()
    app.mainloop()