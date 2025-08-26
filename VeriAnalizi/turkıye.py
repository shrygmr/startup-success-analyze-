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