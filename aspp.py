import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import fitz  
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from translate import Translator
import nltk

nltk.download('punkt')
nltk.download('stopwords')

students = []

interview_questions = {
    "Yazılım Geliştirici": [
        "Neden yazılım geliştirici olarak çalışmak istiyorsunuz?",
        "Çalıştığınız projelerden birini anlatabilir misiniz?",
        "Hangi programlama dillerini biliyorsunuz?",
        "En büyük yazılım başarılarınız nelerdir?"
    ],
    "Siber Güvenlik Uzmanı": [
        "Neden siber güvenlik alanında çalışmak istiyorsunuz?",
        "Siber güvenlikle ilgili deneyimleriniz nelerdir?",
        "Bir siber saldırı karşısında nasıl bir yol izlersiniz?",
        "Siber güvenlikte en önemli gördüğünüz konu nedir?"
    ],
    "Oyun Geliştirici": [
        "Neden oyun geliştirme alanında çalışmak istiyorsunuz?",
        "Geliştirdiğiniz oyunlardan birini anlatabilir misiniz?",
        "Hangi oyun motorlarını kullanıyorsunuz?",
        "En büyük oyun geliştirme başarılarınız nelerdir?"
    ],
    "Ürün Yöneticisi": [
        "Neden ürün yönetimi alanında çalışmak istiyorsunuz?",
        "Ürün geliştirme sürecinde deneyimleriniz nelerdir?",
        "Bir ürünün başarısını nasıl ölçersiniz?",
        "Ürün yönetiminde en önemli gördüğünüz konu nedir?"
    ],
    "Pazarlama Uzmanı": [
        "Neden pazarlama alanında çalışmak istiyorsunuz?",
        "Pazarlama kampanyalarından birini anlatabilir misiniz?",
        "Hangi pazarlama stratejilerini biliyorsunuz?",
        "En büyük pazarlama başarılarınız nelerdir?"
    ],
    "Backend Geliştirici": [
        "Neden backend geliştirme alanında çalışmak istiyorsunuz?",
        "Çalıştığınız backend projelerden birini anlatabilir misiniz?",
        "Hangi backend teknolojilerini biliyorsunuz?",
        "En büyük backend geliştirme başarılarınız nelerdir?"
    ],
    "Frontend Geliştirici": [
        "Neden frontend geliştirme alanında çalışmak istiyorsunuz?",
        "Çalıştığınız frontend projelerden birini anlatabilir misiniz?",
        "Hangi frontend teknolojilerini biliyorsunuz?",
        "En büyük frontend geliştirme başarılarınız nelerdir?"
    ],
    "Mobil Geliştirici": [
        "Neden mobil geliştirme alanında çalışmak istiyorsunuz?",
        "Çalıştığınız mobil projelerden birini anlatabilir misiniz?",
        "Hangi mobil teknolojilerini biliyorsunuz?",
        "En büyük mobil geliştirme başarılarınız nelerdir?"
    ],
    "Web Geliştirici": [
        "Neden web geliştirme alanında çalışmak istiyorsunuz?",
        "Çalıştığınız web projelerden birini anlatabilir misiniz?",
        "Hangi web teknolojilerini biliyorsunuz?",
        "En büyük web geliştirme başarılarınız nelerdir?"
    ],
    "Veri Bilimi Uzmanı": [
        "Neden veri bilimi alanında çalışmak istiyorsunuz?",
        "Veri bilimi ile ilgili deneyimleriniz nelerdir?",
        "Hangi veri bilimi araçlarını biliyorsunuz?",
        "En büyük veri bilimi başarılarınız nelerdir?"
    ],
    "Veri Analisti": [
        "Neden veri analizi alanında çalışmak istiyorsunuz?",
        "Veri analizi ile ilgili deneyimleriniz nelerdir?",
        "Hangi veri analizi araçlarını biliyorsunuz?",
        "En büyük veri analizi başarılarınız nelerdir?"
    ],
    "Sosyal Medya Uzmanı": [
        "Neden sosyal medya alanında çalışmak istiyorsunuz?",
        "Sosyal medya ile ilgili deneyimleriniz nelerdir?",
        "Hangi sosyal medya araçlarını biliyorsunuz?",
        "En büyük sosyal medya başarılarınız nelerdir?"
    ],
    "Yapay Zeka Uzmanı": [
        "Neden yapay zeka alanında çalışmak istiyorsunuz?",
        "Yapay zeka ile ilgili deneyimleriniz nelerdir?",
        "Hangi yapay zeka araçlarını biliyorsunuz?",
        "En büyük yapay zeka başarılarınız nelerdir?"
    ],
    "İş Zekası Uzmanı": [
        "Neden iş zekası alanında çalışmak istiyorsunuz?",
        "İş zekası ile ilgili deneyimleriniz nelerdir?",
        "Hangi iş zekası araçlarını biliyorsunuz?",
        "En büyük iş zekası başarılarınız nelerdir?"
    ],
    "Dijital Pazarlama Uzmanı": [
        "Neden dijital pazarlama alanında çalışmak istiyorsunuz?",
        "Dijital pazarlama ile ilgili deneyimleriniz nelerdir?",
        "Hangi dijital pazarlama araçlarını biliyorsunuz?",
        "En büyük dijital pazarlama başarılarınız nelerdir?"
    ],
}

class CVSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CV Değerlendirme ve Yazılı Mülakat Sistemi")
        self.geometry(f"{800}x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CV Değerlendirme", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.analysis_buttons = []
        methods = ["CV Değerlendir", "Mülakat Başlat", "Sıralamaları Göster"]
        for i, method in enumerate(methods):
            button = ctk.CTkButton(self.sidebar_frame, text=method, command=lambda m=method: self.switch_frame(m))
            button.grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")
            self.analysis_buttons.append(button)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="Arayüz Boyutu:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, rowspan=4, columnspan=3, padx=20, pady=20, sticky="nsew")

        self.name_entry = ctk.CTkEntry(self.content_frame, width=200)
        self.name_entry.grid(row=0, column=1, sticky=(ctk.W, ctk.E), padx=5, pady=5)

        self.job_role = ctk.CTkOptionMenu(self.content_frame, values=list(interview_questions.keys()))
        self.job_role.grid(row=1, column=1, sticky=(ctk.W, ctk.E), padx=5, pady=5)

        self.cv_file = None
        self.result_text = None
        self.canvas_frame = None

        self.show_cv_evaluation()

    def switch_frame(self, method):
        if method == "CV Değerlendir":
            self.show_cv_evaluation()
        elif method == "Mülakat Başlat":
            self.show_interview()
        elif method == "Sıralamaları Göster":
            self.show_rankings()

    def show_cv_evaluation(self):
        for widget in self.content_frame.winfo_children():
            widget.grid_remove()

        ctk.CTkLabel(self.content_frame, text="Ad ve Soyad:").grid(row=0, column=0, sticky=ctk.W, padx=5, pady=5)
        self.name_entry.grid(row=0, column=1, sticky=(ctk.W, ctk.E), padx=5, pady=5)
        self.name_entry.delete(0, ctk.END)

        ctk.CTkLabel(self.content_frame, text="Meslek:").grid(row=1, column=0, sticky=ctk.W, padx=5, pady=5)
        self.job_role.grid(row=1, column=1, sticky=(ctk.W, ctk.E), padx=5, pady=5)
        self.job_role.set("Meslek Seçin")

        ctk.CTkButton(self.content_frame, text="CV Dosyasını Seç", command=self.select_file).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkButton(self.content_frame, text="CV Değerlendir", command=self.evaluate_cv).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = ctk.CTkTextbox(self.content_frame, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, sticky=(ctk.W, ctk.E), padx=5, pady=5)

    def show_interview(self):
        for widget in self.content_frame.winfo_children():
            widget.grid_remove()

        ctk.CTkLabel(self.content_frame, text="Mülakat Başlat").grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.content_frame, text="Mülakat Başlat", command=self.start_interview).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = ctk.CTkTextbox(self.content_frame, height=10, width=50)
        self.result_text.grid(row=2, column=0, columnspan=2, sticky=(ctk.W, ctk.E), padx=5, pady=5)

    def select_file(self):
        self.cv_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.cv_file:
            messagebox.showinfo("Seçilen Dosya", f"Seçilen Dosya: {self.cv_file}")

    def evaluate_cv(self):
        if not self.cv_file or not self.name_entry.get() or self.job_role.get() == "Meslek Seçin":
            messagebox.showerror("Hata", "Lütfen isim, meslek ve CV dosyasını giriniz.")
            return
        
        cv_score = self.process_cv(self.cv_file)
        cv_score = min(cv_score * 4, 100)  
        name = self.name_entry.get()
        job = self.job_role.get()

        self.result_text.insert(ctk.END, f"{name} adlı öğrencinin {job} mesleği için CV puanı: {cv_score}/100\n")

        
        students.append({"name": name, "job": job, "cv_score": cv_score, "interview_score": 0, "average_score": 0})

    def process_cv(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
        except Exception as e:
            messagebox.showerror("PDF Okuma Hatası", f"PDF dosyası okunamadı: {str(e)}")
            return 0

        
        translator = Translator(to_lang="tr")
        if not self.is_turkish(text):
            try:
                text = translator.translate(text)
            except Exception as e:
                messagebox.showerror("Çeviri Hatası", f"Metin çevrilemedi: {str(e)}")
                return 0

        try:
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words("turkish"))
            filtered_tokens = [w for w in tokens if not w.lower() in stop_words]

            sections = {
                "deneyim": 0,
                "proje": 0,
                "yayın": 0,
                "ödül": 0,
                "gönüllülük": 0,
                "sertifika": 0
            }

            experience_points = 0
            project_points = 0
            publication_points = 0
            award_points = 0
            volunteer_points = 0
            certificate_points = 0

            experience_terms = ["deneyim", "work experience", "çalışma deneyimi", "work history", "employment history"]
            project_terms = ["proje", "project", "project work", "projects"]
            publication_terms = ["yayın", "publication", "publications", "research", "article"]
            award_terms = ["ödül", "award", "awards", "prize"]
            volunteer_terms = ["gönüllülük", "volunteer", "volunteering", "volunteer work"]
            certificate_terms = ["sertifika", "certificate", "certificates", "certification"]

            for token in filtered_tokens:
                if any(term in token.lower() for term in experience_terms):
                    experience_points += 1
                if any(term in token.lower() for term in project_terms):
                    project_points += 1
                if any(term in token.lower() for term in publication_terms):
                    publication_points += 1
                if any(term in token.lower() for term in award_terms):
                    award_points += 1
                if any(term in token.lower() for term in volunteer_terms):
                    volunteer_points += 1
                if any(term in token.lower() for term in certificate_terms):
                    certificate_points += 1

            experience_points = min(experience_points, 20)
            project_points = min(project_points, 20)
            publication_points = min(publication_points, 15)
            award_points = min(award_points, 15)
            volunteer_points = min(volunteer_points, 10)
            certificate_points = min(certificate_points, 10)

            total_points = experience_points + project_points + publication_points + award_points + volunteer_points + certificate_points
            return total_points
        except Exception as e:
            messagebox.showerror("Metin Analizi Hatası", f"Metin analizi yapılamadı: {str(e)}")
            return 0

    def is_turkish(self, text):
        turkish_chars = "çğıöşüÇĞİÖŞÜ"
        return any(char in turkish_chars for char in text)

    def start_interview(self):
        if not self.name_entry or not self.name_entry.get():
            messagebox.showerror("Hata", "Lütfen önce CV'yi değerlendiriniz.")
            return

        name = self.name_entry.get()
        job = None
        for student in students:
            if student["name"] == name:
                job = student["job"]
                break

        if not job:
            messagebox.showerror("Hata", "Lütfen önce CV'yi değerlendiriniz.")
            return

        questions = interview_questions.get(job, [])

        interview_score = 0
        for question in questions:
            answer = simpledialog.askstring("Mülakat Sorusu", question)
            interview_score += len(answer.split()) if answer else 0

        interview_score = min(interview_score, 100)  
        self.result_text.insert(ctk.END, f"Mülakat puanı: {interview_score}/100\n")

        for student in students:
            if student["name"] == name:
                student["interview_score"] = interview_score
                student["average_score"] = (student["cv_score"] + interview_score) / 2
                break
        
        average_score = (students[-1]["cv_score"] + interview_score) / 2
        self.result_text.insert(ctk.END, f"Genel Ortalama: {average_score}\n")

        if average_score >= 60:
            self.result_text.insert(ctk.END, "Tebrikler, işe alındınız!\n")
        else:
            self.result_text.insert(ctk.END, "Biz sizi sonra ararız.\n")

    def show_rankings(self):
        for widget in self.content_frame.winfo_children():
            widget.grid_remove()

        students.sort(key=lambda x: x["average_score"], reverse=True)
        ranking_text = "Sıralamalar:\n"
        for i, student in enumerate(students):
            ranking_text += f"{i+1}. {student['name']} - Puan: {student['average_score']}\n"
        
        self.result_text = ctk.CTkTextbox(self.content_frame, height=10, width=50)
        self.result_text.insert(ctk.END, ranking_text)
        self.result_text.grid(row=0, column=0, columnspan=2, sticky=(ctk.W, ctk.E), padx=5, pady=5)

        self.plot_rankings()

    def plot_rankings(self):
        names = [student["name"] for student in students]
        scores = [student["average_score"] for student in students]

        fig, ax = plt.subplots()
        ax.barh(names, scores, color='skyblue')
        ax.set_xlabel('Puan')
        ax.set_title('Öğrenci Puanları Sıralaması')

        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                     str(round((i.get_width()), 2)), 
                     fontsize=10, fontweight='bold', 
                     color='grey')

        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky=(ctk.W, ctk.E), padx=5, pady=5)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling):
        scaling = int(new_scaling.strip('%')) / 100
        ctk.set_widget_scaling(scaling)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = CVSystem()
    app.mainloop()