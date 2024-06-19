import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["Shresth Deorari","Nandini Deorari"]
usernames = ["Shresth_38","Nandini_17"]
passwords = ["13feb2004","17jan2003"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)