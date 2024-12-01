import tkinter as tk
from tkinter import Listbox, PhotoImage
import requests
from bs4 import BeautifulSoup

# Web scraping function
def fetch_countries():
    try:
        url = url_entry.get()
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract country names
        countries_names = soup.findAll("span", class_="ssrcss-ymac56-CountryName")
        global countries
        countries = [element.text.strip().upper() for element in countries_names]  # Convert to uppercase

        country_listbox.delete(0, tk.END)
        # Add countries to the listbox
        for country in countries:
            country_listbox.insert(tk.END, country)

        info_label.config(text=f"Found {len(countries)} countries. Click on a country to see detailed medals.")
    except Exception as e:
        info_label.config(text=f"Error fetching countries: {e}")

# GUI setup
root = tk.Tk()
root.title("Olympics 2024")
root.geometry("500x750")

title_label = tk.Label(root, text="Olympics 2024", font=("Helvetica", 24, "bold"), fg="black")
title_label.pack(pady=(10, 5))

logo_image = PhotoImage(file="olmp.png")  
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

# Chart button (currently no functionality)
chart_button = tk.Button(root, text="Show Chart of Selected Country", font=("Helvetica", 12), fg="black", command=lambda: None)
chart_button.pack(pady=5)

root.mainloop()
