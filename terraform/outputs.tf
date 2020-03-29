output "tf_buttsbot_checked_links_endpoint" {
  value = aws_db_instance.tf_buttsbot_checked_links.endpoint
}

output "tf_buttsbot_repository_url" {
  value = aws_ecr_repository.tf_buttsbot_repository.repository_url
}