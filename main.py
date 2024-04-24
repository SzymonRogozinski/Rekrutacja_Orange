import http.client
import subprocess
import time
import json
from subprocess import Popen

X = 10
Y = 5
host = "tvgo.orange.pl"


def measure_time(conn):
    start = time.time()
    conn.request("GET", "/gpapi/status")
    res = conn.getresponse()
    resp_time = int((time.time() - start) * 1000)
    return res, resp_time


def validate_status(res):
    if not res.status == 200:
        return f"Response failed. Status {res.status}."
    else:
        return "Response succeeded"


def validate_content(res):
    content_type = res.getheader('Content-Type')
    if "json" in content_type:
        return "Correct content type."
    else:
        return "Illegal content type."


def validate_json(js_string):
    try:
        json.loads(js_string)
        return "Correct json scheme."
    except ValueError:
        return "Illegal json scheme."


def serve_response(conn, f):
    # Time measurement
    result, response_time = measure_time(conn)
    time_log = f"Time: {response_time} ms"
    print(time_log)
    log_msg = time_log
    # Status validation
    status_log = validate_status(result)
    print(status_log)
    log_msg = log_msg + "\t" + status_log
    # Content validation
    content_log = validate_content(result)
    print(content_log)
    log_msg = log_msg + "\t" + content_log
    # Json validation
    json_string = result.read().decode()
    json_msg = validate_json(json_string)
    print(json_msg)
    log_msg = log_msg + "\t" + json_msg
    # Response content
    log_msg = log_msg + "\n" + "response content: " + json_string + "\n"
    f.write(log_msg)
    print("Status: {} and content: {}".format(result.status, json_string))


if __name__ == "__main__":
    file = open("log.txt", "w+")
    connection = http.client.HTTPSConnection(host)
    # start measuring ping
    p = Popen(['ping', "-n", "12", host], stdout=subprocess.PIPE)
    for i in range(X):
        serve_response(connection, file)
        time.sleep(Y)
    # end measuring ping
    p.wait()
    output, _ = p.communicate()
    ping_log = output.decode()
    print(ping_log)
    file.write(ping_log)
    file.close()
