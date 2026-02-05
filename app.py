# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# # from serpapi import GoogleSearch
# from dotenv import load_dotenv
# from serpapi import GoogleSearch


# # Load .env file
# load_dotenv()

# # Read API key from environment
# API_KEY = os.environ["API_KEY"]


# def clean_price(price):
#     if not price:
#         return None
#     price = price.replace("₹", "").replace(",", "").strip()
#     try:
#         return float(price)
#     except ValueError:
#         return None


# def compare(med_name):
#     params = {
#         "engine": "google_shopping",
#         "q": med_name,
#         "api_key": API_KEY,
#         "gl": "in"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     return results.get("shopping_results", [])


# c1, c2 = st.columns(2)
# c1.image("kartik.webp", width=200)
# c2.header("E-Pharmacy Price Comparison System")

# st.sidebar.title("Medicine Input")
# med_name = st.sidebar.text_input("Enter medicine name:")
# number = st.sidebar.number_input(
#     "Number of options:", min_value=1, max_value=10, value=3
# )

# medicine_comp = []
# med_price = []

# if st.sidebar.button("Price Compare") and med_name:
#     shopping_results = compare(med_name)

#     if not shopping_results:
#         st.error("No results found.")
#     else:
#         lowest_price = float("inf")
#         lowest_price_index = 0

#         for i in range(min(number, len(shopping_results))):
#             item = shopping_results[i]

#             price = clean_price(item.get("price"))
#             if price is None:
#                 continue

#             medicine_comp.append(item.get("source"))
#             med_price.append(price)

#             if price < lowest_price:
#                 lowest_price = price
#                 lowest_price_index = i

#             st.subheader(f"Option {i + 1}")
#             col1, col2 = st.columns(2)

#             col1.write("Company:")
#             col2.write(item.get("source"))

#             col1.write("Title:")
#             col2.write(item.get("title"))

#             col1.write("Price:")
#             col2.write(item.get("price"))

#             col1.write("Buy link:")
#             col2.write(f"[Link]({item.get('product_link')})")

#             st.divider()

#         st.subheader("✅ Best Option")
#         best = shopping_results[lowest_price_index]
#         col1, col2 = st.columns(2)

#         col1.write("Company:")
#         col2.write(best.get("source"))

#         col1.write("Title:")
#         col2.write(best.get("title"))

#         col1.write("Price:")
#         col2.write(best.get("price"))

#         col1.write("Buy link:")
#         col2.write(f"[Link]({best.get('product_link')})")

#         st.subheader("📊 Price Comparison (Bar Chart)")
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.bar(medicine_comp, med_price)
#         ax.set_xlabel("Company")
#         ax.set_ylabel("Price (₹)")
#         ax.set_title("Medicine Price Comparison")
#         ax.tick_params(axis="x", rotation=45)
#         st.pyplot(fig)

#         st.subheader("🥧 Price Distribution (Pie Chart)")
#         fig2, ax2 = plt.subplots(figsize=(8, 8))
#         ax2.pie(
#             med_price,
#             labels=medicine_comp,
#             autopct="%1.1f%%",
#             startangle=90
#         )
#         ax2.axis("equal")
#         st.pyplot(fig2)



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load .env file
load_dotenv()

# Read API key from environment
API_KEY = os.environ["API_KEY"]

def clean_price(price):
    if not price:
        return None
    price = price.replace("₹", "").replace(",", "").strip()
    try:
        return float(price)
    except ValueError:
        return None

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": API_KEY,
        "gl": "in"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("shopping_results", [])

# Header with image
c1, c2 = st.columns([1, 3])  # Adjust columns proportion for mobile
c1.image("kartik.webp", width=150)  # Use width instead of deprecated use_column_width
c2.header("E-Pharmacy Price Comparison System")

# Sidebar for input
st.sidebar.title("Medicine Input")
med_name = st.sidebar.text_input("Enter medicine name:")
number = st.sidebar.number_input(
    "Number of options:", min_value=1, max_value=10, value=3
)

medicine_comp = []
med_price = []

if st.sidebar.button("Price Compare") and med_name:
    shopping_results = compare(med_name)

    if not shopping_results:
        st.error("No results found.")
    else:
        lowest_price = float("inf")
        lowest_price_index = 0

        for i in range(min(number, len(shopping_results))):
            item = shopping_results[i]

            price = clean_price(item.get("price"))
            if price is None:
                continue

            medicine_comp.append(item.get("source"))
            med_price.append(price)

            if price < lowest_price:
                lowest_price = price
                lowest_price_index = i

            st.subheader(f"Option {i + 1}")
            # Stack vertically on mobile instead of columns
            st.markdown(f"**Company:** {item.get('source')}")
            st.markdown(f"**Title:** {item.get('title')}")
            st.markdown(f"**Price:** {item.get('price')}")
            st.markdown(f"[Buy Link]({item.get('product_link')})")
            st.divider()

        st.subheader("✅ Best Option")
        best = shopping_results[lowest_price_index]
        st.markdown(f"**Company:** {best.get('source')}")
        st.markdown(f"**Title:** {best.get('title')}")
        st.markdown(f"**Price:** {best.get('price')}")
        st.markdown(f"[Buy Link]({best.get('product_link')})")

        st.subheader("📊 Price Comparison (Bar Chart)")
        fig, ax = plt.subplots()
        ax.bar(medicine_comp, med_price, color='skyblue')
        ax.set_xlabel("Company")
        ax.set_ylabel("Price (₹)")
        ax.set_title("Medicine Price Comparison")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig, use_container_width=True)

        st.subheader("🥧 Price Distribution (Pie Chart)")
        fig2, ax2 = plt.subplots()
        ax2.pie(
            med_price,
            labels=medicine_comp,
            autopct="%1.1f%%",
            startangle=90
        )
        ax2.axis("equal")
        st.pyplot(fig2, use_container_width=True)
