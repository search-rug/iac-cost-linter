import re
from typing import List

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck


def is_old_instance_type(it):
    return re.search(r't2|m3|m4|c4', it) != None


class OldGeneration(BaseResourceCheck):
    def __init__(self):
        name = "Ensure instances do not use old generation instance classes to save cost"
        id = "CKV_AWS_807"
        supported_resources = ["AWS::EC2::Instance", "AWS::SageMaker::NotebookInstance", "AWS::RDS::DBInstance"]
        categories = [CheckCategories.CONVENTION]
        guideline = "https://search-rug.github.io/iac-cost-patterns/old-generation/"
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        resource_type = conf.get('Type')
        properties = conf.get('Properties')

        if resource_type is not None and properties is not None:
            if resource_type == "AWS::EC2::Instance" or resource_type == "AWS::SageMaker::NotebookInstance":
                instance_type_prop = "InstanceType"
            elif resource_type == "AWS::RDS::DBInstance":
                instance_type_prop = "DBInstanceClass"

            if instance_type_prop:
                self.evaluated_keys = [f"Properties/{instance_type_prop}"]

                if not is_old_instance_type(properties.get(instance_type_prop)):
                    return CheckResult.PASSED

        return CheckResult.FAILED


check = OldGeneration()
