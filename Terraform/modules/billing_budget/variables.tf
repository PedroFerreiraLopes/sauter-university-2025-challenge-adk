variable "billing_account_id" { 
type = string 
default= "012D12-909E8F-FCF9FC"
}
variable "project_id" { 
    type = string 
    default = "desafio-sauter-adk"
    }
variable "budget_amount" { 
    type = number 
    default = 250
    
    }
variable "notification_channel_ids" {
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

