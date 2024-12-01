import tkinter as tk
from tkinter import Listbox, PhotoImage, messagebox
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Web scraping function
def fetch_countries():
    try:
        url = url_entry.get()
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        global countries
        countries = []

        # Extracting table rows
        rows = soup.find_all("tr", class_="ssrcss-dhlz6k-TableRowBody e1icz100")

        for row in rows:
            country_name_tag = row.find("span", class_="ssrcss-ymac56-CountryName ew4ldjd0")
            gold_tag = row.find("div", class_="ssrcss-z3opd8-CellWrapper ef9ipf0")
            medal_tags = row.find_all("div", class_="ssrcss-1yl2exm-CellWrapper ef9ipf0")

            # Get the values and handle missing data
            country_name = country_name_tag.text.strip().upper() if country_name_tag else "N/A"
            gold = gold_tag.text.strip() if gold_tag else "0"
            silver = medal_tags[1].text.strip() if len(medal_tags) > 0 else "0"
            bronze = medal_tags[2].text.strip() if len(medal_tags) > 1 else "0"

            # Append to countries list
            countries.append({
                "name": country_name,
                "goldmedal": int(gold),
                "silvermedal": int(silver),
                "bronzemedal": int(bronze)
            })

        # Update Listbox
        country_listbox.delete(0, tk.END)
        for country in countries:
            country_listbox.insert(tk.END, country["name"])

        info_label.config(text=f"Found {len(countries)} countries. Click on a country to see detailed medals.")
    except Exception as e:
        info_label.config(text=f"Error fetching countries: {e}")

# Show chart function
def show_chart():
    try:
        selected_index = country_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a country from the list!")
            return

        selected_country = countries[selected_index[0]]

        # Extract medal data
        labels = ['Gold', 'Silver', 'Bronze']
        counts = [selected_country["goldmedal"], selected_country["silvermedal"], selected_country["bronzemedal"]]

        # Create bar chart
        plt.figure(figsize=(6, 4), facecolor='lightgreen')
        plt.bar(labels, counts, color=['gold', 'silver', 'brown'])
        plt.title(f"Medals Count for {selected_country['name']}", fontsize=14, fontweight='bold')
        plt.xlabel("Medal Type", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error generating chart: {e}")

# GUI setup
root = tk.Tk()
root.title("Olympics 2024")
root.geometry("500x750")

title_label = tk.Label(root, text="Olympics 2024", font=("Helvetica", 24, "bold"), fg="black")
title_label.pack(pady=(10, 5))

logo_image = PhotoImage(file="olmp.png")  # Replace with your image path
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(pady=(5, 5))

# URL entry field
url_entry = tk.Entry(root, font=("Helvetica", 12), width=50, justify="center")
url_entry.insert(0, "https://www.bbc.com/sport/olympics/paris-2024/medals")
url_entry.pack(pady=(5, 5))

# Show list button
show_list_button = tk.Button(root, text="Show List", font=("Helvetica", 12), fg="black", command=fetch_countries)
show_list_button.pack(pady=5)

# Country listbox
country_listbox = Listbox(root, font=("Helvetica", 12), height=10, width=50)
country_listbox.pack(pady=(5, 10))

# Information label
info_label = tk.Label(root, text="Click on a country to see detailed medals:", font=("Helvetica", 10), fg="black")
info_label.pack(pady=(5, 5))

# Chart button
chart_button = tk.Button(root, text="Show Chart of Selected Country", font=("Helvetica", 12), fg="black", command=show_chart)
chart_button.pack(pady=5)

# Analysis button (placeholder for future functionality)
analysis_button = tk.Button(root, text="Show top 10 performing countries analytics ", font=("Helvetica", 12), fg="black", command=lambda: None)
analysis_button.pack(pady=5)

root.mainloop()
