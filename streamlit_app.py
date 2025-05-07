# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your Smoothies!
  """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie is:", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
# )

#st.write("You selected:", option)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect ('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingredient_list:
 # st.write (ingredient_list)
 # st.text (ingredient_list)
  ingredient_string = ''
  for fruit_chosen in ingredient_list:
     ingredient_string += fruit_chosen + ' '
  #st.write(ingredient_string)
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
             values ('""" + ingredient_string + """', '""" + name_on_order + """')"""
 #st.write(my_insert_stmt)
 #st.stop()  
  time_to_insert = st.button('Submit Order')   
  if time_to_insert:   
   session.sql(my_insert_stmt).collect()
   st.success('Your Smoothie is ordered!',icon="✅")

#New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

     
