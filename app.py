import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd

st.set_page_config(page_title="ShopSmart AI", page_icon="🛒", layout="wide")

st.title("🛒 ShopSmart AI - E-commerce Agent")
st.write("Finds, compares & recommends the best buy instantly!")

query = st.text_input("Enter the product you want to search:")

if query:
    st.subheader(f"🔎 Searching for: {query}")
    
    products = []
    with DDGS() as ddgs:
        # Force English results (India region, change to 'us-en' for US)
        for r in ddgs.text(
    query + " buy online price",
    region="us-en",   # US-English
            safesearch="Moderate",
            max_results=5
        ):
            title = r.get("title")
            desc = r.get("body")
            link = r.get("href")
            products.append({"Product": title, "Description": desc, "Link": link})
    
    if products:
        st.subheader("📊 Product Comparison Table")
        df = pd.DataFrame(products)
        st.dataframe(df, use_container_width=True)

        # Best pick = first result
        best_product = products[0]
        st.success(f"✅ Best Buy Suggestion: {best_product['Product']}")
        st.markdown(f"[Check it out here]({best_product['Link']})")
    else:
        st.error("No products found. Try another search.")
