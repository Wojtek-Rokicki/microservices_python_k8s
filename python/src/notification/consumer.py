import pika, sys, os, time

from send import email

def main():

    print("Starting connection ...", file = sys.stderr)
    # rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq") # this service name will resolve into ip address
    )
    channel = connection.channel()
    print("Connected", file = sys.stderr)

    def callback(ch, method, properties, body):
        err = email.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag) # if there is a failure to convert the video, then the message won't be deleted from the queue. delivery_tag uniquelly identifies the delivery on the channel
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"), on_message_callback=callback # callback invoked whenever message is pulled of the queue
    )

    print("Begining to consume messages ...", file = sys.stderr)

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)