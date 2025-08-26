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