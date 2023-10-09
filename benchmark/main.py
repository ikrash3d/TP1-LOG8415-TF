import os
import boto3
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')

def initialize_clients():
    lb_client = boto3.client('elbv2', region_name="us-east-1", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)
    cloudwatch_client = boto3.client('cloudwatch', region_name="us-east-1", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)
    return lb_client, cloudwatch_client

def get_elb_info(lb_client):
    response_lb = lb_client.describe_load_balancers()
    raw_arn = response_lb['LoadBalancers'][0]['LoadBalancerArn'].split(':')[-1].split('/')
    elb_name = raw_arn[1] + '/'  + raw_arn[2] + '/' + raw_arn[3]
    return elb_name

def get_target_groups(lb_client):
    response_tg = lb_client.describe_target_groups()
    target_group_m4 = response_tg['TargetGroups'][0]['TargetGroupArn'].split(':')[-1]
    target_group_t2 = response_tg['TargetGroups'][1]['TargetGroupArn'].split(':')[-1]
    return target_group_m4, target_group_t2

def get_metric(cloudwatch_client, elb_name, tg,metric_name,stat,get_value) :
    response = cloudwatch_client.get_metric_data(
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
                                    'Value': elb_name
                                },
                            ]
                        },
                        'Period': 300, #5 min period
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

def get_lb_metrics(cloudwatch_client, elb_name, metric_name,stat) :
    response = cloudwatch_client.get_metric_data(
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
                                    'Value': elb_name
                                },
                            ]
                        },
                        'Period': 300, #5 min period
                        'Stat': stat,
                    }
                },
            ],
            StartTime= datetime.utcnow()- timedelta(days=1), 
            EndTime= datetime.utcnow()+timedelta(days=1),    
        )
    return response['MetricDataResults'][0]['Values']

def target_group_plots(cloudwatch_client, elb_name, target_group_m4, target_group_t2):
    fig, ax = plt.subplots()
    x = [
        sum(get_metric(cloudwatch_client, elb_name, target_group_m4, 'RequestCount', 'Sum', True)),
        sum(get_metric(cloudwatch_client, elb_name, target_group_t2, 'RequestCount', 'Sum', True))
    ]
    plt.bar(['m4','t2'],x)
    plt.title('Number of requests per target group')
    plt.savefig('metrics/target-group-reqs.png', bbox_inches='tight')

    m4 = get_metric(cloudwatch_client, elb_name, target_group_m4,'TargetResponseTime','Average',True)
    t2 = get_metric(cloudwatch_client, elb_name, target_group_t2,'TargetResponseTime','Average',True)
    fig, ax = plt.subplots()

    avg_m4 = sum(m4)/len(m4) if len(m4) > 0 else 0
    avg_t2 = sum(t2)/len(t2) if len(t2) > 0 else 0

    x = [avg_m4, avg_t2]
    
    plt.bar(['m4','t2'],x)
    plt.title('Average response time per target group')
    plt.savefig('metrics/target-group-avg-res.png')


def plot_elb_table(cloudwatch_client, elb_name, target_group_m4, target_group_t2):
    act = get_lb_metrics(cloudwatch_client, elb_name, 'ActiveConnectionCount','Sum')
    if act:
        avg_act = sum(act)/len(act)
    else:
        avg_act = 0    
    pros_bytes = sum(get_lb_metrics(cloudwatch_client, elb_name, 'ProcessedBytes','Sum'))
    rq_count = sum(get_lb_metrics(cloudwatch_client, elb_name, 'RequestCount','Sum'))
    hs_m4 = max(get_metric(cloudwatch_client, elb_name, target_group_m4, 'HealthyHostCount','Maximum', True))
    hs_t2 = max(get_metric(cloudwatch_client, elb_name, target_group_t2,'HealthyHostCount','Maximum', True))

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
    lb_client, cloudwatch_client = initialize_clients()
    elb_name = get_elb_info(lb_client)
    target_group_m4, target_group_t2 = get_target_groups(lb_client)

    plot_elb_table(cloudwatch_client, elb_name, target_group_m4, target_group_t2)
    target_group_plots(cloudwatch_client, elb_name, target_group_m4, target_group_t2)





if __name__ == '__main__':
    main()