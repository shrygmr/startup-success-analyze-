import pandas as pd

df = pd.read_csv('cleaned_funding2_dataset.csv')

ülke_analizi = df['country_code'].value_counts().reset_index()
ülke_analizi.columns = ['Ülke Kodu', 'Şirket Sayısı']

toplam_şirket = len(df)
toplam_ülke = len(ülke_analizi)
en_yüksek_ülke = ülke_analizi.iloc[0]


print("═"*50)
print("ÜLKELERE GÖRE ŞİRKET SAYILARI")
print("═"*50)
print(ülke_analizi.to_markdown(index=False))
print("\n" + "═"*50)
print("TOPLAM İSTATİSTİKLER")
print("═"*50)
print(f"Toplam Şirket Sayısı: {toplam_şirket:,}")
print(f"Toplam Ülke Sayısı: {toplam_ülke}")
print(f"En Çok Şirket Bulunan Ülke: {en_yüksek_ülke['Ülke Kodu']} ({en_yüksek_ülke['Şirket Sayısı']:,} şirket)")
print(f"İlk 5 Ülke Toplamı: {ülke_analizi.head(5)['Şirket Sayısı'].sum():,} (Tüm şirketlerin %{ülke_analizi.head(5)['Şirket Sayısı'].sum()/toplam_şirket*100:.1f}'i)")