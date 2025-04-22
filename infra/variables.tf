variable "region" {
  description = "AWS region"
  type        = string
}

variable "aws_access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  description = "EC2 instance type for ECS"
  type        = string
}

variable "min_size" {
  description = "Minimum number of EC2 instances in ECS cluster"
  type        = string
}

variable "max_size" {
  description = "Maximum number of EC2 instances in ECS cluster"
  type        = string
}

variable "desired_capacity" {
  description = "Desired number of EC2 instances in ECS cluster"
  type        = string
}