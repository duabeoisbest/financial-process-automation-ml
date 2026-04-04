import pandas as pandas
import matplotlib.pyplot as plt
from faker import Faker
import random as random
import numpy as numpy
from datetime import datetime

filename = f"financial_report_{datetime.now().date()}.xlsx"
monthly_summary.to_excel(filename)

fake_data = Faker()

account_types = {'4000': 'Revenue', '5000': 'Expense', '1000': 'Asset', '2000': 'Liability', '3000': 'Equity'}

n_rows = 1000
data = {
    'Date': [fake_data.date_between(start_date='-1y', end_date='today') for _ in range(n_rows)],
    'Account': [random.choice(list(account_types.keys())) for _ in range(n_rows)],
    'Description': [fake_data.sentence() for _ in range(n_rows)],

    'Amount': numpy.random.normal(loc=500, scale=2000, size=n_rows).round(2)
}

df = pandas.DataFrame(data)
df['Account Type'] = df['Account'].map(account_types)
df.to_csv('financial_data.csv', index=False)


print(df.head())

df = pandas.read_csv('financial_data.csv')

df['Date'] = pandas.to_datetime(df['Date'])
df['Profit/Loss'] = df.apply(lambda row: row['Amount'] if row['Account Type'] == 'Revenue' else -row['Amount'] if row['Account Type'] == 'Expense' else 0, axis=1)

df['Month'] = df['Date'].dt.to_period('M')
monthly_summary = df.groupby('Month')['Profit/Loss'].sum().reset_index()

monthly_summary['Revenue_MA'] = monthly_summary['Profit/Loss'].rolling(window=2).mean()

print("Monthly Summary:")
print(monthly_summary)
monthly_summary['Month_Str'] = monthly_summary['Month'].astype(str)
plt.figure(figsize=(10, 6))
monthly_summary["Profit/Loss"].plot()
monthly_summary["Revenue_MA"].plot()
plt.title("Profit/Loss Trend")
plt.xlabel("Month")
plt.ylabel("Value")
plt.xticks(rotation=45)
plt.legend()

plt.savefig("profit_loss_trend.png")

monthly_summary.to_excel('monthly_summary.xlsx', index=False)
print("Report generated: financial_report.xlsx & profit_loss_trend.png")