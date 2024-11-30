import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


users = {}
player_records = []
news_records = []
match_records = []
team_performance_records = []
achievement_records = []


root = tk.Tk()
root.title("KickDataverse Login")
root.geometry("800x600")
root.configure(bg="#f4f4f4")


def clear_entries():
    entry_team_name.delete(0, tk.END)
    entry_manager_name.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def register():
    team_name = entry_team_name.get()
    manager_name = entry_manager_name.get()
    password = entry_password.get()

    if manager_name in users:
        messagebox.showerror("Error", "Manager's name already exists!")
    elif not team_name or not manager_name or not password or len(password) <= 5:
        messagebox.showerror("Error", "All fields are required and password must be more than 5 characters!")
    else:
        users[manager_name] = {"team_name": team_name, "password": password}
        messagebox.showinfo("Success", "Registration successful!")
        clear_entries()


def login():
    manager_name = entry_manager_name.get()
    password = entry_password.get()

    if manager_name in users and users[manager_name]["password"] == password:
        messagebox.showinfo("Success", f"Welcome back, Manager of {users[manager_name]['team_name']}!")
        open_statistics_window()
        clear_entries()
    else:
        messagebox.showerror("Error", "Incorrect manager's name or password!")


def open_statistics_window():
    stats_window = tk.Toplevel(root)
    stats_window.title("KickDataverse")
    stats_window.geometry("800x600")
    stats_window.configure(bg="#f4f4f4")



    header_frame = tk.Frame(stats_window, bg="#333", height=80)
    header_frame.pack(fill="x")

    header_label = tk.Label(
        header_frame, text="KickDataverse", bg="#333", fg="black",
        font=("Arial", 24, "bold")
    )
    header_label.pack(pady=20)


    nav_frame = tk.Frame(stats_window, bg="#444", height=40)
    nav_frame.pack(fill="x")

    def open_news_window():
        news_window = tk.Toplevel(stats_window)
        news_window.title("News")
        news_window.geometry("800x600")
        news_window.configure(bg="#f4f4f4")



        header_label = tk.Label(
            news_window, text="Team News & Records", bg="#333", fg="black",
            font=("Arial", 20, "bold"), pady=10
        )
        header_label.pack(fill="x")


        news_canvas = tk.Canvas(news_window, bg="#f4f4f4")
        news_scrollbar = tk.Scrollbar(news_window, orient="vertical", command=news_canvas.yview)
        news_frame = tk.Frame(news_canvas, bg="#f4f4f4")

        news_frame.bind(
            "<Configure>",
            lambda e: news_canvas.configure(scrollregion=news_canvas.bbox("all"))
        )

        news_canvas.create_window((0, 0), window=news_frame, anchor="nw")
        news_canvas.configure(yscrollcommand=news_scrollbar.set)

        news_canvas.pack(side="left", fill="both", expand=True)
        news_scrollbar.pack(side="right", fill="y")


        subject_label = tk.Label(news_frame, text="Subject:", font=("Arial", 12), bg="#f4f4f4")
        subject_label.pack(anchor="w", pady=(0, 5))
        subject_entry = tk.Entry(news_frame, font=("Arial", 12), width=50)
        subject_entry.pack(fill="x", pady=(0, 10))


        news_text = tk.Text(news_frame, wrap="word", font=("Arial", 12), height=5)
        news_text.pack(fill="x", pady=10)


        def save_news():
            subject = subject_entry.get().strip()
            news_content = news_text.get("1.0", tk.END).strip()
            if subject and news_content:
                timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S")
                news_records.append({"subject": subject, "content": news_content, "timestamp": timestamp})
                messagebox.showinfo("Success", "News/Record saved successfully!")
                display_news()  # Refresh the news display after adding
            else:
                messagebox.showerror("Error", "Subject and content are required!")

        save_button = tk.Button(news_frame, text="Save Record", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=save_news)
        save_button.pack(pady=10)


        def display_news():
            for widget in news_frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget != news_text.master and widget != save_button and widget != subject_entry.master:
                    widget.destroy()

            for idx, record in enumerate(news_records):
                card_frame = tk.Frame(news_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
                card_frame.pack(fill="x", pady=5, expand=True)

                label_date = tk.Label(card_frame, text=record["timestamp"], font=("Arial", 10), fg="#888")
                label_date.pack(anchor="w")

                label_subject = tk.Label(card_frame, text=f"Subject: {record['subject']}", font=("Arial", 14, "bold"), fg="#333")
                label_subject.pack(anchor="w", pady=(5, 0))

                label_content = tk.Label(card_frame, text=record["content"], font=("Arial", 12), fg="#555", wraplength=450, justify="left")
                label_content.pack(anchor="w", pady=(5, 10))

                button_frame = tk.Frame(card_frame, bg="#ffffff")
                button_frame.pack(anchor="w")

                def delete_record(index=idx):
                    del news_records[index]
                    messagebox.showinfo("Deleted", f"Record {index + 1} deleted successfully!")
                    display_news()

                def edit_record(index=idx):
                    subject_entry.delete(0, tk.END)
                    news_text.delete("1.0", tk.END)
                    subject_entry.insert(0, news_records[index]["subject"])
                    news_text.insert("1.0", news_records[index]["content"])
                    save_button.config(text="Update Record", command=lambda: update_news(index))

                delete_button = tk.Button(button_frame, text="Delete", bg="#dc3545", fg="black", font=("Arial", 10), command=delete_record)
                delete_button.pack(side="left", padx=5)

                edit_button = tk.Button(button_frame, text="Edit", bg="#007bff", fg="black", font=("Arial", 10), command=edit_record)
                edit_button.pack(side="left", padx=5)

        def update_news(index):
            updated_subject = subject_entry.get().strip()
            updated_content = news_text.get("1.0", tk.END).strip()
            if updated_subject and updated_content:
                news_records[index]["subject"] = updated_subject
                news_records[index]["content"] = updated_content
                messagebox.showinfo("Success", "News/Record updated successfully!")
                display_news()  # Refresh the news display after updating
                save_button.config(text="Save Record", command=save_news)
            else:
                messagebox.showerror("Error", "Subject and content are required!")

        display_news()

    def open_matches_window():
        matches_window = tk.Toplevel(stats_window)
        matches_window.title("Upcoming Matches")
        matches_window.geometry("800x600")
        matches_window.configure(bg="#f4f4f4")



        header_label = tk.Label(
            matches_window, text="Upcoming Matches", bg="#333", fg="black",
            font=("Arial", 20, "bold"), pady=10
        )
        header_label.pack(fill="x")


        matches_canvas = tk.Canvas(matches_window, bg="#f4f4f4")
        matches_scrollbar = tk.Scrollbar(matches_window, orient="vertical", command=matches_canvas.yview)
        matches_frame = tk.Frame(matches_canvas, bg="#f4f4f4")

        matches_frame.bind(
            "<Configure>",
            lambda e: matches_canvas.configure(scrollregion=matches_canvas.bbox("all"))
        )

        matches_canvas.create_window((0, 0), window=matches_frame, anchor="nw")
        matches_canvas.configure(yscrollcommand=matches_scrollbar.set)

        matches_canvas.pack(side="left", fill="both", expand=True)
        matches_scrollbar.pack(side="right", fill="y")


        match_label = tk.Label(matches_frame, text="Opponent Team:", font=("Arial", 12), bg="#f4f4f4")
        match_label.pack(anchor="w", pady=(0, 5))
        opponent_entry = tk.Entry(matches_frame, font=("Arial", 12), width=50)
        opponent_entry.pack(fill="x", pady=(0, 10))


        date_label = tk.Label(matches_frame, text="Match Date:", font=("Arial", 12), bg="#f4f4f4")
        date_label.pack(anchor="w", pady=(0, 5))
        date_picker = DateEntry(matches_frame, width=16, background='darkblue', foreground='white', date_pattern='dd-mm-yyyy')
        date_picker.pack(fill="x", pady=(0, 10))


        time_label = tk.Label(matches_frame, text="Time (hh:mm AM/PM):", font=("Arial", 12), bg="#f4f4f4")
        time_label.pack(anchor="w", pady=(0, 5))
        time_entry = ttk.Combobox(matches_frame, values=[f"{h:02}:00 AM" for h in range(1, 13)] + [f"{h:02}:30 AM" for h in range(1, 13)] + [f"{h:02}:00 PM" for h in range(1, 13)] + [f"{h:02}:30 PM" for h in range(1, 13)], font=("Arial", 12))
        time_entry.pack(fill="x", pady=(0, 10))


        def save_match():
            opponent = opponent_entry.get().strip()
            match_date = date_picker.get_date()
            match_time = time_entry.get().strip()
            try:
                datetime_obj = datetime.strptime(f"{match_date.strftime('%d-%m-%Y')} {match_time}", "%d-%m-%Y %I:%M %p")
            except ValueError:
                messagebox.showerror("Error", "Invalid date and time format! Use dd-mm-yyyy hh:mm AM/PM")
                return

            if opponent and match_time and datetime_obj > datetime.now():
                match_records.append({"opponent": opponent, "datetime": datetime_obj.strftime("%d %b %Y %I:%M %p")})
                messagebox.showinfo("Success", "Match saved successfully!")
                display_matches()  # Refresh the matches display after adding
            else:
                messagebox.showerror("Error", "Opponent, valid date, and time are required! Date and time must be in the future.")

        save_button = tk.Button(matches_frame, text="Save Match", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=save_match)
        save_button.pack(pady=10)


        def display_matches():
            for widget in matches_frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget != opponent_entry.master and widget != date_picker.master and widget != time_entry.master and widget != save_button:
                    widget.destroy()

            for idx, record in enumerate(match_records):
                card_frame = tk.Frame(matches_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
                card_frame.pack(fill="x", pady=5)

                label_datetime = tk.Label(card_frame, text=record["datetime"], font=("Arial", 10), fg="#888")
                label_datetime.pack(anchor="w")

                label_details = tk.Label(card_frame, text=f"Opponent: {record['opponent']}", font=("Arial", 14, "bold"), fg="#333")
                label_details.pack(anchor="w", pady=(5, 0))

                button_frame = tk.Frame(card_frame, bg="#ffffff")
                button_frame.pack(anchor="w")

                def delete_match(index=idx):
                    del match_records[index]
                    messagebox.showinfo("Deleted", f"Match {index + 1} deleted successfully!")
                    display_matches()

                def edit_match(index=idx):
                    opponent_entry.delete(0, tk.END)
                    time_entry.set(match_records[index]["datetime"].split()[-2] + ' ' + match_records[index]["datetime"].split()[-1])
                    opponent_entry.insert(0, match_records[index]["opponent"])
                    date_picker.set_date(datetime.strptime(match_records[index]["datetime"], "%d %b %Y %I:%M %p"))
                    save_button.config(text="Update Match", command=lambda: update_match(index))

                delete_button = tk.Button(button_frame, text="Delete", bg="#dc3545", fg="black", font=("Arial", 10), command=delete_match)
                delete_button.pack(side="left", pady=(5, 0))

                edit_button = tk.Button(button_frame, text="Edit", bg="#007bff", fg="black", font=("Arial", 10), command=edit_match)
                edit_button.pack(side="left", padx=5)

        def update_match(index):
            updated_opponent = opponent_entry.get().strip()
            updated_date = date_picker.get_date()
            updated_time = time_entry.get().strip()
            try:
                updated_datetime_obj = datetime.strptime(f"{updated_date.strftime('%d-%m-%Y')} {updated_time}", "%d-%m-%Y %I:%M %p")
            except ValueError:
                messagebox.showerror("Error", "Invalid date and time format! Use dd-mm-yyyy hh:mm AM/PM")
                return

            if updated_opponent and updated_time and updated_datetime_obj > datetime.now():
                match_records[index]["opponent"] = updated_opponent
                match_records[index]["datetime"] = updated_datetime_obj.strftime("%d %b %Y %I:%M %p")
                messagebox.showinfo("Success", "Match updated successfully!")
                display_matches()  # Refresh the matches display after updating
                save_button.config(text="Save Match", command=save_match)
            else:
                messagebox.showerror("Error", "Opponent, valid date, and time are required! Date and time must be in the future.")

        display_matches()

    def open_team_performance_window():
        performance_window = tk.Toplevel(stats_window)
        performance_window.title("Team Performance")
        performance_window.geometry("800x600")
        performance_window.configure(bg="#f4f4f4")



        header_label = tk.Label(
            performance_window, text="Team Performance", bg="#333", fg="black",
            font=("Arial", 20, "bold"), pady=10
        )
        header_label.pack(fill="x")


        performance_frame = tk.Frame(performance_window, bg="#f4f4f4")
        performance_frame.pack(pady=20, padx=20, fill="both", expand=True)


        match_date_label = tk.Label(performance_frame, text="Match Date:", font=("Arial", 12), bg="#f4f4f4")
        match_date_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        match_date_entry = tk.Entry(performance_frame, width=30)
        match_date_entry.grid(row=0, column=1, padx=10, pady=5)


        label_opponent_team = tk.Label(performance_frame, text="Opponent Team:", font=("Arial", 12), bg="#f4f4f4")
        label_opponent_team.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_opponent_team = tk.Entry(performance_frame, width=30)
        entry_opponent_team.grid(row=1, column=1, padx=10, pady=5)

        label_goal_scored = tk.Label(performance_frame, text="Goals Scored:", font=("Arial", 12), bg="#f4f4f4")
        label_goal_scored.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_goal_scored = tk.Entry(performance_frame, width=30)
        entry_goal_scored.grid(row=2, column=1, padx=10, pady=5)


        label_goal_conceded = tk.Label(performance_frame, text="Goals Conceded:", font=("Arial", 12), bg="#f4f4f4")
        label_goal_conceded.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        entry_goal_conceded = tk.Entry(performance_frame, width=30)
        entry_goal_conceded.grid(row=3, column=1, padx=10, pady=5)


        label_total_shot = tk.Label(performance_frame, text="Total Shots:", font=("Arial", 12), bg="#f4f4f4")
        label_total_shot.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_total_shot = tk.Entry(performance_frame, width=30)
        entry_total_shot.grid(row=4, column=1, padx=10, pady=5)


        label_shot_on_target = tk.Label(performance_frame, text="Total Shots on Target:", font=("Arial", 12),
                                        bg="#f4f4f4")
        label_shot_on_target.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        entry_shot_on_target = tk.Entry(performance_frame, width=30)
        entry_shot_on_target.grid(row=5, column=1, padx=10, pady=5)


        label_mvp_player = tk.Label(performance_frame, text="MVP Player:", font=("Arial", 12), bg="#f4f4f4")
        label_mvp_player.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        entry_mvp_player = tk.Entry(performance_frame, width=30)
        entry_mvp_player.grid(row=6, column=1, padx=10, pady=5)


        label_yellow_card = tk.Label(performance_frame, text="Yellow Cards:", font=("Arial", 12), bg="#f4f4f4")
        label_yellow_card.grid(row=7, column=0, sticky="e", padx=10, pady=5)
        entry_yellow_card = tk.Entry(performance_frame, width=30)
        entry_yellow_card.grid(row=7, column=1, padx=10, pady=5)

        label_red_card = tk.Label(performance_frame, text="Red Cards:", font=("Arial", 12), bg="#f4f4f4")
        label_red_card.grid(row=8, column=0, sticky="e", padx=10, pady=5)
        entry_red_card = tk.Entry(performance_frame, width=30)
        entry_red_card.grid(row=8, column=1, padx=10, pady=5)


        label_saves = tk.Label(performance_frame, text="Saves:", font=("Arial", 12), bg="#f4f4f4")
        label_saves.grid(row=9, column=0, sticky="e", padx=10, pady=5)
        entry_saves = tk.Entry(performance_frame, width=30)
        entry_saves.grid(row=9, column=1, padx=10, pady=5)


        label_corner_kick = tk.Label(performance_frame, text="Corner Kicks:", font=("Arial", 12), bg="#f4f4f4")
        label_corner_kick.grid(row=10, column=0, sticky="e", padx=10, pady=5)
        entry_corner_kick = tk.Entry(performance_frame, width=30)
        entry_corner_kick.grid(row=10, column=1, padx=10, pady=5)


        label_offside = tk.Label(performance_frame, text="Offsides:", font=("Arial", 12), bg="#f4f4f4")
        label_offside.grid(row=11, column=0, sticky="e", padx=10, pady=5)
        entry_offside = tk.Entry(performance_frame, width=30)
        entry_offside.grid(row=11, column=1, padx=10, pady=5)

        def save_performance():
            performance_data = {
                "match_date": match_date_entry.get(),
                "opponent_team": entry_opponent_team.get(),
                "goal_scored": entry_goal_scored.get(),
                "goal_conceded": entry_goal_conceded.get(),
                "total_shot": entry_total_shot.get(),
                "shot_on_target": entry_shot_on_target.get(),
                "mvp_player": entry_mvp_player.get(),
                "yellow_card": entry_yellow_card.get(),
                "red_card": entry_red_card.get(),
                "saves": entry_saves.get(),
                "corner_kick": entry_corner_kick.get(),
                "offside": entry_offside.get(),
            }
            team_performance_records.append(performance_data)
            messagebox.showinfo("Success", "Team performance record saved successfully!")

        save_button = tk.Button(performance_frame, text="Save Performance", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=save_performance)
        save_button.grid(row=12, column=0, columnspan=2, pady=20)

    def open_achievement_window():
        achievement_window = tk.Toplevel(stats_window)
        achievement_window.title("Achievements")
        achievement_window.geometry("800x600")
        achievement_window.configure(bg="#f4f4f4")


        # Header
        header_label = tk.Label(
            achievement_window, text="Team Achievements", bg="#333", fg="black",
            font=("Arial", 20, "bold"), pady=10
        )
        header_label.pack(fill="x")

        achievement_canvas = tk.Canvas(achievement_window, bg="#f4f4f4")
        achievement_scrollbar = tk.Scrollbar(achievement_window, orient="vertical", command=achievement_canvas.yview)
        achievement_frame = tk.Frame(achievement_canvas, bg="#f4f4f4")

        achievement_frame.bind(
            "<Configure>",
            lambda e: achievement_canvas.configure(scrollregion=achievement_canvas.bbox("all"))
        )

        achievement_canvas.create_window((0, 0), window=achievement_frame, anchor="nw")
        achievement_canvas.configure(yscrollcommand=achievement_scrollbar.set)

        achievement_canvas.pack(side="left", fill="both", expand=True)
        achievement_scrollbar.pack(side="right", fill="y")


        date_label = tk.Label(achievement_frame, text="Date (dd-mm-yyyy):", font=("Arial", 12), bg="#f4f4f4")
        date_label.pack(anchor="w", pady=(0, 5))
        date_picker = DateEntry(achievement_frame, width=16, background='darkblue', foreground='white', date_pattern='dd-mm-yyyy')
        date_picker.pack(fill="x", pady=(0, 10))

        tournament_label = tk.Label(achievement_frame, text="Tournament Name:", font=("Arial", 12), bg="#f4f4f4")
        tournament_label.pack(anchor="w", pady=(0, 5))
        tournament_entry = tk.Entry(achievement_frame, font=("Arial", 12), width=50)
        tournament_entry.pack(fill="x", pady=(0, 10))

        rank_label = tk.Label(achievement_frame, text="Rank Achieved:", font=("Arial", 12), bg="#f4f4f4")
        rank_label.pack(anchor="w", pady=(0, 5))
        rank_entry = tk.Entry(achievement_frame, font=("Arial", 12), width=50)
        rank_entry.pack(fill="x", pady=(0, 10))


        def save_achievement():
            date = date_picker.get_date()
            tournament_name = tournament_entry.get().strip()
            rank = rank_entry.get().strip()
            if tournament_name and rank:
                achievement_records.append({"date": date.strftime("%d %b %Y"), "tournament": tournament_name, "rank": rank})
                messagebox.showinfo("Success", "Achievement saved successfully!")
                display_achievements()  # Refresh the achievements display after adding
            else:
                messagebox.showerror("Error", "Tournament name and rank are required!")

        save_button = tk.Button(achievement_frame, text="Save Achievement", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=save_achievement)
        save_button.pack(pady=10)


        def display_achievements():
            for widget in achievement_frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget != date_picker.master and widget != tournament_entry.master and widget != rank_entry.master and widget != save_button:
                    widget.destroy()

            for idx, record in enumerate(achievement_records):
                card_frame = tk.Frame(achievement_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
                card_frame.pack(fill="x", pady=5, expand=True)

                label_date = tk.Label(card_frame, text=f"Date: {record['date']}", font=("Arial", 10), fg="#888")
                label_date.pack(anchor="w")

                label_tournament = tk.Label(card_frame, text=f"Tournament: {record['tournament']}", font=("Arial", 14, "bold"), fg="#333")
                label_tournament.pack(anchor="w", pady=(5, 0))

                label_rank = tk.Label(card_frame, text=f"Rank: {record['rank']}", font=("Arial", 12), fg="#555")
                label_rank.pack(anchor="w", pady=(5, 10))

                button_frame = tk.Frame(card_frame, bg="#ffffff")
                button_frame.pack(anchor="w")

                def delete_achievement(index=idx):
                    del achievement_records[index]
                    messagebox.showinfo("Deleted", f"Achievement {index + 1} deleted successfully!")
                    display_achievements()

                def edit_achievement(index=idx):
                    tournament_entry.delete(0, tk.END)
                    rank_entry.delete(0, tk.END)
                    tournament_entry.insert(0, achievement_records[index]["tournament"])
                    rank_entry.insert(0, achievement_records[index]["rank"])
                    date_picker.set_date(datetime.strptime(achievement_records[index]["date"], "%d %b %Y"))
                    save_button.config(text="Update Achievement", command=lambda: update_achievement(index))

                delete_button = tk.Button(button_frame, text="Delete", bg="#dc3545", fg="black", font=("Arial", 10), command=delete_achievement)
                delete_button.pack(side="left", padx=5)

                edit_button = tk.Button(button_frame, text="Edit", bg="#007bff", fg="black", font=("Arial", 10), command=edit_achievement)
                edit_button.pack(side="left", padx=5)

        def update_achievement(index):
            updated_tournament = tournament_entry.get().strip()
            updated_rank = rank_entry.get().strip()
            updated_date = date_picker.get_date()
            if updated_tournament and updated_rank:
                achievement_records[index]["tournament"] = updated_tournament
                achievement_records[index]["rank"] = updated_rank
                achievement_records[index]["date"] = updated_date.strftime("%d %b %Y")
                messagebox.showinfo("Success", "Achievement updated successfully!")
                display_achievements()  # Refresh the achievements display after updating
                save_button.config(text="Save Achievement", command=save_achievement)
            else:
                messagebox.showerror("Error", "Tournament name and rank are required!")

        display_achievements()

    exit_button = tk.Button(stats_window, text="Exit Application", bg="#dc3545", fg="black", font=("Arial", 12, "bold"),
                            command=stats_window.quit)
    exit_button.pack(pady=10, side="bottom")
    nav_buttons = ["Team Performance", "Players", "Matches", "News", "Achievements"]
    for btn in nav_buttons:
        tk.Button(
            nav_frame, text=btn, bg="#555", fg="black", font=("Arial", 12, "bold"),
            borderwidth=0, padx=20, pady=5, command=lambda b=btn: open_player_management_window() if b == "Players" else open_news_window() if b == "News" else open_matches_window() if b == "Matches" else open_team_performance_window() if b == "Team Performance" else open_achievement_window() if b == "Achievements" else None
        ).pack(side="left", padx=10)

    # Main content
    main_frame = tk.Frame(stats_window, bg="#f4f4f4")
    main_frame.pack(expand=True, fill="both", pady=20)

    welcome_label = tk.Label(
        main_frame, text="Welcome to KickDataverse", bg="#f4f4f4",
        fg="#333", font=("Arial", 18, "bold")
    )
    welcome_label.pack(pady=20)

    info_label = tk.Label(
        main_frame, text="Discover the latest stats, players, teams, and match results!",
        bg="#f4f4f4", fg="#555", font=("Arial", 14)
    )
    info_label.pack(pady=10)


    footer_frame = tk.Frame(stats_window, bg="#333", height=40)
    footer_frame.pack(fill="x")

    footer_label = tk.Label(
        footer_frame, text="© 2024 KickDataverse App", bg="#333",
        fg="black", font=("Arial", 10)
    )
    footer_label.pack(pady=10)


def open_player_management_window():
    player_window = tk.Toplevel(root)
    player_window.title("Player Management")
    player_window.geometry("600x700")
    player_window.configure(bg="#f4f4f4")


    header_label = tk.Label(
        player_window, text="Player Management", bg="#333", fg="black",
        font=("Arial", 20, "bold"), pady=10
    )
    header_label.pack(fill="x")


    player_frame = tk.Frame(player_window, bg="#f4f4f4")
    player_frame.pack(pady=20)


    label_player_name = tk.Label(player_frame, text="Player Name:", bg="#f4f4f4", font=("Arial", 12))
    label_player_name.grid(row=0, column=0, sticky="e", padx=10, pady=5)
    entry_player_name = tk.Entry(player_frame, width=30)
    entry_player_name.grid(row=0, column=1, padx=10, pady=5)


    label_injury_name = tk.Label(player_frame, text="Injury Name:", bg="#f4f4f4", font=("Arial", 12))
    label_injury_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_injury_name = tk.Entry(player_frame, width=30)
    entry_injury_name.grid(row=1, column=1, padx=10, pady=5)


    label_injury_status = tk.Label(player_frame, text="Injury Status (Yes/No):", bg="#f4f4f4", font=("Arial", 12))
    label_injury_status.grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_injury_status = tk.Entry(player_frame, width=30)
    entry_injury_status.grid(row=2, column=1, padx=10, pady=5)


    label_low_performance = tk.Label(player_frame, text="Low Performance (Yes/No):", bg="#f4f4f4", font=("Arial", 12))
    label_low_performance.grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entry_low_performance = tk.Entry(player_frame, width=30)
    entry_low_performance.grid(row=3, column=1, padx=10, pady=5)


    label_high_performance = tk.Label(player_frame, text="High Performance (Yes/No):", bg="#f4f4f4", font=("Arial", 12))
    label_high_performance.grid(row=4, column=0, sticky="e", padx=10, pady=5)
    entry_high_performance = tk.Entry(player_frame, width=30)
    entry_high_performance.grid(row=4, column=1, padx=10, pady=5)


    buttons_frame = tk.Frame(player_frame, bg="#f4f4f4")
    buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)


    button_add_player = tk.Button(buttons_frame, text="Add Record", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=lambda: add_player(entry_player_name.get(), entry_injury_name.get(), entry_injury_status.get(), entry_low_performance.get(), entry_high_performance.get()))
    button_add_player.pack(side="left", padx=20)


    button_show_players = tk.Button(buttons_frame, text="Show Records", bg="#6c757d", fg="black", font=("Arial", 12, "bold"), command=display_players)
    button_show_players.pack(side="right", padx=20)


def add_player(name, injury_name, injury_status, low_performance, high_performance):
    if not name or not injury_name or not injury_status or not low_performance or not high_performance:
        messagebox.showerror("Error", "All fields are required!")
    else:
        player_records.append({
            "name": name,
            "injury_name": injury_name,
            "injury_status": injury_status,
            "low_performance": low_performance,
            "high_performance": high_performance
        })
        messagebox.showinfo("Success", f"Player {name} added successfully!")


def search_player(name):
    for player in player_records:
        if player["name"].lower() == name.lower():
            messagebox.showinfo("Player Found", f"Name: {player['name']}, Injury: {player['injury_name']}, Injury Status: {player['injury_status']}, Low Performance: {player['low_performance']}, High Performance: {player['high_performance']}")
            return
    messagebox.showerror("Error", "Player not found!")


def delete_player(name):
    for player in player_records:
        if player["name"].lower() == name.lower():
            player_records.remove(player)
            messagebox.showinfo("Success", f"Player {name} deleted successfully!")
            return
    messagebox.showerror("Error", "Player not found!")


def display_players():
    if not player_records:
        messagebox.showinfo("No Players", "No players available to display!")
    else:
        players_info = "\n".join([f"Name: {player['name']}, Injury: {player['injury_name']}, Injury Status: {player['injury_status']}, Low Performance: {player['low_performance']}, High Performance: {player['high_performance']}" for player in player_records])
        messagebox.showinfo("All Players", players_info)


frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(expand=True, pady=40)

label_title = tk.Label(frame, text="Football Team Registration and Login", bg="#f4f4f4", fg="#333", font=("Arial", 18, "bold"))
label_title.grid(row=0, column=0, columnspan=2, pady=10)


label_team_name = tk.Label(frame, text="Team Name:", bg="#f4f4f4", font=("Arial", 12))
label_team_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_team_name = tk.Entry(frame, width=30)
entry_team_name.grid(row=1, column=1, padx=10, pady=5)


label_manager_name = tk.Label(frame, text="Manager Name:", bg="#f4f4f4", font=("Arial", 12))
label_manager_name.grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_manager_name = tk.Entry(frame, width=30)
entry_manager_name.grid(row=2, column=1, padx=10, pady=5)


label_password = tk.Label(frame, text="Password:", bg="#f4f4f4", font=("Arial", 12))
label_password.grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_password = tk.Entry(frame, width=30, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)


buttons_frame = tk.Frame(frame, bg="#f4f4f4")
buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)


button_register = tk.Button(buttons_frame, text="Register", bg="#28a745", fg="black", font=("Arial", 12, "bold"), command=register)
button_register.pack(side="left", padx=20)

# Login Button
button_login = tk.Button(buttons_frame, text="Login", bg="#007bff", fg="black", font=("Arial", 12, "bold"), command=login)
button_login.pack(side="right", padx=20)

# Add Exit Button to Main Dashboard
exit_button = tk.Button(root, text="Exit Application", bg="#dc3545", fg="black", font=("Arial", 12, "bold"), command=root.quit)
exit_button.pack(pady=10)

# Run the app
root.mainloop()
