# # from streamlit_authenticator import Hasher
# import streamlit_authenticator as stauth
# from pathlib import Path
# import pickle

# hashed_passwords = stauth.Hasher(['admin', 'admin']).generate()
# file_pth = Path(__file__).parent / 'hashed_pw.pkl'
# with file_pth.open('wb') as file:
#     pickle.dump(hashed_passwords,file)
# print(hashed_passwords)