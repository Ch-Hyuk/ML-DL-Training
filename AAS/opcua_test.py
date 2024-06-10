from opcua import Client

# OPC UA 서버에 연결
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

# 데이터 읽기
node = client.get_node("ns=2;i=1")  # 데이터가 있는 노드의 식별자를 사용하여 노드 객체 가져오기
value = node.get_value()  # 노드의 값 읽기
print("Value:", value)

# 연결 종료
client.disconnect()