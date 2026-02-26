import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversione da Testo ad Audio")

image = Image.open('PAPI_IS_ANGRY.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Scrivi e/o seleziona un testo per ascoltarlo.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una piccola Favola Bizzarra.")

st.write(
    "«Ah!» disse il topo con tre ombre e nessun corpo. "
    "«Il mondo si sta restringendo come un cervello dimenticato al sole. "
    "All’inizio era infinito, pieno di corridoi che respiravano e porte che sussurravano il mio nome. "
    "Correvo tra pareti di carne e orologi fusi che ticchettavano al contrario. "
    "Ora i muri si stringono come mascelle affamate e il pavimento pulsa sotto le mie zampe.» "
    "Nel fondo della stanza c’era una trappola fatta di specchi. "
    "«Devi solo cambiare direzione» disse il gatto, "
    "un gatto con occhi umani e sorriso cucito. "
    "Il topo cambiò direzione. "
    "La stanza cambiò topo. "
    "E il gatto divorò ciò che rimaneva del silenzio."
)

st.markdown("Vuoi ascoltarla? Copia il testo qui sotto.")

text = st.text_area("Inserisci il testo da ascoltare.")

tld = 'com'

option_lang = st.selectbox(
    "Seleziona la lingua",
    ("Italiano", "English")
)

if option_lang == "Italiano":
    lg = 'it'
elif option_lang == "English":
    lg = 'en'


def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


if st.button("Converti in Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()

    st.markdown("## Il tuo audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Scarica {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="File Audio"), unsafe_allow_html=True)


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
