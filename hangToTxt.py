# python hangToTxt.py d:\Enyim\mylearning\!DevOps hu mkv

# nvidia-smi

# Python 3.11
# FFmpeg szükséges! (lásd lent)
# pip install openai-whisper
# pip uninstall torch torchvision torchaudio -y
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121


import os
import sys
import shutil
import whisper
import torch
from datetime import datetime

# Globális változók
model = None
rootDir = None
parLang = None
fajlTipus = None  # 'mp4' vagy 'webm' stb. pont nélkül is jó

def info():
    print("Használat:")
    print("  hangToTxt.py <Könyvtár pl.: d:\\Liwi\\filmKonyvtár> <Nyelv pl.: en vagy hu> <Típus: webm vagy mp4>")
    print("Példa:")
    print("  hangToTxt.py d:\\Liwi\\filmKonyvtár en mp4")
    print("---- Rendszer infó ----")
    cuda_ok = torch.cuda.is_available()
    print("Videókártyát használja (torch.cuda.is_available()): " + str(cuda_ok))
    try:
        print("CUDA verzió (torch.version.cuda): " + str(torch.version.cuda))
    except Exception:
        print("CUDA verzió nem elérhető")
    try:
        if cuda_ok:
            print("GPU: " + torch.cuda.get_device_name(0))
        else:
            print("Nincs GPU")
    except Exception as e:
        print(f"GPU lekérdezési hiba: {e}")
    print("-----------------------")

def ellenoriz_ffmpeg():
    """Whisperhez FFmpeg kell. Ha nincs az elérési úton, jelezzük."""
    if shutil.which("ffmpeg") is None:
        print("\nFIGYELEM: Az FFmpeg nem található a PATH-ban! A Whisper hibára futhat video/audio beolvasáskor.")
        print("Windows telepítéshez pl.: https://www.gyan.dev/ffmpeg/builds/ vagy choco: choco install ffmpeg")
        print("Linux: sudo apt-get install ffmpeg   |   macOS: brew install ffmpeg\n")

def init():
    global model, rootDir, parLang, fajlTipus
    if len(sys.argv) == 4:
        rootDir = sys.argv[1]
        parLang = sys.argv[2]
        fajlTipus = sys.argv[3].lower().lstrip('.')  # 'mp4' vagy '.mp4' mindegy
        try:
            # Modellek: tiny, base, small, medium, large (small jó kompromisszum)
            # CPU-n: fp16=False kell
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Modell betöltése (small), eszköz: {device}")
            model = whisper.load_model("small", device=device)
            return True
        except Exception as e:
            print(f"Nem sikerült a modell betöltése: {e}")
            return False
    else:
        print("Hibás paraméterezés! (3 paraméter szükséges)")
        return False

def sec_to_minsec(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"

def segments_to_text(result):
    lines = []
    # A whisper.transcribe() result["segments"] listát ad
    for seg in result.get("segments", []):
        start = sec_to_minsec(seg.get("start", 0))
        end = sec_to_minsec(seg.get("end", 0))
        text = seg.get("text", "").strip()
        lines.append(f"[{start} --> {end}] {text}")
    return "\n".join(lines)

def magyar_datum():
    return datetime.now().strftime("%Y. %B %d.").replace(" 0", " ")

def magyar_datum_ido():
    # %Y = év, %B = hónap neve, %d = nap, %H:%M:%S
    datum = datetime.now().strftime("%Y. %B %d. %H:%M:%S")
    return datum.replace(" 0", " ")

def hangki(video):
    global model, parLang
    try:
        print(magyar_datum_ido())
        base_dir = os.path.dirname(video)
        base_name = os.path.splitext(os.path.basename(video))[0]
        txt_path = os.path.join(base_dir, base_name + ".txt")
        print(f"Kimenet: {txt_path}")

        # FP16 csak CUDA esetén
        use_cuda = torch.cuda.is_available()
        transcribe_kwargs = {
            "language": parLang,
            "verbose": True,
            "fp16": use_cuda,  # CPU-n fp16=False
        }

        # Átirat
        result = model.transcribe(video, **transcribe_kwargs)

        # Időbélyeges átírás
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(segments_to_text(result) + "\n")

        print(magyar_datum_ido())
    except Exception as e:
        print(f"Hiba a feldolgozás közben ({video}): {e}")

def main():
    global rootDir, fajlTipus
    print("Feldolgozás gyökérkönyvtára: " + str(rootDir))
    # Megengedjük: .mp4 / mp4 / .webm / webm
    endings = {fajlTipus, f".{fajlTipus}"}
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
            lower = filename.lower()
            if any(lower.endswith(end) for end in endings):
                full_path = os.path.join(dirpath, filename)
                print(f"Feldolgozás: {full_path}")
                hangki(full_path)

if __name__ == "__main__":
    # Windows-on cls, máshol clear – ha nem kell, kikommentezhető
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass

    info()
    ellenoriz_ffmpeg()
    if init():
        main()
    print("Kész")
