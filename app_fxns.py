import pandas as pd
import os
import streamlit as st
from datetime import datetime
import plotly.express as px

def pull_airbnb_data(dir):
    raw_df = pd.read_csv(dir)
    return raw_df

def clean_airbnb_data(df):
    df = df.dropna(subset=['Listing'])
    df = df.drop(columns = ['Arriving by date', 'Currency', 'Paid out', 'Fast pay fee'])
    return df

def filter_airbnb_data(feature, value, df):
    if feature == 'ALL':
        return df
    if value == 'ALL':
        return df
    return df[df[feature] == value]

def date_filtering(df, start_date, end_date):
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    return filtered_df

def create_lead_times_column(df):
    df['Start date'] = pd.to_datetime(df['Start date'])
    df['Booking date'] = pd.to_datetime(df['Booking date'])
    df['Lead time'] = (df['Booking date'] - df['Start date']).dt.days
    df['Lead time'] = df['Lead time'].abs()
    return df

def monthly_kpis(df):
    df['Month'] = df['Start date'].dt.strftime('%B')
    df['Earnings year'] = df['Earnings year'].astype(int)

    result = df.groupby(['Earnings year', 'Month']).agg({
        'Nights': 'sum',
        'Lead time': 'mean',
        'Gross earnings': 'sum',
        'Host service fee': 'sum',
        'Cleaning fee': 'sum',
        'Pet fee': 'sum',
        'Occupancy taxes': 'sum'
    }).reset_index()

    result[['Lead time', 'Nights']] = result[['Lead time', 'Nights']].astype(int)

    month_order = ['January', 'February', 'March', 
                'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 
                'November', 'December']
    result['Month'] = pd.Categorical(result['Month'], categories=month_order, ordered=True)
    result = result.sort_values(by=['Earnings year', 'Month'])

    result['Avg nightly price'] = round((result['Gross earnings'] / result['Nights']),2)

    result['Date'] = pd.to_datetime(result['Earnings year'].astype(str) + ' ' + result['Month'].astype(str), format='%Y %B')

    return result

def generate_plots(df, x, y):
    fig = px.line(df, x=x, y=y, title=y)
    return fig