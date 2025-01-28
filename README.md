# Infrastructure as Code Cost Linter Rules

This repository hosts a set of linter rules for detecting cost issues in Infrastructure as Code artifacts.

Specifically, it contains checks for [Checkov](https://checkov.io) implementing a subset of the IaC cost (anti)patterns, as defined in [search-rug/iac-cost-patterns](https://github.com/search-rug/iac-cost-patterns).

## Usage

Checkov can directly use the checks defined in this repository:
```sh
checkov \
  --external-checks-git https://github.com/search-rug/iac-cost-linter.git//<terraform or cloudformation>/ \
  --check <check ID> \
  --file <file>
```

For the check ID, see the table below.

| Cost (anti)pattern | Terraform check | CloudFormation check |
|---|---|---|
| [Object storage lifecycle rules](https://search-rug.github.io/iac-cost-patterns/object-storage-lifecycle-rules/) | `CKV2_AWS_61` [^1] | `CKV_AWS_805` |
| [Old generation](https://search-rug.github.io/iac-cost-patterns/old-generation/) | `CKV_AWS_804` | `CKV_AWS_807` |
| [AWS - Expensive DynamoDB](https://search-rug.github.io/iac-cost-patterns/aws-expensive-dynamodb/) | `CKV_AWS_801` <br> `CKV_AWS_802` <br> `CKV_AWS_803` | `CKV_AWS_806` |

[^1]: `CKV2_AWS_61` is a built-in Checkov check. Its source is available [here](https://github.com/bridgecrewio/checkov/blob/main/checkov/terraform/checks/graph_checks/aws/S3BucketLifecycle.yaml).

## License

Apache 2.0, see `LICENSE`.
