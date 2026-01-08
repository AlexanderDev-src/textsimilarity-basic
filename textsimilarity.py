import math
import string
from collections import Counter
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from pypdf import PdfReader
import customtkinter as ctk

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "am", "are", 
    "was", "were", "in", "on", "at", "to", "for", "of", "with",
    "it", "this", "that", "i", "you", "he", "she", "we", "they",
    "be", "been", "as", "just"
}
def simple_stemmer(word):
    if word.endswith('s') and len(word) > 3: word = word[:-1]
    if word.endswith('ing') and len(word) > 4: word = word[:-3]
    if word.endswith('ed') and len(word) > 4: word = word[:-2]

    return word
    
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    process_word = [] 
    for w in words:
        if w not in STOP_WORDS:
            process_word.append(simple_stemmer(w))
    return process_word

def get_cosine_similarity(text1, text2):
    vec = Counter(clean_text(text1))
    vec1 = Counter(clean_text(text2))

    all_words = set(vec.keys()).union(set(vec1.keys()))
    
    dot_product = 0
    sum_sq1 = 0
    sum_sq2 = 0

    for word in all_words:
        vecA = vec[word]
        vecB = vec1[word]
        dot_product += vecA * vecB
        sum_sq1 += vecA**2
        sum_sq2 += vecB**2

    magnitude1 = math.sqrt(sum_sq1)
    magnitude2 = math.sqrt(sum_sq2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Plagiarism Checker")
        self.geometry("700x650")

        self.title_label = ctk.CTkLabel(self, text="Plagiarism Checker System", font=("Roboto", 24, "bold"))
        self.title_label.pack(pady=20)

        self.frame1 = ctk.CTkFrame(self)
        self.frame1.pack(pady=5, padx=20, fill="x")
        
        self.lbl1 = ctk.CTkLabel(self.frame1, text="First Text:", font=("Roboto", 14))
        self.lbl1.pack(side="left", padx=10, pady=5)
        
        self.btn_upload1 = ctk.CTkButton(self.frame1, text="📂 Upload PDF/TXT", width=100, 
                                         command=lambda: self.upload_file(self.text_area1))
        self.btn_upload1.pack(side="right", padx=10, pady=5)

        self.text_area1 = ctk.CTkTextbox(self, width=650, height=150, corner_radius=10)
        self.text_area1.pack(pady=5)

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.pack(pady=(20, 5), padx=20, fill="x") 
        
        self.lbl2 = ctk.CTkLabel(self.frame2, text="Second Text:", font=("Roboto", 14))
        self.lbl2.pack(side="left", padx=10, pady=5)
        
        self.btn_upload2 = ctk.CTkButton(self.frame2, text="📂 Upload PDF/TXT", width=100,
                                         command=lambda: self.upload_file(self.text_area2))
        self.btn_upload2.pack(side="right", padx=10, pady=5)

        self.text_area2 = ctk.CTkTextbox(self, width=650, height=150, corner_radius=10)
        self.text_area2.pack(pady=5)

        self.check_btn = ctk.CTkButton(self, text="⚡ RUN ANALYSIS", font=("Roboto", 16, "bold"),
                                       height=50, width=200, fg_color="#E74C3C", hover_color="#C0392B", # สีแดงเท่ๆ
                                       command=self.on_check_click)
        self.check_btn.pack(pady=30)

        self.result_label = ctk.CTkLabel(self, text="Result: Waiting...", font=("Roboto", 20, "bold"))
        self.result_label.pack(pady=5)

    def upload_file(self, target_text_area):
        file_path = filedialog.askopenfilename(filetypes=[("PDF/Text", "*.pdf *.txt")])
        if file_path:
            if file_path.endswith('.pdf'):
                content = extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            target_text_area.delete("1.0", "end")
            target_text_area.insert("1.0", content)

    def on_check_click(self):
        t1 = self.text_area1.get("1.0", "end").strip()
        t2 = self.text_area2.get("1.0", "end").strip()

        if not t1 or not t2:
            messagebox.showwarning("Warning", "Please input text in both fields.")
            return

        similarity = get_cosine_similarity(t1, t2)
        percentage = similarity * 100

        self.result_label.configure(text=f"Similarity: {percentage:.2f}%")
        
        if percentage > 80:
            self.result_label.configure(text_color="#FF5555") 
        elif percentage > 50:
            self.result_label.configure(text_color="#F1C40F") 
        else:
            self.result_label.configure(text_color="#50FA7B")

if __name__ == "__main__":
    app = App()
    app.mainloop()
