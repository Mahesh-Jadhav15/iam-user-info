import boto3
from collections import defaultdict

#will create sections using in the env variables or cred
iam_client = boto3.client('iam')

#dic to store using the users 
policy_user_map = defaultdict(list)

#list all the IAM users 
user =iam_client.list_users()['users']

for user in users:
    usernames = user['Username']

    #get attached user policies
    attached_policies = iam_client.list_attached_user_policies(UserName=usernames)['AttachedPlocies']
    for policy in attached_policies:
        policy_user_map[policy['PolicyName']].append(username)

    #we need to group the user and related variables 
    groups =iam_client.list_groups_for_user(UserName=username)['Groups']    
    for policy in groups:
        group_name = group ['GroupName']

        #we need to attach policies to each of the group 
        group_policies = iam_client.list_attached_group_policies(GroupName=group_name)['AttachedPolicies']
        for policy in group_policies :
            policy_user_map[policy['Policy_Name']].append(username)

#after the we need to print the result 
for policy, user in policy_user_map.items():
    print(f"{policy}): {','.join(sorted(set(users)))}")          

