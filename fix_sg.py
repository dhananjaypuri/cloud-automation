import boto3

region_name = "ap-south-1";
sgList = ["sg-0f66fca43fc6186d2"];

ec2_cli = boto3.client(service_name='ec2', region_name=region_name);

for sg in sgList:
    ec2_res = ec2_cli.describe_security_groups(Filters=[{'Name': 'group-id', 'Values': [sg]}]);

    sg_name = ec2_res['SecurityGroups'][0]['GroupName'];
    print(sg_name);
    sg_update_ruleList = [];
    if(sg_name):
        sg_rule_res = ec2_cli.describe_security_group_rules(Filters=[{'Name': 'group-id', 'Values': [sg]}]);
        if(sg_rule_res):
            for sg_rule in sg_rule_res['SecurityGroupRules']:
                if((sg_rule.get('IsEgress') == False) and (sg_rule.get('CidrIpv4') == "0.0.0.0/0")):
                    SecurityGroupRuleId = sg_rule['SecurityGroupRuleId'];
                    sg_rule['CidrIpv4'] = "10.0.0.0/8";
                    sg_update_ruleList.append(        {
                                                'SecurityGroupRuleId': SecurityGroupRuleId,
                                                'SecurityGroupRule': {
                                                    'IpProtocol': sg_rule.get('IpProtocol'),
                                                    'FromPort': sg_rule.get('FromPort'),
                                                    'ToPort': sg_rule.get('ToPort'),
                                                    'CidrIpv4': sg_rule.get('CidrIpv4'),
                                                    'Description': sg_rule.get('Description')
                                                }
                                            });
                else:
                    continue;
    if(len(sg_update_ruleList)>0):
        print(f"Need to change {len(sg_update_ruleList)} rules in {sg_name} ");
        for rule in sg_update_ruleList:
            print(rule);
    else:
        print("No security group needs to be changed");
                

