import tkinter as tk
from tkinter import ttk
from src import main


def ucitavanje_vrijednosti():
    if not all([ulaz_P.get(), ulaz_n.get(), ulaz_J.get(), ulaz_t3.get(), vrsta_stroja.get(), materijal_povrsina.get(),
                vrsta_opterecenja.get(), ulaz_delta.get(), ulaz_broj_ciklusa.get()]):
        output.insert(tk.END, "Nisu učitani svi podaci\n")
        return

    vrijednosti = {"P": float(ulaz_P.get()), "n": float(ulaz_n.get()), "J": float(ulaz_J.get()),
                   "t3": float(ulaz_t3.get()), "vrsta_stroja": vrsta_stroja.get(),
                   "materijal_tarnih_povrsina": materijal_povrsina.get(), "vrsta_opterecenja": vrsta_opterecenja.get(),
                   "odnos": float(ulaz_delta.get()), "broj_ciklusa": float(ulaz_broj_ciklusa.get())}
    T = main.dimenzioniranje_spojke(vrijednosti)
    output.insert(tk.END, f"T0: {round(T[0], 2)} Nm, Te: {round(T[1], 2)} Nm => Tuk: {round(T[2], 2)} Nm\n")
    izracun = main.dimenzioniranje_vratila(vrijednosti, T[2])
    output.insert(tk.END, f"d_min: {round(izracun[0], 2)} mm\nTau: {round(izracun[1], 2)} N/mm2\n"
                          f"Tau_t: {round(izracun[2], 2)} N/mm2\nDimenzije vratila: {round(izracun[3], 2)} mm\n"
                          f"Pero: {round(izracun[4], 2)} mm\n"
                          f"b1: {round(izracun[5], 2)}\nfi: {round(izracun[6], 2)}\n"
                          f"Sigurnost: {round(izracun[7], 2)}\n"
                          f"----------------------------------------------------------\n")
    return


def ocisti():
    output.delete(1.0, tk.END)


win = tk.Tk()
win.title("Lamelna Spojka")
win.geometry("800x800")
prvi_red = ttk.Frame(win)
prvi_red.pack(side="top", fill="x", expand=True)
ttk.Label(prvi_red, text="Vrsta pogonskog stroja", padding=10).pack(side="left", fill="x", expand=True)
vrsta_stroja = tk.IntVar()
ttk.Radiobutton(prvi_red, text="centrifugalna pumpa, ventilator     ", variable=vrsta_stroja, value=1). \
    pack(side="left", fill="x", expand=True)
ttk.Radiobutton(prvi_red, text="lift, dizalica     ", variable=vrsta_stroja, value=2). \
    pack(side="left", fill="x", expand=True)
ttk.Radiobutton(prvi_red, text="preša", variable=vrsta_stroja, value=3).pack(side="left", fill="x", expand=True)

drugi_red = ttk.Frame(win)
drugi_red.pack(side="top", fill="x", expand=True)
ttk.Label(drugi_red, text="Snaga, P, koja se mora prenijeti na radni stroj", padding=10). \
    pack(side="left", fill="x")
ulaz_P = ttk.Entry(drugi_red, width=7)
ulaz_P.pack(side="left", fill="x")
ttk.Label(drugi_red, text="kW").pack(side="left", fill="x")

treci_red = ttk.Frame(win)
treci_red.pack(side="top", fill="x", expand=True)
ttk.Label(treci_red, text="Brzina vrtnje elektromotora - n1; n2=0; ∆n=n1", padding=10).pack(side="left", fill="x")
ulaz_n = ttk.Entry(treci_red, width=7)
ulaz_n.pack(side="left", fill="x")
ttk.Label(treci_red, text="s-1").pack(side="left", fill="x")

cetvrti_red = ttk.Frame(win)
cetvrti_red.pack(side="top", fill="x", expand=True)
ttk.Label(cetvrti_red, text="Vrsta torzijskog opterećenja", padding=10).pack(side="left", fill="x", expand=True)
vrsta_opterecenja = tk.IntVar()
ttk.Radiobutton(cetvrti_red, text="istosmjerno     ", variable=vrsta_opterecenja, value=1). \
    pack(side="left", fill="x", expand=True)
ttk.Radiobutton(cetvrti_red, text="naizmjenično", variable=vrsta_opterecenja, value=2). \
    pack(side="left", fill="x", expand=True)

peti_red = ttk.Frame(win)
peti_red.pack(side="top", fill="x", expand=True)
ttk.Label(peti_red, text="Moment tromosti svih masa koje se moraju ubrzati J", padding=10).pack(side="left", fill="x")
ulaz_J = ttk.Entry(peti_red, width=7)
ulaz_J.pack(side="left", fill="x")
ttk.Label(peti_red, text="kgm2").pack(side="left", fill="x")

sesti_red = ttk.Frame(win)
sesti_red.pack(side="top", fill="x", expand=True)
ttk.Label(sesti_red, text="Traženo vrijeme ubrzanja spojke t3", padding=10).pack(side="left", fill="x")
ulaz_t3 = ttk.Entry(sesti_red, width=7)
ulaz_t3.pack(side="left", fill="x")
ttk.Label(sesti_red, text="s").pack(side="left", fill="x")

sedmi_red = ttk.Frame(win)
sedmi_red.pack(side="top", fill="x", expand=True)
ttk.Label(sedmi_red, text="Materijal tarnih površina", padding=10).pack(side="left", fill="x", expand=True)
materijal_povrsina = tk.IntVar()
ttk.Radiobutton(sedmi_red, text="čelik/čelik + rad u ulju     ", variable=materijal_povrsina, value=1). \
    pack(side="left", fill="x", expand=True)
ttk.Radiobutton(sedmi_red, text="čelik/sinterobloga + rad na suho     ",
                variable=materijal_povrsina, value=2).pack(side="left", fill="x", expand=True)
ttk.Radiobutton(sedmi_red, text="čelik/sinterobloga + rad u ulju     ",
                variable=materijal_povrsina, value=3).pack(side="left", fill="x", expand=True)

osmi_red = ttk.Frame(win)
osmi_red.pack(side="top", fill="x", expand=True)
ttk.Label(osmi_red, text="Dopušteni odnos preostale Fuo prema uvedenoj uzdužnoj sili uključenja Fun\n"
          "δ = Fuo/Fun", padding=10).pack(side="left", fill="x")
ulaz_delta = ttk.Entry(osmi_red, width=7)
ulaz_delta.pack(side="left", fill="x")

deveti_red = ttk.Frame(win)
deveti_red.pack(side="top", fill="x", expand=True)
ttk.Label(deveti_red, text="Broj ciklusa", padding=10).pack(side="left", fill="x")
ulaz_broj_ciklusa = ttk.Entry(deveti_red, width=7)
ulaz_broj_ciklusa.pack(side="left", fill="x")

gumbi = ttk.Frame(win)
gumbi.pack(side="top", fill="x", expand=True)
ttk.Button(gumbi, text="Izračunaj", command=ucitavanje_vrijednosti).pack(side="left", expand=True)
ttk.Button(gumbi, text="Clear", command=ocisti).pack(side="left", expand=True)
ttk.Button(gumbi, text="Izlaz", command=win.destroy).pack(side="left", expand=True)

ispis = ttk.Frame(win)
ispis.pack(side="top", fill="x")
output = tk.Text(ispis)
output.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    win.mainloop()
