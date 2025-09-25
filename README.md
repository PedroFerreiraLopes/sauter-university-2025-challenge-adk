# 🚀 Repositório Multi-Aplicações - Sauter Digital

Este repositório contém um conjunto de aplicações modernas para demonstrar diferentes tecnologias e arquiteturas de software. Cada aplicação foi desenvolvida com foco em boas práticas, escalabilidade e facilidade de manutenção.

## 📋 Visão Geral do Repositório

Este repositório é organizado como um **monorepo**, onde diferentes aplicações coexistem de forma independente, cada uma com sua própria documentação e configurações específicas.

### 🏗️ Aplicações Disponíveis

| Aplicação | Diretório | Tecnologia Principal | Descrição |
|-----------|-----------|---------------------|-----------|
| **Infraestrutura GCP** | `/Terraform` | Terraform | Provisiona infraestrutura no Google Cloud Platform |
| **Sistema Multi-Agente** | `/agentes_adk` | Google ADK + Python | Chatbot inteligente com agentes especializados |
| **API de Reservatórios** | `/api` | FastAPI + Python | API REST para pipeline ETL e consulta de dados |

---

## 🗺️ Como Navegar no Repositório

### Estrutura Geral
```
📁 repositorio-raiz/
├── 📄 README.md                    # Esta documentação (você está aqui!)
├── 📁 Terraform/                   # Infraestrutura como Código
│   ├── 📄 README.md               # Documentação específica do Terraform
│   ├── 📄 main.tf                 # Recursos principais do GCP
│   └── 📁 modules/                # Módulos reutilizáveis
├── 📁 agentes_adk/                # Sistema de Agentes Inteligentes
│   ├── 📄 README.md               # Documentação específica dos agentes
│   ├── 📁 adk_estudo/             # Exemplo básico
│   └── 📁 agente_implementacao/   # Sistema completo
└── 📁 api/                        # API FastAPI
    ├── 📄 README.md               # Documentação específica da API
    ├── 📄 Dockerfile              # Container Docker
    ├── 📁 src/app/                # Código da aplicação
    └── 📁 pipeline/               # Módulos ETL
```

### Navegação Básica via Terminal

```bash
# 1. Clonar o repositório (se ainda não fez)
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>

# 2. Visualizar a estrutura completa
tree -L 2
# ou se não tiver o tree instalado:
find . -maxdepth 2 -type d | sort

# 3. Listar apenas os diretórios principais
ls -la

# 4. Navegar para uma aplicação específica
cd Terraform          # Para infraestrutura
# ou
cd agentes_adk        # Para sistema de agentes
# ou  
cd api               # Para a API FastAPI

# 5. Voltar para a raiz do repositório
cd ..                # Sobe um nível
# ou
cd ~/caminho/para/repositorio-raiz
```

### Comandos Úteis para Exploração

```bash
# Ver todos os arquivos README.md disponíveis
find . -name "README.md" -type f

# Buscar por arquivos de configuração
find . -name "*.tf" -o -name "*.py" -o -name "Dockerfile" | head -10

# Ver o tamanho de cada diretório
du -sh */ | sort -hr

# Contar linhas de código em cada aplicação
find Terraform -name "*.tf" | xargs wc -l
find agentes_adk -name "*.py" | xargs wc -l  
find api -name "*.py" | xargs wc -l
```

---

## 📚 Documentação Específica de Cada Aplicação

Cada aplicação possui sua **própria documentação detalhada** no arquivo `README.md` dentro do respectivo diretório. Esta abordagem garante que:

- ✅ **Informações Específicas**: Cada README contém instruções exclusivas da aplicação
- ✅ **Contexto Isolado**: Você não se confunde com instruções de outras aplicações  
- ✅ **Manutenção Simplificada**: Atualizações são feitas de forma independente
- ✅ **Onboarding Focado**: Você pode focar apenas na aplicação que precisa usar

### 🎯 Para Começar com uma Aplicação Específica

#### 1. **Terraform (Infraestrutura GCP)**
```bash
cd Terraform
cat README.md        # Leia a documentação completa
terraform --version  # Verifique se tem o Terraform instalado
```
**O que você encontrará:**
- Como provisionar recursos no Google Cloud
- Configuração de VMs, redes e orçamentos
- Comandos passo-a-passo do Terraform

#### 2. **Agentes ADK (Sistema Multi-Agente)**
```bash
cd agentes_adk
cat README.md        # Leia a documentação completa
python --version     # Verifique se tem Python 3.10+
```
**O que você encontrará:**
- Como criar agentes inteligentes com Google ADK
- Sistema de orquestração entre agentes especializados
- API FastAPI para interagir com os agentes

#### 3. **API (Pipeline ETL + Consulta de Dados)**
```bash
cd api
cat README.md        # Leia a documentação completa
pip list | grep fastapi  # Verifique se tem FastAPI instalado
```
**O que você encontrará:**
- API REST para pipeline de dados da ONS
- Integração com BigQuery e Google Cloud Storage
- Sistema completo de ETL (Extract, Transform, Load)

---

## 🛠️ Pré-requisitos Gerais

Antes de trabalhar com qualquer aplicação, certifique-se de ter:

### Software Essencial
```bash
# Python 3.10 ou superior
python --version

# Git para versionamento
git --version

# Google Cloud CLI (para aplicações que usam GCP)
gcloud --version

# Docker (opcional, mas recomendado)
docker --version
```

### Configuração Inicial do Google Cloud
```bash
# 1. Fazer login no Google Cloud
gcloud auth login

# 2. Definir projeto padrão  
gcloud config set project SEU-PROJETO-GCP

# 3. Habilitar autenticação para aplicações
gcloud auth application-default login
```

---

## 🎯 Fluxo de Trabalho Recomendado

### Para Novatos (Primeira vez usando este repositório)

1. **📖 Leia este README** completamente para entender a estrutura geral
2. **🎯 Escolha uma aplicação** que você quer usar ou aprender
3. **📂 Navegue para o diretório** da aplicação escolhida
4. **📚 Leia o README específico** da aplicação
5. **⚡ Siga as instruções** passo-a-passo da documentação específica

### Para Desenvolvedores Experientes

1. **🔍 Explore a estrutura** usando `tree` ou `ls`
2. **📋 Verifique os pré-requisitos** de cada aplicação
3. **🚀 Execute as aplicações** que você precisa
4. **🔧 Customize** conforme suas necessidades

---

## 🤝 Como Contribuir

### Adicionando Nova Aplicação

1. **Crie um novo diretório** na raiz do repositório
2. **Adicione um README.md** seguindo o padrão das outras aplicações
3. **Atualize este README** incluindo a nova aplicação na tabela
4. **Teste** todas as instruções da documentação

### Melhorando Documentação Existente

1. **Identifique pontos confusos** nas documentações
2. **Proponha melhorias** via pull request
3. **Teste as instruções** em ambiente limpo
4. **Documente** qualquer nova dependência ou passo

---

## ❗ Avisos Importantes

### 💰 Custos do Google Cloud
- As aplicações que usam Google Cloud **podem gerar custos**
- Sempre configure **orçamentos e alertas** antes de usar
- Use a **camada gratuita** sempre que possível
- **Monitore** regularmente seus gastos no GCP Console

### 🔐 Segurança
- **NUNCA** commite credenciais nos arquivos de código
- Use **variáveis de ambiente** ou **arquivos ignorados pelo git**
- Configure **permissões mínimas** para Service Accounts
- **Revise** regularmente acessos e permissões

### 📁 Organização
- Cada aplicação é **independente** - não misture configurações
- **Leia sempre** o README específico antes de começar
- **Siga as convenções** de nomenclatura de cada tecnologia
- **Documente** qualquer customização que você fizer

---

## 📞 Suporte e Dúvidas

### Hierarquia de Suporte

1. **📚 Documentação específica** da aplicação (README.md de cada pasta)
2. **🔍 Issues do repositório** (se for um repositório público)
3. **📖 Documentação oficial** das tecnologias usadas:
   - [Terraform](https://terraform.io/docs)
   - [Google Cloud](https://cloud.google.com/docs)  
   - [FastAPI](https://fastapi.tiangolo.com)
   - [Google ADK](https://cloud.google.com/vertex-ai/docs/agent-builder)

### Troubleshooting Geral

```bash
# Verificar versões de software
python --version && terraform --version && gcloud --version

# Verificar autenticação Google Cloud
gcloud auth list

# Verificar projeto ativo
gcloud config get-value project

# Testar conectividade
ping google.com
```

---

## 🎉 Próximos Passos

Agora que você entendeu a estrutura geral, escolha uma das aplicações abaixo e **mergulhe na documentação específica**:

- 🏗️ **Quer provisionar infraestrutura?** → `cd Terraform && cat README.md`
- 🤖 **Quer criar agentes inteligentes?** → `cd agentes_adk && cat README.md` 
- ⚡ **Quer construir APIs de dados?** → `cd api && cat README.md`

**Lembre-se**: Cada aplicação tem sua própria documentação completa e atualizada! 🚀