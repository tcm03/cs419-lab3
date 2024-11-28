import tkinter as tk
from tkinter import ttk
from get_data import get_dicts, get_scores
from vector_space import search_query
import threading
import webbrowser

def main():
    # Load data and models
    term2id, doc2id, id2doc, documents = get_dicts()
    tf, idf, tfidf = get_scores(term2id, doc2id, documents)

    # Create the main window
    window = tk.Tk()
    window.title("Simple Search Engine")
    window.geometry('800x600')

    # Create a frame for the search bar
    search_frame = tk.Frame(window)
    search_frame.pack(pady=10)

    # Create an entry widget for the search query
    search_label = tk.Label(search_frame, text="Enter your search query:")
    search_label.pack(side=tk.LEFT, padx=5)

    query_entry = tk.Entry(search_frame, width=50, font=("DejaVu Sans", 12))
    query_entry.pack(side=tk.LEFT, padx=5)

    # Create another frame for the Top-K textbox and search button
    options_frame = tk.Frame(window)
    options_frame.pack(pady=5)

    # Create an entry widget for top-k results
    top_k_label = tk.Label(options_frame, text="Number of results (Top-K):")
    top_k_label.pack(side=tk.LEFT, padx=5)

    top_k_entry = tk.Entry(options_frame, width=5, font=("DejaVu Sans", 12))
    top_k_entry.insert(0, "10")  # Default value
    top_k_entry.pack(side=tk.LEFT, padx=5)

    # Create a button to perform the search
    search_button = tk.Button(options_frame, text="Search", command=lambda: perform_search())
    search_button.pack(side=tk.LEFT, padx=5)

    # Create a frame for the results
    results_container = tk.Frame(window)
    results_container.pack(fill=tk.BOTH, expand=True)

    # Add a canvas for scrollable results
    canvas = tk.Canvas(results_container)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Add a frame inside the canvas for the results
    results_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=results_frame, anchor="nw")

    # Ensure the canvas updates when the results_frame changes size
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    results_frame.bind("<Configure>", on_frame_configure)

    # Function to open a URL
    def open_url(url):
        webbrowser.open(url)

    # Function to perform the search
    def perform_search():
        query = query_entry.get()
        try:
            top_k = int(top_k_entry.get())
        except ValueError:
            top_k = 10  # Fallback to default

        if not query:
            clear_results()
            tk.Label(results_frame, text="Please enter a search query.", font=("DejaVu Sans", 12)).pack(pady=5)
            return

        clear_results()
        tk.Label(results_frame, text="Searching...", font=("DejaVu Sans", 12)).pack(pady=5)

        def search_thread():
            results = search_query(query, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=top_k)
            clear_results()
            if results:
                for result in results:
                    create_result_widget(result)
            else:
                tk.Label(results_frame, text="No results found.", font=("DejaVu Sans", 12)).pack(pady=5)

        threading.Thread(target=search_thread).start()

    # Function to clear previous results
    def clear_results():
        for widget in results_frame.winfo_children():
            widget.destroy()

    # Function to create a widget for each result
    def create_result_widget(result):
        result_frame = tk.Frame(results_frame, bd=2, relief=tk.RAISED, padx=10, pady=10)
        result_frame.pack(fill=tk.X, pady=5)

        # Title
        title_label = tk.Label(result_frame, text=result['title'], font=("DejaVu Sans Bold", 14), fg="blue", cursor="hand2")
        title_label.pack(anchor="w")
        title_label.bind("<Button-1>", lambda e: open_url(result['url']))

        # Author and Date
        meta_label = tk.Label(result_frame, text=f"By {result['author']} | {result['date']}", font=("DejaVu Sans", 10), fg="gray")
        meta_label.pack(anchor="w")

        # Snippet
        snippet_label = tk.Label(result_frame, text=f"{result['snippet']}...", font=("DejaVu Sans", 12), wraplength=750, justify="left")
        snippet_label.pack(anchor="w")

        # Similarity Score
        similarity_label = tk.Label(result_frame, text=f"Similarity Score: {result['similarity']:.4f}", font=("DejaVu Sans", 10), fg="green")
        similarity_label.pack(anchor="w")

    window.mainloop()

if __name__ == "__main__":
    main()
