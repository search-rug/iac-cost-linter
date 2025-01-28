from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class DynamoDbPayPerRequest(BaseResourceCheck):
    def __init__(self):
        # This is the full description of your check
        description = "Ensure that DynamoDB tables use PAY_PER_REQUEST billing mode"

        # This is the Unique ID for your check
        id = "CKV_AWS_801"

        # These are the terraform objects supported by this check (ex: aws_iam_policy_document)
        supported_resources = ['aws_dynamodb_table']

        guideline = 'https://search-rug.github.io/iac-cost-patterns/aws-expensive-dynamodb/'

        # Valid CheckCategories are defined in checkov/common/models/enums.py
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=description, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        if 'billing_mode' not in conf.keys() or 'PAY_PER_REQUEST' not in conf['billing_mode']:
            self.details.append('Using provisioned billing mode might incur unnecessary cost for infrequently accessed tables')
            return CheckResult.FAILED

        return CheckResult.PASSED


check = DynamoDbPayPerRequest()
