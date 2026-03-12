#python 3.11 kell hozzá!!!!

#pip install openai-whisper

#használat hangToTxt.py d:\Liwi\DevOpsServer en mp4

import os,sys
import whisper
import torch
from datetime import datetime

model = None
root_dir = None
parLang = None
fajlTipus = None

def info():
    print("Használat: hangToTxt.py <Könyvtár Pl: d:\Liwi\DevOpsServer> <Nyelv Pl: en vagy hu> <Tipus: webm vany mp4>")
    print("Használat: hangToTxt.py d:\Liwi\DevOpsServer en mp4")

    print("Video kértyát használja azaz torch.cuda.is_available(): "+str(torch.cuda.is_available()))
    print(torch.version.cuda)
    print(torch.cuda.get_device_name(1) if torch.cuda.is_available() else "Nincs GPU")

def get_input_folder():
    # Ha nincs paraméter → alapértelmezett mappa
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        return r"c:\temp"

    # Ha van paraméter → azt használjuk
    return sys.argv[1]

def init(): 
    #root_dir = r"c:\temp"
    #1) Modell betöltése
    if sys.argv.count==3:
        parLang=sys.argv[2]
        fajlTipus=sys.argv[3]
        model = whisper.load_model("small") # lehet: tiny, base, small, medium, large
        root_dir = get_input_folder()
        return True
    else:
        return False

def sec_to_minsec(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"

def segments_to_text(result):
    lines = []
    for seg in result["segments"]:
        start = sec_to_minsec(seg["start"])
        end = sec_to_minsec(seg["end"])
        text = seg["text"].strip()
        lines.append(f"[{start} --> {end}] {text}")
    return "\n".join(lines)

def magyar_datum():
    return datetime.now().strftime("%Y. %B %d.").replace(" 0", " ")

def magyar_datum_ido():
    # %Y = év, %B = hónap neve, %d = nap, %H:%M = óra:perc
    datum = datetime.now().strftime("%Y. %B %d. %H:%M:%S")
    # a felesleges nullát kivesszük a nap elől
    return datum.replace(" 0", " ")

def hangki(video):
    print(magyar_datum_ido())
    txt_path = os.path.basename(video)
    txt_path=txt_path.replace(sys.argv[3], ".txt")
    print(txt_path)

    # 2) Videó beolvasása és átirat készítése
    result = model.transcribe(video, language=parLang, verbose=True)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(segments_to_text(result)+ "\n\r")  # text volt!!

    print(magyar_datum_ido())
    
def main():
    print("main root_dir: "+root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(fajlTipus):
                full_path = os.path.join(dirpath, filename)
                print(full_path)
                hangki(full_path)

if __name__ == "__main__":
    os.system("cls")
    info()
    if(init()):
        main()
    print("Kész")