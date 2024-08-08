# Trello Time Tracker (ttt)

Trello Time Tracker (ttt) is a command-line tool designed to track time spent on Trello tasks. It allows you to fetch organizations, boards, and tasks from Trello, set the current organization, board, and task, modify the hours worked on a task, and submit the hours as a comment to Trello.

## Features

- Fetch organizations, boards, and tasks from Trello.
- Set the current organization, board, and task.
- Modify hours worked on a task.
- Submit hours worked as a comment to Trello.
- Bash autocompletion for organizations, boards, and tasks.

## Usage

```bash
ttt [OPTIONS] [HOURS]
```

### Options

- `-rt, --reset-token`:
  Reset the current Trello token.

- `-lo, --list-organizations`:
  List all organizations.

- `-o, --organization <name>`:
  Set the currently used organization.

- `-f, --fetch`:
  Fetch all organizations, boards, and tasks from Trello.

- `-lb, --list-boards`:
  List all boards in the selected organization.

- `-b, --board <name>`:
  Set the currently used board.

- `-lt, --list-tasks`:
  List tasks in the selected board.

- `-t, --task <name>`:
  Set the currently used task.

- `-s, --submit`:
  Submit hours worked as a comment to the selected task on Trello.

- `[HOURS]`:
  Modify hours of the current task (e.g., `+10` to add 10 hours, `-5` to subtract 5 hours).

### Examples

- Set the current organization:
  ```bash
  ttt -o "My Organization"
  ```

- List boards in the current organization:
  ```bash
  ttt -lb
  ```

- Set the current board:
  ```bash
  ttt -b "My Board"
  ```

- List tasks in the current board:
  ```bash
  ttt -lt
  ```

- Set the current task:
  ```bash
  ttt -t "My Task"
  ```

- Add 2 hours to the current task:
  ```bash
  ttt +2
  ```

- Submit hours worked as a comment to Trello:
  ```bash
  ttt -s
  ```

## Installation

### Prerequisites

- Python 3.x
- Pip

### Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Bash Autocompletion

To enable bash autocompletion, run the install script:

```bash
chmod +x install_ttt.sh
./install_ttt.sh
```

This script will:
- Add the directory containing the scripts to your `PATH`.
- Add the source command for the bash completion script to your `.bashrc`.

After running the install script, restart your terminal or run:

```bash
source ~/.bashrc
```

## Configuration

Create a `.env` file in the project directory with your Trello API credentials:

```
TRELLO_API_KEY=your_trello_api_key
TRELLO_API_SECRET=your_trello_api_secret
```

### Obtaining Trello Token

The first time you run the script, it will prompt you to obtain a Trello token. Follow the instructions to authorize the application and store the token in the database.

## Libraries Used

- `sqlmodel`: For database modeling and querying.
- `pydantic`: For settings and validation.
- `py-trello`: For interacting with the Trello API.
- `argparse`: For parsing command-line arguments.
- `readline`: For command-line autocompletion.

## Database

The project uses SQLite for storing the following tables:

- **User**: Stores the Trello token.
- **Organization**: Stores Trello organizations.
- **Board**: Stores Trello boards.
- **Task**: Stores Trello tasks.
