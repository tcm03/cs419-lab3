import tkinter as tk
from tkinter import scrolledtext
from get_data import get_dicts, get_scores
from vector_space import search_query
import threading

def main():
    # Load data and models
    term2id, doc2id, id2doc, documents = get_dicts()
    tf, idf, tfidf = get_scores(term2id, doc2id, documents)

    # Create the main window
    window = tk.Tk()
    window.title("Simple Search Engine")

    # Set window size
    window.geometry('800x600')

    # Create a frame for the search bar
    search_frame = tk.Frame(window)
    search_frame.pack(pady=10)

    # Create an entry widget for the search query
    search_label = tk.Label(search_frame, text="Enter your search query:")
    search_label.pack(side=tk.LEFT, padx=5)

    query_entry = tk.Entry(search_frame, width=50, font=("DejaVu Sans", 12))
    query_entry.pack(side=tk.LEFT, padx=5)

    # Create a button to perform the search
    search_button = tk.Button(search_frame, text="Search", command=lambda: perform_search())
    search_button.pack(side=tk.LEFT, padx=5)

    # Create a scrolled text widget to display the results
    results_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=30, font=("DejaVu Sans", 12))
    results_text.pack(pady=10)

    # Function to perform the search
    def perform_search():
        query = query_entry.get()
        if not query:
            results_text.delete('1.0', tk.END)
            results_text.insert(tk.END, "Please enter a search query.")
            return
        print(f'Query: {query}')

        # Clear previous results
        results_text.delete('1.0', tk.END)

        # Display a loading message
        results_text.insert(tk.END, "Searching...")

        # Perform the search in a separate thread to keep the GUI responsive
        def search_thread():
            results = search_query(query, tfidf, idf, term2id, doc2id, id2doc, documents, top_k=10)
            # Update the GUI with the results
            results_text.delete('1.0', tk.END)
            if results:
                for idx, result in enumerate(results, 1):
                    print(f'result: {result['snippet']}')
                    results_text.insert(tk.END, f"{idx}. {result['title']}\n")
                    results_text.insert(tk.END, f"{result['snippet']}...\n")
                    results_text.insert(tk.END, f"Similarity: {result['similarity']:.4f}\n\n")
            else:
                results_text.insert(tk.END, "No results found.")

        threading.Thread(target=search_thread).start()

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()
