# %%
# Setting the working directory
import os
os.chdir("C:\\Users\\andre\\Documents\\VICTORIA_DATA_INTERNSHIP\\week_1")

# %%
# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
# reading the file
sales = pd.read_excel("..\\DataSets\\sales_data.xlsx")
sales.head()

# %%
sales.info()

# %%
#converting object data types
sales['Date'] = pd.to_datetime(sales['Date'])
sales['Customer_ID'] = sales['Customer_ID'].astype('string')
sales['Product'] = sales['Product'].astype('string')
sales['Category'] = sales['Category'].astype('string')
sales['Quantity'] = sales['Quantity'].astype('int32')
sales['Price'] = sales['Price'].astype('float32')
sales['Total_Amount'] = sales['Total_Amount'].astype('float32')

# %%
sales.info()

# %%
#Finding duplicated rows
print(sales.duplicated().sum()) # 0 for not duplicated and 1 for duplicated


# %%
# Identyfying missing values
sales.isnull().sum() # 0 for not missing and 1 for missing

# %%
sales.fillna({'Total_Amount': 800}, inplace=True)


# %%
sales.to_excel('sales_data_cleaned.xlsx', sheet_name='sales', index=False)


# %%
# Renaming Total_Amount to Total_Sales in place for better clarity:
sales.rename(columns={'Total_Amount': 'Total_Sales'}, inplace=True)

# %%
# Creating a histogram for the Total_Sales column
plt.figure(figsize=(10, 6))
plt.hist(sales['Total_Sales'], bins=10, color='#031366', alpha=0.85)
plt.xlabel('Total Sales ($)', fontsize=14, color='grey')

#Movinng the y-axis label to the left
ax = plt.gca()
ax.set_ylabel('Frequency', fontsize=14, color='grey', rotation=0)
ax.yaxis.set_label_coords(-0.12, 0.5)  # Move label further left and keep it centered vertically

#plt.grid(axis='y', alpha=0.75)
plt.grid(False)

plt.tight_layout()

ax = plt.gca()
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis='x', colors='grey')
ax.tick_params(axis='y', colors='grey')
plt.show()

# %%
# Summary Statistics using f-string (Formatting Printing)
print(f"Total_Sales : {sales['Total_Sales'].mean():.2f}, {sales['Total_Sales'].median():.2f}, {sales['Total_Sales'].std():.2f}")




# %%
# Creating a correlation matrix

# Step 1: Creating a new column 'Date_ordinal' to Convert 'Date' to ordinal
sales['Date_ordinal'] = pd.to_datetime(sales['Date']).apply(lambda x: x.toordinal())
sales

# Step 2: Select relevant columns
cols = ['Date_ordinal', 'Quantity', 'Price', 'Total_Sales']

# Step 3: Compute the correlation matrix
corr_matrix = sales[cols].corr()

# Step 4: Print the matrix
print(corr_matrix)

# %%
# Create a 'Month' column (set day to 1 for grouping)
sales['Month'] = sales['Date'].values.astype('datetime64[M]')

# Group by 'Month' and sum 'Total_Sales'
monthly_sales = sales.groupby('Month')['Total_Sales'].sum().sort_values(ascending=False)

print(monthly_sales)

# %%
# Trend line plot with annotations

# Importing necessary libraries for plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set global font properties
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'  # Or another built-in font
plt.rcParams['font.size'] = 16  # Set global font size

# Prepare data
ts = sales.set_index('Date')['Total_Sales']
x = ts.index.map(pd.Timestamp.toordinal)
y = ts.values
z = np.polyfit(x, y, 1)
trend_line = np.poly1d(z)


plt.figure(figsize=(12, 6))
#plt.plot(ts.index, y, '--', color='grey', alpha=0.3)

plt.plot(ts.index, y, color='grey', alpha=0.3)

plt.plot(ts.index, trend_line(x), color='#031366', linewidth=3)


plt.title("Sales have declined over time", fontsize=20, color='#820803', y= 1.35)
plt.xlabel("Date", color='grey')
plt.ylabel("Total Sales($)", color='grey', rotation=0, y=1.05) 
plt.legend().set_visible(False)  # Hide legend
#plt.tight_layout()

# Annotate end of "Actual Sales" line, plt.text(x, y, s, ...) places the string s at the coordinates (x, y) on your plot.
plt.text(ts.index[-1], y[-1], ' Actual Sales', color='grey', va='center', fontsize=14) 

# Annotate end of "Trend Line"
plt.text(ts.index[-1], trend_line(x)[-1], ' Trend Sales', color='#031366', va='center', fontsize=14)

ax = plt.gca()
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis='x', colors='grey')
ax.tick_params(axis='y', colors='grey')

# cover the full range of months.
start_month = ts.index.min().replace(day=1)
end_month = ts.index.max().replace(day=1)
months = pd.date_range(start_month, end_month, freq='MS')
month_labels = [d.strftime('%b') for d in months]

# Annotations on the peak dates
peak_jan_date = pd.Timestamp('2024-01-10')
peak_jan_value = sales.loc[sales['Date'] == peak_jan_date, 'Total_Sales'].values[0]

peak_apr_date = pd.Timestamp('2024-04-05')
peak_apr_value = sales.loc[sales['Date'] == peak_apr_date, 'Total_Sales'].values[0]

plt.annotate(
    'January Peak', 
    xy=(peak_jan_date, peak_jan_value),          # point to annotate
    xytext=(peak_jan_date, peak_jan_value + 200),# position for text
    arrowprops=dict(color='grey', arrowstyle='->'),
    fontsize=14,
    color='grey'
)

plt.annotate(
    'April peak', 
    xy=(peak_apr_date, peak_apr_value), 
    xytext=(peak_apr_date, peak_apr_value + 200),
    arrowprops=dict(color='grey', arrowstyle='->'),
    fontsize=14,
    color='grey'
)
 
plt.text(
    0.02, 1.3,  # X and Y position in axes coordinates (0 = left/bottom, 1 = right/top)
    "While there have been occasional peaks, the overall trend in sales has been downward.\n"
    "If we remove these peaks, sales have remained relatively steady.",
    transform=plt.gca().transAxes,  # So coordinates are relative to axes, not data
    fontsize=14,
    color='dimgray',
    verticalalignment='top'
)

plt.xticks(months, month_labels, color='grey')
plt.show()


# %%
# Creating a bar Plot of Total Sales by Category

category_sales = sales.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
category_sales.plot(kind='bar', color='#031366',alpha=0.85)
plt.title('Total Sales by Category', color = 'grey')
plt.ylabel('Total Sales ($)', color = 'grey', rotation = 0, y =1.05)
plt.xlabel(None)
plt.tight_layout()


ax = plt.gca()
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis='x', colors='grey', rotation=0)
ax.tick_params(axis='y', colors='grey')

plt.show()


# %%
# Grouping sales by region and summing Total_Sales
region_sales = sales.groupby('Region', as_index=False)['Total_Sales'].sum()

# Sort regions by sales for better appearance
region_sales_sorted = region_sales.sort_values('Total_Sales', ascending=True)

plt.figure(figsize=(8, 5))
plt.barh(region_sales_sorted['Region'], region_sales_sorted['Total_Sales'], color='#031366',alpha=0.85)
plt.title('Total Sales by Region', fontsize=16, color='grey')
plt.xlabel('Sales', fontsize=14, color='grey')
plt.ylabel(None)

ax = plt.gca()
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis='x', colors='grey')
ax.tick_params(axis='y', colors='grey')

plt.tight_layout()
plt.show()



