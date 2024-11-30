Project Title
KickDataverse: Football Team Management Application
 
Project Issue / Problem to Be Solved
Managing a football team involves handling large amounts of data about players, matches, team performance, and achievements. Traditional methods like spreadsheets or paper-based records are inefficient, error-prone, and lack real-time collaboration. This application aims to solve these problems by providing a user-friendly platform to organize, update, and retrieve team-related information efficiently.

Current Progress (PDLC: Problem Analysis, Design, etc.)
1. Problem Analysis
•	Identified the need for a central system for managing football team data, such as player records, match schedules, and performance statistics.
•	Determined key user roles and workflows for managers to access and manage data.
2. Design
•	UI/UX: Designed a multi-page Tkinter-based interface for navigation and data entry.
•	Database: Chose sqlite3 for data persistence and designed tables for storing player, match, and team performance data.
3. Implementation
•	Developed core modules for login, registration, CRUD operations, and data visualization.
•	Enabled features like saving, searching, updating, and deleting records for players, matches, and achievements.
4. Testing
•	Validated inputs and tested CRUD operations.
•	Verified that the application behaves correctly for different workflows (e.g., adding a player, editing match schedules).

Project Functions/Features
1.	User Management:
•	Register a football team and login with credentials.
•	Clear input fields after every operation.
2.	Player Management:
•	Add, update, search, and delete player records.
•	Store details like injury status, performance, and other attributes.
3.	Match Management:
•	Schedule upcoming matches with details like opponent, date, and time.
•	Edit or delete scheduled matches.
4.	Team Performance Tracking:
•	Record team performance metrics such as goals scored, shots on target, MVP players, and fouls.
•	Save and retrieve performance records for analysis.
5.	Achievement Recording:
•	Record and manage team achievements, including tournament names and rankings.
6.	News & Records:
•	Add, edit, and delete team news or updates.
•	Display saved news records in a scrollable format.
7.	Data Persistence:
•	All data (players, matches, performance, etc.) is stored in a SQLite database.

Expected Number of Pages
1.	Home Page
2.	Dashboard
3.	Player Management 
4.	Match Management
5.	Team Performance
6.	Achievements
7.	News & Updates

Database Applied
•	Database: SQLite
•	Tables:
•	users (id, team_name, manager_name, password)
•	players (id, name, injury_name, injury_status, performance_status)
•	matches (id, opponent, match_date, match_time)
•	team_performance (id, match_date, stats like goals, shots, MVP)
•	achievements (id, date, tournament_name, rank)
•	news_records (id, subject, content, timestamp)

