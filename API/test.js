import React, { useState } from 'react';

function Counter() {
  // useState를 사용하여 count라는 상태값과 이를 업데이트하는 setCount 함수 생성
  const [count, setCount] = useState(0);

  // 버튼 클릭 시 호출되는 함수
  const handleClick = () => {
    setCount(count + 1); // 상태값을 1 증가시킴
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Counter</h1>
      <p>Current count: {count}</p>
      <button onClick={handleClick}>Increment</button>
    </div>
  );
}

export default Counter;
