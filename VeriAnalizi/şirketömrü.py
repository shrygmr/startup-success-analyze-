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