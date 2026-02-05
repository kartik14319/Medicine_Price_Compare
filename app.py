# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from serpapi import GoogleSearch
# from dotenv import load_dotenv

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
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API key from environment
API_KEY = os.environ.get("API_KEY")

# Helper to clean price strings
def clean_price(price):
    if not price:
        return None
    price = price.replace("₹", "").replace(",", "").strip()
    try:
        return float(price)
    except ValueError:
        return None

# Function to get Google Shopping results
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

# HEADER
st.image("kartik.webp", width=150)
st.title("E-Pharmacy Price Comparison System")

# SIDEBAR INPUTS
st.sidebar.header("Medicine Input")
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

        # Show all options
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

            st.markdown(f"### Option {i + 1}")
            
            # Stack info vertically for mobile
            st.write(f"**Company:** {item.get('source')}")
            st.write(f"**Title:** {item.get('title')}")
            st.write(f"**Price:** {item.get('price')}")
            st.write(f"**Buy link:** [Link]({item.get('product_link')})")
            st.divider()

        # Show best option
        st.markdown("## ✅ Best Option")
        best = shopping_results[lowest_price_index]
        st.write(f"**Company:** {best.get('source')}")
        st.write(f"**Title:** {best.get('title')}")
        st.write(f"**Price:** {best.get('price')}")
        st.write(f"**Buy link:** [Link]({best.get('product_link')})")

        # PRICE COMPARISON BAR CHART
        st.markdown("## 📊 Price Comparison (Bar Chart)")
        fig, ax = plt.subplots(figsize=(6, 4))  # smaller figsize for mobile
        ax.bar(medicine_comp, med_price, color='skyblue')
        ax.set_xlabel("Company")
        ax.set_ylabel("Price (₹)")
        ax.set_title("Medicine Price Comparison")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        # PIE CHART
        st.markdown("## 🥧 Price Distribution (Pie Chart)")
        fig2, ax2 = plt.subplots(figsize=(5, 5))  # smaller for mobile
        ax2.pie(
            med_price,
            labels=medicine_comp,
            autopct="%1.1f%%",
            startangle=90
        )
        ax2.axis("equal")
        plt.tight_layout()
        st.pyplot(fig2)
