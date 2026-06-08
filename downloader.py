import sys
import os
import shutil
import yt_dlp


def check_ffmpeg():
    return shutil.which("ffmpeg") is not None


def download_video(url, audio_only=False, audio_format="webm", output_path="."):
    has_ffmpeg = check_ffmpeg()

    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }
        if audio_format == "m4a":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '0',
            }]
    elif has_ffmpeg:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def get_input(prompt, default=None, validator=None):
    while True:
        if default:
            user_input = input(f"  {prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"  {prompt}: ").strip()
            if not user_input:
                print("    Campo obrigatório.")
                continue

        if validator:
            try:
                return validator(user_input)
            except ValueError as e:
                print(f"    {e}")
                continue
        return user_input


def validate_url(url):
    url = url.strip()
    if not (url.startswith('http://') or url.startswith('https://')):
        raise ValueError("URL deve começar com http:// ou https://")
    if 'youtube.com' not in url and 'youtu.be' not in url:
        raise ValueError("URL deve ser do YouTube")
    return url


def validate_choice(choice, options):
    choice = choice.lower()
    if choice not in options:
        raise ValueError(f"Escolha entre: {', '.join(options)}")
    return choice


def validate_folder(folder):
    folder = folder.strip()
    if not folder:
        return "."
    full_path = os.path.abspath(folder)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def main():
    has_ffmpeg = check_ffmpeg()

    print()
    print("=" * 55)
    print("        YouTube Downloader - Melhor Qualidade")
    print("=" * 55)
    print()

    url = get_input("URL do vídeo", validator=validate_url)

    print()
    print("  Formato de saída:")
    print("    1 - Vídeo + Áudio (MP4)")
    print("    2 - Apenas Áudio")
    choice = get_input("Opção", default="1", validator=lambda x: validate_choice(x, ["1", "2"]))
    audio_only = (choice == "2")

    audio_format = "webm"
    if audio_only:
        print()
        if has_ffmpeg:
            print("  Formato do áudio:")
            print("    1 - WebM/Opus (original, sem conversão)")
            print("    2 - M4A/AAC (convertido, melhor compatibilidade)")
            fmt = get_input("Opção", default="1", validator=lambda x: validate_choice(x, ["1", "2"]))
            audio_format = "m4a" if fmt == "2" else "webm"
        else:
            print("  (ffmpeg não encontrado - usando formato original WebM/Opus)")

    print()
    folder = get_input("Pasta de destino", default="downloads", validator=validate_folder)

    print()
    print("-" * 55)
    print(f"  URL:    {url}")
    if audio_only:
        print(f"  Tipo:   Apenas áudio ({audio_format.upper()})")
    else:
        print(f"  Tipo:   Vídeo + Áudio (MP4)")
    print(f"  Pasta:  {folder}")
    print("-" * 55)
    print()

    confirm = get_input("Iniciar download? [S/n]", default="s", validator=lambda x: validate_choice(x.lower(), ["s", "n", "sim", "nao", "não"]))
    if confirm.lower() in ["n", "nao", "não"]:
        print("\n  Cancelado.")
        return

    print()
    print("  Baixando...")
    print()

    try:
        download_video(url, audio_only, audio_format, folder)
        print()
        print("=" * 55)
        print("  ✓ Download concluído!")
        print(f"  ✓ Pasta: {os.path.abspath(folder)}")
        print("=" * 55)
        print()
    except Exception as e:
        print()
        print("=" * 55)
        print(f"  ✗ Erro: {e}")
        print("=" * 55)
        print()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Cancelado pelo usuário.")
        sys.exit(0)