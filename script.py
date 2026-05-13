"""
Clipboard LeetCode Solver (Gemini version)
- Ctrl+Shift+L: salveaza enuntul din clipboard
- Ctrl+Shift+K: ia antetul din clipboard, combina cu enuntul, trimite la Gemini
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

# state global
stored_problem = {"text": None}

SYSTEM_PROMPT = """You are a competitive programming assistant solving a LeetCode problem.

You will receive:
1. PROBLEM: the problem statement
2. SIGNATURE: the exact function signature/class template from LeetCode

Output requirements:
- Respond with ONLY C++ code, nothing else
- NO comments of any kind (no // comments, no /* */ comments)
- No markdown fences, no explanations, no prose
- Use EXACTLY the signature provided (same class name, function name, parameter names, return type)
- Include any necessary #include directives and using namespace std; if needed
- Add helper functions/members inside the class if needed
- Code must be optimal for the given constraints
- ABSOLUTELY NO COMMENTS. Not a single // or /* anywhere in the output."""


def extract_code(text: str) -> str:
    fence = re.search(r"```(?:cpp|c\+\+)?\s*\n(.*?)```", text, re.DOTALL)
    return fence.group(1).strip() if fence else text.strip()


def capture_problem():
    text = pyperclip.paste()
    if not text or len(text.strip()) < 20:
        print("[!] Clipboard gol sau prea scurt pentru enunt.")
        return
    stored_problem["text"] = text
    print(f"[1/2] Enunt salvat ({len(text)} chars). Acum copiaza antetul si apasa Ctrl+Shift+K.")


def solve_with_signature():
    signature = pyperclip.paste()
    problem = stored_problem["text"]

    if not problem:
        print("[!] N-ai salvat enuntul inca. Apasa Ctrl+Shift+L pe el intai.")
        return
    if not signature or len(signature.strip()) < 10:
        print("[!] Clipboard gol sau prea scurt pentru antet.")
        return

    user_msg = f"PROBLEM:\n{problem}\n\nSIGNATURE:\n{signature}"
    print(f"[2/2] Trimit la Gemini (problem: {len(problem)}, sig: {len(signature)} chars)...")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=user_msg,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=8192,
                ),
            )
            solution = extract_code(response.text)

            if solution.count('{') != solution.count('}'):
                print(f"[!] Raspuns incomplet (attempt {attempt+1}), reincerc...")
                continue

            pyperclip.copy(solution)
            stored_problem["text"] = None
            print(f"[✓] Gata. Solutia ({len(solution)} chars) e in clipboard.")
            return
        except Exception as e:
            print(f"[✗] Eroare: {e}")
            return

    print("[✗] Nu am reusit sa obtin o solutie completa dupa 3 incercari.")

def quit_app():
    print("[Q] Inchid...")
    import subprocess
    os._exit(0)


def main():
    if not API_KEY:
        print("Seteaza GEMINI_API_KEY ca variabila de mediu.")
        return
    print(f"Clipboard LeetCode Solver activ (model: {MODEL}).")
    print("  Ctrl+Shift+L -> salveaza enuntul copiat")
    print("  Ctrl+Shift+K -> trimite enuntul + antetul copiat la AI")
    print("  Ctrl+Shift+Q -> inchide scriptul si consola")
    print("Ctrl+C aici ca sa inchizi.")
    keyboard.add_hotkey("ctrl+shift+l", capture_problem)
    keyboard.add_hotkey("ctrl+shift+k", solve_with_signature)
    keyboard.add_hotkey("ctrl+shift+q", quit_app)
    keyboard.wait()


if __name__ == "__main__":
    main()