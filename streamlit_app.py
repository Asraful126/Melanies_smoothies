# Import python packages
import streamlit as st
# load column package
from snowflake.snowpark.functions import col;

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!
    """)
# Enter customer name
name_on_order = st.text_input("Name on Smootie: ")
st.write("The name on your smoothie will be:", name_on_order)


# Adding Interactive Elements
# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"))

# st.write("Your favourite fruit is:", option)

# session = get_active_session()
# my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
# st.dataframe(data=my_dataframe, use_container_width=True)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients: '
                                  , my_dataframe
                                 , max_selections = 5)

# write the list back on the screen
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        

    # st.write(ingredients_string)
    my_insert_stmt = """ 
        insert into SMOOTHIES.PUBLIC.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """') """
    st.write(my_insert_stmt)
    # st.stop()

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fdc.nal.usda.gov/fdc-app.html#/food-search?query=banana")
st.text(fruityvice_response.json())











