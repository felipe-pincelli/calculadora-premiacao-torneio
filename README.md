# Calculadora de Premiação

Aplicativo desktop para Windows que calcula, em segundos, como dividir a
premiação em dinheiro de um torneio de card games entre os primeiros
colocados.

## Para que serve

Quem organiza torneio de carta (Magic, Pokémon, Yu-Gi-Oh, etc.) normalmente
cobra uma inscrição de cada jogador e devolve parte desse valor como premiação
para quem fica bem colocado. Fazer essa conta na mão (e decidir quantos
lugares premiar) é chato e sujeito a erro, ainda mais no meio da correria de
um evento. Este app resolve isso: você digita quantos jogadores tem, o valor
da inscrição, escolhe quantos lugares quer premiar (ou deixa no automático) e
recebe o valor de cada colocação já formatado em reais.

Não precisa instalar Python nem nada — é um único `.exe` que roda direto no
Windows.

## Como funciona

A tela tem três campos e um botão:

1. **Quantidade de jogadores**
2. **Valor da inscrição (R$)**
3. **Tamanho do pódio** — quantos lugares serão premiados
4. Botão **Calcular Premiação** (ou aperte **Enter** em qualquer campo)

Ao calcular, o app mostra a arrecadação total (jogadores × inscrição) e, logo
abaixo, um cartão para cada colocação premiada — com uma faixa dourada,
prateada ou de bronze para os três primeiros lugares — já com o valor em
reais que aquela posição recebe.

Também dá pra alternar entre tema claro e escuro (interruptor no topo), e a
janela é redimensionável.

### Tamanho do pódio

No campo "Tamanho do pódio" dá pra escolher:

- **Automático** — usa a regra padrão do negócio: **Top 3** se o torneio tem
  menos de 10 jogadores, **Top 4** a partir de 10 jogadores.
- **Top 1 a Top 8** — escolha manual de quantas colocações premiar,
  independente da quantidade de jogadores (o app só bloqueia se você tentar
  premiar mais colocações do que existem jogadores inscritos).

Os percentuais de cada formato (sempre somando 100% da arrecadação):

| Pódio  | 1º  | 2º  | 3º  | 4º  | 5º  | 6º  | 7º  | 8º  |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|
| Top 1  | 100%|     |     |     |     |     |     |     |
| Top 2  | 60% | 40% |     |     |     |     |     |     |
| Top 3  | 50% | 30% | 20% |     |     |     |     |     |
| Top 4  | 40% | 30% | 20% | 10% |     |     |     |     |
| Top 5  | 35% | 25% | 20% | 12% | 8%  |     |     |     |
| Top 6  | 30% | 22% | 18% | 13% | 10% | 7%  |     |     |
| Top 7  | 28% | 20% | 16% | 12% | 10% | 8%  | 6%  |     |
| Top 8  | 25% | 18% | 15% | 12% | 10% | 8%  | 7%  | 5%  |

### Validações

O app não deixa calcular com quantidade de jogadores ou valor de inscrição
vazios, zerados ou negativos, nem com um pódio maior que o número de
jogadores — sempre com uma mensagem de erro explicando o problema.

## Como foi feito

- **Linguagem/UI**: [Python](https://www.python.org/) +
  [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Tkinter
  "modernizado", com cantos arredondados, tema claro/escuro e widgets
  parecidos com os do shadcn/Material). Escolhido por gerar um executável
  leve e rápido de abrir — sem a pegada de um framework tipo Electron.
- **Ícone**: gerado programaticamente com [Pillow](https://python-pillow.org/)
  (`assets/generate_icon.py` desenha um troféu simples e exporta pra `.ico`).
- **Empacotamento**: [PyInstaller](https://pyinstaller.org/) em modo
  `--onefile --windowed`, empacotando o interpretador Python e todas as
  dependências (incluindo o Tcl/Tk do CustomTkinter) dentro de um único
  `CalculadoraPremiacao.exe` — quem recebe o `.exe` não precisa ter Python
  instalado.
- **Arquitetura**: a lógica de cálculo (`app/core/`) é totalmente separada da
  interface (`app/ui/`), sem nenhuma dependência de Tkinter — o que permite
  testar as regras de premiação isoladamente e reaproveitar em outra UI (web,
  mobile, CLI) se um dia fizer sentido. Mais detalhes na seção
  "Arquitetura pensada para expansões futuras" abaixo.
- Todo o desenvolvimento (código, testes manuais na interface e build do
  `.exe`) foi feito com o [Claude Code](https://claude.com/claude-code), a
  partir de uma descrição em português do que o app deveria fazer.

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

O cálculo de premiação (`app/core/prize_calculator.py`) é parametrizado por
uma lista de `PrizeTier` (posição, rótulo, emoji, percentual) em vez de ter os
percentuais fixos espalhados pela UI. Isso deixa o caminho pronto para:

- **Porcentagens 100% personalizadas** (além dos formatos Top 1-8 já
  prontos): bastaria uma tela nova que monte uma lista de `PrizeTier`
  customizada e passe para `calculate_prizes(tiers=...)` — a função já aceita
  isso, só não há UI para editar percentual individual ainda.
- **Histórico de torneios**: `TournamentResult` (em `app/core/models.py`) já é
  uma dataclass simples e serializável — um módulo futuro de histórico só
  precisaria persistir instâncias dela (ex: em JSON ou SQLite) sem remodelar
  nada existente.
- **Exportar PDF/Excel**: mesma ideia — um exportador futuro consumiria um
  `TournamentResult` já pronto, sem precisar recalcular ou reformatar nada.

Nenhuma dessas features foi implementada agora — só a arquitetura já separa
essas responsabilidades para não exigir refatoração grande depois.

## Limitação conhecida

Os emojis de troféu/medalha (🏆🥈🥉🎖️) nos cartões de resultado aparecem em
preto e branco (sem cor) porque a versão do Tcl/Tk usada pelo Python no
Windows (8.6.12) não renderiza emoji colorido — é uma limitação da engine
gráfica do Tk, não do código. O ícone do aplicativo (barra de título/taskbar)
é uma imagem própria (`assets/icon.ico`) e não é afetado por isso.
