# MEVCUT KODUN SONUNA EKLENECEK EKSTRA ANALİZLER

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load your dataset into df (replace 'your_dataset.csv' with your actual file)
df = pd.read_csv('your_dataset.csv')

# 1. FON TURLARI VE BAŞARI İLİŞKİSİ
print("\n" + "═"*50)
print("FON TURLARI VE BAŞARI İLİŞKİSİ".center(50))
print("═"*50)

funding_round_analysis = df.groupby('funding_rounds').agg(
    success_rate=('is_successful', 'mean'),
    avg_funding=('funding_total_usd', 'mean'),
    company_count=('name', 'count')
).query('company_count > 10')

plt.figure(figsize=(12, 6))
sns.barplot(x=funding_round_analysis.index, 
            y='success_rate', 
            data=funding_round_analysis)
plt.title('Fon Tur Sayısına Göre Başarı Oranları (Min. 10 Şirket)')
plt.xlabel('Fon Tur Sayısı')
plt.ylabel('Başarı Oranı')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.show()

# 2. ÇALIŞAN SAYISI ANALİZİ
print("\n" + "═"*50)
print("ÇALIŞAN SAYISI VE BAŞARI İLİŞKİSİ".center(50))
print("═"*50)

plt.figure(figsize=(14, 6))

# Boxplot
plt.subplot(1, 2, 1)
sns.boxplot(x='is_successful', y='employee_count', data=df, showfliers=False)
plt.title('Çalışan Sayısı Dağılımı')
plt.xlabel('Başarı Durumu')
plt.ylabel('Çalışan Sayısı')
plt.yscale('log')

# Regresyon
plt.subplot(1, 2, 2)
sns.regplot(x='employee_count', y='is_successful', 
           data=df, logistic=True,
           scatter_kws={'alpha':0.3})
plt.title('Çalışan Sayısı-Başarı İlişkisi')
plt.xlabel('Çalışan Sayısı')
plt.ylabel('Başarı Olasılığı')
plt.xscale('log')

plt.tight_layout()
plt.show()

# 3. SEKTÖR-ÜLKE ETKİLEŞİM ANALİZİ
print("\n" + "═"*50)
print("SEKTÖR-ÜLKE ETKİLEŞİM ANALİZİ".center(50))
print("═"*50)

# En az 5 şirket olan sektör-ülke kombinasyonları
sector_country = df.groupby(['primary_category', 'country_code']).agg(
    company_count=('name', 'count'),
    success_rate=('is_successful', 'mean')
).query('company_count >= 5').reset_index()

# En başarılı 10 kombinasyon
top_combinations = sector_country.nlargest(10, 'success_rate')
print("\nEn Başarılı Sektör-Ülke Kombinasyonları:")
print(top_combinations.to_markdown(index=False))

plt.figure(figsize=(12, 8))
sns.barplot(x='success_rate', y='primary_category', hue='country_code',
           data=top_combinations, dodge=False)
plt.title('En Başarılı Sektör-Ülke Kombinasyonları')
plt.xlabel('Başarı Oranı')
plt.ylabel('Sektör')
plt.legend(title='Ülke Kodu', bbox_to_anchor=(1.05, 1))
plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

# 4. ZAMAN İÇİNDE FON TRENDLERİ
print("\n" + "═"*50)
print("ZAMAN İÇİNDE FON TRENDLERİ".center(50))
print("═"*50)

# Kuruluş yılına göre fon trendleri
yearly_funding = df.groupby('founded_year').agg(
    avg_funding=('funding_total_usd', 'mean'),
    company_count=('name', 'count')
).query('company_count >= 5')

plt.figure(figsize=(14, 6))
sns.lineplot(x=yearly_funding.index, y='avg_funding', 
            data=yearly_funding, marker='o')
plt.title('Yıllara Göre Ortalama Fon Miktarı Trendi')
plt.xlabel('Kuruluş Yılı')
plt.ylabel('Ortalama Fon (USD)')
plt.yscale('log')
plt.grid(True, alpha=0.3)
plt.show()

# 5. BAŞARI FAKTÖRLERİ KORELASYON ANALİZİ
print("\n" + "═"*50)
print("BAŞARI FAKTÖRLERİ KORELASYON ANALİZİ".center(50))
print("═"*50)

corr_matrix = df[['is_successful', 'funding_total_usd', 
                 'employee_count', 'funding_rounds']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', 
           fmt='.2f', vmin=-1, vmax=1)
plt.title('Başarı Faktörleri Korelasyon Matrisi')
plt.tight_layout()
plt.show()

# 6. FON SEVİYESİNE GÖRE BAŞARI ORANLARI
print("\n" + "═"*50)
print("FON SEVİYESİNE GÖRE BAŞARI ORANLARI".center(50))
print("═"*50)

df['funding_level'] = pd.qcut(df['funding_total_usd'], q=5, 
                             labels=['Çok Düşük','Düşük','Orta','Yüksek','Çok Yüksek'])

funding_level_success = df.groupby('funding_level')['is_successful'].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x=funding_level_success.index, y=funding_level_success.values)
plt.title('Fon Seviyesine Göre Başarı Oranları')
plt.xlabel('Fon Seviyesi')
plt.ylabel('Başarı Oranı')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.show()

# ANALİZ ÖZETİ
print("\n" + "═"*70)
print("EK ANALİZLER ÖZETİ".center(70))
print("═"*70)
print(f"• En yüksek başarı oranına sahip fon tur sayısı: {funding_round_analysis['success_rate'].idxmax()} (Başarı oranı: {funding_round_analysis['success_rate'].max():.1%})")
print(f"• Çalışan sayısı-medyan başarılı şirket: {df[df['is_successful']==1]['employee_count'].median():.0f} çalışan")
print(f"• En başarılı sektör-ülke kombinasyonu: {top_combinations.iloc[0]['primary_category']}-{top_combinations.iloc[0]['country_code']} (%{top_combinations.iloc[0]['success_rate']*100:.1f} başarı)")
print(f"• Son 5 yılda ortalama fon miktarı değişimi: %{(yearly_funding['avg_funding'].iloc[-1]/yearly_funding['avg_funding'].iloc[-5]-1)*100:.1f}")
print(f"• Başarıyla en yüksek korelasyon: {corr_matrix['is_successful'].drop('is_successful').idxmax()} ({corr_matrix['is_successful'].drop('is_successful').max():.2f})")
print(f"• Çok yüksek fonlu şirketlerin başarı oranı: {funding_level_success.iloc[-1]:.1%}")