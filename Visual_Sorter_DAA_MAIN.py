import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >=0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def merge_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1
    if l < r:
        m = (l + r) // 2
        yield from merge_sort(arr, l, m)
        yield from merge_sort(arr, m + 1, r)
        yield from merge(arr, l, m, m + 1, r)
    yield arr

def merge(arr, start1, end1, start2, end2):
    i, j = start1, start2
    temp = []
    while i <= end1 and j <= end2:
        if arr[i] < arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    while i <= end1:
        temp.append(arr[i])
        i += 1
    while j <= end2:
        temp.append(arr[j])
        j += 1
    for i, val in enumerate(temp, start=start1):
        arr[i] = val
        yield arr

def quick_sort(arr, low, high):
    if low < high:
        pi, arr = partition(arr, low, high)
        yield arr
        yield from quick_sort(arr, low, pi-1)
        yield from quick_sort(arr, pi+1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1, arr

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield from heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)

# Binary search algorithm
def binary_search(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        yield arr, mid
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1


class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Sorting Algorithm Visualizer")
        master.geometry("900x650")

        # Dark theme colors
        bg_color = "#212121"  # Background color
        fg_color = "#FFFFFF"  # Foreground (text) color
        button_color = "#333333"  # Button color
        highlight_color = "#FF5722"  # Highlight color for buttons

        # Create a custom style for the OptionMenu
        style = ttk.Style()
        style.theme_use('clam')  # Use any theme to initialize the style
        style.configure('CustomOption.TMenubutton', background=button_color, foreground=fg_color)  # Configure the custom style

        # Input section
        input_frame = tk.Frame(master, padx=10, pady=10, bg=bg_color)
        input_frame.pack(padx=10, pady=5, fill=tk.BOTH)

        self.input_label = ttk.Label(input_frame, text="Enter comma-separated values (up to 100 elements):", foreground=fg_color, background=bg_color)
        self.input_label.grid(row=0, column=0, sticky="w")

        self.input_entry = tk.Entry(input_frame, width=50, bg="black", fg="white")  # Set background to black and foreground to white
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)

        # Algorithm selection
        algo_frame = tk.Frame(master, padx=10, pady=10, bg=bg_color)
        algo_frame.pack(padx=10, pady=5, fill=tk.BOTH)

        self.algo_label = ttk.Label(algo_frame, text="Select Sorting Algorithm:", foreground=fg_color, background=bg_color)
        self.algo_label.grid(row=0, column=0, sticky="w")

        self.algo_var = tk.StringVar(master)
        self.algo_var.set("Bubble Sort")
        self.algorithm_menu = ttk.OptionMenu(algo_frame, self.algo_var, "Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort", "Quick Sort", "Heap Sort", style='CustomOption.TMenubutton')  # Apply custom style
        self.algorithm_menu.grid(row=0, column=1, padx=10, pady=5)

        # Search section
        search_frame = tk.Frame(master, padx=10, pady=10, bg=bg_color)
        search_frame.pack(padx=10, pady=5, fill=tk.BOTH)

        self.search_label = ttk.Label(search_frame, text="Enter value to search:", foreground=fg_color, background=bg_color)
        self.search_label.grid(row=0, column=0, sticky="w")

        self.search_entry = tk.Entry(search_frame, width=30, bg="black", fg="white")  # Set background to black and foreground to white
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        action_frame = tk.Frame(master, padx=10, pady=10, bg=bg_color)
        action_frame.pack(padx=10, pady=5)

        self.sort_button = ttk.Button(action_frame, text="Sort", command=self.visualize_sort, style="Dark.TButton")
        self.sort_button.pack(side="left", padx=(150, 20))

        self.search_button = ttk.Button(action_frame, text="Binary Search", command=self.visualize_search, style="Dark.TButton")
        self.search_button.pack(side="left", padx=(20, 150))

        # Style configuration for dark theme
        style.configure("Dark.TButton", foreground=fg_color, background=button_color, highlightbackground=highlight_color, highlightcolor=highlight_color)


    def visualize_sort(self):
        arr_str = self.input_entry.get()
        try:
            arr = [int(x.strip()) for x in arr_str.split(',')]
            if len(arr) > 100:
                raise ValueError("Array size should not exceed 100 elements.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        algo_name = self.algo_var.get()
        algo_func = None

        if algo_name == "Bubble Sort":
            algo_func = bubble_sort
        elif algo_name == "Insertion Sort":
            algo_func = insertion_sort
        elif algo_name == "Selection Sort":
            algo_func = selection_sort
        elif algo_name == "Merge Sort":
            algo_func = merge_sort
        elif algo_name == "Quick Sort":
            algo_func = lambda arr: quick_sort(arr, 0, len(arr)-1)
        elif algo_name == "Heap Sort":
            algo_func = heap_sort

        if algo_func:
            self.run_animation(arr, algo_func)

    def visualize_search(self):
        arr_str = self.input_entry.get()
        search_str = self.search_entry.get()
        try:
            arr = [int(x.strip()) for x in arr_str.split(',')]
            if len(arr) > 100:
                raise ValueError("Array size should not exceed 100 elements.")
            search_val = int(search_str.strip())
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        arr.sort()  # Ensure the array is sorted for binary search
        self.run_search_animation(arr, binary_search, search_val)

    def run_animation(self, arr, algo_func):
        fig, ax = plt.subplots()
        ax.set_title("Sorting Algorithm Visualizer")
        bars = ax.bar(range(len(arr)), arr, align="edge", color="lightblue")

        animation_frames = algo_func(arr)

        def update_fig(arr, rects):
            for rect, val in zip(rects, arr):
                rect.set_height(val)
            fig.canvas.draw()

        anim = animation.FuncAnimation(fig, func=update_fig, fargs=(bars, ), frames=animation_frames, interval=1, repeat=False, cache_frame_data=False)
        plt.show()

    def run_search_animation(self, arr, search_func, search_val):
        fig, ax = plt.subplots()
        ax.set_title("Binary Search Visualization")
        bars = ax.bar(range(len(arr)), arr, align="edge", color="lightblue")

        def search_frames():
            low, high = 0, len(arr) - 1
            while low <= high:
                mid = (low + high) // 2
                yield mid
                if arr[mid] < search_val:
                    low = mid + 1
                elif arr[mid] > search_val:
                    high = mid - 1
                else:
                    return mid
            return -1

        def update_fig(mid, rects, arr):
            for rect in rects:
                rect.set_color('lightblue')
            if mid != -1:
                rects[mid].set_color('red')
            fig.canvas.draw()

        anim = animation.FuncAnimation(fig, func=update_fig, fargs=(bars, arr), frames=search_frames(), interval=200, repeat=False, cache_frame_data=False)
        plt.show()

def main():
    root = tk.Tk()
    root.configure(bg="#212121")  # Set root background color to match dark theme
    app = SortingVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
