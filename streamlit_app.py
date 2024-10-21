# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session # [removed as advised]
# load column package
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!
    """)
# Enter customer name
# name_on_order = st.text_input("Name on Smootie: ")
st.write("Orders that need to be filled:")


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
# session = get_active_session() # replaced by session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.orders").filter(col("order_filled")==0).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    
    if submitted:
        # st.success('Someone clicked the button', icon='👍')
        og_dataset = session.table("smoothies.public.orders") # original table
        edited_dataset = session.create_dataframe(editable_df) # edited table
    
        try:
            og_dataset.merge(edited_dataset,
            (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']),
            [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success("Order(s) updated!", icon='👍')
        except:
            st.success("Something went wrong")
else:
    st.success("There is no pending order right now", icon='👍')







