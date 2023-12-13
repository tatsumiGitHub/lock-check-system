#!/usr/bin/env python3
import serial

import json, os
import asyncio
from azure.cosmos import CosmosClient, PartitionKey
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient

device_name = os.getenv("IOTHUB_DEVICE_NAME")
conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING', None)
database_name = os.getenv('COSMOS_DB_DATABASE_STRING', None)
container_name = os.getenv('COSMOS_DB_CONTAINER_STRING', None)

def connect_arduino():
    direction = 0
    direction_his = 0
    message = ''
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    ser.readline()
    ser.flush()

    try:
        while True:
            if 0 < ser.in_waiting:
                data = ser.readline().decode('utf-8').rstrip().split(',')
                if 2 < len(data):
                    y = int(data[2])
                    if 50 < y:
                        direction = 1
                    elif y < -50:
                        direction = -1
                    else:
                        direction = 0
                    if direction != direction_his and direction != 0:
                        direction_his = direction
                        if direction == 1:
                            message = 'locked'
                        elif direction == -1:
                            message = 'unlocked'
                        asyncio.run(send_message_to_Azure_IoT_Hub(data[0], message))
    except KeyboardInterrupt:
        print('the system is stopped')
    return

async def send_message_to_Azure_IoT_Hub(_id, _text):
    #
    cosmos_client = CosmosClient.from_connection_string(connection_string)
    database = cosmos_client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    query = "SELECT c.id, c.partitionKey FROM c WHERE c.partitionKey LIKE '" + device_name + "'"
    token = list(container.query_items(query, enable_cross_partition_query=True))
    for t in token:
        container.delete_item(item=t['id'], partition_key=t['partitionKey'])
    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a single message
    print('Sending message...')
    data = {
        'object':_id,
        'text': _text
    }
    msg = Message(json.dumps(data))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    await device_client.send_message(msg)
    print('Message successfully sent!')

    # Finally, shut down the client
    await device_client.shutdown()

if __name__ == '__main__':
    connect_arduino()