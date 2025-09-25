# Terraform Infrastructure Setup

Este diretório contém a configuração de infraestrutura como código (Infrastructure as Code - IaC) para provisionar recursos no Google Cloud Platform (GCP) usando Terraform.

## 📋 Visão Geral

Esta configuração do Terraform provisiona:
- **Compute Engine VM**: Uma máquina virtual `e2-micro` executando Debian 11
- **VPC Network**: Rede virtual privada com sub-redes automáticas
- **Billing Budget**: Orçamento de faturamento com alertas por email
- **Notification Channels**: Canais de notificação por email para alertas

## 🛠 Pré-requisitos

1. **Terraform instalado** (versão >= 1.0)
   ```bash
   # Verificar instalação
   terraform --version
   ```

2. **Google Cloud CLI instalado e configurado**
   ```bash
   # Instalar gcloud CLI
   curl https://sdk.cloud.google.com | bash
   
   # Configurar autenticação
   gcloud auth login
   gcloud config set project SEU-PROJECT-ID
   ```

3. **Credenciais de Service Account**
   - Crie um Service Account no GCP Console
   - Baixe o arquivo JSON de credenciais
   - Renomeie para `credentials.json` e coloque na raiz deste diretório

4. **Permissões necessárias no GCP**
   - Compute Engine Admin
   - Billing Account Administrator
   - Monitoring Admin

## 📁 Estrutura do Projeto

```
Terraform/
├── main.tf                           # Recursos principais
├── variables.tf                      # Variáveis do projeto
├── credentials.json                  # Credenciais GCP (não versionado)
├── .gitignore                       # Arquivos ignorados pelo Git
├── modules/
│   ├── billing_budget/
│   │   ├── main.tf                  # Configuração do orçamento
│   │   └── variables.tf             # Variáveis do orçamento
│   └── notification_channel/
│       ├── main.tf                  # Canais de notificação
│       ├── outputs.tf               # Outputs dos canais
│       └── variables.tf             # Variáveis dos canais
└── README.md                        # Esta documentação
```

## 🚀 Como Usar

### 1. Configuração Inicial

Clone o projeto e navegue para o diretório Terraform:
```bash
cd Terraform
```

### 2. Configurar Variáveis

Edite o arquivo `variables.tf` ou crie um arquivo `terraform.tfvars`:

```hcl
# terraform.tfvars (opcional)
gcp_project_id = "seu-projeto-gcp"
gcp_region = "us-central1"
gcp_zone = "us-central1-a"
billing_account_id = "012345-ABCDEF-GHIJKL"
budget_amount_usd = 250
notification_emails = [
  "admin@empresa.com",
  "devops@empresa.com"
]
```

### 3. Adicionar Credenciais

Coloque seu arquivo de credenciais do Service Account:
```bash
# Copie o arquivo de credenciais para o diretório
cp /caminho/para/suas-credenciais.json ./credentials.json
```

### 4. Executar Terraform

```bash
# Inicializar Terraform (baixar providers)
terraform init

# Validar configuração
terraform validate

# Ver o plano de execução
terraform plan

# Aplicar as mudanças
terraform apply
```

### 5. Verificar Recursos

Após a aplicação bem-sucedida, verifique no GCP Console:
- **Compute Engine** → Instâncias da VM
- **VPC Network** → Redes VPC
- **Billing** → Orçamentos
- **Monitoring** → Canais de notificação

## ⚙️ Variáveis Disponíveis

| Variável | Descrição | Tipo | Valor Padrão |
|----------|-----------|------|--------------|
| `gcp_project_id` | ID do projeto no GCP | string | `"desafio-sauter-adk"` |
| `gcp_region` | Região do GCP | string | `"us-central1"` |
| `gcp_zone` | Zona do GCP | string | `"us-central1-a"` |
| `billing_account_id` | ID da conta de faturamento | string | `"012D12-909E8F-FCF9FC"` |
| `budget_amount_usd` | Valor do orçamento em USD | number | `250` |
| `notification_emails` | Lista de emails para alertas | list(string) | Lista pré-definida |

## 💰 Configuração de Orçamento

O orçamento é configurado com os seguintes alertas:
- **50%** do limite (gastos atuais)
- **80%** do limite (gastos atuais)
- **100%** do limite (gastos previstos)

## 🔧 Comandos Úteis

```bash
# Ver estado atual
terraform show

# Listar recursos gerenciados
terraform state list

# Obter informações de um recurso específico
terraform state show google_compute_instance.vm_instance

# Destruir toda a infraestrutura
terraform destroy

# Reformatar arquivos
terraform fmt

# Importar recurso existente
terraform import google_compute_instance.vm_instance projects/PROJECT_ID/zones/ZONE/instances/INSTANCE_NAME
```

## 🚨 Alertas e Monitoramento

Os alertas de orçamento serão enviados para os emails configurados quando:
1. **50% do orçamento** for atingido (gastos atuais)
2. **80% do orçamento** for atingido (gastos atuais)  
3. **100% do orçamento** for previsto para ser atingido

## 🧹 Limpeza

Para remover todos os recursos criados:
```bash
terraform destroy
```

⚠️ **Atenção**: Este comando remove TODOS os recursos gerenciados pelo Terraform. Use com cuidado!

## 📝 Logs e Debugging

Para debug detalhado:
```bash
export TF_LOG=DEBUG
terraform apply
```

## 🔐 Segurança

- O arquivo `credentials.json` está no `.gitignore` e não deve ser commitado
- Use Service Accounts com permissões mínimas necessárias
- Revise regularmente as permissões e orçamentos configurados

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do Terraform
2. Consulte a [documentação oficial do Terraform](https://www.terraform.io/docs)
3. Verifique a [documentação do provider Google](https://registry.terraform.io/providers/hashicorp/google/latest/docs)