import streamlit as st
from duckduckgo_search import DDGS

st.title("🛒 ShopSmart AI - E-commerce Agent")
st.write("Finds, compares & recommends the best buy instantly!")

query = st.text_input("Enter the product you want to search:")

if query:
    st.subheader(f"🔎 Searching for: {query}")
    
    products = []
    with DDGS() as ddgs:
        # force results to English + set region to India (or US if you prefer)
        for r in ddgs.text(
            query + " buy online price",
            region="in-en",   # India English (use "us-en" for US English)
            safesearch="Moderate",
            max_results=5
        ):
            title = r.get("title")
            link = r.get("href")
            snippet = r.get("body")
            products.append((title, snippet, link))
    
    if products:
        st.subheader("📊 Product Comparison")
        st.table(products)

        # Best pick = first search result
        best_product = products[0]
        st.success(f"✅ Best Buy Suggestion: {best_product[0]}")
        st.markdown(f"[Check it out here]({best_product[2]})")
    else:
        st.error("No products found. Try another search.")
