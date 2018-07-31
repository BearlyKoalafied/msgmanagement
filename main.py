import messaging
import auth

def main():
    reddit = auth.get_refreshable_instance()
    while True:
        messaging.scan_inbox(reddit)

if __name__ == "__main__":
    main()
