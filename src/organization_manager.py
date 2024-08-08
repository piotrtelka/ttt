from sqlalchemy import text
from sqlmodel import select, Session
from src.models import Organization, Board, Task
from trello import TrelloClient


def list_organizations(client: TrelloClient):
    organizations = client.list_organizations()
    return organizations


def set_current_organization(session: Session, org_name: str):
    organization = session.exec(select(Organization).where(Organization.name == org_name)).first()
    if organization:
        session.exec(text("UPDATE organization SET is_selected = False WHERE is_selected = True"))
        organization.is_selected = True
        session.add(organization)
        session.commit()
        print(f"Organization '{org_name}' is now the current organization.")
    else:
        print(f"Organization '{org_name}' not found.")


def fetch_and_store_data(client: TrelloClient, session: Session):
    # Fetch organizations
    trello_organizations = client.list_organizations()
    for trello_org in trello_organizations:
        organization = session.exec(select(Organization).where(Organization.trello_id == trello_org.id)).first()
        if organization:
            organization.name = trello_org.name.replace(' ', '_')
            organization.is_selected = False  # Reset selection when fetching data
        else:
            organization = Organization(trello_id=trello_org.id, name=trello_org.name.replace(' ', '_'), is_selected=False)
        session.add(organization)
        session.commit()

        # Fetch boards for each organization
        trello_boards = trello_org.all_boards()
        for trello_board in trello_boards:
            board = session.exec(select(Board).where(Board.trello_id == trello_board.id)).first()
            if board:
                board.name = trello_board.name.replace(' ', '')
                board.organization_id = organization.id
                board.is_selected = False  # Reset selection when fetching data
            else:
                board = Board(trello_id=trello_board.id, name=trello_board.name.replace(' ', '_'), organization_id=organization.id, is_selected=False)
            session.add(board)
            session.commit()

            # Fetch tasks for each board
            trello_tasks = trello_board.all_cards()
            for trello_task in trello_tasks:
                task = session.exec(select(Task).where(Task.trello_id == trello_task.id)).first()
                if task:
                    task.name = trello_task.name.replace(' ', '_')
                    task.board_id = board.id
                    task.is_selected = False  # Reset selection when fetching data
                    task.hours_worked = task.hours_worked  # Assuming hours worked doesn't change from Trello
                else:
                    task = Task(trello_id=trello_task.id, name=trello_task.name.replace(' ', '_'), board_id=board.id, is_selected=False, hours_worked=0)
                session.add(task)
                session.commit()

    print("Fetched and stored all organizations, boards, and tasks.")


def list_boards(session: Session):
    organization = session.exec(select(Organization).where(Organization.is_selected == True)).first()
    if not organization:
        print("Error: No organization is selected.")
        return
    boards = session.exec(select(Board).where(Board.organization_id == organization.id)).all()
    for board in boards:
        print(board.name)

def set_current_board(session: Session, board_name: str):
    organization = session.exec(select(Organization).where(Organization.is_selected == True)).first()
    if not organization:
        print("Error: No organization is selected.")
        return
    board = session.exec(select(Board).where(Board.name == board_name).where(Board.organization_id == organization.id)).first()
    if board:
        session.exec(text("UPDATE board SET is_selected = False WHERE is_selected = True"))
        board.is_selected = True
        session.add(board)
        session.commit()
        print(f"Board '{board_name}' is now the current board.")
    else:
        print(f"Board '{board_name}' not found in the selected organization.")

def list_tasks(session: Session):
    board = session.exec(select(Board).where(Board.is_selected == True)).first()
    if not board:
        print("Error: No board is selected.")
        return
    tasks = session.exec(select(Task).where(Task.board_id == board.id)).all()
    for task in tasks:
        print(task.name)

def set_current_task(session: Session, task_name: str):
    board = session.exec(select(Board).where(Board.is_selected == True)).first()
    if not board:
        print("Error: No board is selected.")
        return
    task = session.exec(select(Task).where(Task.name == task_name).where(Task.board_id == board.id)).first()
    if task:
        session.exec(text("UPDATE task SET is_selected = False WHERE is_selected = True"))
        task.is_selected = True
        session.add(task)
        session.commit()
        print(f"Task '{task_name}' is now the current task.")
    else:
        print(f"Task '{task_name}' not found in the selected board.")

def modify_task_hours(session: Session, hours: int):
    task = session.exec(select(Task).where(Task.is_selected == True)).first()
    if not task:
        print("Error: No task is selected.")
        return
    task.hours_worked += hours
    if task.hours_worked < 0:
        task.hours_worked = 0
    session.add(task)
    session.commit()
    print(f"Task '{task.name}' now has {task.hours_worked} hours worked.")

def show_current_status(session: Session):
    organization = session.exec(select(Organization).where(Organization.is_selected == True)).first()
    board = session.exec(select(Board).where(Board.is_selected == True)).first()
    task = session.exec(select(Task).where(Task.is_selected == True)).first()

    print("Current Status:")
    if organization:
        print(f"Organization: {organization.name}")
    else:
        print("Organization: None")

    if board:
        print(f"Board: {board.name}")
    else:
        print("Board: None")

    if task:
        print(f"Task: {task.name} (Hours worked: {task.hours_worked})")
    else:
        print("Task: None")
