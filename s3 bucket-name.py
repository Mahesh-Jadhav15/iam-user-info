import boto3
import json
import re

# Step 1: Initialize IAM client
iam = boto3.client('iam')

# Step 2: Get the ARN of the policy
policy_list = iam.list_policies(Scope='Local')['Policies']
policy_arn = None

for policy in policy_list:
    if policy['PolicyName'] == 'interview_s3_read':
        policy_arn = policy['Arn']
        break

if not policy_arn:
    raise Exception("Policy 'interview_s3_read' not found.")

# Step 3: Get the default version of the policy
version_id = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
policy_document = iam.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)['PolicyVersion']['Document']

# Step 4: Extract bucket name
bucket_name = None

for statement in policy_document['Statement']:
    if statement['Effect'] == 'Allow' and 's3:GetObject' in statement['Action']:
        resources = statement['Resource']
        if isinstance(resources, str):
            resources = [resources]

        for resource in resources:
            match = re.match(r'arn:aws:s3:::([^/]+)/\*', resource)
            if match:
                bucket_name = match.group(1)
                break
    if bucket_name:
        break

if not bucket_name:
    raise Exception("S3 bucket not found in policy.")

print("Bucket Name:", bucket_name)

# Step 5: List objects in the bucket
s3 = boto3.client('s3', region_name='ap-south-1')
response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' not in response:
    raise Exception(f"No objects found in bucket '{bucket_name}'")

# Step 6: Find the first JSON file or use 'data.json'
object_key = None
for obj in response['Contents']:
    if obj['Key'].endswith('.json'):
        object_key = obj['Key']
        break

if not object_key:
    raise Exception("No JSON file found in bucket.")

print("Object Key:", object_key)

# Step 7: Download the file
local_filename = 'data.json'
s3.download_file(bucket_name, object_key, local_filename)

# Step 8: Read and parse JSON
with open(local_filename, 'r') as f:
    data = json.load(f)
    print("Result:", data.get('result', 'Key \"result\" not found in JSON'))
