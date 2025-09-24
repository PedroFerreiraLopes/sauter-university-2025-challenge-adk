output "channel_ids" {
  description = "A lista dos IDs dos canais de notificação criados."
  value       = [for channel in google_monitoring_notification_channel.email : channel.id]
}