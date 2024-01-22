import boto3

region_name = "ap-south-1";
sgList = ["sg-0f66fca43fc6186d2"];

ec2_cli = boto3.client(service_name='ec2', region_name=region_name);

for sg in sgList:
    ec2_res = ec2_cli.describe_security_groups(Filters=[{'Name': 'group-id', 'Values': [sg]}]);

    sg_name = ec2_res['SecurityGroups'][0]['GroupName'];
    print(sg_name);
    if(sg_name):
        sg_rule_res = ec2_cli.describe_security_group_rules(Filters=[{'Name': 'group-id', 'Values': [sg]}]);
        if(sg_rule_res):
            for sg_rule in sg_rule_res['SecurityGroupRules']:
                if(sg_rule['IsEgress'] == False):
                    SecurityGroupRuleId = sg_rule['SecurityGroupRuleId'];
                    print(sg_rule);
                else:
                    continue;
                

