import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests

# 你的 DeepLX API 地址
DEEPLX_API_URL = "http://your-deeplx-api.com/translate"


LANGUAGES = {
    "自动检测": "auto",
    "英语": "EN",
    "中文": "ZH",
    "日语": "JA",
    "韩语": "KO",
    "法语": "FR",
    "德语": "DE",
    "俄语": "RU",
    "西班牙语": "ES",
    "意大利语": "IT",
    "葡萄牙语": "PT",
}

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    source_lang = LANGUAGES[source_lang_var.get()]
    target_lang = LANGUAGES[target_lang_var.get()]

    if not text:
        messagebox.showwarning("提示", "请输入要翻译的内容")
        return
    if source_lang == target_lang and source_lang != "auto":
        messagebox.showinfo("提示", "源语言和目标语言相同，无需翻译。")
        return

    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }

    try:
        response = requests.post(DEEPLX_API_URL, json=payload, timeout=10)
        data = response.json()
        if "data" in data and isinstance(data["data"], str):
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, data["data"])
            
            alternatives_text.delete("1.0", tk.END)
            if "alternatives" in data and data["alternatives"]:
                alternatives_text.insert(tk.END, "")
                for alt in data["alternatives"]:
                    alternatives_text.insert(tk.END, f"• {alt}\n")
            else:
                alternatives_text.insert(tk.END, "没有其他翻译建议")
        else:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"[翻译失败] 接口响应：{data}")
            alternatives_text.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("错误", f"请求失败：{e}")


window = tk.Tk()
window.title("DeepLX 多语言翻译助手")
window.geometry("900x600")  # 增加一点高度来容纳新的框

control_frame = tk.Frame(window, pady=10)
control_frame.pack(fill=tk.X)

lang_frame = tk.Frame(control_frame)
lang_frame.pack(side=tk.LEFT, padx=10)

tk.Label(lang_frame, text="源语言：").pack(side=tk.LEFT)
source_lang_var = tk.StringVar(value="自动检测")
source_dropdown = ttk.Combobox(lang_frame, textvariable=source_lang_var, values=list(LANGUAGES.keys()), state="readonly", width=12)
source_dropdown.pack(side=tk.LEFT, padx=5)

tk.Label(lang_frame, text="→ 目标语言：").pack(side=tk.LEFT)
target_lang_var = tk.StringVar(value="中文")
target_dropdown = ttk.Combobox(lang_frame, textvariable=target_lang_var, values=list(LANGUAGES.keys()), state="readonly", width=12)
target_dropdown.pack(side=tk.LEFT, padx=5)

translate_btn = tk.Button(control_frame, text="翻 译", command=translate_text, height=1, width=10)
translate_btn.pack(side=tk.RIGHT, padx=15)

main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=4)
main_frame.rowconfigure(1, weight=1)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

tk.Label(left_frame, text="输入文本：").pack(anchor=tk.W)
input_text = scrolledtext.ScrolledText(left_frame, height=20)
input_text.pack(fill=tk.BOTH, expand=True)

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

tk.Label(right_frame, text="翻译结果：").pack(anchor=tk.W)
output_text = scrolledtext.ScrolledText(right_frame, height=20)
output_text.pack(fill=tk.BOTH, expand=True)

alternatives_frame = tk.Frame(main_frame)
alternatives_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

tk.Label(alternatives_frame, text="其他翻译建议：").pack(anchor=tk.W)
alternatives_text = scrolledtext.ScrolledText(alternatives_frame, height=5)  # 高度设置较小
alternatives_text.pack(fill=tk.BOTH, expand=True)

window.mainloop()
