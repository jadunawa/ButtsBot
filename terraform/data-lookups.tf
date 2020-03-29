data "aws_iam_role" "AWSBatchServiceRole_role" {
  name = "AWSBatchServiceRole"
}

data "aws_iam_instance_profile" "ecsInstanceProfile" {
  name = "ecsInstanceRole"
}