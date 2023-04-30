import math
import json

if __name__ != "__main__":
    with open('src/konstante.json') as f:
        data = json.load(f)
        tablica_K = data[0]
        s = data[1]
        tau_dop = data[2]
        b2 = data[3]["b2"]
        S_potr = data[3]["s_potr"]
        beta = data[3]["beta"]
        fi = data[4]


def unos():
    return {"vrsta_stroja": int(input("Vrsta pogonskog stroja:\n"
                                      "1. centrifugalna pumpa, ventilator    2. lift, dizalica    3. preša\n> ")),
            "P": float(input("Snaga, P[kW], koja se mora prenijeti na radni stroj:\n> ")),
            "n": float(input("Brzina vrtnje elektromotora\nn1[s-1]; n2=0; ∆n=n1\n> ")),
            # materijal input
            "vrsta_opterecenja": int(input("Vrsta torzijskog opterećenja:\n1. istosmjerno    2. naizmjenično\n> ")),
            "J": float(input("Moment tromosti svih masa koje se moraju ubrzati J[kgm2]:\n> ")),
            "t3": float(input("Traženo vrijeme ubrzanja spojke t3[s]:\n> ")),
            "materijal_tarnih_povrsina": int(input("Materijal tarnih površina:\n"
                                                   "1. čelik/čelik + rad u ulju    2. čelik/sinterobloga + rad na suho"
                                                   "    3. čelik/sinterobloga + rad u ulju\n> ")),
            "odnos": float(input("Dopušteni odnos preostale Fuo prema uvedenoj uzdužnoj sili uključenja Fun\n"
                                 "δ = Fuo/Fun\n> ")),
            "broj_ciklusa": int(input("Broj ciklusa uključivanja spojke na sat:\n> "))}


def ispis(vrijednosti):
    print("\n------------------- UNESENE VRIJEDNOSTI ------------------")
    print("1. Tip spojke: mehanička\n2. Pogonski stroj: elektromotor")
    print("3. Vrsta pogonskog stroja: " + ("centrifugalna pumpa, ventilator" if vrijednosti["vrsta_stroja"] == 1
                                           else "lift, dizalica" if vrijednosti["vrsta_stroja"] == 2 else "preša"))
    print("4. Snaga, P[kW], koja se mora prenijeti na radni stroj: " + str(vrijednosti["P"]))
    print("5. Brzina vrtnje elektromotora n1[s-1]; n2=0; ∆n=n1: " + str(vrijednosti["n"]))
    print("6. Vrsta torzijskog opterećenja: " + ("istosmjerno" if vrijednosti["vrsta_opterecenja"] == 1
                                                 else "naizmjenično"))
    print("7. Vratilo spojke: ")
    print("8. Moment tromosti svih masa koje se moraju ubrzati J[kgm2]: " + str(vrijednosti["J"]))
    print("9. Traženo vrijeme ubrzanja spojke t3[s]: " + str(vrijednosti["t3"]))
    print("10. Materijal tarnih površina: " + (
        "čelik/čelik + rad u ulju" if vrijednosti["materijal_tarnih_povrsina"] == 1
        else "čelik/sinterobloga + rad na suho" if vrijednosti["materijal_tarnih_povrsina"] == 2
        else "čelik/sinterobloga + rad u ulju"))
    print("11. Dopušteni odnos preostale Fuo prema uvedenoj uzdužnoj sili uključenja Fun δ = Fuo/Fun: "
          + str(vrijednosti["odnos"]))
    print("12. Broj ciklusa uključivanja spojke na sat: " + str(vrijednosti["broj_ciklusa"]))
    print("13. Način uključenja spojke: pod punim opterećenjem")
    print("14. Položaj ugradnje: vodoravan")
    print("----------------------------------------------------------")


def interval_pero(d):
    return 1.1 if 6 < d <= 8 else 1.7 if 8 < d <= 10 else 2.4 if 10 < d <= 12 else 2.9 if 12 < d <= 17 \
        else 3.5 if 17 < d <= 22 else 4.1 if 22 < d <= 30 else 4.7 if 30 < d <= 38 else 4.9 if 38 < d <= 44 \
        else 5.5 if 44 < d <= 50 else 6.2 if 50 < d <= 58 else 6.8 if 58 < d <= 65 else 7.4 if 65 < d <= 75 \
        else 8.5 if 75 < d <= 85 else 8.7 if 85 < d <= 95 else 9.9 if 95 < d <= 110 else 11.1 if 110 < d <= 130 \
        else 12.3 if 130 < d <= 150 else 13.5 if 150 < d <= 170 else 15.3 if 170 < d <= 200 \
        else 17.0 if 200 < d <= 230 else 19.3 if 230 < d <= 260 else 19.6 if 260 < d <= 290 \
        else 22.0 if 290 < d <= 330 else 24.6 if 330 < d <= 380 else 27.5 if 380 < d <= 440 else 30.4


def interpolacija(d):
    if 0 < d <= 10:
        return 1
    elif 10 < d <= 20:
        x1, x2, y1, y2 = 10, 20, 1, 0.95
    elif 20 < d <= 30:
        x1, x2, y1, y2 = 20, 30, 0.95, 0.9
    elif 30 < d <= 40:
        x1, x2, y1, y2 = 30, 40, 0.9, 0.85
    elif 40 < d <= 60:
        x1, x2, y1, y2 = 40, 60, 0.85, 0.8
    elif 60 < d <= 120:
        x1, x2, y1, y2 = 60, 120, 0.8, 0.75
    elif 120 < d <= 180:
        x1, x2, y1, y2 = 120, 180, 0.75, 0.725
    elif 180 < d <= 240:
        x1, x2, y1, y2 = 180, 240, 0.725, 0.7
    else:
        exit("Greška! Dobivena vrijednost za d je izvan intervala.")
    return y1 + (d - x1) / (x2 - x1) * (y2 - y1)


def dimenzioniranje_spojke(vrijednosti):
    T0 = vrijednosti["P"] * 1000 / (2 * math.pi * vrijednosti["n"])
    Te = vrijednosti["J"] * vrijednosti["n"] / (9.56 * vrijednosti["t3"])
    Tuk = s[str(vrijednosti["materijal_tarnih_povrsina"])] * (tablica_K[str(vrijednosti["vrsta_stroja"])] * T0 + Te)
    print(f"T0: {round(T0, 2)}, Te: {round(Te, 2)} => Tuk: {round(Tuk, 2)}")
    return [T0, Te, Tuk]


def dimenzioniranje_vratila(vrijednosti, Tuk):
    Tau = tau_dop[str(vrijednosti["vrsta_opterecenja"])] / 5
    d_min_start = (Tuk * 1000 / (0.2 * Tau))**(1/3)
    print(f"d_min: {round(d_min_start, 2)}")
    d_min = d_min_start - d_min_start % 5  # zaokruživanje na najbliži manji višekratnik broja 5
    while True:
        d_min += 5
        Tau_t = Tuk * 1000 / (0.2 * (d_min - interval_pero(d_min)) ** 3)
        if Tau_t < Tau:
            S_post = interpolacija(d_min) * b2 * tau_dop[str(vrijednosti["vrsta_opterecenja"])] / \
                     (fi[str(vrijednosti["vrsta_stroja"])] * beta * Tau_t)
            if S_post > S_potr:
                print(f"Tau: {round(Tau, 2)}\nTau_t: {round(Tau_t, 2)}\nDimenzije vratila: {round(d_min, 2)}\n"
                      f"Pero: {round(interval_pero(d_min), 2)}\nb1: {round(interpolacija(d_min), 2)}\n"
                      f"fi: {round(fi[str(vrijednosti['vrsta_stroja'])], 2)}\nSigurnost: {round(S_post, 2)}")
                return [d_min_start, Tau, Tau_t, d_min, interval_pero(d_min), interpolacija(d_min),
                        fi[str(vrijednosti["vrsta_stroja"])], S_post]


def main():
    vrijednosti = unos()
    ispis(vrijednosti)
    Tuk = dimenzioniranje_spojke(vrijednosti)[2]
    dimenzioniranje_vratila(vrijednosti, Tuk)


if __name__ == "__main__":
    with open('konstante.json') as f:
        data = json.load(f)
        tablica_K = data[0]
        s = data[1]
        tau_dop = data[2]
        b2 = data[3]["b2"]
        S_potr = data[3]["s_potr"]
        beta = data[3]["beta"]
        fi = data[4]
    main()
