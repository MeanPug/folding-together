from troposphere import Parameter, Output, Ref, Template, If, Join, Sub, GetAZs, Select, GetAtt, Retain
from troposphere.iam import Role, InstanceProfile, PolicyType, User, Group, Policy, AccessKey
from troposphere.ecr import Repository, LifecyclePolicy
import json


class FrontendPaymentsRegistrationStack(object):
    def __init__(self, sceptre_data):
        self.sceptre_data = sceptre_data
        self.template = Template()

        self.add_params()
        self.add_resources()
        self.add_outputs()

    def add_params(self):
        self.environment = self.template.add_parameter(Parameter(
            'Environment',
            Description='The type of environment (production, staging, etc.) we are in',
            Type='String'
        ))

        self.service_name = self.template.add_parameter(Parameter(
            'ServiceName',
            Description='Name of the frontend service',
            Type='String'
        ))

    def add_resources(self):
        self.add_iam_resources()
        self.add_ecr_resources()

    def add_iam_resources(self):
        self.pod_role = self.template.add_resource(Role(
            'FrontendPaymentsRegistrationPodRole',
            RoleName=Join('-', [
                Join('', [Ref(self.service_name), 'PodRole']),
                Ref(self.environment)]
            ),
            Path=Sub('/${Environment}/pod_roles/'),
            AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
        ))

    def add_ecr_resources(self):
        self.template.add_resource(Repository(
            'FrontendPaymentsRegistrationECRRepo',
            LifecyclePolicy=LifecyclePolicy(
                LifecyclePolicyText=json.dumps({
                    "rules": [
                        {
                            "rulePriority": 10,
                            "description": "Expire images more than 10 pushes old",
                            "selection": {
                                "tagStatus": "any",
                                "countType": "imageCountMoreThan",
                                "countNumber": 10
                            },
                            "action": {
                                "type": "expire"
                            }
                        }
                    ]
                })
            ),
            RepositoryName=Sub('${Environment}/frontend-payments-registration')
        ))

    def add_outputs(self):
        pass


def sceptre_handler(sceptre_user_data):
    stack = FrontendPaymentsRegistrationStack(sceptre_user_data)
    return stack.template.to_json()
