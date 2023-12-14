import cv2
import torch
import torchvision.transforms as T
from torch import nn
from torchvision.models.detection import fasterrcnn_resnet50_fpn

# # 디바이스 설정 (CPU 또는 GPU)
# device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Faster R-CNN 모델 로드
model = fasterrcnn_resnet50_fpn(pretrained=True)
#model.to(device)
model.eval()

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 영상 저장을 위한 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Torch 텐서로 변환 및 전처리
    image_tensor = torch.from_numpy(frame).permute(2, 0, 1).unsqueeze(0).float().to(device) / 255.0
    transform = T.Compose([T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    image_tensor = transform(image_tensor)

    # 객체 감지 수행
    with torch.no_grad():
        predictions = model(image_tensor)

    # 결과 파싱 및 바운딩 박스 그리기
    for prediction in predictions[0]['boxes']:
        x1, y1, x2, y2 = prediction.cpu().numpy().astype(int)
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 영상 저장
    out.write(frame)

    # 화면에 출력
    cv2.imshow("Object Detection", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitQKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제, 영상 저장 파일 닫기, 창 닫기
cap.release()
out.release()
cv2.destroyAllWindows()