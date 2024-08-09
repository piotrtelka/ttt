from sqlalchemy import text
from sqlmodel import select
from src.models import User


def check_token(session):
    user = session.exec(select(User)).first()
    if not user:
        return None
    return user.trello_token


def obtain_and_save_token(session, api_key):
    print("Please visit the following URL to authorize the application and get the token:")
    auth_url = f"https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key={api_key}"
    print(auth_url)
    token = input("Please enter the token you received: ")
    user = User(trello_token=token)
    session.add(user)
    session.commit()
    print("Token saved successfully.")
    return token

def reset_token(session):
    session.exec(text("DELETE FROM user"))
    session.commit()
    print("Token has been reset.")
