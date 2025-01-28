from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class DynamoDbNoGlobalSecondaryIndex(BaseResourceCheck):
    def __init__(self):
        # This is the full description of your check
        description = "Ensure that no global secondary indices are used"

        # This is the Unique ID for your check
        id = "CKV_AWS_803"

        # These are the terraform objects supported by this check (ex: aws_iam_policy_document)
        supported_resources = ['aws_dynamodb_table']

        guideline = 'https://search-rug.github.io/iac-cost-patterns/aws-expensive-dynamodb/'

        # Valid CheckCategories are defined in checkov/common/models/enums.py
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=description, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        if 'global_secondary_index' in conf.keys():
            self.details.append('Global secondary indices are expensive and may not be necessary')
            return CheckResult.FAILED

        return CheckResult.PASSED


check = DynamoDbNoGlobalSecondaryIndex()
