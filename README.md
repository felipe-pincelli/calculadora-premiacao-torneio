# Calculadora de Premiação

Aplicativo desktop para Windows que calcula a divisão de premiação de torneios
de card games a partir da quantidade de jogadores e do valor da inscrição.

## Regras de premiação

- **Arrecadação total** = quantidade de jogadores × valor da inscrição
- **Menos de 10 jogadores** (Top 3): 1º 50% / 2º 30% / 3º 20%
- **10 jogadores ou mais** (Top 4): 1º 40% / 2º 30% / 3º 20% / 4º 10%

## Rodando em modo desenvolvimento

Requer Python 3.10+ instalado.

```powershell
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python main.py
```

## Gerando o executável (.exe)

```powershell
.\build.ps1
```

Isso gera `dist\CalculadoraPremiacao.exe` — um arquivo único, sem instalador,
que roda em qualquer Windows sem precisar de Python instalado (todas as
dependências, incluindo o Tcl/Tk do CustomTkinter, ficam embutidas no
próprio .exe via PyInstaller `--onefile`).

Se quiser rodar o PyInstaller manualmente em vez de usar `build.ps1`, o
comando equivalente é:

```powershell
venv\Scripts\pyinstaller --noconfirm --onefile --windowed `
  --name "CalculadoraPremiacao" `
  --icon "assets/icon.ico" `
  --add-data "assets;assets" `
  --collect-all customtkinter `
  main.py
```

## Estrutura do projeto

```
main.py                     Ponto de entrada — cria a janela e inicia o mainloop
app/
  core/                      Lógica pura, sem UI (fácil de testar isoladamente)
    models.py                 Dataclasses: PrizeTier, PrizePlace, TournamentResult
    prize_calculator.py       Regras de negócio: formatos de premiação e cálculo
    formatting.py             Formatação de moeda em padrão brasileiro (R$ 0,00)
  ui/
    theme.py                  Paleta de cores (claro/escuro) e constantes visuais
    widgets.py                 Componentes reutilizáveis (PrizeCard, SummaryRow)
    main_window.py             Janela principal (CustomTkinter): formulário + resultados
assets/
  icon.ico / icon.png          Ícone do troféu (gerado por generate_icon.py)
  generate_icon.py             Script utilitário para regenerar o ícone (dev only)
build.ps1                     Script que empacota o .exe com PyInstaller
requirements.txt              Dependências (customtkinter, pillow, pyinstaller)
```

## Arquitetura pensada para expansões futuras

O cálculo de premiação (`app/core/prize_calculator.py`) já é parametrizado por
uma lista de `PrizeTier` (posição, rótulo, emoji, percentual) em vez de ter os
percentuais fixos espalhados pela UI. Isso deixa o caminho pronto para:

- **Porcentagens personalizadas**: bastaria uma tela nova que monte uma lista
  de `PrizeTier` customizada e passe para `calculate_prizes(tiers=...)` — a
  função já aceita isso, só não há UI para editar ainda.
- **Histórico de torneios**: `TournamentResult` (em `app/core/models.py`) já é
  uma dataclass simples e serializável — um módulo futuro de histórico só
  precisaria persistir instâncias dela (ex: em JSON ou SQLite) sem remodelar
  nada existente.
- **Exportar PDF/Excel**: mesma ideia — um exportador futuro consumiria um
  `TournamentResult` já pronto, sem precisar recalcular ou reformatar nada.
- **Configurar formatos automaticamente**: `get_default_tiers()` centraliza a
  regra de "quantos jogadores usam qual formato" num único lugar.

Nenhuma dessas features foi implementada agora — só a arquitetura já separa
essas responsabilidades para não exigir refatoração grande depois.

## Limitação conhecida

Os emojis de troféu/medalha (🏆🥈🥉🎖️) nos cartões de resultado aparecem em
preto e branco (sem cor) porque a versão do Tcl/Tk usada pelo Python no
Windows (8.6.12) não renderiza emoji colorido — é uma limitação da engine
gráfica do Tk, não do código. O ícone do aplicativo (barra de título/taskbar)
é uma imagem própria (`assets/icon.ico`) e não é afetado por isso.
