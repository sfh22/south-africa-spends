import streamlit as st
import pandas as pd
import numpy as np
import datetime

def process_data(df_all_original):
    df_2023 = df_all_original.copy()
    df_2023 = df_2023.drop(columns=['Unnamed: 0', 'Placement Code', 'Placement Date', 'Purchase Order Number','Invoice Number','Client Document Status',
                                    'Publication Station','Placement Status','RateCard Unit Cost Gross Home',
                                    'Commitment Disc Home Amount','Early Booking Disc Amount','Neg Disc Home Amount','Other Disc Home Amount',
                                    'Added Val Disc Home Amount','Surcharge Home Amount','Effective Discount Home','Commission'])
    dict = {'Placement Month': 'Month',
            'Placement Year': 'Year',
            'Client Name': 'Customer Name',
            'Client Product Name':'Brand Name',
            'Media Category Name':'Medium Type',
            'Media Owner':'Vendor Name',
            'NettHome':'NTC (LCY)'}

    df_2023.rename(columns=dict,
            inplace=True)


    df_2023.insert(loc=4, column='Year/ Month', value='')
    df_2023.insert(loc=8, column='Market', value='RSA')
    df_2023.insert(loc=9, column='Currency', value='ZAR')

    df_2023 = df_2023[['Customer Name', 'Brand Name', 'Year', 'Month','Year/ Month','Medium Type','Vendor Name','NTC (LCY)','Market','Currency','Campaign Name']]
    df_2023 = df_2023.dropna(0,subset=['Customer Name'])

    df_2023['Year'] = df_2023['Year'].apply(lambda x:int(x))

    for index, row in df_2023.iterrows():
        #print(row['Month'])
        month_int = datetime.strptime(str(row['Month']), '%B').month
        if int(month_int) < 10:
            month_int = '0' + str(month_int)
        
        month_abbr = row['Month'][0:3]
        
        month_combined = str(row['Year']) + '-' + str(month_int) + ' (' + month_abbr + ')'
        
        df_2023['Year/ Month'][index] = month_combined

    def extract_brand(t):
        x = t.find("-")
        if x != -1:
            t = t.split('-')[0].rstrip()
        return t

    df_2023['Brand Name'] = df_2023['Brand Name'].apply(lambda x:extract_brand(x))
    df_2023.loc[df_2023['Brand Name'] == 'CENTRUM 301000746' ,'Brand Name'] = 'CENTRUM'

    return df_2023, 

def main():
    st.title("South Africa Spends Data Processing App")

    # Upload files
    uploaded_all_file = st.file_uploader("Upload South Africa Data File (Excel)", type=["xlsx"])

    if uploaded_all_file:
        # Read the uploaded files into Pandas DataFrames
        df_all_original = pd.read_excel(uploaded_all_file)
        df_all = df_all_original.copy()

        # Process the data
        df_all_processed = process_data(df_all)

        # Provide a download button for the processed data
        st.markdown(f"### Download Processed Data")
        st.download_button('Download file',data=pd.DataFrame.to_csv(df_all_processed,index=False), mime='text/csv')

if __name__ == "__main__":
    main()
