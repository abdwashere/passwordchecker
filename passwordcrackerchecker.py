import tkinter as tk
from tkinter import messagebox
import math
import string
import re

# ── Forward declarations (silences Pylance) ──────────────────────────────────
entry_pw:         tk.Entry
lbl_classical_res: tk.Label
lbl_quantum_res:   tk.Label
lbl_grade:         tk.Label
lbl_warnings:      tk.Label
meter_canvas:      tk.Canvas
meter_bar:         int

# ── Top-500 common / leaked passwords ────────────────────────────────────────
COMMON_PASSWORDS = {
    "123456","password","123456789","12345678","12345","1234567","1234567890",
    "qwerty","abc123","111111","123123","admin","letmein","monkey","1234",
    "dragon","master","sunshine","princess","welcome","shadow","superman",
    "michael","football","iloveyou","trustno1","batman","pass","hello",
    "charlie","donald","password1","qwerty123","qwertyuiop","1q2w3e4r",
    "123qwe","zxcvbnm","asdfghjkl","password123","123456a","a123456",
    "666666","7777777","1000000","123321","654321","123abc","987654321",
    "pass123","login","test","guest","root","toor","admin123","adminadmin",
    "qazwsx","1q2w3e","aaaaaa","abc","abcdef","abcd1234","abcdefg",
    "baseball","basketball","soccer","hockey","tennis","golf","pokemon",
    "nintendo","minecraft","roblox","fortnite","starwars","matrix",
    "whatever","nothing","anything","something","everything","mypassword",
    "passpass","passwort","passwd","security","computer","internet",
    "windows","linux","ubuntu","google","facebook","twitter","instagram",
    "summer","winter","spring","autumn","january","february","march",
    "april","may","june","july","august","september","october","november",
    "december","monday","tuesday","wednesday","thursday","friday","saturday",
    "sunday","sunshine","rainbow","thunder","lightning","tornado","hurricane",
    "qweasdzxc","1234qwer","zaq1xsw2","!qaz2wsx","q1w2e3r4","1qaz2wsx",
    "000000","11111111","222222","333333","444444","555555","777777",
    "888888","999999","121212","696969","1111111","11111","0000",
    "112233","123654","159357","123123123","321321","111222","112211",
    "2580","0987654321","9876543210","1234554321","1111111111","0123456789",
    "love","sex","god","money","time","life","death","hell","fire","ice",
    "blue","red","green","black","white","orange","purple","yellow","pink",
    "maverick","merlin","thomas","jordan","hunter","ranger","harley","eagle",
    "tiger","bear","wolf","lion","shark","falcon","cobra","viper","raven",
    "phoenix","matrix","neo","trinity","morpheus","agent","smith","oracle",

    # ── South Asia (Pakistan / India / Bangladesh / Sri Lanka / Nepal) ─────────
    # Religious & spiritual
    "allah","allah123","allah1","bismillah","mashallah","inshallah",
    "alhamdulillah","subhanallah","yarabi","yallah","muhammad","muhammad1",
    "muhammad123","mohammed","mohammed1","mohammed123","mohammad","mohammad1",
    "ahmad","ahmed","ahmed123","ali","ali123","ali1234","aliali",
    "usman","usman123","umer","umer123","bilal","bilal123","hassan","hussain",
    "fatima","fatima123","khadija","ayesha","ayesha123","maryam","maryam123",
    "zainab","zainab123","rama","krishna","krishna123","shiva","vishnu",
    "ganesh","ganesh123","hanuman","durga","lakshmi","saraswati",
    "jai","jaihind","vande","vandemataram","bharat","bharat123",
    "hindustan","pakistan","pakistan1","pakistan123","pak123","pak1",
    "india","india123","india1","bharat1","bangladesh","bangladesh1",

    # Common South Asian names (male)
    "rahul","rahul123","rohit","rohit123","amit","amit123","raj","raj123",
    "rajan","rajesh","rajesh123","suresh","suresh123","ramesh","ramesh123",
    "mahesh","mukesh","dinesh","ganesh1","rakesh","naresh","vikas","vikram",
    "arjun","arjun123","ravi","ravi123","sanjay","sanjay123","ajay","vijay",
    "nikhil","akhil","ankit","ankur","anil","anil123","kapil","kapil123",
    "deepak","deepak123","manish","manish123","pradeep","praveen","girish",
    "imran","imran123","ali123456","zaid","zaid123","hamza","hamza123",
    "omar","omar123","tariq","tariq123","asif","asif123","asad","asad123",
    "waheed","waheed123","naveed","naveed123","rashid","rashid123",
    "shahid","shahid123","khalid","khalid123","sajid","sajid123",
    "waqas","waqas123","faisal","faisal123","kamran","kamran123",
    "farhan","farhan123","danish","danish123","hassan123","talha","talha123",
    "rana","rana123","raja","raja123","baig","khan","khan123","khan1",
    "sheikh","sheikh123","malik","malik123","chaudhry","chaudhary",
    "arif","arif123","nasir","nasir123","tahir","tahir123","zahid",
    "zahid123","irfan","irfan123","adnan","adnan123","salman","salman123",
    "furqan","furqan123","suleman","suleman123","ibrahim","ibrahim123",

    # Common South Asian names (female)
    "priya","priya123","pooja","pooja123","neha","neha123","anjali",
    "anjali123","divya","divya123","sunita","sunita123","kavita","kavita123",
    "geeta","geeta123","rekha","rekha123","nisha","nisha123","swati",
    "komal","komal123","sana","sana123","sara","sara123","hina","hina123",
    "nadia","nadia123","rabia","rabia123","amna","amna123","saima",
    "saima123","sumera","sumera123","mehwish","mehwish123","zara","zara123",
    "layla","layla123","mariam","mariam123","noor","noor123","iqra",
    "iqra123","aroha","aroha123","mahnoor","mahnoor123",

    # Cities & places
    "lahore","lahore123","karachi","karachi1","karachi123","islamabad",
    "islamabad1","rawalpindi","rawalpindi1","peshawar","peshawar1",
    "multan","multan123","faisalabad","faisalabad1","quetta","quetta1",
    "mumbai","mumbai123","delhi","delhi123","newdelhi","kolkata","kolkata1",
    "chennai","chennai1","bangalore","bangalore1","hyderabad","hyderabad1",
    "pune","pune123","ahmedabad","ahmedabad1","dhaka","dhaka123",
    "chittagong","chittagong1","kathmandu","kathmandu1","colombo","colombo1",

    # Cricket (massive in South Asia)
    "cricket","cricket123","cricket1","icc","bcci","pcb","virat","virat18",
    "kohli","kohli18","sachin","sachin10","tendulkar","dhoni","dhoni7",
    "ms7","msd7","rohit45","bumrah","babar","babar56","babarazam",
    "shaheen","afridi","afridi10","shoaib","waqar","wasim","imrankhan",
    "worldcup","worldcup2023","ipl","psl","psl2024","t20","t20world",

    # Bollywood / culture
    "bollywood","shahrukh","srk","srkfan","salmankhan","aamir","hrithik",
    "deepika","priyanka","kareena","katrina","ranveer","ranbir","amitabh",
    "bachchan","dilwale","ddlj","kuchkuchhotahai","devdas","mughalazam",

    # Common Urdu/Hindi words romanised
    "pyaar","mohabbat","dosti","yaar","yaara","yaaraa","bhai","bhai123",
    "bhaijaan","behan","dil","dilse","zindagi","zindagi1","duniya",
    "khuda","khudahafiz","hafiz","hafiz123","meri","mera","tera",
    "apna","apni","shukriya","shukria","meherbani","jazakallah",
    "mashallah1","subhan","subhanallah1","allahuakbar","allahuakbar1",
    "bismillah1","kalma","shahada","namaz","namaz123","rozay","roza",
    "eid","eid123","eidmubarak","ramazan","ramzan","ramzan123",

    # Number patterns common in South Asia (phone/ID combos)
    "03001234567","03211234567","03331234567","03121234567",
    "00923001234","9876543210","9123456789","8123456789",
    "1947","14august","14aug1947","pakistan1947","india1947",
    "1971","16december","16dec1971",
}

# ── Keyboard walk patterns ────────────────────────────────────────────────────
KEYBOARD_WALKS = [
    "qwerty","qwert","werty","asdf","asdfg","zxcv","zxcvb",
    "qazwsx","1qaz","2wsx","3edc","4rfv","5tgb","6yhn","7ujm",
    "qwertyuiop","asdfghjkl","zxcvbnm",
    "1234","12345","123456","1234567","12345678","123456789",
    "0987","9876","98765","987654","9876543","98765432",
    "abcd","abcde","abcdef","abcdefg","abcdefgh",
]

# ── Leet-speak normalisation map ─────────────────────────────────────────────
LEET_MAP = str.maketrans({
    "@": "a", "3": "e", "1": "i", "!": "i",
    "4": "a", "|": "l", "0": "o", "5": "s", "$": "s", "+": "t",
    "7": "t", "8": "b", "6": "g", "9": "g",
})

# ── Charset helper ────────────────────────────────────────────────────────────
def get_charset_size(password: str) -> int:
    size = 0
    if any(c in string.ascii_lowercase for c in password): size += 26
    if any(c in string.ascii_uppercase for c in password): size += 26
    if any(c in string.digits            for c in password): size += 10
    if any(c in string.punctuation       for c in password): size += 32
    if any(ord(c) > 127                  for c in password): size += 128
    return max(size, 1)

# ── Pattern / dictionary analysis ────────────────────────────────────────────
def analyse_password(password: str) -> tuple[int, list[str]]:
    """
    Returns (penalty_bits, list_of_warning_strings).
    penalty_bits is subtracted from effective entropy before crack-time calc.
    """
    warnings: list[str] = []
    penalty  = 0
    low      = password.lower()
    deleet   = low.translate(LEET_MAP)   # leet-normalised version

    # 1. Length
    if len(password) < 6:
        warnings.append("Too short (< 6 chars)")
        penalty += 20
    elif len(password) < 8:
        warnings.append("Short (< 8 chars)")
        penalty += 10

    # 2. Only one character class
    classes = sum([
        any(c in string.ascii_lowercase for c in password),
        any(c in string.ascii_uppercase for c in password),
        any(c in string.digits           for c in password),
        any(c in string.punctuation      for c in password),
    ])
    if classes == 1:
        warnings.append("Only one character type used")
        penalty += 15
    elif classes == 2:
        warnings.append("Only two character types used")
        penalty += 5

    # 3. Common password (direct)
    if low in COMMON_PASSWORDS:
        warnings.append("Found in leaked password list!")
        penalty += 40

    # 4. Common password after leet-speak normalisation
    elif deleet in COMMON_PASSWORDS:
        warnings.append("Leet-speak variant of a common password")
        penalty += 30

    # 5. Keyboard walks
    for walk in KEYBOARD_WALKS:
        if walk in low:
            warnings.append(f'Keyboard pattern detected ("{walk}…")')
            penalty += 20
            break

    # 6. Repeated characters  (aaa / 111 / ababab)
    if re.search(r'(.)\1{2,}', password):
        warnings.append("Repeated characters detected (e.g. aaa)")
        penalty += 15

    # 7. Sequential digits / letters
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', low):
        warnings.append("Sequential characters detected")
        penalty += 10

    # 8. All-digit password
    if password.isdigit():
        warnings.append("Digits only — very easy to crack")
        penalty += 20

    return penalty, warnings

# ── Grade from effective entropy ─────────────────────────────────────────────
def get_grade(effective_bits: float) -> tuple[str, str]:
    """Returns (letter_grade, hex_colour)."""
    if effective_bits < 20:  return "F",  "#FF3333"
    if effective_bits < 30:  return "D",  "#FF6633"
    if effective_bits < 40:  return "C",  "#FFAA00"
    if effective_bits < 50:  return "B",  "#CCFF00"
    if effective_bits < 65:  return "A",  "#55FF55"
    return                          "A+", "#00FFCC"

# ── Meter update ──────────────────────────────────────────────────────────────
METER_W = 340
METER_H = 18

def update_meter(effective_bits: float) -> None:
    pct   = min(effective_bits / 80, 1.0)   # 80 bits = full bar
    width = max(int(pct * METER_W), 4)

    # Interpolate red → yellow → green
    if pct < 0.5:
        r, g = 255, int(pct * 2 * 200)
    else:
        r, g = int((1 - pct) * 2 * 255), 200
    colour = f"#{r:02x}{g:02x}00"

    meter_canvas.coords(meter_bar, 0, 0, width, METER_H)
    meter_canvas.itemconfig(meter_bar, fill=colour)

# ── Time formatter ────────────────────────────────────────────────────────────
def format_time(seconds: float) -> str:
    if seconds < 1e-6: return "Instant (<1 µs)"
    if seconds < 1:    return f"{seconds*1000:.3f} Milliseconds"
    if seconds < 60:   return f"{seconds:.2f} Seconds"
    m = seconds / 60
    if m < 60:         return f"{m:.2f} Minutes"
    h = m / 60
    if h < 24:         return f"{h:.2f} Hours"
    d = h / 24
    if d < 365.25:     return f"{d:.2f} Days"
    y = d / 365.25
    if y < 1e3:        return f"{y:,.1f} Years"
    if y < 1e6:        return f"{y/1e3:,.1f} Thousand Years"
    if y < 1e9:        return f"{y/1e6:,.1f} Million Years"
    if y < 1e12:       return f"{y/1e9:,.1f} Billion Years"
    return "Longer than the age of the universe"

# ── Main calculation ──────────────────────────────────────────────────────────
def calculate_time() -> None:
    password = entry_pw.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password!")
        return

    # Raw entropy
    charset_size  = get_charset_size(password)
    entropy_bits  = len(password) * math.log2(charset_size)

    # Penalty & warnings
    penalty, warnings = analyse_password(password)
    effective_bits = max(entropy_bits - penalty, 0)

    avg_combinations = (2 ** effective_bits) / 2

    # Classical (GPU cluster, fast hash)
    seconds_classical = avg_combinations / 1e11

    # Quantum – Grover's √N speedup, ~1 MHz gate ops
    seconds_quantum = math.sqrt(avg_combinations) / 1e6

    # Grade
    grade, grade_colour = get_grade(effective_bits)

    # Update UI
    lbl_classical_res.config(text=format_time(seconds_classical), fg="#FF5555")
    lbl_quantum_res.config(text=format_time(seconds_quantum),   fg="#55FF55")
    lbl_grade.config(
        text=f"Grade: {grade}   |   Entropy: {effective_bits:.1f} bits",
        fg=grade_colour
    )

    if warnings:
        lbl_warnings.config(text="⚠  " + "   •   ".join(warnings), fg="#FFAA00")
    else:
        lbl_warnings.config(text="✔  No common patterns detected", fg="#55FF55")

    update_meter(effective_bits)

# ── Toggle show/hide password ─────────────────────────────────────────────────
def toggle_pw() -> None:
    if entry_pw.cget("show") == "*":
        entry_pw.config(show="")
        btn_toggle.config(text="🙈")
    else:
        entry_pw.config(show="*")
        btn_toggle.config(text="👁")

# ══════════════════════════════════════════════════════════════════════════════
#  GUI  (layout identical to original — only new rows appended)
# ══════════════════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("Quantum vs Classical Cracker")
root.geometry("440x560")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

title_font  = ("Arial", 16, "bold")
label_font  = ("Arial", 10)
small_font  = ("Arial",  8)

tk.Label(root, text="Password Strength Simulator",
         font=title_font, bg="#1e1e1e", fg="white", pady=16).pack()

tk.Label(root, text="Enter Password to Test:",
         font=label_font, bg="#1e1e1e", fg="#aaaaaa").pack()

# Password row (entry + eye toggle)
pw_frame = tk.Frame(root, bg="#1e1e1e")
pw_frame.pack(pady=6)

entry_pw = tk.Entry(pw_frame, font=("Arial", 14), show="*", width=22)
entry_pw.pack(side=tk.LEFT, padx=(0, 6))

btn_toggle = tk.Button(pw_frame, text="👁", command=toggle_pw,
                       bg="#333333", fg="white", relief=tk.FLAT,
                       font=("Arial", 13), cursor="hand2")
btn_toggle.pack(side=tk.LEFT)

btn_calc = tk.Button(root, text="Calculate Crack Time", command=calculate_time,
                     bg="#007acc", fg="white",
                     font=("Arial", 10, "bold"), padx=20, pady=5)
btn_calc.pack(pady=14)

# ── Strength meter ────────────────────────────────────────────────────────────
tk.Label(root, text="Password Strength:", bg="#1e1e1e", fg="#aaaaaa",
         font=small_font).pack()

meter_canvas = tk.Canvas(root, width=METER_W, height=METER_H,
                         bg="#333333", highlightthickness=0)
meter_canvas.pack(pady=(2, 8))
meter_bar = meter_canvas.create_rectangle(0, 0, 0, METER_H, fill="#555555", outline="")

# ── Grade + entropy ───────────────────────────────────────────────────────────
lbl_grade = tk.Label(root, text="Grade: ---",
                     font=("Courier", 11, "bold"), bg="#1e1e1e", fg="#aaaaaa")
lbl_grade.pack(pady=(0, 6))

# ── Original result labels ────────────────────────────────────────────────────
tk.Label(root, text="Time for Normal Computer (GPU):",
         bg="#1e1e1e", fg="white").pack()
lbl_classical_res = tk.Label(root, text="---",
                              font=("Courier", 12, "bold"), bg="#1e1e1e")
lbl_classical_res.pack(pady=4)

tk.Label(root, text="Time for Quantum Computer (Grover's):",
         bg="#1e1e1e", fg="white").pack()
lbl_quantum_res = tk.Label(root, text="---",
                            font=("Courier", 12, "bold"), bg="#1e1e1e")
lbl_quantum_res.pack(pady=4)

# ── Warnings ──────────────────────────────────────────────────────────────────
lbl_warnings = tk.Label(root, text="",
                         font=("Arial", 8), bg="#1e1e1e", fg="#FFAA00",
                         wraplength=400, justify=tk.CENTER)
lbl_warnings.pack(pady=(8, 4))

root.mainloop()