import streamlit as st
import pandas as pd
from datetime import datetime

def process_data(df_all_original):
    df_2023 = df_all_original.copy()
    # Drop unnecessary columns
    columns_to_drop = ['Unnamed: 0', 'Placement Code', 'Placement Date', 'Purchase Order Number', 'Invoice Number',
                       'Client Document Status', 'Publication Station', 'Placement Status', 'RateCard Unit Cost Gross Home',
                       'Commitment Disc Home Amount', 'Early Booking Disc Amount', 'Neg Disc Home Amount', 'Other Disc Home Amount',
                       'Added Val Disc Home Amount', 'Surcharge Home Amount', 'Effective Discount Home', 'Commission']
    df_2023 = df_2023.drop(columns=columns_to_drop)

    # Rename columns
    column_mapping = {
        'Placement Month': 'Month',
        'Placement Year': 'Year',
        'Client Name': 'Customer Name',
        'Client Product Name': 'Brand Name',
        'Media Category Name': 'Medium Type',
        'Media Owner': 'Vendor Name',
        'NettHome': 'NTC (LCY)'
    }
    df_2023.rename(columns=column_mapping, inplace=True)

    # Add columns
    df_2023['Year/ Month'] = ''
    df_2023['Market'] = 'RSA'
    df_2023['Currency'] = 'ZAR'

    # Reorder columns
    df_2023 = df_2023[['Customer Name', 'Brand Name', 'Year', 'Month', 'Year/ Month', 'Medium Type', 'Vendor Name', 'NTC (LCY)', 'Market', 'Currency', 'Campaign Name']]

    # Drop rows with missing Customer Name
    df_2023 = df_2023.dropna(subset=['Customer Name'])

    # Convert Year column to integer
    df_2023['Year'] = df_2023['Year'].astype(int)

    # Process Month column
    df_2023['Month'] = df_2023['Month'].apply(lambda x: datetime.strptime(x, '%B').month)
    df_2023['Month'] = df_2023['Month'].apply(lambda x: f'{x:02d}')  # Format month as zero-padded string

    # Combine Year and Month columns
    df_2023['Year/ Month'] = df_2023['Year'].astype(str) + '-' + df_2023['Month'].astype(str)

    # Extract Brand Name
    df_2023['Brand Name'] = df_2023['Brand Name'].apply(lambda x: x.split('-')[0].strip())
    df_2023.loc[df_2023['Brand Name'] == 'CENTRUM 301000746', 'Brand Name'] = 'CENTRUM'

    return df_2023

def main():
    st.title("South Africa Spends Data Processing App")

    # Upload files
    uploaded_all_file = st.file_uploader("Upload South Africa Data File (Excel)", type=["xlsx"])

    if uploaded_all_file:
        # Read the uploaded file into a Pandas DataFrame
        df_all_original = pd.read_excel(uploaded_all_file, header=4)

        # Process the data
        df_all_processed = process_data(df_all_original)

        # Provide a download button for the processed data
        st.markdown("### Download Processed Data")
        st.download_button('Download file', data=df_all_processed.to_csv(index=False), mime='text/csv')

if __name__ == "__main__":
    main()
