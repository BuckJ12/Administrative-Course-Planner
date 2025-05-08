# ChronoSync

**ChronoSync** is a powerful administrative scheduling tool designed to generate optimized academic schedules by balancing instructor availability, room constraints, course demand, and seat allocation. Built with usability and automation in mind, it helps institutions streamline their semester planning process with a single click.

## 🧠 Key Features

- 🗓️ **Automated Scheduling**: Uses Google OR-Tools to create conflict-free schedules.
- 👨‍🏫 **Instructor & Room Availability**: Accounts for specific availability and restrictions.
- 🏛️ **Seat Allocation Management**: Prioritizes maximum seat usage across classrooms.
- 🎓 **Student-centric Planning**: Ensures prerequisite and conflict resolution for student course loads.
- 📊 **Modern Dashboard**: Intuitive frontend for admins and schedulers to visualize and interact with data.

## 🛠️ Tech Stack

- **Frontend**: Vite + React
- **Backend**: Python Flask
- **Database**: MySQL
- **Optimization Engine**: Google OR-Tools

## 📦 Installation

### Prerequisites

- Node.js & npm
- Python 3.10+
- MySQL server
- `pip` for Python package management

### Clone and Setup

```bash
git clone https://github.com/yourusername/chronosync.git
cd chronosync
```

#### Backend Setup

```bash
cd Flask
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
touch .env  # Update MySQL credentials and settings
```

##### ENV

```
        MYSQL_PUBLIC_URL = "mysql+pymysql://username:password@IPADDRESS:PORT/DATABASENAME"
```

#### Frontend Setup

```bash
cd frontend
npm install
```

## Run Website

from the top-level directory
```
npm run start
```


## ⚙️ Usage

1. Open Website
2. Define courses, professors, rooms, and their constraints.
3. Click **"Schedule"** to run the optimization engine.
4. Review the generated timetable.

## 🧪 Development Notes

- OR-Tools is used for solving constraint satisfaction problems.
- Flask handles API routes and connects to the MySQL database.
- React communicates via RESTful endpoints and visualizes scheduling results dynamically.

## 📄 License

MIT License. See `LICENSE` file for details.


