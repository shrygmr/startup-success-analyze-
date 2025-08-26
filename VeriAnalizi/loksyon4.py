import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. VERİ HAZIRLAMA
df = pd.read_csv('cleaned_funding2_dataset.csv')

# Temizlik ve dönüşümler
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')
df = df.dropna(subset=['country_code', 'funding_total_usd'])

# 2. ÜLKE BAZINDA FON ANALİZLERİ
country_stats = df.groupby('country_code').agg(
    company_count=('name', 'count'),
    total_funding=('funding_total_usd', 'sum'),
    avg_funding=('funding_total_usd', 'mean')
).sort_values('total_funding', ascending=False)

# 3. GÖRSELLEŞTİRMELER
plt.figure(figsize=(14, 18))  # Grafik boyutu optimize edildi

# Grafik 1: Toplam fon alan ilk 20 ülke
plt.subplot(3, 1, 1)
top20_total = country_stats.head(20)
sns.barplot(
    y=top20_total.index,
    x=top20_total['total_funding']/1e9,
    palette="Blues_r",
    edgecolor='black'
)
plt.title('1. Toplamda En Fazla Fon Alan İlk 20 Ülke (Milyar USD)', fontsize=12)
plt.xlabel('Toplam Fon (B$)')
plt.ylabel('Ülke Kodu')

# Değer etiketleri
for i, value in enumerate(top20_total['total_funding']/1e9):
    plt.text(value + 0.5, i, f"{value:,.1f}B", va='center')

# Grafik 2: Ortalama fon miktarı en yüksek 20 ülke (DÜZELTİLDİ)
plt.subplot(3, 1, 2)
# Minimum şirket sayısı filtresi kaldırıldı veya 1 yapıldı
top20_avg = country_stats.nlargest(20, 'avg_funding')  # Filtresiz versiyon
sns.barplot(
    y=top20_avg.index,
    x=top20_avg['avg_funding']/1e6,
    palette="Reds_r",
    edgecolor='black'
)
plt.title('2. Ortalama Fon Miktarı En Yüksek 20 Ülke (Milyon USD)', fontsize=12)
plt.xlabel('Ortalama Fon (M$)')
plt.ylabel('Ülke Kodu')

# Değer etiketleri
for i, value in enumerate(top20_avg['avg_funding']/1e6):
    plt.text(value + 0.1, i, f"{value:,.1f}M", va='center')

# Grafik 3: 100+ şirketi olan ülkelerde ortalama fon
plt.subplot(3, 1, 3)
large_countries = country_stats.query('company_count >= 100').sort_values('avg_funding', ascending=False)
sns.barplot(
    y=large_countries.index,
    x=large_countries['avg_funding']/1e6,
    palette="Greens_r",
    edgecolor='black'
)
plt.title('3. 100+ Şirketli Ülkelerde Şirket Başına Ortalama Fon (Milyon USD)', fontsize=12)
plt.xlabel('Ortalama Fon (M$)')
plt.ylabel('Ülke Kodu')

# Değer etiketleri
for i, value in enumerate(large_countries['avg_funding']/1e6):
    plt.text(value + 0.1, i, f"{value:,.1f}M", va='center')

plt.tight_layout()
plt.show()

# 4. ÖZET ÇIKTIz
print("\n═"*70)
print("ANALİZ ÖZETİ".center(70))
print("═"*70)
print(f"• Toplam Ülke Sayısı: {len(country_stats)}")
print(f"• 100+ Şirket Bulunan Ülke Sayısı: {len(large_countries)}")
print(f"• En Yüksek Ortalama Fon: ${country_stats['avg_funding'].max():,.0f} ({country_stats['avg_funding'].idxmax()})")
print(f"• En Yüksek Toplam Fon: ${country_stats['total_funding'].max():,.0f} ({country_stats['total_funding'].idxmax()})")
print(f"• Ortalama Fon Şampiyonu: {top20_avg.index[0]} (${top20_avg['avg_funding'].iloc[0]/1e6:,.1f}M)")