import pandas as pd
import tableauserverclient as TSC
import logging
import time
import os
import datetime

# Define the log directory path where the files are located
directory_path = "logs/"

# Define the threshold time to delete files that are older than 10 days
threshold_time = datetime.datetime.now() - datetime.timedelta(days=10)

""" SPECIFY TABLEAU SERVER LOGIN DETAILS BELOW """
server_url = 'http://abc.com/'
sites = ''
username = ''
password = ''

LOG_FILE_GEN_TIME = time.strftime("%Y%m%d-%H%M%S")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(name)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    filename='logs/SubscriptionsRemoval{0}.log'.format(LOG_FILE_GEN_TIME),
    filemode='a'
)

logger = logging.getLogger(__name__)


def delete_logs():
    global directory_path
    # Loop through all files in the logs directory
    try:
        for file_name in os.listdir(directory_path):
            # Get the creation time of the file
            file_path = os.path.join(directory_path, file_name)
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            # Check if the file is older than the threshold time
            if creation_time < threshold_time:
                # Delete the file if it's older than the threshold time
                os.remove(file_path)
                print(f"Log Deleted file: {file_name}")
                logger.info(f"Log file older than 10 days deleted file: {file_name}")
    except Exception as e:
        logging.error(f"Error while deleting log files: {str(e)}")


def execute_main():
    global server_url
    try:
        df_all_subscriptions = pd.DataFrame()
        """ Create connection to Tableau Server """
        logger.info('Connecting to Tableau Server: %s', server_url)
        print('Connecting to Tableau Server: %s', server_url)
        tableau_auth = TSC.TableauAuth(username, password)
        server = TSC.Server(server_url)
        server.add_http_options({'verify': False})

        """ Loop through sites and fetch all subscriptions """
        with server.auth.sign_in(tableau_auth):
            logger.info('Connected to Tableau Server: %s', server_url)
            print('Connected to Tableau Server: %s', server_url)
            for site in TSC.Pager(server.sites):
                server.auth.switch_site(site)
                logger.info('Authenticated to site: %s', site.name)
                logger.info(f'Fetching subscriptions for site: ({site.name})...')
                print('Authenticated to site: %s', site.name)
                print(f'Fetching subscriptions for site: ({site.name})...')
                #subscriptions, pagination_item = server.subscriptions.get()
                for subscription in TSC.Pager(server.subscriptions):
                    view = server.views.get_by_id(subscription.target.id)
                    if site.name == "Default":
                        link = server_url + "#/views/" + view.content_url
                        link = link.replace("sheets/", "")
                        link_html = f'<a href="{link}">click here</a>'
                        logger.info(f'Deleting subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        print(f'Deleting subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        df_all_subscriptions = df_all_subscriptions.append(
                            {'site_name': site.name,
                             'subscription_id': subscription.id,
                             'subscription_subject': subscription.subject,
                             'target view': view.name,
                             'view_url': link_html,
                             'user_id': subscription.user_id}, ignore_index=True)
                        server.subscriptions.delete(subscription.id)
                        logger.info(f'Deleted subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        print(f'Deleted subscription {subscription.id} of ({link}) view for site ({site.name})...')
                    else:
                        link = server_url + "#/site/" + site.content_url + "/views/" + view.content_url
                        link = link.replace("sheets/", "")
                        link_html = f'<a href="{link}">click here</a>'
                        logger.info(f'Deleting subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        print(f'Deleting subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        df_all_subscriptions = df_all_subscriptions.append(
                            {'site_name': site.name,
                             'subscription_id': subscription.id,
                             'subscription_subject': subscription.subject,
                             'target view': view.name,
                             'view_url': link_html,
                             'user_id': subscription.user_id}, ignore_index=True)
                        server.subscriptions.delete(subscription.id)
                        logger.info(f'Deleted subscription {subscription.id} of ({link}) view for site ({site.name})...')
                        print(f'Deleted subscription {subscription.id} of ({link}) view for site ({site.name})...')
        """ Sign out of Tableau Server """
        server.auth.sign_out
        df_all_subscriptions.to_excel('data\\df_all_subscriptions.xlsx')
        print("Completed deletion operations and signed out!")
        logger.info("Completed deletion operations and signed out!")
    except Exception as e:
        logging.error(f'Error while deleting subscription {subscription.id} of ({link}) view for site ({site.name})...')


if __name__ == '__main__':
    logging.info(('#' * 15) + ' Subscription CleanUp Operation Started ' + ('#' * 15))
    print(('#' * 15) + ' Subscription CleanUp Operation Started ' + ('#' * 15))
    delete_logs()
    execute_main()
    print(('#' * 15) + ' Subscription CleanUp Operation Completed ' + ('#' * 15))
    logging.info(('#' * 15) + ' Subscription CleanUp Operation Completed ' + ('#' * 15))