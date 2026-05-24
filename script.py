"""
Verilog SOC Solver (Gemini)
- Ctrl+Shift+L : salveaza fisierul .v copiat (poti apela de mai multe ori pentru fisiere multiple)
- Ctrl+Shift+K : rezolva si pune solutia in clipboard
- Ctrl+Alt+T : toggle stealth typing - fiecare tasta apasata scrie urmatorul caracter din solutie
- Ctrl+Shift+R : reseteaza
- Ctrl+Shift+Q : inchide scriptul
"""

import os
import re
import pyperclip
import keyboard
from google import genai
from google.genai import types

# ===== CONFIG =====
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
# ==================

client = genai.Client(api_key=API_KEY)

stored_file = {"text": None}
solution_buffer = {"text": None, "index": 0, "active": False}

SYSTEM_PROMPT = """You are a Verilog HDL expert solving a lab/exam problem.

You will receive one or more .v file contents (the problem skeleton and possibly a testbench).

Your task: implement the body of the 'solution' module (or the module the problem skeleton asks you to implement) so the testbench passes.

CRITICAL output rules:
- Respond with ONLY the Verilog code for the solution module, nothing else
- Keep the EXACT module declaration (name, port list, widths, types) from the skeleton
- Do NOT include the testbench in your output
- Do NOT include the problem statement comments
- NO comments anywhere in the code (no //, no /* */)
- NO blank lines between logically related statements - write compact code
- DO NOT vertically align '=' or '<=' across multiple lines - write naturally:
  BAD:  a   = 1;
        bcd = 2;
  GOOD: a = 1;
        bcd = 2;
- Use 4-space indentation
- Write as a student would write quickly: compact, minimal whitespace, no decorative alignment
- Use standard Verilog-2001 syntax unless the skeleton clearly uses SystemVerilog
- The code must synthesize and pass all testbench cases"""


def extract_code(text: str) -> str:
    fence = re.search(r"```(?:verilog|systemverilog|sv|v)?\s*\n(.*?)```", text, re.DOTALL)
    return fence.group(1).strip() if fence else text.strip()


def call_gemini(file_content: str) -> str:
    for attempt in range(3):
        response = client.models.generate_content(
            model=MODEL,
            contents=file_content,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )
        solution = extract_code(response.text)
        if "module" in solution and "endmodule" in solution:
            return solution
        print(f"[!] Raspuns incomplet (attempt {attempt+1}), reincerc...")
    raise Exception("Nu am reusit sa obtin o solutie completa dupa 3 incercari.")


# ===== HOTKEY HANDLERS =====

def capture_file():
    text = pyperclip.paste()
    if not text or len(text.strip()) < 20:
        print("[!] Clipboard gol sau prea scurt.")
        return

    if stored_file["text"] is None:
        stored_file["text"] = text
        count = 1
    else:
        stored_file["text"] += "\n\n// ===== NEXT FILE =====\n\n" + text
        count = stored_file["text"].count("===== NEXT FILE =====") + 1

    print(f"[+] Fisier #{count} salvat ({len(text)} chars). "
          f"Total: {len(stored_file['text'])} chars.")
    print("    Mai apasa Ctrl+Shift+L pentru alt fisier, sau Ctrl+Shift+K pentru solutie.")


def solve():
    file_content = stored_file["text"]
    if not file_content:
        print("[!] N-ai salvat fisierul inca. Apasa Ctrl+Shift+L pe el intai.")
        return

    print(f"[2/2] Trimit la Gemini ({len(file_content)} chars)...")
    try:
        solution = call_gemini(file_content)
        pyperclip.copy(solution)
        solution_buffer["text"] = solution
        solution_buffer["index"] = 0
        solution_buffer["active"] = False
        stored_file["text"] = None
        print(f"[OK] Solutia ({len(solution)} chars) e in clipboard.")
        print("     Apasa Ctrl+Shift+T in editor pentru stealth typing.")
    except Exception as e:
        print(f"[ERR] {e}")


def toggle_typing():
    if not solution_buffer["text"]:
        print("[!] Nu exista o solutie. Ruleaza Ctrl+Shift+K intai.")
        return
    solution_buffer["active"] = not solution_buffer["active"]
    if solution_buffer["active"]:
        remaining = len(solution_buffer["text"]) - solution_buffer["index"]
        print(f"[T] STEALTH TYPING PORNIT. {remaining} chars ramase. "
              f"Apasa orice tasta in editor. Ctrl+Shift+T = stop.")
    else:
        print(f"[T] STEALTH TYPING OPRIT la indexul {solution_buffer['index']}/{len(solution_buffer['text'])}.")


def reset():
    stored_file["text"] = None
    solution_buffer["text"] = None
    solution_buffer["index"] = 0
    solution_buffer["active"] = False
    print("[R] Reset complet.")


def quit_script():
    print("[Q] Inchid...")
    os._exit(0)


# ===== STEALTH TYPING ENGINE =====

PASSTHROUGH_KEYS = {
    "ctrl", "alt", "shift",
    "left ctrl", "right ctrl", "left alt", "right alt",
    "left shift", "right shift", "left windows", "right windows",
    "esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "print screen", "scroll lock", "pause", "insert", "delete",
    "home", "end", "page up", "page down",
    "up", "down", "left", "right",
    "caps lock", "num lock", "backspace"
}


def on_key_event(event):
    if event.event_type != "down":
        return True
    if not solution_buffer["active"]:
        return True
    if event.name in PASSTHROUGH_KEYS:
        return True
    if keyboard.is_pressed("ctrl") or keyboard.is_pressed("alt") or keyboard.is_pressed("windows"):
        return True

    if solution_buffer["index"] >= len(solution_buffer["text"]):
        solution_buffer["active"] = False
        print("[T] Solutie scrisa complet. Stealth typing oprit.")
        return True

    char = solution_buffer["text"][solution_buffer["index"]]
    solution_buffer["index"] += 1
    keyboard.write(char)
    if char == '\n':
        # dupa newline, sterge auto-indent-ul editorului
        keyboard.send("home")
        keyboard.send("shift+end")
        keyboard.send("delete")
    return False


# ===== MAIN =====

def main():
    if not API_KEY:
        print("Seteaza GEMINI_API_KEY ca variabila de mediu.")
        return

    print(f"Verilog SOC Solver activ (model: {MODEL}).")
    print("  Ctrl+Shift+L -> salveaza fisierul .v copiat (apeleaza de mai multe ori pentru fisiere multiple)")
    print("  Ctrl+Shift+K -> rezolva si pune solutia in clipboard")
    print("  Ctrl+Alt+T -> toggle stealth typing")
    print("  Ctrl+Shift+R -> reseteaza")
    print("  Ctrl+Shift+Q -> inchide")
    print()

    keyboard.add_hotkey("ctrl+shift+l", capture_file)
    keyboard.add_hotkey("ctrl+shift+k", solve)
    keyboard.add_hotkey("ctrl+alt+t", toggle_typing)
    keyboard.add_hotkey("ctrl+shift+r", reset)
    keyboard.add_hotkey("ctrl+shift+q", quit_script)

    keyboard.hook(on_key_event, suppress=True)
    keyboard.wait()


if __name__ == "__main__":
    main()