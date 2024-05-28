import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_google_maps(query):
    try:
        url = f"https://www.google.com/maps/search/{query}"
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na solicitação

        soup = BeautifulSoup(response.content, "html.parser")
        results = []

        for item in soup.find_all("div", class_="cX2WmPgCkHi__result-container"):
            name_element = item.find("h3", class_="section-result-title")
            share_link_element = item.find("a", class_="section-result-action-button")
            phone_element = item.find("span", class_="section-result-info-phone")
            
            if name_element and share_link_element and phone_element:
                name = name_element.text.strip()
                share_link = share_link_element.get("href", "")
                phone = phone_element.text.strip()
                results.append({"Nome": name, "Link de Compartilhamento": share_link, "Telefone": phone})

        return results
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a solicitação para o Google Maps: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao processar a pesquisa: {e}")
        return []

class GoogleMapsScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Maps Scraper")

        self.query_label = ttk.Label(root, text="Local:")
        self.query_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.query_entry = ttk.Entry(root, width=40)
        self.query_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.search_button = ttk.Button(root, text="Pesquisar", command=self.search)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        self.result_label = ttk.Label(root, text="Resultados:")
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        self.result_text = tk.Text(root, width=60, height=10)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    def search(self):
        query = self.query_entry.get()
        if query:
            results = search_google_maps(query)
            if results:
                df = pd.DataFrame(results)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, df.to_string(index=False))
            else:
                messagebox.showinfo("Sem Resultados", "Não foi possível obter os resultados. Por favor, tente novamente.")
        else:
            messagebox.showwarning("Campo Vazio", "Por favor, digite o local que deseja pesquisar.")

def main():
    root = tk.Tk()
    app = GoogleMapsScraperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
