from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class DynamoDbHighRwCapacity(BaseResourceCheck):
    def __init__(self):
        # This is the full description of your check
        description = "Ensure that DynamoDB tables do not use high read/write capacity"

        # This is the Unique ID for your check
        id = "CKV_AWS_802"

        # These are the terraform objects supported by this check (ex: aws_iam_policy_document)
        supported_resources = ['aws_dynamodb_table']

        guideline = 'https://search-rug.github.io/iac-cost-patterns/aws-expensive-dynamodb/'

        # Valid CheckCategories are defined in checkov/common/models/enums.py
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=description, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        # read_capacity and write_capacity are ignored in PAY_PER_REQUEST MODE
        if 'billing_mode' in conf.keys() and 'PAY_PER_REQUEST' in conf['billing_mode']:
            return CheckResult.PASSED

        if 'read_capacity' in conf.keys() and any((isinstance(v, int) and v > 1) for v in conf['read_capacity']):
            self.details.append('Using high read capacity might incur unnecessary cost for infrequently accessed tables')
            return CheckResult.FAILED

        if 'write_capacity' in conf.keys() and any((isinstance(v, int) and v > 1) for v in conf['write_capacity']):
            self.details.append('Using high write capacity might incur unnecessary cost for infrequently accessed tables')
            return CheckResult.FAILED

        return CheckResult.PASSED


check = DynamoDbHighRwCapacity()
