import json
import boto3

s3_cli = boto3.client(service_name='s3');
bucket = "bucket-dj-2024";

policy = s3_cli.get_bucket_policy(Bucket=bucket);

policyObj =json.loads(policy['Policy']);

policy_to_add =       {
    "Sid": "AllowSSLRequestsOnly",
    "Action": "s3:*",
    "Effect": "Deny",
    "Resource": [
        f"arn:aws:s3:::{bucket}",
        f"arn:aws:s3:::{bucket}/*"
    ],
    "Condition": {
        "Bool": {
        "aws:SecureTransport": "false"
        }
    },
    "Principal": "*"
    };

if(policyObj.get('Statement') != None):
    print("bucket has policies");
    policyObj['Statement'].append(policy_to_add);
    print(json.dumps(policyObj, indent = "  "));
    policy_res = s3_cli.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policyObj, indent = "  "));
    if(policy_res["ResponseMetadata"] != None):
        print("Policy added successfully !!!!! ");
    else:
        print("Policy cannot be added !!!!!");
else:
    print(f"{bucket} has no policies !!!!!");
