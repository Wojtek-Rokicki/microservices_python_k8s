import jwt, datetime, os # for auth we will use JSON tokens, set expiration date, use env variables to configure MYSQL connections
from flask import Flask, request # creating flask server and making http requests
from flask_mysqldb import MySQL # allow us to query database

server = Flask(__name__) # configures server: routes etc.
mysql = MySQL(server) # enables the application to connect and query MySQL database 

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST") # we can store our configuration variables
# print(server.config["MYSQL_HOST"])
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth: # if request misses authorization header then we return unathorized error code
        return 'missing credentials', 401
    
    # check db for username and password
    cur = mysql.connection.cursor() # cursor for executing queries
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username, )
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401
    
# In the production you should spend your time on checking the type in Authorization header
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "not authorized", 403
    
    return decoded, 200
    
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000) # listen on all docker container ports

    # auth.username
    # auth.password