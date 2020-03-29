resource "aws_iam_role" "tf_container_job_role" {
  name = "tf_container_job_role"
  assume_role_policy = <<EOF
{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Principal":{
        "Service":"ecs-tasks.amazonaws.com"
        },
      "Action":"sts:AssumeRole"}]
    }
EOF
}

resource "aws_iam_role" "tf_cloudwatch_buttsbot_event_target_role" {
  name = "tf_cloudwatch_buttsbot_event_target_role"

  assume_role_policy = <<EOF
{
  "Version":"2012-10-17",
  "Statement":[{
    "Effect":"Allow",
    "Principal":{
      "Service":"events.amazonaws.com"
    },
    "Action":"sts:AssumeRole"
  }]
}
EOF
}