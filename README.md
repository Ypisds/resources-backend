# 🚀 FastResources API

O **FastResources** é uma API RESTful de alta performance desenvolvida em **FastAPI**. O sistema atua como um repositório centralizado de materiais didáticos, integrando segurança robusta via **JWT** e Inteligência Artificial (Smart Assist) para auxiliar conteudistas na curadoria e categorização automática de materiais educacionais.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

---

## 🔗 Links Úteis

* **🌐 Aplicação em Produção:** [Acesse o FastResources no Render](https://resources-frontend.onrender.com/)
* **💻 Repositório do Frontend:** [Ypisds/resources-frontend](https://github.com/Ypisds/resources-frontend)

## 📋 Status dos Requisitos do Projeto

Abaixo está o mapeamento dos requisitos solicitados no desafio técnico e o que foi implementado:

| Requisito | Categoria | Status |
| :--- | :--- | :---: |
| CRUD de Recursos (Listagem, Criar, Editar, Deletar) | Funcional | ✅ |
| Paginação de Resultados | Funcional | ✅ |
| **Autenticação e Segurança (JWT + OAuth2)** | Segurança | ✅ |
| Integração com LLM (Gemini) | IA | ✅ |
| Smart Assist (Geração automática de Descrição e 3 Tags) | IA | ✅ |
| Prompt de Sistema (Assistente Pedagógico) | IA | ✅ |
| Retorno da IA em formato JSON Estrito | IA | ✅ |
| Validação de Dados com Pydantic | Técnico | ✅ |
| Variáveis de Ambiente (`.env` no `.gitignore`) | Técnico | ✅ |
| Banco de Dados Relacional (PostgreSQL) | Técnico | ✅ |
| Pipeline de CI (Lint no GitHub Actions) | DevOps | ✅ |
| Observabilidade (Logs Estruturados e Latência de IA) | Diferencial | ⏳ *Não implementado* |

---

## 🧠 Smart Assist (Integração com IA)

O grande diferencial desta API é o endpoint de assistência inteligente. Utilizando técnicas de **Prompt Engineering**, a IA é instruída a atuar como um "Assistente Pedagógico". 

**Fluxo:**
1. O Frontend envia o `Título` e o `Tipo` do material.
2. O Backend se comunica com a LLM.
3. A LLM retorna uma resposta estritamente formatada em **JSON** contendo uma descrição curta e 3 tags relevantes, prontas para preencher o formulário do usuário.

---

## 🔐 Segurança

A API é protegida utilizando o padrão OAuth2 com Password Flow e JSON Web Tokens (JWT).
- As senhas são cacheadas utilizando algoritmos de hashing seguros antes de irem para o banco.
- Endpoints de escrita e leitura de recursos exigem um cabeçalho válido: `Authorization: Bearer <token>`.

---

## ⚙️ DevOps: Integração e Entrega Contínuas (CI/CD)

O projeto conta com uma pipeline automatizada utilizando **GitHub Actions** para garantir a qualidade do código e realizar o deploy de forma contínua e segura.



A pipeline é dividida em dois *jobs* principais (`build` e `deploy`) e é engatilhada automaticamente em dois cenários:
* Abertura de um **Pull Request** para a branch `main`.
* **Push** direto na branch `main`.

### 1. Continuous Integration (CI)
O job de `build` roda em um ambiente Ubuntu e é responsável por validar a integridade do código antes que ele seja mesclado ou vá para produção.

* **Setup e Cache:** Configura o ambiente Python e utiliza cache para o `pip`, acelerando a instalação das dependências em execuções futuras.
* **Code Formatting (Black):** Verifica se o código segue os padrões de formatação PEP 8. A flag `--check` garante que a pipeline falhe se houver arquivos fora do padrão.
* **Linting (Flake8):** Analisa o código em busca de erros de sintaxe, variáveis não utilizadas e complexidade, ignorando pastas de ambiente virtual (`.venv`, `__pycache__`).
* **Testes Automatizados (Pytest):** Executa a suíte de testes da aplicação para garantir que as novas alterações não quebraram funcionalidades existentes.

### 2. Continuous Deployment (CD)
O job de `deploy` é responsável por colocar a aplicação no ar, mas possui regras estritas de execução:

* **Condicional de Sucesso:** Só é executado se o job de `build` (lint e testes) passar com sucesso (`needs: build`).
* **Condicional de Gatilho:** Só ocorre em eventos de `push` na branch `main`. Pull Requests rodam os testes, mas não disparam o deploy.
* **Integração com o Render:** Utiliza um webhook seguro (`RENDER_DEPLOY_HOOK` armazenado no GitHub Secrets) para avisar o servidor do Render que uma nova versão validada está pronta para ser colocada em produção.

---

## 🚦 Endpoints Principais

A documentação interativa (Swagger UI) com todos os schemas e rotas pode ser acessada em `/docs` ao rodar o projeto.

| Método | Rota | Autenticação | Descrição |
| :--- | :--- | :---: | :--- |
| `POST` | `/token` | ❌ | Autentica o usuário e retorna o token JWT. |
| `POST` | `/create-user` | ❌ | Endpoint para a criação de um novo usuário. |
| `GET` | `/resources` | ✅ | Lista os recursos didáticos com paginação e filtros. |
| `POST` | `/resources` | ✅ | Cadastra um novo recurso no banco de dados. |
| `PUT` | `/resources/{id}` | ✅ | Atualiza as informações de um recurso existente. |
| `DELETE` | `/resources/{id}` | ✅ | Remove um recurso do sistema. |
| `POST` | `/ai` | ✅ | Envia dados para a LLM e retorna sugestões (Smart Assist). |

---

## 🛠️ Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior
- PostgreSQL rodando localmente ou em nuvem
- API Key própria para IA

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/fastresources.git](https://github.com/SEU_USUARIO/fastresources.git)
   cd fastresources
   ```
2. **Crie e ative o ambiente virtual:**
  ```bash
  python -m venv venv
  # Linux/macOS:
  source venv/bin/activate
  # Windows:
  venv\Scripts\activate
  ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configuração de Variáveis de Ambiente:**
  Crie um arquivo .env na raiz do projeto contendo as seguintes chaves (não utilize aspas nas chaves):
  ```
  DATABASE_URL=postgresql://usuario:senha@localhost:5432/fastresources
  SECRET_KEY=sua_chave_secreta_jwt_aqui
  OPENAI_API_KEY=sua_chave_da_api_de_ia_aqui
  ```
5. **Iniciando o servidor local**:
   Na raiz do projeto, utilize:
   ```bash
   fastapi dev app/main.py
   ```

6. **Acesse o servidor local**:

   Abra seu navegador em `http://localhost:8000/docs` para testar as rotas via Swagger.

