import socket # Comunicação de rede
import pickle # Envia objetos entre diferentes programas Python

# Banco de dados que irá armazenar as perguntas e as respostas
perguntas = [
    {
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["Brasília", "Paris", "Lisboa", "Londres"],
        "resposta": 0
    },
    {
        "pergunta": "Em qual país surgiu a Apple?",
        "opcoes": ["Itália", "Brasil", "Estados Unidos", "Portugal"],
        "resposta": 2
    },
    {
        "pergunta": "Qual seleção foi a campeã da copa de 2022?",
        "opcoes": ["Portugal", "Argentina", "França", "México"],
        "resposta": 1
    },
]

def handle_client(client_socket):
    score = 0
    answers = []

    # Enviando as perguntas do servidor para o cliente
    client_socket.send(pickle.dumps(perguntas))
    
    for q in perguntas:
        pergunta_text = q["pergunta"]
        opcoes = q["opcoes"]
        resposta = q["resposta"]
        
        print(f"Enviando pergunta: {pergunta_text}")
        answer = int(client_socket.recv(1024).decode())
        answers.append((pergunta_text, opcoes[answer]))
        
        if answer == resposta:
            score += 1
    
    client_socket.send(pickle.dumps({"score": score, "answers": answers}))
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 129))
    server.listen(5)
    print("Servidor aguardando conexões...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Conexão estabelecida com {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
