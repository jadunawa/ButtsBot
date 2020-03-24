resource "aws_db_instance" "tf-buttsbot-checked-links" {
  engine                    = "mariadb"
  instance_class            = "db.t2.micro"
  allocated_storage         = 20
  username                  = "buttsbot"
  password                  = var.rds_password
  identifier                = "tf-buttsbot-checked-links"
  final_snapshot_identifier = "tf-buttbost-checked-links-final-snapshot"
  skip_final_snapshot       = "false"
  publicly_accessible       = "true"
  vpc_security_group_ids    = ["${aws_security_group.tf-buttsbot-checked-links-open-world.id}"] # attach security group to db
}

resource "aws_security_group" "tf-buttsbot-checked-links-open-world" {
  name = "tf-buttsbot-checked-links-open-world"

  ingress {
    description = "Access from anywhere"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
  }

  egress {
    description = "Access to the outside"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
  }
}


output "tf-buttsbot-checked-links-endpoint" {
  value = aws_db_instance.tf-buttsbot-checked-links.endpoint
}