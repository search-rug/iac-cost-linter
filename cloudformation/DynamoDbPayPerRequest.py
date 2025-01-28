from typing import List

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck


class DynamoDbPayPerRequest(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that a DynamoDB table uses pay-per-request billing"
        id = "CKV_AWS_806"
        supported_resources = ["AWS::DynamoDB::Table"]
        categories = [CheckCategories.CONVENTION]
        guideline = "https://search-rug.github.io/iac-cost-patterns/aws-expensive-dynamodb/"
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        properties = conf.get('Properties')
        if properties is not None:
            billing_mode = properties.get('BillingMode')
            if billing_mode == 'PAY_PER_REQUEST':
                return CheckResult.PASSED
        return CheckResult.FAILED

    def get_evaluated_keys(self) -> List[str]:
        return ["Properties/BillingMode"]


check = DynamoDbPayPerRequest()
