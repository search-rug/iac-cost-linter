from typing import List

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck


class S3BucketLifecycleRules(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that an S3 bucket has lifecycle rules"
        id = "CKV_AWS_805"
        supported_resources = ["AWS::S3::Bucket"]
        categories = [CheckCategories.LOGGING]
        guideline = "https://search-rug.github.io/iac-cost-patterns/object-storage-lifecycle-rules/"
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        properties = conf.get('Properties')
        if properties is not None:
            lifecycle_config = properties.get('LifecycleConfiguration')
            if lifecycle_config is not None:
                rules = lifecycle_config.get('Rules')
                if rules is not None and len(rules) >= 1:
                    return CheckResult.PASSED
        return CheckResult.FAILED

    def get_evaluated_keys(self) -> List[str]:
        return ["Properties/LifecycleConfiguration/Rules"]


check = S3BucketLifecycleRules()
