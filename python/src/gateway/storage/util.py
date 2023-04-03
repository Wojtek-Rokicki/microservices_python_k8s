import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
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
            properites = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # messages should persist in the queue in case our pod crashes or restarts
            ),
        )
    except:
        fs.delete(fid) # if cannot send message file will not be processed, so delete it
        return "internal server error", 500