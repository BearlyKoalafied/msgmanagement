import messaging
import auth
import logger

def main():
    logger.prep(logger.MSG_LOGGER)
    reddit = auth.get_refreshable_instance()
    while True:
        messaging.scan_inbox(reddit)

if __name__ == "__main__":
    main()
