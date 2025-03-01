import requests
import tkinter as tk
root = tk.Tk()
root.title('Conversor de moedas')
root.geometry("400x300")
token = '17986|ulfb50c9Bdpf04LjcxcIXeJaSHKxBAdO'
def calcular():
    try:
        moeda = tipo_moeda.get()
        valor_moeda_origem = float(valor_inserido.get())
        if valor_moeda_origem <= 0:
            label_resultado.config(text="O valor deve ser positivo.")
            return
    except ValueError:
        label_resultado.config(text="Por favor, insira um valor numérico válido.")
        return
    try:
        label_resultado.config(text="Carregando...")
        root.update()
        
        request = requests.get(f'https://api.invertexto.com/v1/currency/{moeda}_BRL?token={token}')
        request = request.json()
    
        valor_moeda_destino = float(request[f'{moeda}_BRL']['price'])
        resultado = valor_moeda_origem * valor_moeda_destino
        label_resultado.config(text=f' R$ {resultado:.2f}')
    except requests.exceptions.RequestException as e:
        label_resultado.config(text=f"Erro ao encontrar preço do {moeda}. Tente novamente mais tarde.")
        print(f"Erro: {e}")

label_tipo_moeda = tk.Label(root, text="Tipo de Moeda")
label_tipo_moeda.pack()

tipo_moeda = tk.StringVar()
opcoes_moedas = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"]
menu_moeda = tk.OptionMenu(root, tipo_moeda, *opcoes_moedas)
menu_moeda.pack()

label_moeda_entrada = tk.Label(root, text="Digite um valor")
label_moeda_entrada.pack()
valor_inserido = tk.Entry(root, text='Digite o valor em real: ')
valor_inserido.pack()

botao = tk.Button(root, text="Calcular", command=calcular)
botao.pack()

label_resultado = tk.Label(root)
label_resultado.pack()

root.mainloop()