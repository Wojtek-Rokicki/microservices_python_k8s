import pika, json, sys

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err, file=sys.stderr)
        return "internal server error", 500
    
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange = "",
            routing_key = "video", # which will be the name of the queue, because of not specifying exchange
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # messages should persist in the queue in case our pod crashes or restarts
            ),
        )
    except Exception as err:
        print(err, file=sys.stderr)
        fs.delete(fid) # if cannot send message file will not be processed, so delete it
        return "internal server error", 500