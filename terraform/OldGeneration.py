import re

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


def is_old_instance_type(it):
    return re.search(r't2|m4', it) != None


def is_old_volume_type(vt):
    return re.search(r'gp2', vt) != None


class OldGeneration(BaseResourceCheck):
    def __init__(self):
        # This is the full description of your check
        description = "Ensure instances and volumes do not use older generation versions to save cost"

        # This is the Unique ID for your check
        id = "CKV_AWS_804"

        # These are the terraform objects supported by this check (ex: aws_iam_policy_document)
        supported_resources = ['aws_instance', 'aws_ebs_volume']

        guideline = 'https://search-rug.github.io/iac-cost-patterns/old-generation/'

        # Valid CheckCategories are defined in checkov/common/models/enums.py
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=description, id=id, categories=categories, supported_resources=supported_resources, guideline=guideline)

    def scan_resource_conf(self, conf):
        if self.entity_type == 'aws_instance':
            if 'instance_type' in conf.keys() and is_old_instance_type(conf['instance_type'][0]):
                self.details.append('Older generation instances might have worse performance and cost more than newer generations')
                return CheckResult.FAILED

            if 'root_block_device' in conf.keys():
                block = conf['root_block_device'][0]
                if isinstance(block, dict) and 'volume_type' in block.keys() and is_old_instance_type(block['volume_type'][0]):
                    self.details.append('Older generation volumes might have worse performance and cost more than newer generations')
                    return CheckResult.FAILED

        elif self.entity_type == 'aws_ebs_volume' and 'type' in conf.keys() and is_old_volume_type(conf['type'][0]):
            self.details.append('Older generation volumes might have worse performance and cost more than newer generations')
            return CheckResult.FAILED

        return CheckResult.PASSED


check = OldGeneration()
