import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib import patches
from matplotlib.patheffects import withStroke
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")
import squarify

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


################## Function ##################
def Policy_calculator(Policy_list):
    c, d = 0, 0
    for x, y in Policy_list.items():
        c += (df[df["COUNTRY"] == x][y].sum() + df[df["COUNTRY"] == x]["TOPLAM_PRIM_USD_TEK"].sum())
        d = df[~df["COUNTRY"].isin([key for key in Policy_list])]["TOPLAM_PRIM_USD"].sum()
        g = round(df["TOPLAM_PRIM_USD"].sum(), 2)
        e = round(c + d, 2)
        fark = round(e - g, 2)
        değişim = round(((e - g) / g) * 100, 2)
        fark2 = round(fark/1000000,1)

        j = df["TOPLAM_PRIM_USD_TAB"].sum()
        h = fark
        değişimd = round((h / j) * 100, 2)
        fark2d = round(h/1000000,1)


        sig0["Toplam Değişim"] = 0  # Ülke bazındaki değişim
        for a, b in Policy_list.items():
            sig0.loc[sig0["COUNTRY"] == a, "Toplam Değişim"] = sig0[sig0["COUNTRY"] == a][b]
        sig1 = sig0.loc[sig0["Toplam Değişim"] != 0, ["COUNTRY", "PRIME_ESAS_TUTARI_USD_TAB", "TOPLAM_PRIM_USD_TAB",
                                              "Toplam Değişim"]].groupby("COUNTRY").\
            agg({"PRIME_ESAS_TUTARI_USD_TAB": "sum",
                     "TOPLAM_PRIM_USD_TAB": "sum",
                     "Toplam Değişim": "sum"})
        sig1 = sig1.reset_index().sort_values(by="Toplam Değişim", ascending=True)
        sig1 = sig1.rename(columns={"COUNTRY": "Country",
                                        "PRIME_ESAS_TUTARI_USD_TAB": "Prime Esas Sevkiyat Tutarı",
                                        "TOPLAM_PRIM_USD_TAB": "Mevcut Prim Tutarı",
                                        "Toplam Değişim": "Değişim"})


    for a, b in Policy_list.items():        # En çok maliyeti artan 30 sigortalı
        sig3 = sig0.groupby(["SIGORTALI_NO", "CUSTOMER"]).agg({"PRIME_ESAS_TUTARI_USD_TAB": "sum",
                                                                    "TOPLAM_PRIM_USD_TAB": "sum",
                                                                    "Toplam Değişim": "sum"})
        sig3.reset_index(inplace=True)
        sig3["Yüzde Değişim"] = sig3["Toplam Değişim"] / sig3["TOPLAM_PRIM_USD_TAB"] * 100

        sig3 = sig3.sort_values(by="PRIME_ESAS_TUTARI_USD_TAB", ascending=False).head(100)
        sig3 = sig3.sort_values(by="Yüzde Değişim", ascending=True).tail(30)

#    print(sig1.head(20))
#    print(sig3.head(20))

    xs = [f'Current Revenue \n \n {g:,} USD',
          f'Expected Revenue \n \n {e:,} USD']

    names = ["Toplam Prim Geliri"]
    value1 = [g]
    value2 = [fark]

    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)
#    fig.suptitle('ÜRS Değişiminin Etkisi', fontsize="20")
    fig.subplots_adjust(hspace=1.50, wspace=0.8, left=0.08, right=0.98)
#    plt.rcParams.update({'figure.autolayout': False})

    gs = GridSpec(4, 24, figure=fig)
    ax0 = fig.add_subplot(gs[0:2, 0:5]) # Bilgilendirme metni
    ax1 = fig.add_subplot(gs[0:2, 5:8]) # Toplam prim tutarındaki değişim
    ax10 = fig.add_subplot(gs[0:2, 9:12]) # Toplam prim tutarındaki değişim (Tablolu)
    ax7 = fig.add_subplot(gs[0:2, 12:15]) # Ort. net oranındaki tutarındaki değişim
    ax11 = fig.add_subplot(gs[0:2, 15:18]) # Ort. net oranındaki tutarındaki değişim (Tablolu)

    ax3 = fig.add_subplot(gs[:, 18:24])  # Sigortalı bazında yüzde değişim (maliyet)
    # identical to ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=3))
    ax4 = fig.add_subplot(gs[2:4, 0:4]) # Etkilenecek sigortalı sayısı
    ax6 = fig.add_subplot(gs[2:4, 5:11]) # Ülke bazında ort. net prim oranı
    ax2 = fig.add_subplot(gs[2:4, 11:18]) # Ülke bazında toplam değişim

    ax0.yaxis.set_visible(False)
    ax0.xaxis.set_visible(False)
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.text(-0.1, 0.2, f'Projection Period:\n        07/20XX-06/20XX \n\n'
                        f'Current Revenue:\n        {round(g):,} USD \n\n'
                        f'Expected Revenue:\n        {round(e):,} USD \n\n'
                        f'Profit/Loss: {round(fark):,} USD\n           (% {değişim})', fontsize=12)

    ax1.bar(names, value1, color="tab:blue", edgecolor='white', alpha=0.5)
    ax1.bar(names, value2, bottom=value1, color="tab:red", alpha=0.7)
    ax1.set_title('Total Premium Amount\n', fontsize=11)
    ax1.text(-0.30, e + 1000000, f"       Δ% {değişim} \n({fark2:,} Million USD)")
    ax1.set_ylabel('Million USD')
    ax1.ticklabel_format(style="sci", axis="y", scilimits=(6, 6))
    ax1.set_ylim((0, 100000000))
    ax1.set_xticklabels("")
    ax1.set_xmargin(0.2)
    ax1.set_xticks([])

    namesd = ["Toplam Tablolu Prim Geliri"]
    value1d = [j]
    value2d = [fark]

    ax10.bar(namesd, value1d, color="tab:blue", edgecolor='white', alpha=0.5)
    ax10.bar(namesd, value2d, bottom=value1d, color="tab:red", alpha=0.7)
    ax10.set_title('Total Premium Amount\n(Special Program)', fontsize=11)
    ax10.text(-0.30, j+fark + 1000000, f"    Δ% {değişimd} \n({fark2d:,} Million USD)")
    ax10.set_ylabel('Million USD')
    ax10.ticklabel_format(style="sci", axis="y", scilimits=(6, 6))
    ax10.set_ylim((0, 100000000))
    ax10.set_xticklabels("")
    ax10.set_xmargin(0.2)
    ax10.set_xticks([])


#    colors = ["#01489C", "#0159AA", "#006AB2", "#0778B9", "#338BC5", "#509DCD"]
    sig11 = sig1.copy()
    sig11["Toplam Prim"] = sig1["Mevcut Prim Tutarı"]+sig1["Değişim"]
    sig11 = sig11.sort_values(by="Toplam Prim", ascending=True)
    ALICI_ULKESI_ADI = sig11["Country"].tail(15).tolist()
    Mevcut = sig11["Mevcut Prim Tutarı"].tail(15).tolist()
    Toplam_Değişim = sig11["Değişim"].tail(15).tolist()
#    print(sig11)
    isim = [i * 0.9 for i in range(len(ALICI_ULKESI_ADI))]
    ax2.barh(isim, Mevcut, height=0.55, align="edge", color="tab:blue", alpha=0.4, label="Current")
    ax2.barh(isim, Toplam_Değişim, left=Mevcut, height=0.55, align="edge", color="tab:red", alpha=0.5, label="Change")
#    ax2.set_axisbelow(True)
    ax2.grid(axis="x", color="#A8BAC4", lw=1.2, alpha=0.2)
#    ax2.spines["right"].set_visible(False)
#    ax2.spines["top"].set_visible(False)
#    ax2.spines["bottom"].set_visible(False)
#    ax2.spines["left"].set_lw(1.5)
    ax2.yaxis.set_visible(False)
    PAD = 0.3
    for name, y_pos in zip(ALICI_ULKESI_ADI, isim):
        x = 0
        color = "black"
        ax2.text(
            x + PAD, y_pos + 0.5 / 2, name,
            color=color, va="center",
        )
#    ax2.barh(sig3["ALICI_ULKESI_ADI"], sig3["Toplam Değişim"], data=sig3, color="tab:blue", alpha=0.5)
    ax2.set_title('Total Premium by Country\n(Per thousand USD)', fontsize=11)
    ax2.legend()
    ax2.ticklabel_format(style="sci", axis="x", scilimits=(3, 3))

#    siggg["SIGORTALI_NO"] = siggg["SIGORTALI_NO"].astype(str)
#    ax3.barh(sig3["SIGORTALI_ADI"], sig3["Yüzde Değişim"], data=sig0, alpha=0.4)
    ax3.set_title('The Most Affected \n 30 Customers (%)',fontsize=11)
#    ax3.ticklabel_format(style="sci", axis="x", scilimits=(3, 3))
    #    ax3.xlabel('Oluşacak Ek Maliyet (Bin USD)')
    SIGORTALI_ADI = sig3["CUSTOMER"].tolist()
    Toplam_Değişima = sig3["Yüzde Değişim"].to_list()
    ya= [i * 1 for i in range(len(SIGORTALI_ADI))]
    ax3.barh(ya, Toplam_Değişima, height=0.80, align="center", color="tab:blue", alpha=0.4)
    ax3.yaxis.set_visible(False)
    ax3.grid(axis="x", color="#A8BAC4", lw=1.2, alpha=0.2)
    #    ax2.set_axisbelow(True)
    # ax3.grid(axis="x", color="#A8BAC4", lw=1.2, alpha=0.5)
    #    ax2.spines["right"].set_visible(False)
    #    ax2.spines["top"].set_visible(False)
    #    ax2.spines["bottom"].set_visible(False)
    #    ax2.spines["left"].set_lw(1.5)
    PAD = 0.3
    for name, y_pos in zip(SIGORTALI_ADI, ya):
        x = 0
        color = "black"
        ax3.text(
            x + PAD, y_pos, name,
            color=color, fontfamily="Econ Sans Cnd", va="center"
        )
#    ax3.spines['top'].set_visible(False)
#    ax3.spines['right'].set_visible(False)
#    ax3.spines['bottom'].set_visible(False)
#    ax3.spines['left'].set_visible(False)

    sig4 = sig0.groupby("SIGORTALI_NO").agg({"Toplam Değişim":"sum"})
    sig4 = sig4.reset_index()

    Etkilenmeyecek_sig_sayısı  = sig0["SIGORTALI_NO"].nunique() - sig4.loc[sig4["Toplam Değişim"] != 0]["SIGORTALI_NO"].nunique()
    Etkilenecek_sig_sayısı = sig4.loc[sig4["Toplam Değişim"] > 0]["SIGORTALI_NO"].nunique()
    Olumlu_etki_sig_sayısı = sig4.loc[sig4["Toplam Değişim"] < 0]["SIGORTALI_NO"].nunique()
    myfigures = np.array([Etkilenecek_sig_sayısı, Etkilenmeyecek_sig_sayısı, Olumlu_etki_sig_sayısı])
    mylabels = [f"\nNegatively Affected\n{Etkilenecek_sig_sayısı}",
                f"Netural\n         {Etkilenmeyecek_sig_sayısı}",
                f"Positively\nAffected {Olumlu_etki_sig_sayısı}"]
    myexplode = [0, 0.1, 0.1]
    col = ["tab:blue", "tab:gray", "tab:green"]
    ax4.pie(myfigures, labels=mylabels, explode=myexplode, autopct='%1.1f%%', startangle=180, colors=col, wedgeprops={'alpha':0.55})
    ax4.set_title('Number of Customers to be Affected \n', fontsize=11)
#    plt.setp(pcts, color='white', fontweight='bold')

#    print(sig4[["ÜLKE", "Prim Tutarı"]].groupby("ÜLKE").describe())

    Ort_Prim = round((df["TOPLAM_PRIM_USD"].sum()/df["PRIME_ESAS_TUTARI_USD"].sum())*1000,2)
    Yeni_Ort_Prim = round((e/df["PRIME_ESAS_TUTARI_USD"].sum())*1000,2)
    Ort_Prim_list_value = [Ort_Prim, Yeni_Ort_Prim]
    Ort_Prim_list_key = ["Current", "Expected"]

    ax7.bar(Ort_Prim_list_key, Ort_Prim_list_value, color=["tab:blue", "tab:orange"], alpha=0.5)
    ax7.set_ylim((0, 5))
#    ax7.set_xticklabels("")
    ax7.set_yticklabels("")
    ax7.set_title('Average\nPremium Rate\n(Per thousand)', fontsize=11)
    ax7.set_yticks([])
#    ax7.set_xyticks([])
    for container in ax7.containers:
        ax7.bar_label(container)

    Tab_Ort_Prim = round((df["TOPLAM_PRIM_USD_TAB"].sum() / df["PRIME_ESAS_TUTARI_USD_TAB"].sum()) * 1000, 2)
    Tab_Yeni_Ort_Prim = round(((j+fark) / df["PRIME_ESAS_TUTARI_USD_TAB"].sum()) * 1000, 2)
    Tab_Ort_Prim_list_value = [Tab_Ort_Prim, Tab_Yeni_Ort_Prim]
    Tab_Ort_Prim_list_key = ["Current", "Expected"]

    ax11.bar(Tab_Ort_Prim_list_key, Tab_Ort_Prim_list_value, color=["tab:blue", "tab:orange"], alpha=0.5)
    ax11.set_ylim((0, 5))
    #    ax7.set_xticklabels("")
    ax11.set_yticklabels("")
    ax11.set_title('Average Premium Rate \n(Special Program)\n(Per thousand)', fontsize=11)
    ax11.set_yticks([])
    #    ax7.set_xyticks([])
    for container in ax11.containers:
        ax11.bar_label(container)

    sig1["Net Premium Rate"] = (sig1["Mevcut Prim Tutarı"]/sig1["Prime Esas Sevkiyat Tutarı"])*1000
    sig1["New Net Premium Rate"] = ((sig1["Mevcut Prim Tutarı"]+sig1["Değişim"])/sig1["Prime Esas Sevkiyat Tutarı"])*1000
    sig1 = sig1.set_index("Country")
    #    ax2.ylabel("Pies Consumed")
    sig1["Net Premium Rate"] = round(sig1["Net Premium Rate"], 2)
    sig1["New Net Premium Rate"] = round(sig1["New Net Premium Rate"], 2)
#    sig1["sort_val"] = sig1["Net Prim Oranı"]/sig1["Yeni Net Prim Oranı"]
#    print(sig1)
#    sig1[["Net Prim Oranı", "Yeni Net Prim Oranı", "sort_val"]].sort_values(by="sort_val", ascending=True).drop("sort_val", 1).head(15).\
#        plot(ax=ax6, kind='bar', rot=45, alpha=0.5)
    sig1[["Net Premium Rate", "New Net Premium Rate", "Prime Esas Sevkiyat Tutarı"]].sort_values(by="Prime Esas Sevkiyat Tutarı", ascending=False).drop("Prime Esas Sevkiyat Tutarı", 1).head(7).\
        plot(ax=ax6, kind='bar', rot=45, alpha=0.5)
    ax6.set_title("Average Net Premium Rate\nby Country (Per Thousand)", fontsize=11)
    ax6.set_ylim((0, sig1["Yeni Net Prim Oranı"].max()*1.4))
    ax6.set_yticks([])
    ax6.set_yticklabels("")
    ax6.set_xlabel("")
    ax6.set_xmargin(0.05)
#    ax6.spines['top'].set_visible(False)
#    ax6.spines['right'].set_visible(False)
#    ax6.spines['bottom'].set_visible(False)
#    ax6.spines['left'].set_visible(False)
    for container in ax6.containers:
        ax6.bar_label(container)


    plt.show()

    xs1 = {'\n'
           '\n'
           'Mevcut Durumda Prim Geliri:': f'{g:,} USD',
          'Önerilen Durumda Prim Geliri:': f'{e:,} USD',
          "Fark:": f'{fark:,} USD',
          "Değişim (%):": f'{değişim}'}

    for k, v in xs1.items():
        print(k, v)
#############################################


######## POLICY DETERMINATION ################
Policy_list = {"COUNTRY 5":2,
         "COUNTRY 15":7,
         "COUNTRY 1":4,
         "COUNTRY 8":2,
         "COUNTRY 55":4,
         "COUNTRY 105":7,
         "COUNTRY 240":3,
         "COUNTRY 6":4,
         "COUNTRY 101":7,
         "COUNTRY 41":5}
################################################


################################################
Policy_calculator(Policy_list)
################################################



