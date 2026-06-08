# YouTube Downloader

Script em Python para baixar vídeos e áudios do YouTube em alta qualidade.

## Requisitos

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/download.html) _(opcional, apenas para converter áudio para M4A)_

## Instalação

```bash
# Instalar yt-dlp
pip install yt-dlp

# ou
python -m pip install yt-dlp
```

Para o modo áudio em M4A, instale o ffmpeg:

```bash
# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg

# macOS (Homebrew)
brew install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg
```

## Uso

```bash
python downloader.py
```

O script é totalmente interativo e vai perguntar:

1. **URL do vídeo** - cole o link do YouTube
2. **Formato de saída**
   - `1` - Vídeo + Áudio (MP4)
   - `2` - Apenas Áudio
3. **Formato do áudio** _(apenas se escolheu áudio)_
   - `1` - WebM/Opus _(original, sem conversão, não precisa ffmpeg)_
   - `2` - M4A/AAC _(convertido, melhor compatibilidade, precisa ffmpeg)_
4. **Pasta de destino** - padrão: `downloads`
5. **Confirmação** - `S` para iniciar

## Exemplos

```
URL do vídeo: https://www.youtube.com/watch?v=VIDEO_ID

Opção [1]: 2

Formato do áudio:
  1 - WebM/Opus (original, sem conversão)
  2 - M4A/AAC (convertido, melhor compatibilidade)
Opção [1]: 2

Pasta de destino [downloads]: musicas

Iniciar download? [S/n]: S
```

## Estrutura

```
Projetos-Git/
├── downloader.py    # Script principal
├── README.md        # Este arquivo
└── downloads/       # Pasta padrão de downloads
```

## Notas

- **Sem ffmpeg**: o áudio é baixado no formato original (WebM/Opus)
- **Com ffmpeg**: pode converter para M4A/AAC
- **Vídeo**: sempre baixa em MP4 com a melhor qualidade disponível
- A pasta de destino é criada automaticamente se não existir
- Pressione `Ctrl+C` a qualquer momento para cancelar
