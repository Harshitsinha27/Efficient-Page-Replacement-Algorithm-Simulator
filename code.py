import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Page Replacement Algorithms
class PageReplacementSimulator:
    def __init__(self, memory_size, reference_string):
        self.memory_size = memory_size
        self.reference_string = reference_string
        self.frames = []
        self.page_faults = 0
        self.page_hits = 0

    def fifo(self):
        self.frames.clear()
        self.page_faults = self.page_hits = 0
        for page in self.reference_string:
            if page in self.frames:
                self.page_hits += 1
            else:
                self.page_faults += 1
                if len(self.frames) < self.memory_size:
                    self.frames.append(page)
                else:
                    self.frames.pop(0)
                    self.frames.append(page)
        return self.page_faults, self.page_hits

    def lru(self):
        self.frames.clear()
        self.page_faults = self.page_hits = 0
        recent_use = []
        for page in self.reference_string:
            if page in self.frames:
                self.page_hits += 1
                recent_use.remove(page)
                recent_use.append(page)
            else:
                self.page_faults += 1
                if len(self.frames) < self.memory_size:
                    self.frames.append(page)
                else:
                    lru_page = recent_use.pop(0)
                    self.frames[self.frames.index(lru_page)] = page
                recent_use.append(page)
        return self.page_faults, self.page_hits

    def optimal(self):
        self.frames.clear()
        self.page_faults = self.page_hits = 0
        for i in range(len(self.reference_string)):
            page = self.reference_string[i]
            if page in self.frames:
                self.page_hits += 1
            else:
                self.page_faults += 1
                if len(self.frames) < self.memory_size:
                    self.frames.append(page)
                else:
                    # Find Optimal Page to Replace
                    future = self.reference_string[i + 1:]
                    replace_index = -1
                    farthest = -1
                    for frame in self.frames:
                        if frame not in future:
                            replace_index = self.frames.index(frame)
                            break
                        else:
                            index = future.index(frame)
                            if index > farthest:
                                farthest = index
                                replace_index = self.frames.index(frame)
                    self.frames[replace_index] = page
        return self.page_faults, self.page_hits


# GUI Class
class PageReplacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Efficient Page Replacement Algorithm Simulator")
        self.root.geometry("800x600")

        # Inputs
        tk.Label(root, text="Memory Size:").grid(row=0, column=0, padx=10, pady=10)
        self.memory_size_entry = tk.Entry(root)
        self.memory_size_entry.grid(row=0, column=1)

        tk.Label(root, text="Reference String (comma-separated):").grid(row=1, column=0, padx=10, pady=10)
        self.reference_string_entry = tk.Entry(root)
        self.reference_string_entry.grid(row=1, column=1)

        # Algorithm Selection
        self.algorithm_var = tk.StringVar(value="FIFO")
        tk.Label(root, text="Select Algorithm:").grid(row=2, column=0, padx=10, pady=10)
        tk.Radiobutton(root, text="FIFO", variable=self.algorithm_var, value="FIFO").grid(row=2, column=1)
        tk.Radiobutton(root, text="LRU", variable=self.algorithm_var, value="LRU").grid(row=2, column=2)
        tk.Radiobutton(root, text="Optimal", variable=self.algorithm_var, value="Optimal").grid(row=2, column=3)

        # Buttons
        tk.Button(root, text="Simulate", command=self.simulate).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(root, text="Clear", command=self.clear).grid(row=3, column=2, pady=20)

        # Output
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.grid(row=4, column=0, columnspan=4, pady=10)

        # Visualization Canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=4)

    def simulate(self):
        try:
            memory_size = int(self.memory_size_entry.get())
            reference_string = list(map(int, self.reference_string_entry.get().split(',')))

            simulator = PageReplacementSimulator(memory_size, reference_string)

            if self.algorithm_var.get() == "FIFO":
                faults, hits = simulator.fifo()
            elif self.algorithm_var.get() == "LRU":
                faults, hits = simulator.lru()
            elif self.algorithm_var.get() == "Optimal":
                faults, hits = simulator.optimal()
            else:
                messagebox.showerror("Error", "Invalid Algorithm Selected")
                return

            hit_ratio = round((hits / len(reference_string)) * 100, 2)
            fault_ratio = round((faults / len(reference_string)) * 100, 2)

            result_text = f"Page Faults: {faults}\nPage Hits: {hits}\nHit Ratio: {hit_ratio}%\nFault Ratio: {fault_ratio}%"
            self.result_label.config(text=result_text)

            # Visualization
            self.ax.clear()
            labels = ['Page Faults', 'Page Hits']
            values = [faults, hits]
            self.ax.bar(labels, values, color=['red', 'green'])
            self.ax.set_title(f"{self.algorithm_var.get()} Results")
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def clear(self):
        self.memory_size_entry.delete(0, tk.END)
        self.reference_string_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.ax.clear()
        self.canvas.draw()


# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementApp(root)
    root.mainloop()
