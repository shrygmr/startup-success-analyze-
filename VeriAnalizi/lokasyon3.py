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