# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched
import pandas as pd

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the friuts you want in your custom smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe,
                                 max_selections = 5)

if ingredients_list:
    ingredients_string = ''

    for chosen_fruits in ingredients_list:
        ingredients_string += chosen_fruits + ' '
        st.subheader(chosen_fruits + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + chosen_fruits)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit order')
    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




