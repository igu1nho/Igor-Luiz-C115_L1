import socket
import pickle

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.0.112", 129))
    
    perguntas = pickle.loads(client.recv(4096))  # Recebe as perguntas do servidor

    opcao_escolhida = []  # Armazenamento das respostas escolhidas pelo cliente
    opcao_correta = 0  # Contador de respostas corretas acertadas pelo cliente

    for p in perguntas:
        pergunta_texto = p["pergunta"]
        opcoes = p["opcoes"]
        resposta_correta_index = p["resposta"]  # Resposta correta
        
        print(pergunta_texto)
        for i, option in enumerate(opcoes):
            print(f"{i}. {option}")

        resposta = int(input("Escolha a opção correta: "))
        opcao_escolhida.append((pergunta_texto, opcoes[resposta], opcoes[resposta_correta_index]))
        
        if resposta == resposta_correta_index:
            opcao_correta += 1
        client.send(str(resposta).encode())

    print("\nRespostas:")
    for p, r_esc, r_cor in opcao_escolhida:
        print(f"Pergunta: {p}\nResposta escolhida: {r_esc} ; Resposta Correta: {r_cor}")
    
    print("\nResultado:")
    print(f"{opcao_correta} resposta(s) corretas")
    
    client.close()

if __name__ == "__main__":
    main()
