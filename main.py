import argparse
import sys
import readline
from sqlmodel import Session, select
from src.models import Organization, Board, Task
from src.database import create_db_and_tables, get_session
from src.config import load_credentials
from trello import TrelloClient
from src.token_manager import check_token, obtain_and_save_token, reset_token
from src.organization_manager import (
    list_organizations,
    set_current_organization,
    fetch_and_store_data,
    list_boards,
    set_current_board,
    list_tasks,
    set_current_task,
    modify_task_hours, show_current_status
)


def initialize_database():
    create_db_and_tables()


def get_current_organization_names():
    with get_session() as session:
        organizations = session.exec(select(Organization.name)).all()
        return [org.name for org in organizations]


def get_current_board_names():
    with get_session() as session:
        organization = session.exec(select(Organization).where(Organization.is_selected == True)).first()
        if not organization:
            return []
        boards = session.exec(select(Board.name).where(Board.organization_id == organization.id)).all()
        return [board.name for board in boards]


def get_current_task_names():
    with get_session() as session:
        board = session.exec(select(Board).where(Board.is_selected == True)).first()
        if not board:
            return []
        tasks = session.exec(select(Task.name).where(Task.board_id == board.id)).all()
        return [task.name for task in tasks]


def submit_hours_to_trello(session, client):
    task = session.exec(select(Task).where(Task.is_selected == True)).first()
    if not task:
        print("Error: No task is selected.")
        return

    comment = f"Worked {task.hours_worked} hours on this task."
    trello_card = client.get_card(task.trello_id)
    trello_card.comment(comment)
    print(f"Submitted comment to task '{task.name}': {comment}")
    print(f"Link: https://trello.com/c/{task.trello_id}")


def completer(text, state):
    print(text, state)
    options = []
    buffer = readline.get_line_buffer().split()
    print(f"Buffer: {buffer}, Text: {text}")

    if '-o' in buffer:
        options = get_current_organization_names()
    elif '-b' in buffer:
        options = get_current_board_names()
    elif '-t' in buffer:
        options = get_current_task_names()

    matches = [option for option in options if option.startswith(text)]
    print(f"Matches: {matches}")
    return matches[state] if state < len(matches) else None


def main():
    parser = argparse.ArgumentParser(description="Trello Time Tracker (ttt)")
    parser.add_argument('-rt', '--reset-token', action='store_true', help="Reset current token")
    parser.add_argument('-lo', '--list-organizations', action='store_true', help="List organizations")
    parser.add_argument('-o', '--organization', type=str, help="Set currently used organization")
    parser.add_argument('-f', '--fetch', action='store_true', help="Fetch all organizations, boards, and tasks from Trello")
    parser.add_argument('-lb', '--list-boards', action='store_true', help="List all boards in selected organization")
    parser.add_argument('-b', '--board', type=str, help="Set currently used board")
    parser.add_argument('-lt', '--list-tasks', action='store_true', help="List tasks in selected board")
    parser.add_argument('-ltt', '--list-tasks-time', action='store_true', help="List tasks with time worked in selected board")
    parser.add_argument('-t', '--task', type=str, help="Set currently used task")
    parser.add_argument('-s', '--submit', action='store_true', help="Submit hours worked as a comment to the selected task on Trello")
    parser.add_argument('hours', nargs='?', type=str, help="Modify hours of the current task (e.g., +10 to add 10 hours, -5 to subtract 5 hours)")
    args = parser.parse_args()

    credentials = load_credentials()

    # Initialize the database
    initialize_database()

    with get_session() as session:
        if args.reset_token:
            reset_token(session)
            sys.exit(0)

        trello_token = check_token(session)

        if trello_token is None:
            trello_token = obtain_and_save_token(session, credentials.trello_api_key)

        client = TrelloClient(
            api_key=credentials.trello_api_key,
            api_secret=credentials.trello_api_secret,
            token=trello_token
        )

        if args.list_organizations:
            organizations = list_organizations(client)
            for org in organizations:
                print(org.name)
            sys.exit(0)

        if args.organization:
            set_current_organization(session, args.organization)
            sys.exit(0)

        if args.fetch:
            fetch_and_store_data(client, session)
            sys.exit(0)

        if args.list_boards:
            list_boards(session)
            sys.exit(0)

        if args.board:
            set_current_board(session, args.board)
            sys.exit(0)

        if args.list_tasks:
            list_tasks(session)
            sys.exit(0)

        if args.list_tasks_time:
            list_tasks(session, show_time=True, worked=True)
            sys.exit(0)

        if args.task:
            set_current_task(session, args.task)
            sys.exit(0)

        if args.hours:
            try:
                hours = int(args.hours)
                modify_task_hours(session, hours)
            except ValueError:
                print("Error: Hours must be a valid integer, prefixed with '+' or '-'.")
            sys.exit(0)

        if args.submit:
            submit_hours_to_trello(session, client)
            sys.exit(0)

        # If no arguments are provided, show the current status
        show_current_status(client, session)


if __name__ == "__main__":
    main()

