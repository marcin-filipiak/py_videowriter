import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

FONT_MAP = {
    "HERSHEY_SIMPLEX": cv2.FONT_HERSHEY_SIMPLEX,
    "HERSHEY_PLAIN": cv2.FONT_HERSHEY_PLAIN,
    "HERSHEY_DUPLEX": cv2.FONT_HERSHEY_DUPLEX,
    "HERSHEY_COMPLEX": cv2.FONT_HERSHEY_COMPLEX,
    "HERSHEY_TRIPLEX": cv2.FONT_HERSHEY_TRIPLEX,
    "HERSHEY_COMPLEX_SMALL": cv2.FONT_HERSHEY_COMPLEX_SMALL,
    "HERSHEY_SCRIPT_SIMPLEX": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    "HERSHEY_SCRIPT_COMPLEX": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
}

COLOR_MAP = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
}

class TypingVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Effect Video")

        self.video_path = ""

        tk.Label(root, text="Enter text:").pack()
        self.text_input = tk.Text(root, height=10, width=60)
        self.text_input.pack()

        tk.Label(root, text="Choose font:").pack()
        self.font_var = tk.StringVar(value="HERSHEY_SIMPLEX")
        tk.OptionMenu(root, self.font_var, *FONT_MAP.keys()).pack()

        tk.Label(root, text="Choose text color:").pack()
        self.color_var = tk.StringVar(value="white")
        tk.OptionMenu(root, self.color_var, *COLOR_MAP.keys()).pack()

        tk.Button(root, text="Select video", command=self.select_video).pack(pady=5)
        tk.Button(root, text="Render with effect", command=self.render_video).pack(pady=5)

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if path:
            self.video_path = path

    def render_video(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video first.")
            return

        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text.")
            return

        lines = text.split("\n")
        font = FONT_MAP[self.font_var.get()]
        color = COLOR_MAP[self.color_var.get()]
        font_scale = 1
        thickness = 2
        line_height = 35

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_chars = sum(len(line) for line in lines)

        out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

        printed_chars = 0
        chars_per_frame = 1
        hold_frames = int(fps * 2)         # hold time (2 seconds)
        fade_frames = int(fps * 1)         # fade time (1 second)
        fade_counter = 0
        done_typing = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            overlay = frame.copy()

            if not done_typing:
                printed_chars = min(printed_chars + chars_per_frame, total_chars)
                if printed_chars >= total_chars:
                    done_typing = True
            else:
                if hold_frames > 0:
                    hold_frames -= 1
                elif fade_counter < fade_frames:
                    fade_counter += 1

            chars_left = printed_chars
            y_start = height - 20 - (len(lines) - 1) * line_height

            for i, line in enumerate(lines):
                to_print = line[:chars_left] if chars_left > 0 else ""
                chars_left -= len(to_print)
                position = (10, y_start + i * line_height)
                if done_typing and hold_frames <= 0:
                    alpha = 1.0 - (fade_counter / fade_frames) if fade_counter < fade_frames else 0.0
                    temp = overlay.copy()
                    cv2.putText(temp, to_print, position, font, font_scale, color, thickness, cv2.LINE_AA)
                    overlay = cv2.addWeighted(overlay, 1.0, temp, alpha, 0)
                else:
                    cv2.putText(overlay, to_print, position, font, font_scale, color, thickness, cv2.LINE_AA)

            out.write(overlay)

            if done_typing and hold_frames <= 0 and fade_counter >= fade_frames:
                break

        cap.release()
        out.release()
        messagebox.showinfo("Done", "File output.mp4 has been saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingVideoApp(root)
    root.mainloop()

