resource "aws_batch_compute_environment" "tf_batch_buttsbot_compute_environment" {
  type                     = "MANAGED"
  compute_environment_name = "tf_batch_buttsbot_compute_environment"
  service_role             = data.aws_iam_role.AWSBatchServiceRole_role.arn

  compute_resources {
    instance_role      = data.aws_iam_instance_profile.ecsInstanceProfile.arn
    instance_type      = ["a1.medium"]
    max_vcpus          = 256
    min_vcpus          = 1
    desired_vcpus      = 2
    security_group_ids = ["sg-834d07af"]
    subnets            = ["subnet-35c9236a", "subnet-d5c86bdb", "subnet-e84ba58e", "subnet-3930c418", "subnet-a7f4c999", "subnet-d19f269c"]
    type               = "EC2"
  }
}

resource "aws_batch_job_queue" "tf_batch_buttsbot_job_queue" {
  name                 = "tf_batch_buttsbot_job_queue"
  state                = "ENABLED"
  priority             = 1
  compute_environments = ["${aws_batch_compute_environment.tf_batch_buttsbot_compute_environment.arn}"]
}

resource "aws_batch_job_definition" "tf_batch_buttsbot_job_definition" {
  name = "tf_batch_buttsbot_job_definition"
  type = "container"

  container_properties = <<CONTAINER_PROPERTIES
  {
    "image": "935278506128.dkr.ecr.us-east-1.amazonaws.com/tf_buttsbot_repository:latest",
    "memory": 1024,
    "vcpus": 16,
    "jobRoleArn": "${aws_iam_role.tf_container_job_role.arn}"
  }
  CONTAINER_PROPERTIES
}