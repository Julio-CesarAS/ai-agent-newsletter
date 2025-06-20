from src.crew.news_crew import NewsCrew

def main():
    print("## Bem-vindo ao Crew de Newsletter de Design e Tecnologia ##")
    print("---------------------------------------------------------")
    
    # Este e-mail será o destinatário da newsletter.
    # No futuro, você obterá essa lista do Supabase.
    recipient_email = input("Por favor, insira o e-mail do destinatário: ")

    if not recipient_email:
        print("Nenhum e-mail fornecido. Encerrando.")
        return

    news_crew = NewsCrew(recipient_email)
    result = news_crew.run()
    
    print("\n---------------------------------------------------------")
    print(f"Processo finalizado. Resultado: {result}")
    print("## Fim da execução ##")

if __name__ == "__main__":
    main()