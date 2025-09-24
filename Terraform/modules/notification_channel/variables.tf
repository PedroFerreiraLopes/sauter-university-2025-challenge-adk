variable "notification_emails" {
  description = "A lista de e-mails para criar os canais."
  type        = list(string)
  default = [  "jamille.galdinogomes@gmail.com",
    "ogcarvalho@sauter.digital",
    "david.lopes@sauter.digital",
    "mylena.mahatma@sauter.digital",
    "leticiaomf2017@icloud.com" ]
}