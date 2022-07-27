#           BIBLIOTECAS
from playwright.sync_api import sync_playwright # AUTOMAÇÃO WEB
from getpass import getpass # CAMPO DE SENHA
import os # LIMPAR A TELA
import time # PAUSAR O CÓDIGO

def padrãoEmail(): # RESPONSÁVEL POR MANIPULAR OS EMAILS NECESSÁRIOS (REMETENTE E DESTINATÁRIO)
    with open('emails.txt') as arquivo: # ABRE O ARQUIVO QUE GUARDA OS EMAILS
        num_lin = sum(1 for linha in arquivo) # CONTA A QUANTIDADE DE LINHAS QUE O DOCUMENTO TEM

    with open('emails.txt', 'r', encoding='utf-8') as arquivo: # ABRE O ARQUIVO QUE GUARDA OS EMAILS
        print("Você pode escolher entre")
        for i in range(num_lin): # VAI DE 0 ATÉ O NÚMERO DE LINHAS
            texto = arquivo.readline() # LÊ A LINHA
            lugar = texto.find('-') # PROCURA O SINAL '-'
            print(texto[0:lugar-1]) # ESCREVE TUDO DESDE O PRIMEIRO CARACTER ATÉ 1 ANTES DO '-'
    email = input("\nInformar o email ou a opção que deseja: ").lower() # GUARDA NA VARIÁVEL LOCAL EM MINÚSCULO
    print("---------------------------")
    with open('emails.txt', 'r', encoding='utf-8') as arquivo: # ABRE O ARQUIVO QUE GUARDA OS EMAILS
        for i in range(num_lin):  # VAI DE 0 ATÉ O NÚMERO DE LINHAS
            texto = arquivo.readline() # LÊ A LINHA
            if(texto.find(email+" ")!= -1): # SE NA LINHA HOUVER O ID OU O EMAIL DO INDIVIDUO
                lugar = texto.find('-') # ELE LOCALIZA A POSIÇÃO DO '-'
                email = texto[lugar + 1:] # ELE GUARDA TODO O RESTO APÓS O '-' NA VARIÁVEL EMAIL
                return email # E MANDA
        # SE ELE NÃO RETORNOU NADA, QUER DIZER QUE O TEXTO DIGITADO ERA UM EMAIL NÃO REGISTRADO
        with open('emails.txt', "a", encoding="utf-8") as editavel: # ABRE O ARQUIVO EM MODO DE EDIÇÃO
            opcao = input("Deseja guardar o contato? ") # PERGUNTA SE O USUÁRIO QUER QUE O CONTATO SEJA GUARDADO
            if 's' in opcao: # SE OUVER UM S NA OPÇÃO
                nome = input("Insira seu nome ") # SOLICITA O NOME
                adicionar = (f'\n{num_lin+1} {nome} -{email} ') # GUARDA O TEXTO QUE SERÁ INSERIDO
                editavel.write(adicionar) # CRIA A LINHA NO DOCUMENTO
            else: # SE A RESPOSTA NÃO FOR POSITIVA
                print("Ok") # ESCREVE 'OK'
            return email # RETORNA O QUE FOI ESCRITO

def iniciarNavegador():
    os.system('cls') or None  # LIMPA A TELA
    print("Analisando os dados e enviando-os   | 1/14 |")
    navegador = p.firefox.launch()  # INICIA O NAVEGADOR
    # navegador = p.firefox.launch(headless=False) PARA DEIXAR A EXECUÇÃO VISÍVEL
    # Chromium é mais rápido, porém ele não deixa fazer login, o Firefox e o WebKit deixam
    return navegador.new_page()  # ABRE A PÁGINA INICIAL


os.system('cls') or None # LIMPA A TELA
print("---------- Login ----------")
email = padrãoEmail() # GUARDA O EMAIL DO REMETENTE NESTA VARIÁVEL
senha = getpass("Informe sua senha: ") #GUARDA A SENHA DO EMAIL DO REMETENTE SEM QUE O USUÁRIO VEJA O QUE ESTÁ DIGITANDO
os.system('cls') or None # LIMPA A TELA
opcao = input("Deseja enviar a mensagem por onde? \n1 - Email\n2 - Discord\n")
print("---------- Envio ----------")
if opcao == '1':
    email_destino = [padrãoEmail()] # GUARDA O EMAIL DO DESTINATÁRIO (É UMA LISTA POIS 1 EMAIL PODE SER ENVIADO A MAIS DE 1 PESSOA)
    destinatario = input("Deseja adicionar mais um destinatário?: ").lower() # PERGUNTA SE DESEJA ADICIONAR OUTRO DESTINATÁRIO
    while 's' in destinatario: # ENQUANTO O USUÁRIO RESPONDER (SIM, SI, S ou POSITIVO), IRÁ ADICIONAR DESTINATÁRIOS
        email_destino.append(padrãoEmail()) # ADICIONA MAIS UM DESTINATÁRIO
        destinatario = input("Deseja adicionar mais um destinatário?: ").lower() # PERGUNTA SE DESEJA ADICIONAR OUTRO DESTINATÁRIO
        os.system('cls') or None # LIMPA A TELA

    print("----------Mensagem---------")
    assunto = input("Informe o assunto da mensagem: ") # GUARDA O ASSUNTO DA MENSAGEM
    print("---------------------------")
    corpo = input("Informe o corpo da mensagem: ") # GUARDA O CONTEÚDO DA MENSAGEM
    with sync_playwright() as p:
        pagina = iniciarNavegador()
        print("Navegador iniciado                  | 2/14 |")
        # VAI PRA PRÁGINA DE LOGIN DO GOOGLE
        pagina.goto("https://accounts.google.com/ServiceLogin/identifier?hl=pt-BR&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        pagina.fill('xpath=//*[@id="identifierId"]', email) # PREENCHE O CAMPO EMAIL
        pagina.keyboard.press('Enter')
        # PREENCHE O CAMPO SENHA
        pagina.fill('xpath=/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input', senha)
        print("Email confirmado                    | 3/14 |")
        pagina.keyboard.press('Enter')
        # ESPERA ATÉ CHEGAR NA PÁGINA INICIAL DO GOOGLE, POIS ASSIM É CERTEZA QUE PASSOU DA FASE DE VERIFICAÇÃO
        pagina.wait_for_timeout(1000)
        pagina.wait_for_url('https://www.google.com/')
        print("Senha confirmada                    | 4/14 |")
        print("Conta acessada!                     | 5/14 |")
        pagina.goto('https://mail.google.com/mail/u/0/#inbox')
        pagina.wait_for_url('https://mail.google.com/mail/u/0/#inbox') # ESPERA ATÉ A PÁGINA DO GMAIL ABRIR
        print("Email aberto!                       | 6/14 |")
        # CLICA NO BOTÃO "+ ESCREVER"
        pagina.click('xpath=/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div')
        print("Caixa de envio abrindo...           | 7/14 |")
        # ESPERA ATÉ QUE A PÁGINA CARREGUE
        pagina.wait_for_url('https://mail.google.com/mail/u/0/#inbox?compose=new')
        time.sleep(1) # ESPERA 1 SEGUNDO PARA DAR TEMPO DA CAIXA ABRIR
        print("Caixa de envio aberta!              | 8/14 |")
        # INFORMA OS EMAILS DOS DESTINATÁRIOS E APERTA TAB APÓS CADA 1 PARA INFORMAR O OUTRO
        for emails in email_destino:
            pagina.keyboard.insert_text(emails)
            pagina.keyboard.press('Tab')
        print("Email dos destinatários confirmado  | 9/14 |")
        pagina.keyboard.press('Tab') # VAI ATÉ A CAIXA "ASSUNTO"
        pagina.keyboard.insert_text(assunto) # INSERE O ASSUNTO
        print("Assunto confirmado                  | 10/14 |")
        pagina.keyboard.press('Tab') # VAI ATÉ A CAIXA "CORPO"
        pagina.keyboard.insert_text(corpo) # INSERE O CORPO
        print("Corpo confirmado                    | 11/14 |")
        pagina.keyboard.press('Tab') # VAI ATÉ O BOTÃO "ENVIAR"
        pagina.keyboard.press('Enter') # APERTA ENTER
        print("Envio confirmado                    | 12/14 |")
        pagina.wait_for_url('https://mail.google.com/mail/u/0/#inbox') # ESPERA ATÉ A CAIXA DE MENSAGEM FECHAR
        time.sleep(3) # ESPERA 3 SEGUNDOS PARA DAR TEMPO DA MENSAGEM SER ENVIADA
        print("Encerrando navegador                | 13/14 |")
        pagina.close()
        print("Navegador encerrado                 | 14/14 |")
        print("Email enviado com sucesso")

elif opcao == '2':
    nick = input("Informe o nick da conversa ou pessoa que deseja enviar a mensagem: ")
    msg = input(f"Informe a mensagem que deseja enviar a {nick}: ")
    with sync_playwright() as p:
        pagina = iniciarNavegador()
        print("Navegador iniciado                  | 2/14 |")
        pagina.goto('https://discord.com/login?redirect_to=%2Fchannels%2F%40me')
        pagina.wait_for_url("https://discord.com/login?redirect_to=%2Fchannels%2F%40me")
        pagina.wait_for_timeout(1000)
        pagina.keyboard.insert_text(email)
        pagina.keyboard.press('Tab')
        pagina.keyboard.insert_text(senha)
        pagina.keyboard.press('Enter')
        pagina.wait_for_url('https://discord.com/channels/@me')
        pagina.wait_for_timeout(1000)
        pagina.click('//*[@id="app-mount"]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]/nav/div[1]/button')
        pagina.wait_for_timeout(1000)
        pagina.keyboard.insert_text(nick)
        pagina.keyboard.press('Enter')
        pagina.wait_for_selector('xpath=//*[@id="app-mount"]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/button/div/svg/path')
        pagina.wait_for_timeout(2000)
        pagina.keyboard.insert_text(msg)
        pagina.keyboard.press('Enter')

        pagina.wait_for_timeout(10000)