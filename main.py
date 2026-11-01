from tkinter import *

# ---------- PALETA "NOITE NEON" ----------
COR_FUNDO = "#0d1117"      # fundo da janela
COR_TELA = "#161b26"       # fundo do visor
COR_TEXTO = "#e6edf3"      # texto principal
COR_TEXTO_SUAVE = "#6e7a8a"

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
FONTE_VISOR = ("Consolas", 26, "bold")

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

app_label = Label(frame_tela, textvariable=valor_texto, anchor="e",
                  justify=RIGHT, font=FONTE_VISOR, bg=COR_TELA, fg=COR_TEXTO,
                  padx=12, height=2)
app_label.pack(fill=X)

# ---------- LÓGICA (inalterada) ----------
def entrar_valores(event):
    global todos_valores, apagar_result

    operadores = ("+", "-", "*", "/", "%")

    # Se acabou de calcular, um número começa uma nova conta.
    if apagar_result:
        if event not in operadores:
            todos_valores = ""
        apagar_result = False

    todos_valores += str(event)
    valor_texto.set(todos_valores)


def limpar_valores():
    global todos_valores, apagar_result

    todos_valores = ""
    apagar_result = False
    valor_texto.set("")


def resultado():
    global todos_valores, apagar_result

    try:
        resultado_calculo = eval(todos_valores)

        valor_texto.set(str(resultado_calculo))
        todos_valores = str(resultado_calculo)
        apagar_result = True

    except ZeroDivisionError:
        valor_texto.set("Divisão por zero")
        todos_valores = ""
        apagar_result = False

    except (SyntaxError, NameError, TypeError):
        valor_texto.set("Expressão inválida")
        todos_valores = ""
        apagar_result = False

    except Exception:
        valor_texto.set("Erro no cálculo")
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