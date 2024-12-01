import tkinter as tk
from tkinter import Listbox, PhotoImage, messagebox
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class VisualMP2:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Olympics 2024")
        self.parent.geometry("500x750")

        self.countries = []
        self.initUI()

    def initUI(self):
        title_label = tk.Label(self.parent, text="Olympics 2024", font=("Helvetica", 24, "bold"), fg="black")
        title_label.pack(pady=(10, 5))

        self.logo_image = PhotoImage(file="olmp.png") 
        self.logo_label = tk.Label(self.parent, image=self.logo_image)
        self.logo_label.pack(pady=(5, 5))

        self.url_entry = tk.Entry(self.parent, font=("Helvetica", 12), width=50, justify="center")
        self.url_entry.insert(0, "https://www.bbc.com/sport/olympics/paris-2024/medals")
        self.url_entry.pack(pady=(5, 5))

        show_list_button = tk.Button(self.parent, text="Show List", font=("Helvetica", 12), fg="black", command=self.fetch_countries)
        show_list_button.pack(pady=5)

        self.country_listbox = Listbox(self.parent, font=("Helvetica", 12), height=10, width=50)
        self.country_listbox.pack(pady=(5, 10))

        self.info_label = tk.Label(self.parent, text="Click on a country to see detailed medals:", font=("Helvetica", 10), fg="black")
        self.info_label.pack(pady=(5, 5))

        chart_button = tk.Button(self.parent, text="Show Chart of Selected Country", font=("Helvetica", 12), fg="black", command=self.show_chart)
        chart_button.pack(pady=5)

        analysis_button = tk.Button(self.parent, text="Show top 10 performing countries analytics", font=("Helvetica", 12), fg="black", command=self.show_top_10_analytics)
        analysis_button.pack(pady=5)

    def fetch_countries(self):
        try:
            url = self.url_entry.get()
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            self.countries = []

            rows = soup.find_all("tr", class_="ssrcss-dhlz6k-TableRowBody e1icz100")

            for row in rows:
                country_name_tag = row.find("span", class_="ssrcss-ymac56-CountryName ew4ldjd0")
                gold_tag = row.find("div", class_="ssrcss-z3opd8-CellWrapper ef9ipf0")
                medal_tags = row.find_all("div", class_="ssrcss-1yl2exm-CellWrapper ef9ipf0")

                country_name = country_name_tag.text.strip().upper() if country_name_tag else "N/A"
                gold = gold_tag.text.strip() if gold_tag else "0"
                silver = medal_tags[1].text.strip() if len(medal_tags) > 0 else "0"
                bronze = medal_tags[2].text.strip() if len(medal_tags) > 1 else "0"
                total = medal_tags[3].text.strip() 
                
                self.countries.append({
                    "name": country_name,
                    "goldmedal": int(gold),
                    "silvermedal": int(silver),
                    "bronzemedal": int(bronze),
                    "totalmedal": int(total)
                })

            self.country_listbox.delete(0, tk.END)
            for country in self.countries:
                self.country_listbox.insert(tk.END, country["name"])

            self.info_label.config(text=f"Found {len(self.countries)} countries. Click on a country to see detailed medals.")
        except Exception as e:
            self.info_label.config(text=f"Error fetching countries: {e}")

    def show_chart(self):
        try:
            selected_index = self.country_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a country from the list!")
                return

            selected_country = self.countries[selected_index[0]]

            labels = ['Gold', 'Silver', 'Bronze']
            counts = [selected_country["goldmedal"], selected_country["silvermedal"], selected_country["bronzemedal"]]

            plt.figure(figsize=(6, 4))
            plt.bar(labels, counts, color=['gold', 'silver', 'brown'])
            plt.title(f"Medals Count for {selected_country['name']}", fontsize=14, fontweight='bold')
            plt.xlabel("Medal Type", fontsize=12)
            plt.ylabel("Count", fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error generating chart: {e}")

    def show_top_10_analytics(self):
        try:
            top_10_countries = sorted(self.countries, key=lambda x: x["totalmedal"], reverse=True)[:10]

            gold_medals = [country["goldmedal"] for country in top_10_countries]
            silver_medals = [country["silvermedal"] for country in top_10_countries]
            bronze_medals = [country["bronzemedal"] for country in top_10_countries]
            country_names = [country["name"] for country in top_10_countries]

            fig, axs = plt.subplots(2, 2, figsize=(10, 8))
            axs[0, 0].pie(gold_medals, labels=country_names, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
            axs[0, 0].set_title("Gold Medals", fontsize=12, fontweight='bold')

            axs[0, 1].pie(silver_medals, labels=country_names, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
            axs[0, 1].set_title("Silver Medals", fontsize=12, fontweight='bold')

            axs[1, 0].pie(bronze_medals, labels=country_names, autopct='%1.1f%%', colors=plt.cm.Dark2.colors)
            axs[1, 0].set_title("Bronze Medals", fontsize=12, fontweight='bold')

            axs[1, 1].plot(country_names, [country["totalmedal"] for country in top_10_countries], marker='o', linestyle='-', color='blue')
            axs[1, 1].set_title("Total Medals", fontsize=12, fontweight='bold')
            axs[1, 1].set_ylabel("Number of Medals")
            axs[1, 1].set_xlabel("Countries")
            axs[1, 1].tick_params(axis='x', rotation=45)
            axs[1, 1].grid(axis='y', linestyle='--', alpha=0.7)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Error generating analytics: {e}")

def main():
    root = tk.Tk()
    app = VisualMP2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
