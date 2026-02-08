import os
import shutil
import sys
import subprocess
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

FORMATOS_AUDIO = {".mp3", ".wav", ".m4a", ".mp4", ".ogg", ".flac"}

# Caminhos comuns do ffmpeg no Windows (quando não está no PATH)
_CAMINHOS_FFMPEG_WIN = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg", "bin", "ffmpeg.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\ffmpeg\bin\ffmpeg.exe"),
    os.path.expandvars(r"%ProgramFiles%\ffmpeg\bin\ffmpeg.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\ffmpeg\bin\ffmpeg.exe"),
    r"C:\ffmpeg\bin\ffmpeg.exe",
]

# Duração máxima por chunk para o Google (segundos); áudios longos são divididos
DURACAO_CHUNK = 50


def _achar_ffmpeg():
    """Retorna o caminho do executável ffmpeg ou None se não encontrar."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    if sys.platform == "win32":
        for p in _CAMINHOS_FFMPEG_WIN:
            if p and os.path.isfile(p):
                return p
    return None


def _instrucoes_ffmpeg():
    print()
    print("  O ffmpeg não foi encontrado. Ele é necessário para converter este arquivo.")
    print("  1. Baixe: https://www.gyan.dev/ffmpeg/builds/ (ffmpeg-release-essentials.zip)")
    print("  2. Extraia (ex.: C:\\ffmpeg) e adicione ao PATH a pasta bin (ex.: C:\\ffmpeg\\bin)")
    print("  Ou coloque a pasta 'ffmpeg' com subpasta 'bin' e ffmpeg.exe na mesma pasta deste script.")
    print()


def _mp4_para_wav_ffmpeg(arquivo_entrada, arquivo_wav_saida):
    """Converte MP4/M4A para WAV usando ffmpeg (fallback quando pydub falha)."""
    ffmpeg_exe = _achar_ffmpeg()
    if not ffmpeg_exe:
        _instrucoes_ffmpeg()
        return False
    try:
        cmd = [
            ffmpeg_exe, "-y", "-i", os.path.abspath(arquivo_entrada),
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            os.path.abspath(arquivo_wav_saida)
        ]
        kw = {"capture_output": True, "timeout": 120}
        if sys.platform == "win32":
            kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        r = subprocess.run(cmd, **kw)
        if r.returncode != 0 or not os.path.isfile(arquivo_wav_saida):
            if r.stderr:
                print("  FFmpeg:", r.stderr.decode("utf-8", errors="replace")[:500])
            if not os.path.isfile(arquivo_wav_saida):
                _instrucoes_ffmpeg()
            return False
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        _instrucoes_ffmpeg()
        return False


def transcribe_audio(file_path):
    # Verificar se o arquivo existe
    if not os.path.isfile(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return False

    # Extrair a extensão do arquivo
    file_ext = os.path.splitext(file_path)[1].lower()

    # Carregar o arquivo de áudio e converter para WAV se necessário
    wav_criado_por_nos = False  # para apagar no final só se nós criarmos
    if file_ext in ['.mp3', '.mp4', '.m4a']:
        wav_path = os.path.splitext(file_path)[0] + '.wav'
        if file_ext == '.mp3':
            try:
                audio = AudioSegment.from_mp3(file_path)
                audio.export(wav_path, format='wav')
                wav_criado_por_nos = True
            except Exception:
                print("Erro ao converter MP3 com pydub.")
                return False
        elif file_ext in ('.mp4', '.m4a'):
            try:
                audio = AudioSegment.from_file(file_path, format='mp4')
                audio.export(wav_path, format='wav')
                wav_criado_por_nos = True
            except (IndexError, Exception):
                # Alguns MP4 (vídeo) quebram o pydub; usar ffmpeg
                print("Convertendo para WAV com ffmpeg...")
                fd, wav_path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                if not _mp4_para_wav_ffmpeg(file_path, wav_path):
                    if os.path.isfile(wav_path):
                        try:
                            os.remove(wav_path)
                        except OSError:
                            pass
                    print("Não foi possível converter o arquivo.")
                    return False
                wav_criado_por_nos = True
        else:
            try:
                audio = AudioSegment.from_file(file_path)
                audio.export(wav_path, format='wav')
                wav_criado_por_nos = True
            except Exception:
                print("Erro ao converter o arquivo com pydub.")
                return False
    elif file_ext == '.wav':
        wav_path = file_path
    else:
        print(f"Formato de arquivo não suportado: {file_ext}")
        return False

    # Inicializar o reconhecedor e transcrever
    recognizer = sr.Recognizer()
    print("Transcrevendo áudio (requer internet)...")

    try:
        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            textos = []
            while True:
                try:
                    chunk = recognizer.record(source, duration=DURACAO_CHUNK)
                except OSError:
                    break
                raw = chunk.get_raw_data()
                if not raw or len(raw) == 0:
                    break
                t = None
                for lang in ("pt-BR", "en-US"):
                    try:
                        t = recognizer.recognize_google(chunk, language=lang)
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(f"Erro na requisição ao serviço de reconhecimento: {e}")
                        break
                if t and t.strip():
                    textos.append(t)

        print()
        print("Transcrição:")
        if textos:
            print(" ".join(textos))
        else:
            print("(Nenhuma fala detectada. O áudio pode ser só música ou o reconhecimento não conseguiu entender.)")
    except Exception as e:
        print(f"Erro ao transcrever: {e}")
        import traceback
        traceback.print_exc()

    # Remover o arquivo WAV temporário, se tiver sido criado por nós
    if wav_criado_por_nos and os.path.isfile(wav_path):
        try:
            os.remove(wav_path)
        except OSError:
            pass
    return True


def transcrever_pasta(pasta):
    """Transcreve todos os arquivos de áudio na pasta."""
    if not os.path.isdir(pasta):
        print(f"Pasta não encontrada: {pasta}")
        return
    arquivos = sorted(f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f)))
    audios = [f for f in arquivos if os.path.splitext(f)[1].lower() in FORMATOS_AUDIO]
    if not audios:
        print(f"Nenhum arquivo de áudio encontrado na pasta: {pasta}")
        print("Formatos aceitos:", ", ".join(sorted(FORMATOS_AUDIO)))
        return
    for i, nome in enumerate(audios, 1):
        caminho = os.path.join(pasta, nome)
        print()
        print(f"--- [{i}/{len(audios)}] {nome} ---")
        transcribe_audio(caminho)
    print()
    print("Concluído.")


def _normalizar_alvo(alvo):
    """Converte nome da pasta atual ou '.' no caminho completo."""
    if not alvo:
        return alvo
    cwd = os.getcwd()
    # Pasta atual pelo nome (ex.: usuário digitou "contador pasta teste" estando dentro dela)
    if alvo == os.path.basename(cwd):
        return cwd
    # "." = pasta atual
    if alvo.strip() == ".":
        return cwd
    # Caminho relativo (ex.: .\arquivo.mp3 ou pasta\arquivo.mp3)
    if not os.path.isabs(alvo) and (os.path.isfile(alvo) or os.path.isdir(alvo)):
        return os.path.abspath(alvo)
    return alvo


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        alvo = sys.argv[1]
    else:
        print("  --- Transcrição de áudio ---")
        print()
        alvo = input("Digite o endereço do arquivo ou da pasta de áudio: ").strip()
        if not alvo:
            print("Nenhum endereço informado. Encerrando.")
            sys.exit(1)

    alvo = _normalizar_alvo(alvo)

    if os.path.isdir(alvo):
        transcrever_pasta(alvo)
    else:
        transcribe_audio(alvo)
