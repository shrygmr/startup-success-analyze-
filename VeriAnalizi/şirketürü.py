import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Veri setini yükleme
df = pd.read_csv('cleaned_funding2_dataset.csv')

# 1. Fon Miktarlarına Göre Temel Analiz
print("\nFon Miktarı İstatistikleri:")
print(df['funding_total_usd'].describe())

# 2. En Yüksek Fon Alan 20 Şirket
top_funded = df.nlargest(20, 'funding_total_usd')[['name', 'funding_total_usd', 'status', 'category_list']]
print("\nEn Yüksek Fon Alan 20 Şirket:")
print(top_funded)

# 3. Kategorilere Göre Fon Dağılımı (İlk kategoriyi baz alarak)
df['primary_category'] = df['category_list'].str.split('|').str[0]
category_funding = df.groupby('primary_category')['funding_total_usd'].agg(['sum', 'mean', 'count']).nlargest(20, 'sum')
category_funding = category_funding.rename(columns={'sum': 'total_funding', 'mean': 'avg_funding', 'count': 'company_count'})

# 4. Başarılı Sektörlerin Belirlenmesi (Operating/Closed oranına göre)
operating_companies = df[df['status'] == 'operating'].groupby('primary_category').size()
closed_companies = df[df['status'] == 'closed'].groupby('primary_category').size()
success_ratio = (operating_companies / closed_companies).sort_values(ascending=False).dropna()
success_ratio = success_ratio[success_ratio.index.isin(category_funding.index)]

# GRAFİK 1: Kategorilere Göre Toplam Fon Dağılımı (Aynı grafik)
plt.figure(figsize=(14, 8))
sns.barplot(x=category_funding['total_funding'], y=category_funding.index, palette='viridis')
plt.title('Kategorilere Göre Toplam Fon Dağılımı (Top 20)')
plt.xlabel('Toplam Fon Miktarı (USD)')
plt.ylabel('Kategori')
plt.xscale('log')  # Log scale for better visualization
plt.grid(True, which="both", ls="--", axis='x')
plt.tight_layout()
plt.show()

# GRAFİK 2: En Başarılı Sektörler (Operating/Closed Oranı)
plt.figure(figsize=(14, 8))
success_ratio.head(20).sort_values().plot(kind='barh', color='green')
plt.title('En Başarılı Sektörler (Operating/Closed Oranı)')
plt.xlabel('Operating/Closed Oranı (Ne kadar yüksekse o kadar başarılı)')
plt.ylabel('Kategori')
plt.grid(True, which="both", ls="--", axis='x')
plt.tight_layout()
plt.show()

# GRAFİK 3: Fon Miktarı ve Başarı Oranı İlişkisi
merged_data = pd.merge(
    category_funding, 
    success_ratio.rename('success_ratio'), 
    left_index=True, 
    right_index=True
)

plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=merged_data,
    x='total_funding',
    y='success_ratio',
    size='company_count',
    sizes=(50, 500),
    hue=merged_data.index,
    palette='tab20',
    alpha=0.7,
    legend=False
)

# En önemli noktaları etiketle
for line in range(0, merged_data.shape[0]):
    plt.text(
        merged_data['total_funding'][line]*1.1, 
        merged_data['success_ratio'][line], 
        merged_data.index[line], 
        horizontalalignment='left', 
        size='medium', 
        color='black'
    )

plt.xscale('log')
plt.title('Fon Miktarı ve Başarı Oranı İlişkisi')
plt.xlabel('Toplam Fon Miktarı (USD, log scale)')
plt.ylabel('Operating/Closed Oranı')
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()
