import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(r"D:\Car Sales Analysis\Car Sales.xlsx - car_data.csv")

df = df.dropna()

df['Company_cleaned'] = df['Company'].str.lower().str.strip().str.replace(" ", "", regex=False)

df['Price ($)'] = pd.to_numeric(df['Price ($)'], errors='coerce')

avg_price_per_company = df.groupby('Company_cleaned')['Price ($)'].mean().reset_index()

avg_price_per_company = avg_price_per_company.sort_values(by='Price ($)', ascending=False)

st.title('Car Sales Analysis')

st.subheader('Average Price of Models per Company ($)')

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(avg_price_per_company['Company_cleaned'], avg_price_per_company['Price ($)'], color='skyblue')
ax.set_title('Average Price of Models per Company ($)', fontsize=16)
ax.set_xlabel('Company', fontsize=14)
ax.set_ylabel('Average Price per Car ($)', fontsize=14)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

company_names = avg_price_per_company['Company_cleaned'].unique()
selected_company = st.selectbox('Select a Company:', company_names)

avg_price_per_model = df.groupby(['Company_cleaned', 'Model'])['Price ($)'].mean().reset_index()

filtered_data = avg_price_per_model[avg_price_per_model['Company_cleaned'] == selected_company]

st.subheader(f'Average Prices of Models for {selected_company.capitalize()}:')
st.dataframe(filtered_data)

fig_model, ax_model = plt.subplots(figsize=(12, 6))
bars_model = ax_model.bar(filtered_data['Model'], filtered_data['Price ($)'], color='skyblue')
ax_model.set_title(f'Average Prices of Models for {selected_company.capitalize()} ($)', fontsize=16)
ax_model.set_xlabel('Model', fontsize=14)
ax_model.set_ylabel('Average Price per Model ($)', fontsize=14)
ax_model.tick_params(axis='x', rotation=45)
ax_model.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars_model:
    yval = bar.get_height()
    ax_model.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

if selected_company == 'ford':
    windstar_price = filtered_data.loc[filtered_data['Model'].str.lower() == 'windstar', 'Price ($)']
    if not windstar_price.empty:
        windstar_value = windstar_price.values[0]
        st.markdown(f"**Average Price of Ford Windstar:** ${windstar_value:.2f}")

st.pyplot(fig_model)

if selected_company == 'ford':
    windstar_sales_data = df[df['Company_cleaned'] == 'ford']
    windstar_sales_data = windstar_sales_data[windstar_sales_data['Model'].str.lower() == 'windstar']

    total_windstar_sales = windstar_sales_data['Price ($)'].sum()

    st.subheader('Total Sales Volume for Ford Windstar ($):')
    st.markdown(f"${total_windstar_sales:.2f}")

    fig_windstar_sales, ax_windstar_sales = plt.subplots(figsize=(6, 6))
    ax_windstar_sales.bar('Windstar', total_windstar_sales, color='lightcoral')
    ax_windstar_sales.set_title('Total Sales Volume for Ford Windstar ($)', fontsize=16)
    ax_windstar_sales.set_ylabel('Total Sales Volume ($)', fontsize=14)
    ax_windstar_sales.grid(axis='y', linestyle='--', alpha=0.7)

    ax_windstar_sales.text(0, total_windstar_sales, f'{total_windstar_sales:.2f}', ha='center', va='bottom', fontsize=10)

    st.pyplot(fig_windstar_sales)

    avg_price = 23682.84
    recommended_price = 26170.83

    revenue_avg = avg_price * len(windstar_sales_data)
    estimated_profit_avg = revenue_avg * 0.2

    revenue_rec = recommended_price * len(windstar_sales_data)
    estimated_profit_rec = revenue_rec * 0.2

    profit_increase = estimated_profit_rec - estimated_profit_avg
    revenue_increase = revenue_rec - revenue_avg

    st.subheader('Profit and Revenue Comparison for Windstar:')
    st.markdown(f"Using average price of ${avg_price:.2f}:")
    st.markdown(f"  - Revenue: ${revenue_avg:.2f}")
    st.markdown(f"  - Estimated Profit: ${estimated_profit_avg:.2f}")
    st.markdown(f"Using recommended price of ${recommended_price:.2f}:")
    st.markdown(f"  - Revenue: ${revenue_rec:.2f} (Updated from $2.8 million to $3.1 million)")
    st.markdown(f"  - Estimated Profit: ${estimated_profit_rec:.2f}")
    st.markdown(f"\nProfit increase with recommended price: ${profit_increase:.2f}")
    st.markdown(f"Revenue increase with recommended price: ${revenue_increase:.2f}")

    all_models_sales_data = df[df['Company_cleaned'] == selected_company].groupby('Model')['Price ($)'].sum().reset_index()
    all_models_sales_data['Revenue'] = all_models_sales_data['Price ($)']

    all_models_sales_data.loc[all_models_sales_data['Model'].str.lower() == 'windstar', 'Revenue'] = revenue_rec

    fig_total_sales_volume, ax_total_sales_volume = plt.subplots(figsize=(12, 6))
    ax_total_sales_volume.bar(all_models_sales_data['Model'], all_models_sales_data['Revenue'], color='skyblue')
    ax_total_sales_volume.set_title('Total Sales Volume of All Models ($)', fontsize=16)
    ax_total_sales_volume.set_ylabel('Total Sales Volume ($)', fontsize=14)
    ax_total_sales_volume.grid(axis='y', linestyle='--', alpha=0.7)

    for i in range(len(all_models_sales_data)):
        ax_total_sales_volume.text(i, all_models_sales_data['Revenue'].values[i],
                                   f'{all_models_sales_data["Revenue"].values[i]:.2f}',
                                   ha='center', va='bottom', fontsize=10)

    st.pyplot(fig_total_sales_volume)

    fig_windstar_total_sales, ax_windstar_total_sales = plt.subplots(figsize=(6, 6))
    ax_windstar_total_sales.bar('Windstar', total_windstar_sales, color='lightcoral')
    ax_windstar_total_sales.set_title('Total Sales Volume for Ford Windstar ($)', fontsize=16)
    ax_windstar_total_sales.set_ylabel('Total Sales Volume ($)', fontsize=14)
    ax_windstar_total_sales.grid(axis='y', linestyle='--', alpha=0.7)

    ax_windstar_total_sales.text(0, total_windstar_sales, f'{total_windstar_sales:.2f}', ha='center', va='bottom', fontsize=10)

    st.pyplot(fig_windstar_total_sales)
