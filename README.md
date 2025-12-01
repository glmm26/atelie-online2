# 🧵 Ateliê Online

Um sistema online voltado para **ajustes, consertos, customização e estamparia**, oferecendo uma plataforma simples e intuitiva para que clientes possam solicitar serviços diretamente pela internet. 

## 📖 Sobre o Projeto
O **Ateliê Online** tem como objetivo modernizar a forma como ateliês atendem seus clientes, permitindo:
- Solicitação de **ajustes e consertos** de roupas de forma online.  
- Envio de **peças para customização** de maneira prática.  
- Serviços de **estamparia sob demanda**.  
- Controle do fluxo de pedidos, orçamentos e status do serviço.  

Atualmente, o projeto encontra-se **em desenvolvimento**, buscando oferecer uma experiência completa tanto para os clientes quanto para o time do ateliê.

---

# 🧵 Ateliê Online

Um sistema online voltado para ajustes, consertos, customização e estamparia. A plataforma permite que clientes solicitem serviços diretamente pela internet de forma simples e intuitiva.

## 📖 Sobre o projeto

O Ateliê Online busca modernizar o atendimento de ateliês, oferecendo:

- Solicitação de ajustes e consertos de roupas online
- Envio de peças para customização
- Serviços de estamparia sob demanda
- Controle de pedidos, orçamentos e status dos serviços

O projeto está em desenvolvimento.

---

## 🚀 Funcionalidades

- Cadastro e autenticação de clientes
- Cadastro e gerenciamento de serviços
- Sistema de solicitação de serviços online
- Acompanhamento do status do pedido
- Integração com banco de dados
- Interface responsiva

---

## 🛠 Tecnologias

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python (Flask)
- Banco de dados: PostgreSQL

---

## Estrutura do projeto

atelie-online/
├── atelie_online/        # código fonte da aplicação
├── static/               # arquivos estáticos (CSS, JS, imagens)
├── templates/            # templates HTML
├── app.py                # ponto de entrada
├── requirements.txt      # dependências
└── README.md             # documentação

---

## Como executar localmente

1. Clone este repositório

```bash
git clone https://github.com/glmm26/AtelieGUI2.git
```

2. Entre na pasta do projeto

```bash
cd Atelie-Online-main
```

3. Crie e ative um ambiente virtual

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Instale as dependências

```bash
pip install -r requirements.txt
```

5. Configure o banco de dados (PostgreSQL)

- Crie um banco de dados no PostgreSQL
- Atualize as credenciais no `app.py` ou em um arquivo `.env`

6. Execute a aplicação

```bash
flask run
```

---

## Status

- Em desenvolvimento 🚧

---

## Contribuição

1. Faça um fork deste repositório
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Faça commits descritivos: `git commit -m "Minha feature"`
4. Envie para o repositório remoto: `git push origin minha-feature`
5. Abra um Pull Request

Obrigado por olhar o projeto! Se quiser, abra uma issue antes de implementar alterações maiores.

---

Projeto: AtelieGUI2 (Ateliê Online)