# Local LoRA Training Guide (Low VRAM Edition)

Wir nutzen **Ostris AI-Toolkit**. Das ist aktuell das effizienteste Tool für Flux-Training und ermöglicht durch Optimierungen (Gradient Checkpointing, 8-bit Optimizer) das Training auf 12GB Karten.

## 1. Installation
Da Training eine andere Umgebung braucht als ComfyUI, installieren wir es separat.

### Voraussetzungen
- [Python 3.10 oder 3.11](https://www.python.org/downloads/) installiert?
- [Git](https://git-scm.com/) installiert?

### Schritt-für-Schritt
1.  Öffne ein Terminal in: `C:\Users\k4_PC\Projekte\ai_influencer`
2.  Clone das Repo:
    ```powershell
    git clone https://github.com/ostris/ai-toolkit.git
    cd ai-toolkit
    ```
3.  Erstelle eine virtuelle Umgebung (damit wir ComfyUI nicht zerschießen):
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  Installiere Dependencies:
    ```powershell
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    pip install -r requirements.txt
    ```

## 2. Low VRAM Config (Der Trick)
Ich werde dir eine spezielle Konfigurationsdatei (`config_lena.yaml`) erstellen.
**Die kritischen Einstellungen für deine 3080 Ti:**
- `batch_size: 1` (Langsam, aber speicherschonend)
- `gradient_checkpointing: true` (Spart massiv VRAM)
- `optimizer: adamw8bit` (Braucht weniger RAM als normaler Adam)
- `quantize: true` (Wir laden das Base-Model in FP8)

## 3. Training starten
Befehl wird sein:
`python run.py config_lena.yaml`

Dauer: Vermutlich 2-4 Stunden (perfekt für über Nacht).
