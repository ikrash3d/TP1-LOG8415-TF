import os
import boto3
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')


def initialize_clients():
    elbv2_client = boto3.client('elbv2', region_name="us-east-1", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)
    cloudwatch = boto3.client('cloudwatch', region_name="us-east-1", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)
    return elbv2_client, cloudwatch

def get_elb_info(elbv2_client):
    load_balancers = elbv2_client.describe_load_balancers()
    arns = load_balancers['LoadBalancers'][0]['LoadBalancerArn'].split(':')[-1].split('/')
    elbv2_info = arns[1] + '/'  + arns[2] + '/' + arns[3]
    return elbv2_info

def get_target_groups(elbv2_client):
    target_groups = elbv2_client.describe_target_groups()
    target_group_m4 = target_groups['TargetGroups'][0]['TargetGroupArn'].split(':')[-1]
    target_group_t2 = target_groups['TargetGroups'][1]['TargetGroupArn'].split(':')[-1]
    return target_group_m4, target_group_t2

def get_metric(cloudwatch, elbv2_info, tg,metric_name,stat,get_value) :
    response = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'myrequest',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/ApplicationELB',
                            'MetricName': metric_name,
                            'Dimensions': [
                                {
                                    'Name': 'TargetGroup',
                                    'Value': tg
                                },
                                {                        
                                    'Name': 'LoadBalancer',
                                    'Value': elbv2_info
                                },
                            ]
                        },
                        'Period': 300,
                        'Stat': stat,
                    }
                },
            ],
            StartTime= datetime.utcnow()- timedelta(days=1), 
            EndTime= datetime.utcnow()+timedelta(days=1),    
        )

    if get_value : 
        return response['MetricDataResults'][0]['Values']
    else :
        return response

def get_lb_metrics(cloudwatch, elbv2_info, metric_name, stat) :
    response = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'myrequest',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/ApplicationELB',
                            'MetricName': metric_name,
                            'Dimensions': [
                                {                        
                                    'Name': 'LoadBalancer',
                                    'Value': elbv2_info
                                },
                            ]
                        },
                        'Period': 300,
                        'Stat': stat,
                    }
                },
            ],
            StartTime= datetime.utcnow()- timedelta(days=1), 
            EndTime= datetime.utcnow()+timedelta(days=1),    
        )
    return response['MetricDataResults'][0]['Values']

def build_target_groups(cloudwatch, elbv2_info, target_group_m4, target_group_t2):
    fig, ax = plt.subplots()
    x = [
        sum(get_metric(cloudwatch, elbv2_info, target_group_m4, 'RequestCount', 'Sum', True)),
        sum(get_metric(cloudwatch, elbv2_info, target_group_t2, 'RequestCount', 'Sum', True))
    ]
    plt.bar(['m4','t2'],x)
    plt.title('Number of requests per target group')
    plt.savefig('metrics/target-group-reqs.png', bbox_inches='tight')

    m4 = get_metric(cloudwatch, elbv2_info, target_group_m4,'TargetResponseTime','Average',True)
    t2 = get_metric(cloudwatch, elbv2_info, target_group_t2,'TargetResponseTime','Average',True)
    fig, ax = plt.subplots()

    avg_m4 = sum(m4)/len(m4) if len(m4) > 0 else 0
    avg_t2 = sum(t2)/len(t2) if len(t2) > 0 else 0

    x = [avg_m4, avg_t2]
    
    plt.bar(['m4','t2'],x)
    plt.title('Average response time per target group')
    plt.savefig('metrics/target-group-avg-res.png')


def build_table(cloudwatch, elbv2_info, target_group_m4, target_group_t2):
    act = get_lb_metrics(cloudwatch, elbv2_info, 'ActiveConnectionCount','Sum')
    if act:
        avg_act = sum(act)/len(act)
    else:
        avg_act = 0    
    pros_bytes = sum(get_lb_metrics(cloudwatch, elbv2_info, 'ProcessedBytes','Sum'))
    rq_count = sum(get_lb_metrics(cloudwatch, elbv2_info, 'RequestCount','Sum'))
    hs_m4 = max(get_metric(cloudwatch, elbv2_info, target_group_m4, 'HealthyHostCount','Maximum', True))
    hs_t2 = max(get_metric(cloudwatch, elbv2_info, target_group_t2,'HealthyHostCount','Maximum', True))

    table_data=[
    ["Average active connection count", avg_act],
    ["Total bytes processed", pros_bytes],
    ["Total request count", rq_count],
    ["Number of healty hosts in M4", hs_m4],
    ['Number of healthy hosts in T2', hs_t2]
    ]

    fig, ax = plt.subplots()
    table = ax.table(cellText=table_data, loc='center')
    table.set_fontsize(14)
    table.scale(1,4)
    ax.axis('off')
    plt.title('Different elb metrics')
    plt.savefig('metrics/elb-plots.png', bbox_inches='tight')

def main():
    elbv2_client, cloudwatch = initialize_clients()
    elbv2_info = get_elb_info(elbv2_client)
    target_group_m4, target_group_t2 = get_target_groups(elbv2_client)

    build_table(cloudwatch, elbv2_info, target_group_m4, target_group_t2)
    build_target_groups(cloudwatch, elbv2_info, target_group_m4, target_group_t2)


if __name__ == '__main__':
    main()