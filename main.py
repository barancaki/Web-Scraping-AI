import streamlit as st
from scrape import scrape_the_link, clean_body
from parse import parse_with_ollama

st.title("Web Kazıyıcı Aracına Hoş Geldiniz")

url = st.text_input("Lütfen kazıma yapmak istediğiniz website urlsini giriniz :")

if st.button("Taramaya Başla !"):
    if url:
        st.text("Tarama İşlemi Başlatıldı ...")
        try:
            website_source = scrape_the_link(url)
            cleaned_html = clean_body(website_source)
            st.session_state["cleaned_html"] = cleaned_html  # sonucu session state'e kaydet
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Lütfen geçerli bir URL giriniz!")

if "cleaned_html" in st.session_state:
    with st.expander("Websitesi Temiz Sözdizimi için Tıklayın"):
        st.text_area("Temiz Dizim", st.session_state["cleaned_html"], height=300)

    prompt = st.text_area("Sormak istediğinizi sorun !")
    if st.button("Gönder"):
        if prompt.strip() == "":
            st.warning("Lütfen bir soru yazınız.")
        else:
            st.write("Çözülüyor...")
            response = parse_with_ollama(st.session_state["cleaned_html"], prompt)
            st.write(response)
