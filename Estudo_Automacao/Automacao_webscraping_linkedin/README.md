Automação de Busca de Vagas no LinkedIn

Este script automatiza a busca de vagas no LinkedIn, coletando os links das oportunidades e salvando-os em uma planilha do Excel.

Objetivo

O LinkedIn frequentemente exibe vagas que não correspondem exatamente aos termos pesquisados. Com este script, você pode coletar todas as vagas de uma vez e filtrá-las posteriormente, garantindo uma triagem mais eficiente.

🚀 Funcionalidades

✅ Busca automática de vagas com base no cargo e localização.

✅ Salvamento dos links das vagas em uma planilha Excel.

✅ Login automatizado no LinkedIn para evitar buscas manuais.

📌 Funcionalidades Futuras (em desenvolvimento):

🔍 Filtro por data (exibir apenas vagas recentes).

🏢 Captura do tipo da vaga (Presencial, Remoto, Híbrido).

📄 Coleta da descrição e requisitos da vaga.

🛠 Filtragem automática para eliminar vagas irrelevantes.

📌 Requisitos

Antes de executar a automação, certifique-se de ter instalado:

Python 3+

Selenium

OpenPyXL

Google Chrome

ChromeDriver (compatível com a versão do seu navegador)

🛠 Como Usar

1️⃣ Criar Arquivo de Credenciais

Crie um arquivo chamado credentials.txt na mesma pasta do script e preencha no seguinte formato:


username=seu_email

password=sua_senha

2️⃣ Configurar a Pesquisa

No código, altere as seguintes variáveis:

nome_vaga: Cargo desejado.

cidade: Cidade onde deseja buscar vagas.

3️⃣ Executar o Script

Após configurar as credenciais e a pesquisa, execute o script com:


python script.py

🔹 O que o script faz?

Abre o navegador e faz login no LinkedIn.

Acessa a página de vagas e insere os critérios de busca.

Coleta os links das vagas disponíveis.

Salva os resultados em um arquivo Excel na mesma pasta do script.

⚠️ Observações
O script possui poucos delays (sleeps), então após alguns usos, o LinkedIn pode exibir captchas.

Recomenda-se utilizar a automação com moderação para evitar bloqueios na conta.

✉️ Contato

Caso tenha dúvidas ou sugestões, sinta-se à vontade para entrar em contato!

Referências

Este projeto foi inspirado no vídeo "Automatizando Busca de Vagas no LinkedIn" - [https://youtu.be/-ur_fIGxIGI], criado pelo Marcos. A automação foi adaptada e expandida para incluir novas funcionalidades, tornando o processo de coleta e filtragem de vagas mais eficiente.
