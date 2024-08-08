import sys
from sqlmodel import select
from models import Organization, Board, Task
from database import get_session


def get_current_organization_names():
    with get_session() as session:
        organizations = session.exec(select(Organization)).all()
        return [org.name for org in organizations]


def get_current_board_names():
    with get_session() as session:
        organization = session.exec(select(Organization).where(Organization.is_selected == True)).first()
        if not organization:
            return []
        boards = session.exec(select(Board).where(Board.organization_id == organization.id)).all()
        return [board.name for board in boards]


def get_current_task_names():
    with get_session() as session:
        board = session.exec(select(Board).where(Board.is_selected == True)).first()
        if not board:
            return []
        tasks = session.exec(select(Task).where(Task.board_id == board.id)).all()
        return [task.name for task in tasks]


def main():
    if len(sys.argv) < 2:
        return

    command = sys.argv[1]

    if command == '-o':
        options = get_current_organization_names()
    elif command == '-b':
        options = get_current_board_names()
    elif command == '-t':
        options = get_current_task_names()
    else:
        return

    for option in options:
        print(option)


if __name__ == "__main__":
    main()
