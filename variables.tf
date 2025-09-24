variable "gcp_project_id" {
  description = "O ID do seu projeto no Google Cloud (ex: meu-projeto-12345)."
  type        = string
  default     = "desafio-sauter-adk"
}

variable "gcp_region" {
  description = "A região do GCP a ser usada (ex: us-central1 para o Nível Gratuito)."
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "A zona do GCP a ser usada (ex: us-central1-a)."
  type        = string
  default     = "us-central1-a"
}

variable "billing_account_id" {
  description = "O ID da sua conta de faturamento (Billing Account ID)."
  type        = string
  default     = "012D12-909E8F-FCF9FC"
}

variable "notification_emails" {
  description = "Uma lista de e-mails para receber os alertas de orçamento."
  type        = list(string)
  default     = [
    "jamille.galdinogomes@gmail.com",
    "ogcarvalho@sauter.digital",
    "david.lopes@sauter.digital",
    "mylena.mahatma@sauter.digital",
    "leticiaomf2017@icloud.com"
  ]
}

variable "budget_amount_usd" {
  description = "O valor total do orçamento em Dólares (USD)."
  type        = number
  default     = 250
}