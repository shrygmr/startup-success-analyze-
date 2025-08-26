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
