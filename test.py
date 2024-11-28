import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Vietnamese Text Test")
    window.geometry('400x200')

    # text_widget = tk.Text(window, font=("DejaVu Sans", 12))
    text_widget = tk.Text(window, font=("Arial", 12))
    text_widget.pack(expand=True, fill="both")

    sample_text = "ỉ is a Vietnamese character. Hồ Chí Minh"
    text_widget.insert(tk.END, sample_text)

    window.mainloop()

if __name__ == "__main__":
    main()
