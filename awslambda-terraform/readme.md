# AWS Lambda in Python via Terraform

Deploy a lambda function with terraform that is triggered by SNS messages.


## Example

```shell
$ ./scripts.build.sh
$ terraform init #do once, after creating a bucket in S3
$ terraform apply
```


## Learnings about Lambdas

1. Lambda Triggers are created by `aws_lambda_permission`, and the lambda won't
   do anything without it.  This is listed in the AWS Console under Lambda ->
   Configuration -> Triggers.
1. Lambdas need `AWSLambdaBasicExecutionRole`, in order to log to CloudWatch.
1. Lambda responses automatically format as JSON, when invoked synchonously,
   when returning a `dict`:
   https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html#python-handler-return


## Organizing Terraform

It's helping to name and organize terraform files that:

* Primary entities are listed in workflow order, where possible, and
  alphabetically otherwise.
* Secondary data and entities appear after their primary counterparts, following
  the step-down rule.  An IAM policy is listed after the IAM role that refers to
  it, for example.
* Dependent entities are named with their owner, like `echo_role` being the IAM
  role for the `echo` function.
