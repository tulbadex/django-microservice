resource "aws_ecs_cluster" "main" {
  name = "task-processing-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = "production"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "task-processing-app"
  network_mode             = "bridge"
  requires_compatibilities = ["EC2"]
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  
  container_definitions = jsonencode([
    {
      name      = "web",
      image     = "${aws_ecr_repository.app.repository_url}:latest",
      essential = true,
      portMappings = [
        {
          containerPort = 8000,
          hostPort      = 8000
        }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options   = {
          awslogs-group         = "/ecs/task-processing",
          awslogs-region        = var.region,
          awslogs-stream-prefix = "web"
        }
      }
    },
    {
      name      = "celery",
      image     = "${aws_ecr_repository.app.repository_url}:latest",
      essential = true,
      command   = ["celery", "-A", "email_api", "worker", "--loglevel=info"],
      logConfiguration = {
        logDriver = "awslogs",
        options   = {
          awslogs-group         = "/ecs/task-processing",
          awslogs-region        = var.region,
          awslogs-stream-prefix = "celery"
        }
      }
    },
    {
      name      = "redis",
      image     = "redis:alpine",
      essential = true,
      portMappings = [
        {
          containerPort = 6379,
          hostPort      = 6379
        }
      ]
    }
  ])

  tags = {
    Environment = "production"
  }
}

resource "aws_ecs_service" "app" {
  name            = "task-processing-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "EC2"

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Environment = "production"
  }
}

resource "aws_ecr_repository" "app" {
  name = "task-processing-app"
}

resource "aws_cloudwatch_log_group" "ecs" {
  name = "/ecs/task-processing"
  retention_in_days = 7
}