from search import search_prompt

def main():
    print("Chat com Documentos - Sistema RAG")
    print("=" * 50)
    print("Digite suas perguntas sobre o documento PDF.")
    print("Digite 'sair' para encerrar o programa.")
    print("=" * 50)
    
    # Configurar a chain de busca
    print("Inicializando sistema de busca...")
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        print("Certifique-se de que:")
        print("- O banco de dados PostgreSQL está rodando")
        print("- As variáveis de ambiente estão configuradas no .env")
        print("- A ingestão do PDF foi executada com sucesso")
        return
    
    print("Sistema inicializado com sucesso!")
    print("\n" + "=" * 50)
    
    while True:
        try:
            # Obter pergunta do usuário
            pergunta = input("\nFaça sua pergunta: ").strip()
            
            # Verificar se o usuário quer sair
            if pergunta.lower() in ['sair', 'quit', 'exit', 'q']:
                print("Encerrando o chat...")
                break
                
            # Verificar se a pergunta não está vazia
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue
            
            print(f"\nPERGUNTA: {pergunta}")
            print("Buscando informações relevantes...")
            
            # Gerar resposta usando a chain RAG
            resposta = chain.invoke(pergunta)
            
            print("=" * 50)
            print(f"RESPOSTA: {resposta}")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\nChat interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")
            print("Tente novamente com uma pergunta diferente.")

if __name__ == "__main__":
    main()