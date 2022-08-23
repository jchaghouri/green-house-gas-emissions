import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import sklearn
import streamlit as st
import pandas as pd

import streamlit as st

@st.cache
def read_csv(path):
    return pd.read_csv(path)

filename = 'greenhouse_gas_inventory_data_data.csv'
df = read_csv(filename)

table = pd.pivot_table(df, values='value', index=['country_or_area', 'year'], columns=['category'])
gasnames = table.columns.values
#st.write(df.head)



by_category  = df.groupby(['category'])
category_count = by_category.count()
strp = category_count.index

new_category_index = []
for string in strp:
    p = len(string)
    pos = string.find("_in_kilotonne_co2_equivalent",0,p)
    string = string[:pos]
    new_category_index.append(string)
    
new_category_index_reborn = []
for lingo in new_category_index:
    q = len(lingo)
    pos = lingo.find("_without",0,p)
    lingo = lingo[:pos]
    new_category_index_reborn.append(lingo)
    
short_category = ["co2","ghg(indirect co2)","ghg","hfc","ch4","nf3","n2o","pfc","sf6","hfc+pfc"]

category_count["Shorted_category"] = short_category

trying_emission = df

replaced_emission = trying_emission.replace(to_replace=["carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_"
                                     "forestry_lulucf_in_kilotonne_co2_equivalent","greenhouse_gas_ghgs_emissions_including_indirect_co2"
                                    "_without_lulucf_in_kilotonne_co2_equivalent","greenhouse_gas_ghgs_emissions_without_land_use_land_use"
                                    "_change_and_forestry_lulucf_in_kilotonne_co2_equivalent","hydrofluorocarbons_hfcs_emissions_in_kilotonne_co2_equivalent",
                                    "methane_ch4_emissions_without_land_use_land_use_change"
                                    "_and_forestry_lulucf_in_kilotonne_co2_equivalent","nitrogen_trifluoride_nf3_emissions_in_kilotonne_co2_equivalent",
                                    "nitrous_oxide_n2o_emissions_without_land_use_land_use_change" 
                                    "_and_forestry_lulucf_in_kilotonne_co2_equivalent","perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent",
                                    "sulphur_hexafluoride_sf6_emissions_in_kilotonne_co2_equivalent",
                                    "unspecified_mix_of_hydrofluorocarbons_hfcs_and_perfluorocarbons"
                                    "_pfcs_emissions_in_kilotonne_co2_equivalent"], value = ["CO2","GHG(Indirect CO2)","GHG","HFC","CH4","NF3","N2O","PFC","SF6","HFC+PFC"])

data_div = pd.pivot_table(replaced_emission,values="value",index = ["country_or_area", "year"],columns = ["category"])
gases = data_div.columns.values
print(gases)









def country_plot(nameOfCountry):
    data = table.loc[nameOfCountry]
    plt.figure(figsize=(20,20))
    plt.plot(data)
    plt.yscale('log')
    plt.xlabel('Years',size=25)
    plt.ylabel('Emissions (KtCO2e)',size=25)
    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.legend(gases,prop={'size': 15})
    plt.title(nameOfCountry,size=25)
   

st.set_option('deprecation.showPyplotGlobalUse', False)
#Add sidebar to the app
st.sidebar.markdown("### Green House Gas Visualization")
st.sidebar.markdown("Welcome to my Green House Gas Data Visualization. This app is built using streamlit and uses data from the United Nations on the UNData site. I downloaded the data here: <https://www.kaggle.com/datasets/unitednations/international-greenhouse-gas-emissions> ")
st.sidebar.markdown(" ")


#Add title and subtitle to the main interface of the app
st.title("Green House Gasses")

st.markdown("The Greenhouse Gas (GHG) Inventory Data covers the gasses emitted resulting from human activities between 1990 to 2015.")
st.markdown("  ")
st.markdown("The x axis in the plot below is the years from 1990 to 2015.")
st.markdown("The y axis in the plot below is the measured emissions in kilotonnes of carbon dioxide equivalent (KtCO2e). The y axis is also in log scale so the data can be interreted more accurately.")
st.markdown("Read more about the data and how GHG emissions are measured [here](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/EN.ATM.CO2E.KT#:~:text=The%20unit%20of%20measurement%20is,to%20that%20of%20carbon%20dioxide).")



labels = df['country_or_area'].unique()
print(labels)
nameOfCountry = labels



country_selected = st.selectbox("Choose a country",nameOfCountry)


fig = country_plot(country_selected) 

st.pyplot(fig)
 