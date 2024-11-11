const express = require('express');
const app = express();

// 데이터베이스 연결 설정 (예시이므로 실제 연결 코드는 제외)

// A 코드 목록 반환 API
app.get('/getACodes', (req, res) => {
  // 데이터베이스에서 A 코드 목록 조회
  // 예시 데이터 사용
  const aCodes = [
    { code: 'A01', name: '대분류 A01' },
    { code: 'B01', name: '대분류 B01' }
  ];
  res.json(aCodes);
});

// B 코드 목록 반환 API
app.get('/getBCodes', (req, res) => {
  const aCode = req.query.aCode;
  // 데이터베이스에서 해당 A 코드에 종속된 B 코드 목록 조회
  // 예시 데이터 사용
  const bCodes = [
    { code: aCode + '01', name: '중분류 ' + aCode + '01' },
    { code: aCode + '02', name: '중분류 ' + aCode + '02' }
  ];
  res.json(bCodes);
});

// C 코드 목록 반환 API
app.get('/getCCodes', (req, res) => {
  const bCode = req.query.bCode;
  // 데이터베이스에서 해당 B 코드에 종속된 C 코드 목록 조회
  // 예시 데이터 사용
  const cCodes = [
    { code: bCode + '01', name: '소분류 ' + bCode + '01' },
    { code: bCode + '02', name: '소분류 ' + bCode + '02' }
  ];
  res.json(cCodes);
});

// 서버 실행
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
