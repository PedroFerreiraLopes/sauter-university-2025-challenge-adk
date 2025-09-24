
resource "google_monitoring_notification_channel" "email" {
  for_each = toset(var.notification_emails)

  display_name = "Canal de Notificação (${each.value})"
  type         = "email"
  labels = {
    email_address = each.value
  }
}