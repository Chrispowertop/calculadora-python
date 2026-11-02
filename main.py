from tkinter import *
import re

# ---------- PALETA "NOITE NEON" ----------
COR_FUNDO = "#0d1117"      # fundo da janela
COR_TELA = "#161b26"       # fundo do visor
COR_TEXTO = "#e6edf3"      # texto principal
COR_TEXTO_SUAVE = "#6e7a8a"
COR_ERRO = "#ff4d8d"       # cor das mensagens de erro

COR_NUM = "#1c2333"        # botões numéricos
COR_NUM_HOVER = "#273049"

COR_FUNC = "#2a3350"       # C e %
COR_FUNC_HOVER = "#36426a"

COR_OP = "#00e5c3"         # operadores (verde-água neon)
COR_OP_HOVER = "#5af5dc"
COR_OP_TEXTO = "#0d1117"

COR_IGUAL = "#ff4d8d"      # botão de igual (rosa neon)
COR_IGUAL_HOVER = "#ff7aa9"

FONTE_BOTAO = ("Segoe UI", 16, "bold")

janela = Tk()
janela.title("Calculadora Neon")
janela.geometry("320x470")
janela.resizable(False, False)
janela.config(bg=COR_FUNDO)

# ---------- VISOR ----------
frame_tela = Frame(janela, bg=COR_TELA, highlightthickness=2,
                   highlightbackground=COR_OP, highlightcolor=COR_OP)
frame_tela.pack(fill=X, padx=16, pady=(18, 10))

titulo = Label(frame_tela, text="◆ CALC", font=("Segoe UI", 9, "bold"),
               bg=COR_TELA, fg=COR_OP, anchor="w")
titulo.pack(fill=X, padx=12, pady=(8, 0))

todos_valores = ""
apagar_result = False

valor_texto = StringVar()

# Área de altura fixa para o visor não "pular" quando a fonte muda de tamanho
area_visor = Frame(frame_tela, bg=COR_TELA, height=70)
area_visor.pack(fill=X)
area_visor.pack_propagate(False)

app_label = Label(area_visor, textvariable=valor_texto, anchor="e",
                  justify=RIGHT, font=("Consolas", 26, "bold"),
                  bg=COR_TELA, fg=COR_TEXTO, padx=12)
app_label.pack(fill=BOTH, expand=True)


def mostrar(texto, erro=False):
    """Mostra o texto no visor, reduzindo a fonte se ele for grande."""
    tamanho = len(texto)
    if tamanho <= 12:
        fonte = 26
    elif tamanho <= 16:
        fonte = 20
    elif tamanho <= 20:
        fonte = 16
    else:
        fonte = 12

    app_label.config(font=("Consolas", fonte, "bold"),
                     fg=COR_ERRO if erro else COR_TEXTO)
    valor_texto.set(texto)


# ---------- LÓGICA ----------
def aplicar_porcentagem(expressao):
    """
    Converte o '%' para o comportamento de uma calculadora comum:
      200+10%  ->  200 + (10% de 200)  = 220
      200-10%  ->  200 - (10% de 200)  = 180
      50*10%   ->  50 * 0,10           = 5
      50%      ->  0,50
    """
    padrao = re.compile(r"(\d+\.?\d*|\.\d+)%")

    while True:
        achou = padrao.search(expressao)
        if not achou:
            return expressao

        numero = achou.group(1)
        antes = expressao[:achou.start()]
        depois = expressao[achou.end():]

        if antes.endswith(("+", "-")) and antes[:-1]:
            # Soma/subtração: a porcentagem é calculada sobre o valor anterior
            base = eval(antes[:-1])
            valor = f"({base}*{numero}/100)"
        else:
            valor = f"({numero}/100)"

        expressao = antes + valor + depois


def formatar_numero(numero):
    """Tira ruídos de ponto flutuante (0.30000000000000004 -> 0.3) e o '.0'."""
    if isinstance(numero, float):
        numero = round(numero, 10)
        if numero == int(numero):
            return str(int(numero))
    return str(numero)


def entrar_valores(event):
    global todos_valores, apagar_result

    operadores = ("+", "-", "*", "/", "%")

    # "%" só faz sentido logo depois de um número
    if event == "%" and (not todos_valores or not todos_valores[-1].isdigit()):
        return

    # Se acabou de calcular, um número começa uma nova conta.
    if apagar_result:
        if event not in operadores:
            todos_valores = ""
        apagar_result = False

    todos_valores += str(event)
    mostrar(todos_valores)


def limpar_valores():
    global todos_valores, apagar_result

    todos_valores = ""
    apagar_result = False
    mostrar("")


def resultado():
    global todos_valores, apagar_result

    if not todos_valores:
        return

    try:
        expressao = aplicar_porcentagem(todos_valores)
        resultado_calculo = formatar_numero(eval(expressao))

        mostrar(resultado_calculo)
        todos_valores = resultado_calculo
        apagar_result = True

    except ZeroDivisionError:
        mostrar("Divisão por zero", erro=True)
        todos_valores = ""
        apagar_result = False

    except (SyntaxError, NameError, TypeError):
        mostrar("Expressão inválida", erro=True)
        todos_valores = ""
        apagar_result = False

    except Exception:
        mostrar("Erro no cálculo", erro=True)
        todos_valores = ""
        apagar_result = False


# ---------- BOTÕES ----------
frame_corpo = Frame(janela, bg=COR_FUNDO)
frame_corpo.pack(fill=BOTH, expand=True, padx=12, pady=(0, 14))

for i in range(4):
    frame_corpo.columnconfigure(i, weight=1, uniform="col")
for i in range(5):
    frame_corpo.rowconfigure(i, weight=1, uniform="lin")


def criar_botao(texto, comando, linha, coluna, cor, cor_hover,
                fg=COR_TEXTO, colspan=1):
    botao = Button(frame_corpo, text=texto, command=comando, font=FONTE_BOTAO,
                   bg=cor, fg=fg, activebackground=cor_hover,
                   activeforeground=fg, relief=FLAT, bd=0, cursor="hand2")
    botao.grid(row=linha, column=coluna, columnspan=colspan,
               sticky="nsew", padx=4, pady=4)
    # efeito ao passar o mouse
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor))
    return botao


# Linha 0
criar_botao("C", limpar_valores, 0, 0, COR_FUNC, COR_FUNC_HOVER, colspan=2)
criar_botao("%", lambda: entrar_valores("%"), 0, 2, COR_FUNC, COR_FUNC_HOVER)
criar_botao("/", lambda: entrar_valores("/"), 0, 3, COR_OP, COR_OP_HOVER, COR_OP_TEXTO)

# Linha 1
criar_botao("7", lambda: entrar_valores("7"), 1, 0, COR_NUM, COR_NUM_HOVER)
criar_botao("8", lambda: entrar_valores("8"), 1, 1, COR_NUM, COR_NUM_HOVER)
criar_botao("9", lambda: entrar_valores("9"), 1, 2, COR_NUM, COR_NUM_HOVER)
criar_botao("*", lambda: entrar_valores("*"), 1, 3, COR_OP, COR_OP_HOVER, COR_OP_TEXTO)

# Linha 2
criar_botao("4", lambda: entrar_valores("4"), 2, 0, COR_NUM, COR_NUM_HOVER)
criar_botao("5", lambda: entrar_valores("5"), 2, 1, COR_NUM, COR_NUM_HOVER)
criar_botao("6", lambda: entrar_valores("6"), 2, 2, COR_NUM, COR_NUM_HOVER)
criar_botao("-", lambda: entrar_valores("-"), 2, 3, COR_OP, COR_OP_HOVER, COR_OP_TEXTO)

# Linha 3
criar_botao("1", lambda: entrar_valores("1"), 3, 0, COR_NUM, COR_NUM_HOVER)
criar_botao("2", lambda: entrar_valores("2"), 3, 1, COR_NUM, COR_NUM_HOVER)
criar_botao("3", lambda: entrar_valores("3"), 3, 2, COR_NUM, COR_NUM_HOVER)
criar_botao("+", lambda: entrar_valores("+"), 3, 3, COR_OP, COR_OP_HOVER, COR_OP_TEXTO)

# Linha 4
criar_botao("0", lambda: entrar_valores("0"), 4, 0, COR_NUM, COR_NUM_HOVER, colspan=2)
criar_botao(".", lambda: entrar_valores("."), 4, 2, COR_NUM, COR_NUM_HOVER)
criar_botao("=", resultado, 4, 3, COR_IGUAL, COR_IGUAL_HOVER, "#ffffff")

janela.mainloop()