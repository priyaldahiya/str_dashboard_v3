# app.py
import streamlit as st
import os
from app_fxns import *
import datetime
import plotly.express as px

airbnb_path = 'airbnb_.csv'

st.header('Short Term Rental Dashboard 3')

col1, col2, col3 = st.columns(3)

platform = st.sidebar.selectbox('Select a platform', ['ALL'] + list(['Airbnb', 'VRBO']))
if platform == 'Airbnb':
    df = pull_airbnb_data(airbnb_path)
    df = clean_airbnb_data(df)
else:
    st.write('No VRBO data, displaying Airbnb data only')
    df = pull_airbnb_data(airbnb_path)
    df = clean_airbnb_data(df)

start_date = col1.date_input("Select Start Date", datetime.date.today() - datetime.timedelta(days=365))
end_date = col2.date_input("Select End Date", datetime.date.today())
dated_df = date_filtering(df, start_date, end_date)

listing = col3.selectbox('Choose listing:', ['ALL'] + list(dated_df['Listing'].unique()))
filtered_df = filter_airbnb_data('Listing', listing, dated_df)

filtered_df = create_lead_times_column(filtered_df)

monthly_kpis_df = monthly_kpis(filtered_df)

columns_to_exclude = ['Earnings year', 'Month', 'Date', 'Host service fee', 'Cleaning fee', 'Occupancy taxes']
remaining_columns = [col for col in monthly_kpis_df.columns if col not in columns_to_exclude]
# st.write(remaining_columns)

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Nights', 'Lead time',
                                        'Gross earning','Pet fee',
                                        'Avg nightly price'])

tab1.write(generate_plots(monthly_kpis_df, 'Date', 'Nights'))
tab2.write(generate_plots(monthly_kpis_df, 'Date', 'Lead time'))
tab3.write(generate_plots(monthly_kpis_df, 'Date', 'Gross earnings'))
tab4.write(generate_plots(monthly_kpis_df, 'Date', 'Pet fee'))
tab5.write(generate_plots(monthly_kpis_df, 'Date', 'Avg nightly price'))