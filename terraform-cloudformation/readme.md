# CloudFormation from Terraform

Create a CloudFormation stack from terraform, for places where terraform does
not have direct support.


## Installation

1. `awscli`, following the latest instructions.  At the time of writing:

    ```
    aws-cli/2.2.17 Python/3.8.8 Darwin/20.5.0 exe/x86_64 prompt/off
    ```


## Usage

Create something in AWS with CloudFormation and see the created resources:

```shell
$ ./scripts/create-stack.sh
$ ./scripts/describe-stack-resources.sh
$ ./scripts/list-sns-topics.sh
```

The same CloudFormation template can be used in terraform, so that terraform
still controls the deployment.

```shell
$ terraform init #do once, after creating a bucket in S3
$ terraform apply
```


## Reference

* General description:
  https://stackoverflow.com/questions/64541206/terraform-resolving-cloudformation-outputs
* `aws_cloudformation_stack`:
  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudformation_stack
