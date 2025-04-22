provider "aws" {
  region     = var.region
  # Only use these if environment variables aren't set
  access_key = var.aws_access_key != "" ? var.aws_access_key : null
  secret_key = var.aws_secret_key != "" ? var.aws_secret_key : null
}