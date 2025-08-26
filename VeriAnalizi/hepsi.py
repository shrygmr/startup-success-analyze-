import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_funding2_dataset.csv')

success_statuses = ["operating", "acquired", "ipo"]

failure_statuses = ["closed", "closed_down"]

df['success'] = df['status'].apply(lambda x: 1 if x in success_statuses else 
                                  (0 if x in failure_statuses else -1))

success_rate = (df['success'] == 1).mean() * 100
failure_rate = (df['success'] == 0).mean() * 100
neutral_rate = (df['success'] == -1).mean() * 100

rates = pd.Series({
    'Başarılı': success_rate,
    'Başarısız': failure_rate,
    'Diğer': neutral_rate
})

plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
plt.pie(rates, 
        labels=rates.index, 
        autopct='%1.1f%%',
        colors=['#4CAF50', '#F44336', '#FFC107'],
        explode=(0.05, 0.05, 0),
        shadow=True)
plt.title('Başarı/Başarısızlık Oranları')

plt.subplot(1, 2, 2)
status_counts = df['status'].value_counts()
status_counts.plot(kind='barh', color=['#4CAF50' if x in success_statuses 
                                     else '#F44336' if x in failure_statuses 
                                     else '#FFC107' for x in status_counts.index])
plt.title('Durumlara Göre Şirket Sayıları')
plt.xlabel('Şirket Sayısı')

plt.tight_layout()
plt.show()

print("\n" + "="*50)
print("DETAYLI BAŞARI ANALİZİ".center(50))
print("="*50)
print(f"Toplam Şirket Sayısı: {len(df)}")
print(f"Başarılı Şirket Oranı: {success_rate:.1f}%")
print(f"Başarısız Şirket Oranı: {failure_rate:.1f}%")
print("\nDurum Dağılımı:")
print(status_counts)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('cleaned_funding2_dataset.csv')

country_counts = df['country_code'].value_counts().head(20)

plt.figure(figsize=(12, 8))
sns.barplot(
    y=country_counts.index,
    x=country_counts.values,
    palette="viridis",
    edgecolor='black'
)

plt.title('Ülkelere Göre Şirket Sayıları (Top 20)', fontsize=14, pad=20)
plt.xlabel('Şirket Sayısı', fontsize=12)
plt.ylabel('Ülke Kodu', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)

for i, value in enumerate(country_counts.values):
    plt.text(value + 10, i, f"{value:,}", va='center', fontsize=10)

plt.tight_layout()
plt.show()

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

import pandas as pd
import matplotlib.pyplot as plt

# Veriyi yükle
df = pd.read_csv('cleaned_funding2_dataset.csv')

# Başarı metriği oluştur
df['is_successful'] = df['status'].isin(['operating','acquired','ipo']).astype(int)

# 1. TÜM ÜLKELERİN LİSTESİ
country_stats = df.groupby('country_code').agg(
    company_count=('name','count'),
    success_rate=('is_successful','mean')
).sort_values('company_count', ascending=False)

print("TÜM ÜLKELERİN LİSTESİ:")
print("Ülke Kodu | Şirket Sayısı | Başarı Oranı")
print("----------------------------------------")
for country, row in country_stats.iterrows():
    print(f"{country:8} | {row['company_count']:>12} | {row['success_rate']:.1%}")

# 2. GRAFİK (100+ ŞİRKET OLAN ÜLKELER)
significant_countries = country_stats.query('company_count >= 100')

plt.figure(figsize=(10,6))
significant_countries['success_rate'].sort_values().plot.barh(
    color='#2ecc71',
    edgecolor='black',
    width=0.8
)

plt.title('100+ Şirket Bulunan Ülkelerin Başarı Oranları', pad=20)
plt.xlabel('Başarı Oranı')
plt.xlim(0, 1)
plt.grid(axis='x', alpha=0.3)

# Değer etiketleri ekle
for i, v in enumerate(significant_countries['success_rate'].sort_values()):
    plt.text(v + 0.02, i, f"{v:.1%}", color='black', va='center')

plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


success_statuses = ["operating", "acquired", "ipo"]
df['is_successful'] = df['status'].isin(success_statuses).astype(int)
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



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Veri setini yükleme
df = pd.read_csv('cleaned_funding2_dataset.csv')

# 1. Veri Hazırlama
# Tarihleri datetime'a çevirme ve şirket ömrünü hesaplama
df['founded_at'] = pd.to_datetime(df['founded_at'], errors='coerce')
df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')
df['company_age_days'] = (df['last_funding_at'] - df['founded_at']).dt.days

# Sadece geçerli ömür bilgisi olan ve faaliyette olan şirketleri filtreleme
valid_companies = df.dropna(subset=['company_age_days', 'category_list'])
operating_companies = valid_companies[valid_companies['status'] == 'operating']

# Kategorileri ayırma (ilk kategoriyi kullanarak)
operating_companies['primary_category'] = operating_companies['category_list'].str.split('|').str[0]

# 2. Analiz: Kategorilere Göre Ortalama Şirket Ömrü
category_age = operating_companies.groupby('primary_category')['company_age_days'].agg(['mean', 'count'])
category_age = category_age[category_age['count'] >= 5]  # En az 5 şirket olan kategoriler
top_10_longest = category_age.nlargest(10, 'mean')

# Günü yıla çevirme
top_10_longest['mean_years'] = top_10_longest['mean'] / 365

# 3. Görselleştirme
plt.figure(figsize=(14, 8))
sns.set_style("whitegrid")

# Ana grafik
ax = sns.barplot(x='mean_years', y=top_10_longest.index, data=top_10_longest, palette='viridis')

# Şirket sayılarını ekleme
for i, (_, row) in enumerate(top_10_longest.iterrows()):
    ax.text(row['mean_years'] + 0.2, i, f"n={int(row['count'])}", 
            va='center', ha='left', fontsize=10)

# Grafik düzenleme
plt.title('En Uzun Ömürlü Şirket Türleri (Ortalama Faaliyet Süresi)', fontsize=16)
plt.xlabel('Ortalama Faaliyet Süresi (Yıl)', fontsize=12)
plt.ylabel('Kategori', fontsize=12)
plt.xlim(0, top_10_longest['mean_years'].max() + 2)

plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 4. Ek Analiz: Fon Miktarı ile Ömür İlişkisi
plt.figure(figsize=(12, 6))
sns.scatterplot(x='company_age_days', y='funding_total_usd', 
                hue=operating_companies['primary_category'],
                size=operating_companies['funding_rounds'],
                sizes=(20, 200), alpha=0.7, 
                data=operating_companies)
plt.yscale('log')
plt.title('Şirket Ömrü ile Toplam Fon Miktarı İlişkisi', fontsize=14)
plt.xlabel('Şirket Ömrü (Gün)', fontsize=12)
plt.ylabel('Toplam Fon (USD - log scale)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükle ve başarı metriğini oluştur
df = pd.read_csv('cleaned_funding2_dataset.csv')
df['is_successful'] = df['status'].isin(['operating', 'acquired', 'ipo']).astype(int)

# 1. Türkiye'deki şirketleri filtrele
turkey_df = df[df['country_code'] == 'TUR'].copy()

# 2. Türkiye'deki şirketlerin listesi
print("═"*70)
print("TÜRKİYE'DEKİ ŞİRKET LİSTESİ".center(70))
print("═"*70)
print(turkey_df[['name', 'category_list', 'status', 'funding_total_usd']].to_markdown(index=False))

# 3. Kategorilere göre dağılım
turkey_df['primary_category'] = turkey_df['category_list'].str.split('|').str[0].str.strip()
category_dist = turkey_df['primary_category'].value_counts(normalize=True) * 100

plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
category_dist.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    colormap='tab20',
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}
)
plt.title('Türkiye: Şirket Kategorilerinin Dağılımı (%)', pad=20)
plt.ylabel('')

# 4. Başarı oranı analizi
plt.subplot(1, 2, 2)
success_rate = turkey_df['is_successful'].mean() * 100
other_rate = 100 - success_rate

plt.bar(
    ['Başarılı', 'Diğer'],
    [success_rate, other_rate],
    color=['#4CAF50', '#F44336'],
    edgecolor='black'
)
plt.title('Türkiye: Şirket Başarı Oranı', pad=20)
plt.ylabel('Oran (%)')
plt.ylim(0, 100)

# Değer etiketleri ekle
for i, v in enumerate([success_rate, other_rate]):
    plt.text(i, v + 2, f"{v:.1f}%", ha='center')

plt.tight_layout()
plt.show()

# 5. Detaylı istatistikler
print("\n═"*70)
print("TÜRKİYE İSTATİSTİKLERİ".center(70))
print("═"*70)
print(f"• Toplam Şirket Sayısı: {len(turkey_df)}")
print(f"• Başarı Oranı: {success_rate:.1f}%")
print(f"• En Popüler Kategori: {category_dist.index[0]} (%{category_dist.iloc[0]:.1f})")
print("\nKategori Dağılımı:")
print(category_dist.head(10).to_markdown(floatfmt=".1f"))

# 6. Kategori bazında başarı oranları (en az 3 şirket olan kategoriler)
category_success = turkey_df.groupby('primary_category').agg(
    company_count=('name', 'count'),
    success_rate=('is_successful', 'mean')
).query('company_count >= 3').sort_values('success_rate', ascending=False)

if not category_success.empty:
    print("\n═"*70)
    print("KATEGORİ BAZINDA BAŞARI ORANLARI (En az 3 şirket)".center(70))
    print("═"*70)
    print(category_success.to_markdown(floatfmt=".2f"))
else:
    print("\nNot: Kategori bazında analiz için yeterli veri yok (en az 3 şirket gerekiyor)")
    

    import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükle ve temizle
df = pd.read_csv('cleaned_funding2_dataset.csv')
df['is_successful'] = df['status'].isin(['operating', 'acquired', 'ipo']).astype(int)

# 1. Kategori sütununu oluştur (eğer yoksa)
if 'category_list' in df.columns:
    df['primary_category'] = df['category_list'].str.split('|').str[0].str.strip()
else:
    df['primary_category'] = 'Unknown'  # Kategori bilgisi yoksa varsayılan değer

# 2. Türkiye'deki başarılı şirketleri filtrele
turkey_successful = df[(df['country_code'] == 'TUR') & (df['is_successful'] == 1)].copy()

# 3. Eğer Türkiye'de başarılı şirket yoksa uyarı ver
if turkey_successful.empty:
    print("⚠️ Uyarı: Türkiye'de başarılı şirket bulunamadı!")
else:
    # 4. Ortalama fon miktarını hesapla (USD cinsinden)
    average_funding = turkey_successful['funding_total_usd'].mean()

    # 5. Görselleştirme
    plt.figure(figsize=(14, 6))
    
    # Boxplot ile dağılım
    plt.subplot(1, 2, 1)
    sns.boxplot(
        y=turkey_successful['funding_total_usd'] / 1e6,  # Milyon USD cinsinden
        color='#4CAF50',
        width=0.4
    )
    plt.title('Türkiye: Başarılı Şirketlerin Fon Dağılımı', pad=20)
    plt.ylabel('Fon Miktarı (Milyon USD)')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Barplot ile ortalama
    plt.subplot(1, 2, 2)
    sns.barplot(
        x=['Ortalama'],
        y=[average_funding / 1e6],
        color='#2196F3',
        edgecolor='black',
        width=0.5
    )
    plt.title('Türkiye: Başarılı Şirketlerin Ortalama Fonu', pad=20)
    plt.ylabel('Fon Miktarı (Milyon USD)')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.text(0, average_funding / 1e6 + 0.5, f"{average_funding / 1e6:.1f}M", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # 6. Kategori bazında analiz (en az 2 şirket olanlar)
    if 'primary_category' in turkey_successful.columns:
        category_funding = turkey_successful.groupby('primary_category').agg(
            company_count=('name', 'count'),
            avg_funding=('funding_total_usd', 'mean')
        ).query('company_count >= 2').sort_values('avg_funding', ascending=False)
        
        if not category_funding.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(
                y=category_funding.index,
                x=category_funding['avg_funding'] / 1e6,
                palette='viridis',
                edgecolor='black'
            )
            plt.title('Kategorilere Göre Ortalama Fon (Başarılı Şirketler)', pad=20)
            plt.xlabel('Ortalama Fon (Milyon USD)')
            plt.grid(axis='x', linestyle='--', alpha=0.6)
            
            for i, v in enumerate(category_funding['avg_funding'] / 1e6):
                plt.text(v + 0.1, i, f"{v:.1f}M", va='center')
            
            plt.tight_layout()
            plt.show()

    # 7. Detaylı istatistikler
    print("\n═"*70)
    print("TÜRKİYE'DEKİ BAŞARILI ŞİRKET ANALİZİ".center(70))
    print("═"*70)
    print(f"• Toplam Başarılı Şirket Sayısı: {len(turkey_successful)}")
    print(f"• Ortalama Fon Miktarı: ${average_funding:,.0f} USD")
    print(f"• Medyan Fon Miktarı: ${turkey_successful['funding_total_usd'].median():,.0f} USD")
    
    if not turkey_successful.empty:
        max_funding = turkey_successful['funding_total_usd'].max()
        max_company = turkey_successful.loc[turkey_successful['funding_total_usd'].idxmax(), 'name']
        print(f"• En Yüksek Fon Alan Şirket: {max_company} (${max_funding:,.0f} USD)")
    
    if 'primary_category' in turkey_successful.columns and not category_funding.empty:
        print("\n═"*70)
        print("KATEGORİ BAZINDA ORTALAMA FONLAR".center(70))
        print("═"*70)
        print(category_funding.to_markdown(floatfmt=".0f"))

        import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Veriyi yükle ve temizle
df = pd.read_csv('cleaned_funding2_dataset.csv')
df['is_successful'] = df['status'].isin(['operating', 'acquired', 'ipo']).astype(int)

# 1. Korelasyon Analizi
correlation = df[['funding_total_usd', 'is_successful']].corr(method='pearson')
print("═"*50)
print("FON MİKTARI VE BAŞARI KORELASYONU".center(50))
print("═"*50)
print(correlation)

# 2. Görselleştirme
plt.figure(figsize=(12, 6))

# a) Scatter Plot (Log ölçekli)
plt.subplot(1, 2, 1)
sns.scatterplot(
    x='funding_total_usd',
    y='is_successful',
    data=df,
    alpha=0.3,
    color='blue'
)
plt.xscale('log')
plt.title('Fon Miktarı ve Başarı İlişkisi (Tüm Şirketler)')
plt.xlabel('Fon Miktarı (USD - log scale)')
plt.ylabel('Başarı Durumu (1=Başarılı)')
plt.grid(True, alpha=0.2)

# b) Fon Aralıklarına Göre Başarı Oranları
plt.subplot(1, 2, 2)
df['funding_range'] = pd.cut(
    df['funding_total_usd'],
    bins=[0, 1e5, 1e6, 5e6, 1e7, 5e7, np.inf],
    labels=['<100K', '100K-1M', '1M-5M', '5M-10M', '10M-50M', '50M+']
)
success_by_funding = df.groupby('funding_range')['is_successful'].mean() * 100

sns.barplot(
    x=success_by_funding.index,
    y=success_by_funding.values,
    palette='viridis',
    edgecolor='black'
)
plt.title('Fon Aralığına Göre Başarı Oranları')
plt.xlabel('Fon Miktarı Aralığı')
plt.ylabel('Başarı Oranı (%)')
plt.xticks(rotation=45)
plt.ylim(0, 100)

# Değer etiketleri
for i, v in enumerate(success_by_funding.values):
    plt.text(i, v + 2, f"{v:.1f}%", ha='center')

plt.tight_layout()
plt.show()

# 3. İstatistiksel Test (Opsiyonel)
from scipy.stats import ttest_ind

successful = df[df['is_successful'] == 1]['funding_total_usd']
unsuccessful = df[df['is_successful'] == 0]['funding_total_usd']

t_stat, p_value = ttest_ind(successful, unsuccessful, equal_var=False)
print("\n═"*50)
print("İSTATİSTİKSEL TEST SONUCU".center(50))
print("═"*50)
print(f"Başarılı şirketlerin ortalama fonu: ${successful.mean():,.0f}")
print(f"Başarısız şirketlerin ortalama fonu: ${unsuccessful.mean():,.0f}")
print(f"t-istatistiği: {t_stat:.2f}, p-değeri: {p_value:.4f}")
if p_value < 0.05:
    print("Sonuç: Başarılı ve başarısız şirketlerin fon miktarları arasında istatistiksel olarak anlamlı fark var.")
else:
    print("Sonuç: Anlamlı fark yok.")
